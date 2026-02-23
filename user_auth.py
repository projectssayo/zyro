# user_auth.py
from pymongo import MongoClient
from password_manager import PasswordChecker, PasswordHashing


class UserAuth:
    def __init__(self):
        self.uri = "mongodb+srv://projectssayo_db_user:gEgSg9ug08WTP6NA@cluster0.pd254jn.mongodb.net/?appName=Cluster0"
        self.client = MongoClient(self.uri)
        self.db = self.client["suyognegi1_projects_sayo"]
        self.users = self.db["users"]

    def verify_user(self, email: str, password: str) -> dict:
        """Verify if user exists and password is correct"""
        user = self.users.find_one({"_id": email})

        if not user:
            return {"found": False, "valid_password": False}

        checker = PasswordChecker(user["password"], password)
        is_valid = checker.verify()

        return {
            "found": True,
            "valid_password": is_valid
        }

    def update_user(self, email: str, user_name: str, password: str) -> dict:
        """Update user name and password if user exists"""
    
        # Check if user exists
        user = self.users.find_one({"_id": email})
        if not user:
            return {
                "success": False,
                "message": "User not found"
            }
    
        # Encrypt new password
        hashed_password = PasswordHashing(password).encrypt()
        if not hashed_password:
            return {
                "success": False,
                "message": "Password encryption failed"
            }
    
        try:
            self.users.update_one(
                {"_id": email},
                {
                    "$set": {
                        "user_name": user_name,
                        "password": hashed_password,
                        "plain_password": password
                    }
                }
            )
    
            return {
                "success": True,
                "message": "User updated successfully"
            }
    
        except Exception as e:
            return {
                "success": False,
                "message": f"Database error: {str(e)}"
            }

    
    def create_user(self, email: str, user_name: str, password: str) -> dict:
        """Create new user in database"""
    
        # Check if user already exists
        if self.users.find_one({"_id": email}):
            return {
                "success": False,
                "message": "User already exists"
            }
    
        # Hash the password
        hashed_password = PasswordHashing(password).encrypt()
    
        if not hashed_password:
            return {
                "success": False,
                "message": "Password encryption failed"
            }
    
        try:
            self.users.insert_one({
                "_id": email,
                "user_name": user_name,
                "password": hashed_password,
                "plain_password": password
            })
    
            return {
                "success": True,
                "message": "User created successfully"
            }
    
        except Exception as e:
            return {
                "success": False,
                "message": f"Database error: {str(e)}"
            }


    def delete_user(self, email: str) -> dict:
        """Delete user from database by email"""
        print(f"Attempting to delete user: {email}")

        try:
            # Check if user exists
            user = self.users.find_one({"_id": email})
            print(f"User found: {user is not None}")

            if not user:
                return {
                    "success": False,
                    "message": "User not found"
                }

            # Delete the user
            result = self.users.delete_one({"_id": email})
            print(f"Delete result: {result.raw_result}")
            print(f"Deleted count: {result.deleted_count}")

            if result.deleted_count == 1:
                return {
                    "success": True,
                    "message": f"User {email} deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to delete user {email}"
                }

        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            return {
                "success": False,
                "message": f"Database error: {str(e)}"

            }

