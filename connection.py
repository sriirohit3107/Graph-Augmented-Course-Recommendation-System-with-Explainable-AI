from pymongo import MongoClient
from config import MONGODB_URI, DATABASE_NAME
import streamlit as st

def get_database_connection():
    """Get MongoDB database connection with error handling"""
    try:
        # Connect to the cluster using the URI directly
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=10000)
        
        # Test the connection
        client.admin.command('ping')
        
        # Use the specified database
        db = client[DATABASE_NAME]
        
        # Create/get collections
        students_col = db["students"]
        courses_col = db["courses"]
        
        return client, db, students_col, courses_col
        
    except Exception as e:
        if 'streamlit' in str(type(st)):
            st.error(f"❌ Failed to connect to MongoDB: {str(e)}")
        else:
            print(f"❌ Failed to connect to MongoDB: {str(e)}")
        return None, None, None, None

# Initialize global variables as None
client, db, students_col, courses_col = None, None, None, None

def initialize_connection():
    """Initialize the database connection when needed"""
    global client, db, students_col, courses_col
    if client is None:
        client, db, students_col, courses_col = get_database_connection()
    return client, db, students_col, courses_col
