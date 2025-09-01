from pymongo import MongoClient
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import itertools

# MongoDB Connection (same as other files)
from connection import get_database_connection

# Get database connection
client, db, students_col, courses_col = get_database_connection()

# Check if connection failed
if not client:
    raise Exception("Failed to connect to MongoDB. Please check your configuration.")

def get_recommendations(roll, name, major, interests, completed, credit_min, credit_max, category_filter, difficulty_filter, must_take, avoid):
    # --- Fetch Courses ---
    all_courses = pd.DataFrame(list(courses_col.find()))
    eligible = all_courses[~all_courses["code"].isin(completed + avoid)]

    # --- Check Prerequisites ---
    def is_eligible(prereqs):
        return all(p in completed for p in prereqs)
    eligible = eligible[eligible["prerequisites"].apply(is_eligible)].copy()

    # --- Add Must-Take Back In ---
    for code in must_take:
        if code in avoid or code in completed:
            continue
        if code not in eligible['code'].values:
            course = courses_col.find_one({"code": code})
            if course and is_eligible(course["prerequisites"]):
                eligible = pd.concat([eligible, pd.DataFrame([course])], ignore_index=True)

    # --- Tag Matching (Cosine Similarity) ---
    vectorizer = CountVectorizer()
    tag_matrix = vectorizer.fit_transform(eligible['tags'].apply(lambda x: ' '.join(x)))
    interest_vector = vectorizer.transform([' '.join(interests)])
    similarity_scores = cosine_similarity(interest_vector, tag_matrix).flatten()
    eligible["match_score"] = similarity_scores

    # --- Apply Filters ---
    if category_filter != "All":
        eligible = eligible[eligible["category"].str.lower() == category_filter.lower()]
    if difficulty_filter != "All":
        eligible = eligible[eligible["difficulty"].str.lower() == difficulty_filter.lower()]

    # --- Sort ---
    eligible = eligible.sort_values(by=["match_score", "credits"], ascending=False).reset_index(drop=True)

    # --- Generate Sets ---
    def generate_sets(courses, min_credits, max_credits, max_sets=3):
        course_list = courses.to_dict("records")
        combos = []
        for r in range(1, len(course_list)+1):
            for combo in itertools.combinations(course_list, r):
                total = sum(c["credits"] for c in combo)
                if min_credits <= total <= max_credits:
                    combos.append(combo)
                if len(combos) >= max_sets:
                    return combos
        return combos

    recommendation_sets = generate_sets(eligible, credit_min, credit_max)

    # --- Future Suggestions ---
    future_suggestions = []
    recommended_codes = [c["code"] for s in recommendation_sets for c in s]
    for course in courses_col.find():
        if (course["code"] not in completed
            and course["code"] not in avoid
            and course["code"] not in recommended_codes):
            missing = [p for p in course["prerequisites"] if p not in completed]
            if len(missing) == 1:
                future_suggestions.append((course["code"], course["name"], missing[0]))

    return recommendation_sets, future_suggestions
