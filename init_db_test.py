import os
import sys

sys.path.append(os.getcwd())

try:
    from app.database import init_db
    print("Step 1: Successfully imported init_db.")
    
    print("Step 2: Attempting to create database file...")
    init_db()
    
    # Check if file exists
    if os.path.exists("test.db"):
        print(f"SUCCESS: 'test.db' created at {os.path.abspath('test.db')}")
    else:
        print("FAILURE: The function ran but no file was created.")

except ModuleNotFoundError as e:
    print(f"ERROR: Could not find the 'app' folder. Are you in the root directory? {e}")
except Exception as e:
    print(f"AN UNEXPECTED ERROR OCCURRED: {e}")