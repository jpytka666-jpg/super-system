"""
USER MODULE
===========
This module handles everything related to users.

KEY CONCEPTS:
- Classes: Templates for creating objects
- Encapsulation: Keeping related data and functions together
- Methods: Functions that belong to a class
"""

class User:
    """
    A User represents a person using our application.
    
    This is a CLASS - a blueprint for creating user objects.
    Each user has properties (data) and methods (functions).
    """
    
    def __init__(self, name, email):
        """
        Constructor - called when creating a new User
        
        Example: user = User("Alice", "alice@example.com")
        """
        self.name = name        # User's name
        self.email = email      # User's email
        self.created_at = self._get_current_time()
    
    def _get_current_time(self):
        """
        Private method (notice the _ prefix)
        Gets the current time - helper function
        """
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M")
    
    def display_info(self):
        """
        Display user information
        Public method - can be called from outside
        """
        print(f"👤 User: {self.name}")
        print(f"📧 Email: {self.email}")
        print(f"🕐 Joined: {self.created_at}")
    
    def get_name(self):
        """Getter method - returns the user's name"""
        return self.name
    
    def update_email(self, new_email):
        """Update the user's email address"""
        self.email = new_email
        print(f"✓ Email updated to: {new_email}")


"""
WHAT YOU'VE LEARNED:
--------------------

1. CLASSES are templates for creating objects
   - Like a cookie cutter that makes cookies
   - Define properties (data) and methods (behavior)

2. OBJECTS are instances of classes
   - Each object has its own data
   - user1 and user2 can have different names

3. METHODS are functions inside a class
   - They operate on the object's data
   - Use 'self' to access the object's properties

4. ENCAPSULATION keeps related things together
   - User data and user operations in one place
   - Easy to understand and maintain

USAGE EXAMPLE:
--------------
    from user import User
    
    user = User("Bob", "bob@example.com")
    user.display_info()
    user.update_email("new@example.com")
    print(user.get_name())
"""
