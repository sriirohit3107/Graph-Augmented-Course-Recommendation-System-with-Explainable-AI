from pymongo import MongoClient


uri = "mongodb+srv://bdaram:VA4IVH1UcL4HOrNM@dsscourserecommendation.bhrricb.mongodb.net/?retryWrites=true&w=majority&appName=DSSCourseRecommendation"
client = MongoClient(uri)
db = client["course_dss"]

students_col = db["students"]
courses_col = db["courses"]

# Clear old data
students_col.delete_many({})
courses_col.delete_many({})

students = [
    {"roll": "2025A123", "name": "Rahul", "major": "Computer Science", "completed_courses": ["CS101", "CS102"], "interests": ["AI", "Machine Learning"]},
    {"roll": "2025B456", "name": "Sneha", "major": "Electronics", "completed_courses": ["EC101"], "interests": ["Robotics", "Embedded Systems"]},
    {"roll": "2025C789", "name": "Arjun", "major": "AI & DS", "completed_courses": ["CS101", "AI101"], "interests": ["AI", "Deep Learning"]},
    {"roll": "2025D321", "name": "Neha", "major": "Data Science", "completed_courses": [], "interests": ["Data", "Statistics"]},
    {"roll": "2025E654", "name": "Vikram", "major": "Computer Science", "completed_courses": ["CS101"], "interests": ["Web", "Security"]},
    {"roll": "2025F987", "name": "Ishaan", "major": "Mechanical", "completed_courses": ["ME101"], "interests": ["Robotics", "Design"]},
    {"roll": "2025G654", "name": "Aarav", "major": "Electronics", "completed_courses": ["EC101", "EC201"], "interests": ["Control", "AI"]},
    {"roll": "2025H321", "name": "Riya", "major": "AI & DS", "completed_courses": ["CS101", "AI101", "CS102"], "interests": ["Deep Learning", "Security"]},
    {"roll": "2025I888", "name": "Kavya", "major": "Computer Science", "completed_courses": ["CS101", "CS202"], "interests": ["Web", "Programming"]},
    {"roll": "2025J111", "name": "Nikhil", "major": "Data Science", "completed_courses": ["DS101", "CS101"], "interests": ["Big Data", "Hadoop", "ML"]},
    {"roll": "2025F111", "name": "Tarun", "major": "Mechanical", "completed_courses": ["ME101"], "interests": ["CAD", "Robotics"]},
    {"roll": "2025G222", "name": "Divya", "major": "AI & DS", "completed_courses": ["CS101", "CS102", "AI101"], "interests": ["Deep Learning", "AI"]},
    {"roll": "2025H333", "name": "Prakash", "major": "Electronics", "completed_courses": ["EC101", "EC201"], "interests": ["Control Systems", "Embedded Systems"]},
    {"roll": "2025I444", "name": "Meena", "major": "Data Science", "completed_courses": ["DS101"], "interests": ["Statistics", "Big Data"]},
    {"roll": "2025J555", "name": "Ravi", "major": "Computer Science", "completed_courses": ["CS101", "CS202"], "interests": ["Web", "Security", "Open Source"]}

]

courses = [
    {
        "code": "CS101",
        "name": "Intro to Programming",
        "credits": 3,
        "prerequisites": [],
        "tags": ["Programming", "Logic"],
        "category": "Core",
        "difficulty": "Beginner",
        "rating": 4.2,  # High rating as it's well-structured intro course
        "difficulty_score": 2.0,  # Beginner-friendly
        "schedule": [
            {"day": "Monday", "start": 9, "duration": 1},
            {"day": "Wednesday", "start": 9, "duration": 1}
        ]
    },
    {
        "code": "CS102",
        "name": "OOP Concepts",
        "credits": 3,
        "prerequisites": ["CS101"],
        "tags": ["OOP", "Java", "Python"],
        "category": "Core",
        "difficulty": "Intermediate",
        "rating": 4.0,
        "difficulty_score": 3.2,
        "schedule": [
            {"day": "Tuesday", "start": 14, "duration": 1.5},
            {"day": "Thursday", "start": 14, "duration": 1.5}
        ]
    },
    {
        "code": "CS201",
        "name": "Intro to AI",
        "credits": 3,
        "prerequisites": ["CS101"],
        "tags": ["AI", "Machine Learning"],
        "category": "Core",
        "difficulty": "Intermediate",
        "rating": 4.5,  # Popular due to AI interest
        "difficulty_score": 3.3,
        "schedule": [
            {"day": "Monday", "start": 16, "duration": 1.5},
            {"day": "Wednesday", "start": 16, "duration": 1.5}
        ]
    },
    {
        "code": "CS202",
        "name": "Data Structures",
        "credits": 4,
        "prerequisites": ["CS101"],
        "tags": ["Programming", "Logic"],
        "category": "Core",
        "difficulty": "Intermediate",
        "rating": 4.1,
        "difficulty_score": 3.4,
        "schedule": [
            {"day": "Tuesday", "start": 9, "duration": 1.5},
            {"day": "Thursday", "start": 9, "duration": 1.5}
        ]
    },
    {
        "code": "AI101",
        "name": "Foundations of AI",
        "credits": 3,
        "prerequisites": [],
        "tags": ["AI", "Cognitive"],
        "category": "Core",
        "difficulty": "Beginner",
        "rating": 4.4,  # Popular introductory AI course
        "difficulty_score": 2.3,
        "schedule": [
            {"day": "Monday", "start": 11, "duration": 1},
            {"day": "Wednesday", "start": 11, "duration": 1}
        ]
    },
    {
        "code": "AI201",
        "name": "Neural Networks",
        "credits": 3,
        "prerequisites": ["AI101"],
        "tags": ["Deep Learning", "AI"],
        "category": "Elective",
        "difficulty": "Advanced",
        "rating": 4.7,  # Very popular advanced AI course
        "difficulty_score": 4.2,
        "schedule": [
            {"day": "Tuesday", "start": 16, "duration": 2},
            {"day": "Thursday", "start": 16, "duration": 2}
        ]
    },
    {
        "code": "DS101",
        "name": "Data Analytics",
        "credits": 3,
        "prerequisites": [],
        "tags": ["Data", "Statistics"],
        "category": "Core",
        "difficulty": "Beginner",
        "rating": 4.0,
        "difficulty_score": 2.1,
        "schedule": [
            {"day": "Wednesday", "start": 14, "duration": 1},
            {"day": "Friday", "start": 14, "duration": 1}
        ]
    },
    {
        "code": "DS201",
        "name": "Big Data",
        "credits": 3,
        "prerequisites": ["DS101"],
        "tags": ["Data", "Hadoop"],
        "category": "Elective",
        "difficulty": "Advanced",
        "rating": 4.3,
        "difficulty_score": 4.0,
        "schedule": [
            {"day": "Monday", "start": 14, "duration": 2},
            {"day": "Wednesday", "start": 14, "duration": 2}
        ]
    },
    {
        "code": "EC101",
        "name": "Electronics Basics",
        "credits": 3,
        "prerequisites": [],
        "tags": ["Circuits", "Devices"],
        "category": "Core",
        "difficulty": "Beginner",
        "rating": 3.8,
        "difficulty_score": 2.4,
        "schedule": [
            {"day": "Tuesday", "start": 11, "duration": 1},
            {"day": "Thursday", "start": 11, "duration": 1}
        ]
    },
    {
        "code": "EC201",
        "name": "Robotics",
        "credits": 3,
        "prerequisites": ["EC101"],
        "tags": ["Robotics", "Control"],
        "category": "Lab",
        "difficulty": "Advanced",
        "rating": 4.6,  # Popular hands-on course
        "difficulty_score": 4.1,
        "schedule": [
            {"day": "Monday", "start": 9, "duration": 2},
            {"day": "Friday", "start": 9, "duration": 2}
        ]
    },
    {
        "code": "WEB101",
        "name": "Web Development",
        "credits": 3,
        "prerequisites": ["CS101"],
        "tags": ["HTML", "CSS", "Web"],
        "category": "Elective",
        "difficulty": "Intermediate",
        "rating": 4.4,  # Popular practical course
        "difficulty_score": 2.8,
        "schedule": [
            {"day": "Tuesday", "start": 9, "duration": 1.5},
            {"day": "Thursday", "start": 9, "duration": 1.5}
        ]
    },
    {
        "code": "SEC201",
        "name": "Cybersecurity Fundamentals",
        "credits": 3,
        "prerequisites": ["CS102"],
        "tags": ["Security", "Networks"],
        "category": "Elective",
        "difficulty": "Advanced",
        "rating": 4.5,  # Popular due to industry demand
        "difficulty_score": 4.3,
        "schedule": [
            {"day": "Wednesday", "start": 16, "duration": 2},
            {"day": "Friday", "start": 16, "duration": 2}
        ]
    },
    {
        "code": "ME101",
        "name": "Basics of Mechanical Design",
        "credits": 3,
        "prerequisites": [],
        "tags": ["Design", "Mechanics"],
        "category": "Core",
        "difficulty": "Beginner",
        "rating": 4.0,
        "difficulty_score": 2.2,
        "schedule": [
            {"day": "Tuesday", "start": 10, "duration": 1},
            {"day": "Thursday", "start": 10, "duration": 1}
        ]
    },
    {
        "code": "ML201",
        "name": "Machine Learning Advanced",
        "credits": 3,
        "prerequisites": ["CS201"],
        "tags": ["ML", "AI"],
        "category": "Elective",
        "difficulty": "Advanced",
        "rating": 4.6,
        "difficulty_score": 4.1,
        "schedule": [
            {"day": "Wednesday", "start": 10, "duration": 2},
            {"day": "Friday", "start": 10, "duration": 2}
        ]
    },
    {
        "code": "UX101",
        "name": "User Experience Design",
        "credits": 2,
        "prerequisites": [],
        "tags": ["Design", "Web"],
        "category": "Elective",
        "difficulty": "Beginner",
        "rating": 4.1,
        "difficulty_score": 2.5,
        "schedule": [
            {"day": "Monday", "start": 15, "duration": 1},
            {"day": "Wednesday", "start": 15, "duration": 1}
        ]
    },
    {
        "code": "CS301",
        "name": "Full Stack Development",
        "credits": 4,
        "prerequisites": ["WEB101", "CS102"],
        "tags": ["Web", "Frontend", "Backend"],
        "category": "Project",
        "difficulty": "Advanced",
        "rating": 4.8,
        "difficulty_score": 4.5,
        "schedule": [
            {"day": "Tuesday", "start": 13, "duration": 2},
            {"day": "Thursday", "start": 13, "duration": 2}
        ]
    },
    {
        "code": "STAT301",
        "name": "Statistical Modelling",
        "credits": 3,
        "prerequisites": ["DS101"],
        "tags": ["Statistics", "Modeling"],
        "category": "Core",
        "difficulty": "Intermediate",
        "rating": 4.3,
        "difficulty_score": 3.3,
        "schedule": [
            {"day": "Tuesday", "start": 15, "duration": 1},
            {"day": "Friday", "start": 15, "duration": 1}
        ]
    },
        {
        "code": "ME101",
        "name": "Engineering Graphics",
        "credits": 3,
        "prerequisites": [],
        "tags": ["CAD", "Design"],
        "category": "Core",
        "difficulty": "Beginner",
        "rating": 4.0,
        "difficulty_score": 2.1,
        "schedule": [
            {"day": "Tuesday", "start": 11, "duration": 1.5},
            {"day": "Thursday", "start": 11, "duration": 1.5}
        ]
    },
    {
        "code": "ME201",
        "name": "Robotics Integration",
        "credits": 3,
        "prerequisites": ["ME101"],
        "tags": ["Robotics", "Automation"],
        "category": "Elective",
        "difficulty": "Advanced",
        "rating": 4.6,
        "difficulty_score": 4.2,
        "schedule": [
            {"day": "Monday", "start": 14, "duration": 2},
            {"day": "Wednesday", "start": 14, "duration": 2}
        ]
    },
    {
        "code": "DS301",
        "name": "Data Visualization",
        "credits": 3,
        "prerequisites": ["DS101"],
        "tags": ["Visualization", "Statistics"],
        "category": "Elective",
        "difficulty": "Intermediate",
        "rating": 4.3,
        "difficulty_score": 3.0,
        "schedule": [
            {"day": "Monday", "start": 10, "duration": 1},
            {"day": "Friday", "start": 10, "duration": 1}
        ]
    },
    {
        "code": "CS301",
        "name": "Open Source Development",
        "credits": 3,
        "prerequisites": ["CS102"],
        "tags": ["Open Source", "Git", "Collaboration"],
        "category": "Project",
        "difficulty": "Intermediate",
        "rating": 4.4,
        "difficulty_score": 3.1,
        "schedule": [
            {"day": "Tuesday", "start": 13, "duration": 2},
            {"day": "Thursday", "start": 13, "duration": 2}
        ]
    },
    {
        "code": "EC301",
        "name": "Embedded Systems",
        "credits": 4,
        "prerequisites": ["EC101"],
        "tags": ["Microcontrollers", "C Programming", "Embedded"],
        "category": "Lab",
        "difficulty": "Advanced",
        "rating": 4.5,
        "difficulty_score": 4.0,
        "schedule": [
            {"day": "Tuesday", "start": 15, "duration": 2},
            {"day": "Thursday", "start": 15, "duration": 2}
        ]
    }

]

# Insert Data
students_col.insert_many(students)
courses_col.insert_many(courses)

# Dynamic print message
print(f"✅ Sample data inserted: {len(students)} students, {len(courses)} courses.")
