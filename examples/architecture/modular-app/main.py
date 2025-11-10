"""
MODULAR APPLICATION - See Architecture in Action
=================================================

This example demonstrates how to organize code into modules.
Instead of one giant file, we split code into logical pieces.

WHAT YOU'LL OBSERVE:
- How to import code from other files
- How modules communicate with each other
- How to organize a larger project

RUN THIS:
    python main.py

Then explore the other files to see how they work together!
"""

# Import our custom modules
# These are the other Python files in this directory
from user import User
from task_manager import TaskManager
from display import Display

def main():
    """
    Main entry point - coordinates all the modules
    This is like the conductor of an orchestra
    """
    
    print("=" * 60)
    print("🏗️  MODULAR APPLICATION ARCHITECTURE")
    print("=" * 60)
    
    # MODULE 1: User Management
    # The User module handles user-related data and operations
    print("\n📦 MODULE 1: User Management")
    print("-" * 60)
    user = User("Alex", "alex@example.com")
    user.display_info()
    
    # MODULE 2: Task Manager
    # The TaskManager module handles all task-related logic
    print("\n📦 MODULE 2: Task Manager")
    print("-" * 60)
    task_manager = TaskManager(user)
    
    # Add some tasks
    task_manager.add_task("Learn Python basics")
    task_manager.add_task("Build a project")
    task_manager.add_task("Understand modular architecture")
    
    # Complete a task (task IDs start from 1)
    task_manager.complete_task(1)
    
    # MODULE 3: Display
    # The Display module handles presentation logic
    print("\n📦 MODULE 3: Display")
    print("-" * 60)
    Display.show_header("Task Summary")
    tasks = task_manager.get_all_tasks()
    Display.show_tasks(tasks)
    
    stats = task_manager.get_statistics()
    Display.show_statistics(stats)
    
    # OBSERVE THE FLOW
    print("\n" + "=" * 60)
    print("🔍 ARCHITECTURE OBSERVATION")
    print("=" * 60)
    print("""
Notice how the code is organized:

1. main.py (this file)
   - Entry point
   - Coordinates other modules
   - High-level flow

2. user.py
   - Manages user data
   - Knows nothing about tasks
   - Single responsibility

3. task_manager.py
   - Manages tasks
   - Uses the User class
   - Single responsibility

4. display.py
   - Handles output formatting
   - Doesn't know about business logic
   - Single responsibility

BENEFITS OF THIS ARCHITECTURE:
✓ Easy to understand - each file has one job
✓ Easy to modify - change one module without breaking others
✓ Easy to test - test each module independently
✓ Easy to reuse - use modules in different projects
✓ Easy to collaborate - different people work on different modules

This is how professional applications are built!
    """)
    
    print("=" * 60)


if __name__ == "__main__":
    main()

"""
EXPERIMENT IDEAS:
-----------------
1. Add a new module (e.g., 'storage.py' to save tasks to a file)
2. Modify the User class to track more information
3. Add more task management features
4. Create a new display format
5. Add error handling to each module

NEXT STEPS:
-----------
Open each file (user.py, task_manager.py, display.py) and read through them.
See how they're organized and how they interact with each other.
"""
