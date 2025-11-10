#!/usr/bin/env python3
"""
LISTS - Working with Collections of Data
=========================================
This demonstrates:
- How to store multiple items in one variable
- How to add, remove, and modify items
- How to loop through data
- How programs work with collections

TRY THIS:
1. Run it: python lists.py
2. Watch how the list changes
3. Read the comments to understand each operation
"""

def show_list(items, title="Current list"):
    """Helper function to display a list nicely"""
    print(f"\n{title}:")
    if len(items) == 0:
        print("  (empty)")
    else:
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item}")


def main():
    print("=" * 60)
    print("📋 WORKING WITH LISTS")
    print("=" * 60)
    
    # CREATING A LIST
    # A list is like a container that holds multiple items
    # Use square brackets [] to create a list
    print("\n🔹 CREATING A LIST")
    shopping_list = ["apples", "bread", "milk"]
    show_list(shopping_list, "Initial shopping list")
    
    # ADDING ITEMS
    # .append() adds an item to the end
    print("\n🔹 ADDING ITEMS")
    print("Adding 'eggs' to the list...")
    shopping_list.append("eggs")
    show_list(shopping_list)
    
    print("Adding 'butter' to the list...")
    shopping_list.append("butter")
    show_list(shopping_list)
    
    # ACCESSING ITEMS
    # Use [index] to get a specific item
    # Python counts from 0! So [0] is the first item
    print("\n🔹 ACCESSING ITEMS")
    print(f"The first item (index 0) is: {shopping_list[0]}")
    print(f"The second item (index 1) is: {shopping_list[1]}")
    print(f"The last item is: {shopping_list[-1]}")  # -1 means "last item"
    
    # MODIFYING ITEMS
    # You can change an item by assigning a new value
    print("\n🔹 MODIFYING ITEMS")
    print(f"Changing 'bread' to 'whole wheat bread'...")
    shopping_list[1] = "whole wheat bread"
    show_list(shopping_list)
    
    # REMOVING ITEMS
    # .remove() removes a specific item
    print("\n🔹 REMOVING ITEMS")
    print("Removing 'milk' from the list...")
    shopping_list.remove("milk")
    show_list(shopping_list)
    
    # LOOPING THROUGH A LIST
    # This is how you do something with each item
    print("\n🔹 LOOPING THROUGH THE LIST")
    print("Let's 'buy' each item:")
    for item in shopping_list:
        print(f"  ✓ Bought {item}")
    
    # COUNTING AND CHECKING
    print("\n🔹 USEFUL LIST OPERATIONS")
    print(f"Total items in list: {len(shopping_list)}")
    print(f"Is 'eggs' in the list? {('eggs' in shopping_list)}")
    print(f"Is 'cookies' in the list? {('cookies' in shopping_list)}")
    
    # SORTING
    print("\n🔹 SORTING THE LIST")
    shopping_list.sort()  # Sorts alphabetically
    show_list(shopping_list, "Sorted alphabetically")
    
    # CLEARING THE LIST
    print("\n🔹 CLEARING THE LIST")
    print("After shopping, we clear the list:")
    shopping_list.clear()
    show_list(shopping_list, "Empty list")
    
    print("\n" + "=" * 60)
    print("Done! You now understand how lists work! ✨")
    print("=" * 60)


if __name__ == "__main__":
    main()

"""
WHY ARE LISTS IMPORTANT?
------------------------
Lists are fundamental to programming because:

1. REAL PROGRAMS WORK WITH MULTIPLE ITEMS
   - A todo app has a list of tasks
   - A store has a list of products
   - A game has a list of players

2. THEY'RE EFFICIENT
   - Instead of: item1, item2, item3, item4...
   - You have: items = [item1, item2, item3, item4]

3. YOU CAN PROCESS THEM AUTOMATICALLY
   - Loop through thousands of items with the same code
   - Sort, filter, search automatically

EXPERIMENT IDEAS:
-----------------
- Create a list of your favorite movies
- Add and remove items
- Try sorting numbers: [5, 2, 9, 1, 7]
- Create a list of lists (nested lists)
- Make a program that lets users add items interactively
- Count how many items start with a certain letter
"""
