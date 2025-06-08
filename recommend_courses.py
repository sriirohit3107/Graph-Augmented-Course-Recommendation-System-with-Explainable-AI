from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import itertools

# Time slot mapping
TIME_SLOTS = {
    "Morning": [9, 10],
    "Midday": [11, 12],
    "Afternoon": [14, 15],
    "Evening": [16, 17]
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
HOURS = list(range(9, 18))  # 9AM to 5PM

# === MongoDB Connection ===
uri = "mongodb+srv://bdaram:VA4IVH1UcL4HOrNM@dsscourserecommendation.bhrricb.mongodb.net/?retryWrites=true&w=majority&appName=DSSCourseRecommendation"
client = MongoClient(uri)
db = client["course_dss"]
students_col = db["students"]
courses_col = db["courses"]

# === User Inputs ===
roll = input("Enter your roll number: ").strip()
name = input("Enter your name: ").strip()
major = input("Enter your major: ").strip()

# === Validate Student ===
student = students_col.find_one({"roll": roll, "name": name, "major": major})
if not student:
    print("❌ The student data doesn't match. Please check your details correctly.")
    exit()

intended_min = int(input("Minimum credits this semester: "))
intended_max = int(input("Maximum credits this semester: "))

manual_completed = input("Enter completed courses (comma-separated like CS101,CS102) or press Enter to auto-fetch: ").strip()
interests = input("Enter your interests (comma-separated like AI,Robotics): ").strip().split(',')

category_filter = input("Preferred course category (Core, Elective, Lab, Project, All): ").strip().title()
difficulty_filter = input("Preferred difficulty (Beginner, Intermediate, Advanced, All): ").strip().title()

must_take = input("Enter must-take course codes (comma-separated, optional): ").strip().split(',') if input("Any must-take courses? (y/n): ").strip().lower() == 'y' else []
# Proper avoid input
avoid = []
if input("Any courses to avoid? (y/n): ").strip().lower() == 'y':
    avoid_input = input("Enter courses to avoid (comma-separated, optional): ").strip()
    avoid = [code.strip() for code in avoid_input.split(',') if code.strip()]

# === Course Completion ===
if manual_completed:
    completed = [code.strip() for code in manual_completed.split(',')]
else:
    completed = student.get("completed_courses", [])

if not completed:
    print("\n🆕 You're a freshman! We'll suggest beginner-level courses.\n")

# === Fetch Courses ===
all_courses = pd.DataFrame(list(courses_col.find()))
eligible = all_courses[~all_courses["code"].isin(completed + [a.strip() for a in avoid if a.strip()])]

# === Filter by Prerequisites ===
def is_eligible(course_prereqs):
    return all(p in completed for p in course_prereqs)

eligible = eligible[eligible["prerequisites"].apply(is_eligible)].copy()

# === Apply Category Filter ===
if category_filter != "All":
    eligible = eligible[eligible["category"].str.title() == category_filter]

# === Apply Difficulty Filter ===
if difficulty_filter != "All":
    eligible = eligible[eligible["difficulty"].str.title() == difficulty_filter]

# === Add Must-Take Courses Back In ===
for code in must_take:
    code = code.strip()
    if code and code not in eligible['code'].values and code not in completed:
        if code in avoid:
            print(f"⚠️ Skipping must-take course '{code}' because it’s also in your avoid list.")
            continue
        course = courses_col.find_one({"code": code})
        if course and is_eligible(course["prerequisites"]):
            eligible = pd.concat([eligible, pd.DataFrame([course])], ignore_index=True)


# === Interest Matching ===
vectorizer = CountVectorizer()
tag_matrix = vectorizer.fit_transform(eligible['tags'].apply(lambda x: ' '.join(x)))
interest_vector = vectorizer.transform([' '.join(interests)])
similarity_scores = cosine_similarity(interest_vector, tag_matrix).flatten()
eligible["match_score"] = similarity_scores

eligible = eligible.sort_values(by=["match_score", "credits"], ascending=False).reset_index(drop=True)

# === Generate Course Sets (Flexible Range) ===
def generate_credit_sets(courses, min_credits, max_credits, max_sets=3):
    course_list = courses.to_dict("records")
    combos = []
    for r in range(1, len(course_list) + 1):
        for combo in itertools.combinations(course_list, r):
            total = sum(course["credits"] for course in combo)
            if min_credits <= total <= max_credits:
                combos.append(combo)
            if len(combos) >= max_sets:
                return combos
    return combos

recommendation_sets = generate_credit_sets(eligible, intended_min, intended_max)

# Final filter to remove avoid-listed courses from sets
filtered_sets = []
for course_set in recommendation_sets:
    if not any(course["code"] in avoid for course in course_set):
        filtered_sets.append(course_set)


recommendation_sets = filtered_sets


# === Output ===
if recommendation_sets:
    print(f"\n📚 Recommended Course Sets for {intended_min}-{intended_max} credits:")
    for i, course_set in enumerate(recommendation_sets, start=1):
        print(f"\n📦 SET {i}:")
        for course in course_set:
            print(f" - {course['code']} | {course['name']} | {course['credits']} credits")
            print(f"   ↳ Category: {course['category']} | Level: {course['difficulty']} | Rating: {course.get('rating', 'N/A')}/5 | Difficulty Score: {course.get('difficulty_score', 'N/A')}/5")
            print(f"   ↳ Tags: {', '.join(course['tags'])}")

            # Explainability bullets
            reasons = []
            
            # Interest match
            matching_tags = set(course['tags']).intersection(set(interests))
            if matching_tags:
                reasons.append(f"✅ Matches your interest in: {', '.join(matching_tags)}")

            # Prerequisite match
            for prereq in course['prerequisites']:
                if prereq in completed:
                    reasons.append(f"✅ You’ve completed the required course: {prereq}")

            # Category match
            if category_filter != "All" and course['category'].lower() == category_filter.lower():
                reasons.append(f"✅ Matches your preferred category: {course['category']}")

            # Difficulty match
            if difficulty_filter != "All" and course['difficulty'].lower() == difficulty_filter.lower():
                reasons.append(f"✅ Matches your difficulty preference: {course['difficulty']}")

            # Print explanations
            for reason in reasons:
                print(f"    {reason}")
else:
    if avoid:
        print("\n❗ All course combinations included at least one course you wanted to avoid.")
        print("Try adjusting your avoid list or credit range.")
    else:
        print("\n❗ No course combinations found within your credit range and preferences.")
        print("You may relax filters or increase your credit range.")

# === Prerequisite Tree Guidance ===
print("\n📘 Future Course Suggestions:")

# All course codes already recommended
recommended_codes = [course["code"] for course_set in recommendation_sets for course in course_set]

# Go through all courses in DB
for course in courses_col.find():
    code = course["code"]
    prereqs = course["prerequisites"]
    
    # Skip if:
    if (
        code in completed or
        code in avoid or
        code in recommended_codes or
        code in eligible["code"].values
    ):
        continue

    # Find missing prerequisites
    missing = [p for p in prereqs if p not in completed]

    # Suggest only if 1 prereq is missing
    if len(missing) == 1:
        print(f"🔔 If you complete '{missing[0]}', you’ll be eligible for '{code} - {course['name']}'")

# === Ask Student to Pick a Set ===
if recommendation_sets:
    print("\n🎯 Choose a course set to view weekly schedule:")
    set_choice = int(input(f"Enter set number (1 to {len(recommendation_sets)}): ").strip())
    
    if not (1 <= set_choice <= len(recommendation_sets)):
        print("❌ Invalid set number.")
        exit()

    selected_set = recommendation_sets[set_choice - 1]

    # === Time Conflict Detection ===
    print("\n🔍 Checking for time conflicts...\n")

    occupied = {}
    conflict_found = False

    # For timetable grid
    timetable = {day: {hour: "" for hour in range(9, 18)} for day in DAYS}

    for course in selected_set:
        for session in course.get("schedule", []):
            day = session["day"]
            start = session["start"]
            duration = session["duration"]

            for hour in range(start, start + int(duration)):
                key = (day, hour)
                if key in occupied:
                    print(f"⚠️ Conflict: '{course['code']}' overlaps with '{occupied[key]}' on {day} at {hour}:00")
                    conflict_found = True
                else:
                    occupied[key] = course["code"]
                    if day in timetable and hour in timetable[day]:
                        timetable[day][hour] = course["code"]

    if not conflict_found:
        print("✅ No timing conflicts detected!\n")

    # === Render Weekly Timetable ===
    print("📆 Weekly Timetable (Selected Set):\n")

# Time labels for hours
hour_labels = {9: " 9AM", 10: "10AM", 11: "11AM", 12: "12PM", 13: " 1PM", 14: " 2PM", 15: " 3PM", 16: " 4PM", 17: " 5PM"}
hours = list(range(9, 18))
col_width = 10
line_sep = "+" + "+".join(["-" * col_width for _ in ["Time"] + hours]) + "+"

# Header
print(line_sep)
print("|" + "|".join(f"{label:^{col_width}}" for label in ["Time"] + [hour_labels[h] for h in hours]) + "|")
print(line_sep)

# Rows per day with cell merging
for day in DAYS:
    row_str = f"|{day:^{col_width}}"
    h = 9
    while h <= 17:
        current = timetable[day].get(h, "")
        span = 1

        # Check how long the same course continues
        while h + span <= 17 and timetable[day].get(h + span, "") == current and current:
            span += 1

        if current:
            display = current[:col_width * span - 1]  # trim if too long
            cell = f"{display:^{col_width * span}}"
            row_str += "|" + cell
            h += span
        else:
            row_str += "|" + " " * col_width
            h += 1
    row_str += "|"
    print(row_str)
    print(line_sep)

# === Course Legend ===
print("\n📘 Legend:")
printed = set()
for course in selected_set:
    if course['code'] not in printed:
        print(f"{course['code']} = {course['name']}")
        printed.add(course['code'])


