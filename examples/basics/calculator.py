#!/usr/bin/env python3
"""
CALCULATOR - Functions and User Input
======================================
This program demonstrates:
- How to get input from users
- How to organize code into functions
- How to do calculations
- How data flows through a program

TRY THIS:
1. Run it: python calculator.py
2. Enter some numbers when prompted
3. See the results
4. Read the code to understand how it works
"""

def add(a, b):
    """
    A function is a reusable piece of code
    This one adds two numbers together
    
    Parameters:
    - a: first number
    - b: second number
    
    Returns: the sum of a and b
    """
    result = a + b
    print(f"  ➜ Adding {a} + {b} = {result}")
    return result


def subtract(a, b):
    """Subtracts b from a"""
    result = a - b
    print(f"  ➜ Subtracting {a} - {b} = {result}")
    return result


def multiply(a, b):
    """Multiplies a and b"""
    result = a * b
    print(f"  ➜ Multiplying {a} × {b} = {result}")
    return result


def divide(a, b):
    """Divides a by b"""
    # Be careful! Can't divide by zero
    if b == 0:
        print("  ⚠️  Error: Can't divide by zero!")
        return None
    
    result = a / b
    print(f"  ➜ Dividing {a} ÷ {b} = {result}")
    return result


def main():
    """
    The main function - where our program starts
    This is like the control center that calls other functions
    """
    print("=" * 50)
    print("🧮 SIMPLE CALCULATOR")
    print("=" * 50)
    
    # Get input from the user
    # input() shows a message and waits for the user to type
    # float() converts the text to a number
    print("\nEnter two numbers to calculate:")
    num1 = float(input("First number: "))
    num2 = float(input("Second number: "))
    
    print("\n" + "=" * 50)
    print("CALCULATING ALL OPERATIONS:")
    print("=" * 50)
    
    # Call each function to perform operations
    # Watch how data (num1, num2) flows into each function
    add(num1, num2)
    subtract(num1, num2)
    multiply(num1, num2)
    divide(num1, num2)
    
    print("\n" + "=" * 50)
    print("Done! ✨")
    print("=" * 50)


# This is Python's way of saying "start here"
# It runs the main() function when you execute this file
if __name__ == "__main__":
    main()

"""
ARCHITECTURE OBSERVATION:
-------------------------
Notice how this program is organized:

1. FUNCTIONS at the top (add, subtract, etc.)
   - Each does ONE specific thing
   - Each is reusable
   - Each is easy to understand

2. MAIN function in the middle
   - Coordinates everything
   - Gets user input
   - Calls the other functions

3. ENTRY POINT at the bottom
   - Starts the program

This organization makes code:
- Easy to read
- Easy to modify
- Easy to test
- Easy to reuse

EXPERIMENT IDEAS:
-----------------
- Add a power function (a to the power of b)
- Add a modulo function (remainder after division)
- Make it ask which operation the user wants
- Add more print statements to show each step
- Try breaking it (enter letters instead of numbers) to see error handling
"""
