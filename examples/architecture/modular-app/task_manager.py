"""
TASK MANAGER MODULE
===================
This module handles all task-related operations.

DEMONSTRATES:
- Working with collections (lists)
- CRUD operations (Create, Read, Update, Delete)
- Business logic separation
"""

class TaskManager:
    """
    Manages all tasks for a user.
    
    This class shows how to handle collections of data
    and perform operations on them.
    """
    
    def __init__(self, user):
        """
        Initialize the task manager for a specific user
        
        Notice: This class USES the User class
        This is called COMPOSITION - building complex things from simpler parts
        """
        self.user = user
        self.tasks = []  # List to store all tasks
        self.next_id = 1  # Counter for task IDs
    
    def add_task(self, description):
        """
        CREATE operation - add a new task
        """
        task = {
            'id': self.next_id,
            'description': description,
            'completed': False
        }
        self.tasks.append(task)
        self.next_id += 1
        
        print(f"✓ Added task #{task['id']}: {description}")
        return task
    
    def get_all_tasks(self):
        """
        READ operation - get all tasks
        """
        return self.tasks.copy()  # Return a copy to prevent external modification
    
    def get_task_by_id(self, task_id):
        """
        READ operation - get a specific task
        """
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def complete_task(self, task_id):
        """
        UPDATE operation - mark a task as completed
        """
        task = self.get_task_by_id(task_id)
        if task:
            task['completed'] = True
            print(f"✓ Completed task #{task_id}: {task['description']}")
            return True
        else:
            print(f"✗ Task #{task_id} not found")
            return False
    
    def delete_task(self, task_id):
        """
        DELETE operation - remove a task
        """
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            print(f"✓ Deleted task #{task_id}")
            return True
        else:
            print(f"✗ Task #{task_id} not found")
            return False
    
    def get_statistics(self):
        """
        Business logic - calculate statistics
        """
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task['completed'])
        remaining = total - completed
        
        return {
            'total': total,
            'completed': completed,
            'remaining': remaining,
            'completion_rate': (completed / total * 100) if total > 0 else 0
        }
    
    def get_completed_tasks(self):
        """Filter and return only completed tasks"""
        return [task for task in self.tasks if task['completed']]
    
    def get_pending_tasks(self):
        """Filter and return only pending tasks"""
        return [task for task in self.tasks if not task['completed']]


"""
ARCHITECTURAL INSIGHTS:
-----------------------

1. SINGLE RESPONSIBILITY
   - This module only handles tasks
   - Doesn't care about display, storage, or users
   - Focuses on ONE thing and does it well

2. DATA STRUCTURES
   - Uses a list to store tasks
   - Each task is a dictionary with properties
   - Easy to add, remove, and search

3. CRUD PATTERN
   - Create: add_task()
   - Read: get_all_tasks(), get_task_by_id()
   - Update: complete_task()
   - Delete: delete_task()
   
   This pattern is universal in software!

4. ENCAPSULATION
   - All task logic is in one place
   - If you need to change how tasks work, change this file
   - Other modules don't need to know the details

5. COMPOSITION
   - TaskManager uses a User object
   - Building complex functionality from simpler parts
   - Each part can be developed and tested independently

DATA FLOW:
----------
main.py creates TaskManager
    ↓
TaskManager stores tasks in a list
    ↓
Methods modify the list
    ↓
main.py can retrieve and display tasks

USAGE EXAMPLE:
--------------
    from user import User
    from task_manager import TaskManager
    
    user = User("Alice", "alice@example.com")
    manager = TaskManager(user)
    
    manager.add_task("Learn Python")
    manager.add_task("Build a project")
    manager.complete_task(0)
    
    print(manager.get_statistics())
"""
