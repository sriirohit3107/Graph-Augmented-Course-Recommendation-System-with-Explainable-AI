import streamlit as st
from pymongo import MongoClient
import pandas as pd
import numpy as np
from recommend_engine import get_recommendations
import matplotlib.pyplot as plt
import io



DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
HOURS = list(range(9, 18))  # 9AM to 5PM


# MongoDB connection
from connection import initialize_connection

# Get database connection
client, db, students_col, courses_col = initialize_connection()

# Check if connection failed
if not client:
    st.error("❌ Database connection failed! Please check your configuration.")
    st.stop()
else:
    st.success("✅ Connected to MongoDB Atlas successfully!")

# === PAGE CONFIG ===
st.set_page_config(page_title="Course Recommendation DSS", layout="wide")

from config import APP_TITLE, APP_DESCRIPTION

st.title(f"🎓 {APP_TITLE}")
st.markdown(APP_DESCRIPTION)

# === SIDEBAR UI ===
with st.sidebar:
    st.header("🧾 Student Details")

    with st.expander("🔐 Identity", expanded=True):
        all_majors = sorted({student["major"] for student in students_col.find()})
        roll = st.text_input("Roll Number", key="roll_input")
        name = st.text_input("Name", key="name_input")
        major = st.selectbox("Major", options=all_majors, key="major_select")

    with st.expander("🎓 Academic Record", expanded=True):
        # Fetch student for completed courses
        student = students_col.find_one({"roll": roll, "name": name, "major": major})
        if student:
            completed_from_db = student.get("completed_courses", [])
            st.success("✅ Record found. Completed courses pre-selected.")
            completed_courses_input = st.multiselect(
                "Completed Courses", options=completed_from_db, default=completed_from_db, disabled=True
            )
        else:
            completed_courses_input = []
            st.warning("⚠️ Enter a valid Roll, Name, and Major to fetch completed courses.")

    with st.expander("📊 Credit Range", expanded=True):
        from config import DEFAULT_CREDIT_MIN, DEFAULT_CREDIT_MAX
        credit_min = st.number_input("Minimum Credits", min_value=1, max_value=30, value=DEFAULT_CREDIT_MIN)
        credit_max = st.number_input("Maximum Credits", min_value=1, max_value=30, value=DEFAULT_CREDIT_MAX)

    with st.expander("🎯 Course Preferences", expanded=True):
        category = st.selectbox("Preferred Category", ["All", "Core", "Elective", "Lab", "Project"])
        difficulty = st.selectbox("Preferred Difficulty", ["All", "Beginner", "Intermediate", "Advanced"])
        must_take = st.text_input("Must-Take Course Codes (comma-separated)")
        avoid = st.text_input("Courses to Avoid (comma-separated)")

    with st.expander("✨ Interests", expanded=True):
        all_interests = sorted({tag for course in courses_col.find() for tag in course.get("tags", [])})
        interest_list = st.multiselect("Your Interests", options=all_interests)

    # Submit Button
    if "submit_clicked" not in st.session_state:
        st.session_state["submit_clicked"] = False

    # --- Inside Sidebar after the button ---
    if st.button("🚀 Get Recommendations"):
        st.session_state["submit_clicked"] = True
        st.session_state.pop("selected_set_index", None)  # Reset timetable selection
  # Reset timetable selection
with st.sidebar.expander("🎨 Theme Tips"):
    st.markdown("Switch between **Light/Dark themes** via:")
    st.markdown("`Settings > Theme > Choose your mode` ⚙️")


# === Recommendation Trigger ===
if st.session_state.get("submit_clicked", False):
    st.info("🔍 Processing your recommendations...")

    student = students_col.find_one({"roll": roll, "name": name, "major": major})
    if not student:
        st.error("❌ Student data doesn't match. Please check Roll Number, Name, and Major.")
        st.stop()

    must_take_list = [m.strip() for m in must_take.split(",") if m.strip()]
    avoid_list = [a.strip() for a in avoid.split(",") if a.strip()]

    st.success(f"✅ Hello {name}! Found your record.")

    # ✅ Determine completed courses (manual input OR from DB)
    completed_courses_input = completed_courses_input if 'completed_courses_input' in locals() else []
    completed_courses = completed_courses_input if completed_courses_input else student.get("completed_courses", [])
    st.info(f"📘 Completed Courses: {', '.join(completed_courses)}")

    # ✅ Parse must-take and avoid course codes
    must_take_list = [m.strip() for m in must_take.split(",") if m.strip()]
    avoid_list = [a.strip() for a in avoid.split(",") if a.strip()]


        # Call recommendation logic
        # === Call Recommendation Engine ===
    sets, future_suggestions = get_recommendations(
        roll=roll,
        name=name,
        major=major,
        interests=interest_list,
        completed=completed_courses,
        credit_min=credit_min,
        credit_max=credit_max,
        category_filter=category,
        difficulty_filter=difficulty,
        must_take=must_take_list,
        avoid=avoid_list
    )

    st.session_state["recommendation_sets"] = sets
    st.session_state.pop("selected_set_index", None)

    if not sets:
        st.warning("⚠️ No valid course combinations found. Try adjusting filters or credit range.")
    else:
        st.subheader("📚 Recommended Course Combinations")

        for i, course_set in enumerate(sets, start=1):
            total_credits = sum(c["credits"] for c in course_set)
            with st.expander(f"📦 SET {i} (Total Credits: {total_credits})"):

                for course in course_set:
                    # 💡 Title + Credits
                    st.markdown(f"### {course['code']} - {course['name']} ({course['credits']} credits)")

                    # 🌟 Difficulty Color Badge
                    difficulty = course.get("difficulty", "")
                    diff_color = {
                        "Beginner": "#d1fae5",     # green
                        "Intermediate": "#fef08a", # yellow
                        "Advanced": "#fecaca",     # red
                    }.get(difficulty, "#e5e7eb")

                    st.markdown(
                        f"<span style='background-color:{diff_color}; padding:5px 10px; border-radius:6px;'>"
                        f"Level: {difficulty}</span>",
                        unsafe_allow_html=True
                    )

                    # ⭐ Star Rating
                    rating = course.get("rating", 0)
                    stars = "⭐️" * int(round(rating))
                    st.markdown(f"Rating: {stars} ({rating}/5)")

                    # 🏷️ Styled Tags
                    tag_html = " ".join([
                        f"<span style='background-color:#dbeafe; padding:4px 8px; border-radius:10px; margin-right:4px; font-size:12px;'>{tag}</span>"
                        for tag in course["tags"]
                    ])
                    st.markdown("Tags:", unsafe_allow_html=True)
                    st.markdown(tag_html, unsafe_allow_html=True)

                    # ✅ Reasoning
                    reason_lines = []
                    if any(prereq in completed_courses for prereq in course.get("prerequisites", [])):
                        reason_lines.append("📘 Because you completed a prerequisite course.")
                    if any(interest.lower() in [tag.lower() for tag in course.get("tags", [])] for interest in interest_list):
                        reason_lines.append("⭐ Matches your interest area.")

                    if reason_lines:
                        st.markdown("**Why this course?**")
                        for reason in reason_lines:
                            st.markdown(f"👉 {reason}")

                    st.markdown("---")

                if st.button(f"🗓️ Use SET {i} for timetable", key=f"use_set_{i}"):
                    st.session_state["selected_set_index"] = i - 1


    # === Weekly Timetable Trigger (SET selection section follows here...)
    if (
        st.session_state.get("submit_clicked", False)
        and "recommendation_sets" in st.session_state
        and "selected_set_index" in st.session_state
    ):
        st.subheader("📅 Weekly Timetable")

        # Build table structure for merging cells
        timetable = {day: {hr: "" for hr in HOURS} for day in DAYS}
        cell_spans = {day: {hr: 1 for hr in HOURS} for day in DAYS}
        conflicts = []

        sets = st.session_state.get("recommendation_sets", [])
        selected_set = sets[st.session_state["selected_set_index"]]

        for course in selected_set:
            for session in course.get("schedule", []):
                day = session["day"]
                start = session["start"]
                duration = session["duration"]

                for hr in np.arange(start, start + duration, 1):
                    hr = int(hr)
                    if timetable[day].get(hr):
                        conflicts.append((day, hr, course["code"], timetable[day][hr]))
                    timetable[day][hr] = course["code"]

                for hr in np.arange(start + 1, start + duration, 1):
                    hr = int(hr)
                    timetable[day][hr] = None  # Mark as merged

                cell_spans[day][int(start)] = int(duration)

        # Create HTML table
        html = """
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
                font-family: monospace;
            }
            th, td {
                border: 1px solid #ddd;
                text-align: center;
                padding: 6px;
            }
            th {
                background-color: #f2f2f2;
            }
            td.course {
                background-color: #e0f7fa;
                font-weight: bold;
            }
        </style>
        <table>
            <tr>
                <th>Day</th>
        """

        for hr in HOURS:
            label = f"{hr if hr <= 12 else hr - 12}{'AM' if hr < 12 else 'PM'}"
            html += f"<th>{label}</th>"
        html += "</tr>"

        for day in DAYS:
            html += f"<tr><td><b>{day}</b></td>"
            h = 9
            while h <= 17:
                course_code = timetable[day].get(h, "")
                if course_code is None:
                    h += 1
                    continue
                colspan = cell_spans[day].get(h, 1)
                if course_code == "":
                    html += f"<td></td>"
                else:
                    html += f"<td class='course' colspan='{colspan}'>{course_code}</td>"
                h += colspan
            html += "</tr>"
        html += "</table>"

        st.markdown(html, unsafe_allow_html=True)

        if conflicts:
            st.warning("⚠️ Time Conflicts Detected:")
            for day, hr, new, old in conflicts:
                st.markdown(f"• {day} at {hr}:00 — `{new}` overlaps with `{old}`")
        else:
            st.success("✅ No timing conflicts detected!")

        # === Feedback on recommendations ===
        st.subheader("📝 Was this recommendation helpful?")
        feedback = st.radio("Your feedback:", ["👍 Yes", "👎 No"], horizontal=True, key="feedback_radio")

        if feedback == "👍 Yes":
            st.success("🎉 Great! We're glad it helped.")
        elif feedback == "👎 No":
            st.info("💡 Thanks for the feedback! We'll try to improve future suggestions.")
