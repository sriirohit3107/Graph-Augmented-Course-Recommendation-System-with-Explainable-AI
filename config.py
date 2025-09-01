import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://dsscourse:rohit%4012345@dss.eqisrso.mongodb.net/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "course_dss")

# App Configuration
APP_TITLE = "Course Recommendation DSS"
APP_DESCRIPTION = "Welcome! This system helps students choose the best combination of courses for their semester based on interests, eligibility, credit range, and more."

# Default Values
DEFAULT_CREDIT_MIN = 6
DEFAULT_CREDIT_MAX = 9
