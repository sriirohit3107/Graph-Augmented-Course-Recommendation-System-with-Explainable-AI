from pymongo import MongoClient

# Replace <db_password> with your actual password
uri = "mongodb+srv://bdaram:VA4IVH1UcL4HOrNM@dsscourserecommendation.bhrricb.mongodb.net/?retryWrites=true&w=majority&appName=DSSCourseRecommendation"

# Connect to the cluster
client = MongoClient(uri)

# Use a database named 'course_dss'
db = client["course_dss"]

# Create/get collections
students_col = db["students"]
courses_col = db["courses"]

print("✅ Connected to MongoDB Atlas successfully!")
