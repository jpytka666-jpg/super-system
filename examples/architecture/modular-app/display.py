"""
DISPLAY MODULE
==============
This module handles all output formatting and presentation.

DEMONSTRATES:
- Separation of presentation logic from business logic
- Static methods (utility functions)
- Consistent formatting
"""

class Display:
    """
    Handles all display/output operations.
    
    Uses static methods because we don't need to store any data.
    These are like utility functions organized in a class.
    """
    
    @staticmethod
    def show_header(title):
        """
        Display a formatted header
        
        @staticmethod means we can call this without creating a Display object
        Example: Display.show_header("My Title")
        """
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)
    
    @staticmethod
    def show_tasks(tasks):
        """
        Display a list of tasks in a formatted way
        """
        if not tasks:
            print("  No tasks to display")
            return
        
        print("\n  Your Tasks:")
        print("  " + "-" * 56)
        
        for task in tasks:
            # Choose symbol based on completion status
            symbol = "✓" if task['completed'] else "○"
            status = "DONE" if task['completed'] else "TODO"
            
            # Format: [✓] Task description (DONE)
            print(f"  [{symbol}] #{task['id']}: {task['description']} ({status})")
        
        print("  " + "-" * 56)
    
    @staticmethod
    def show_statistics(stats):
        """
        Display task statistics in a formatted way
        """
        print("\n  📊 Statistics:")
        print("  " + "-" * 56)
        print(f"  Total Tasks:     {stats['total']}")
        print(f"  Completed:       {stats['completed']}")
        print(f"  Remaining:       {stats['remaining']}")
        print(f"  Completion Rate: {stats['completion_rate']:.1f}%")
        print("  " + "-" * 56)
    
    @staticmethod
    def show_error(message):
        """Display an error message"""
        print(f"\n  ❌ ERROR: {message}")
    
    @staticmethod
    def show_success(message):
        """Display a success message"""
        print(f"\n  ✅ SUCCESS: {message}")
    
    @staticmethod
    def show_info(message):
        """Display an informational message"""
        print(f"\n  ℹ️  INFO: {message}")


"""
WHY SEPARATE DISPLAY LOGIC?
----------------------------

1. FLEXIBILITY
   - Want to change how things look? Change this file only
   - Want a different output format? Create another display module
   - Want to add colors? Modify this module

2. TESTABILITY
   - Business logic doesn't depend on display
   - Can test task operations without worrying about output
   - Can test display separately

3. REUSABILITY
   - Same display functions work for different data sources
   - Can use in console apps, web apps, or GUIs
   - Just change the Display module implementation

4. SINGLE RESPONSIBILITY
   - This module ONLY handles presentation
   - TaskManager ONLY handles logic
   - Each focuses on what it does best

ALTERNATIVE DISPLAYS:
---------------------
You could create:
- DisplayJSON - output as JSON
- DisplayHTML - generate HTML
- DisplayCSV - export as CSV
- DisplayGUI - create graphical interface

All without changing your business logic!

ARCHITECTURE PATTERN:
---------------------
This is called PRESENTATION LAYER or VIEW LAYER

   USER SEES
       ↓
   DISPLAY (this module) - How to show it
       ↓
   BUSINESS LOGIC (task_manager) - What to show
       ↓
   DATA (tasks list) - What we have

Each layer has a specific job!

USAGE EXAMPLE:
--------------
    from display import Display
    
    Display.show_header("My Application")
    
    tasks = [
        {'id': 1, 'description': 'Task 1', 'completed': True},
        {'id': 2, 'description': 'Task 2', 'completed': False}
    ]
    Display.show_tasks(tasks)
    
    stats = {'total': 2, 'completed': 1, 'remaining': 1, 'completion_rate': 50}
    Display.show_statistics(stats)
"""
