#!/usr/bin/env python3
"""
DATA FLOW DEMONSTRATION
=======================
This program shows how data flows through an application.

OBSERVE:
- Data comes IN (user input)
- Data is PROCESSED (functions transform it)
- Data is STORED (variables hold it)
- Data goes OUT (displayed to user)

Think of data like water flowing through pipes!
"""

import json


def demonstrate_data_flow():
    """Main demonstration of data flow"""
    
    print("=" * 70)
    print("💧 DATA FLOW VISUALIZATION")
    print("=" * 70)
    
    # ==========================================
    # STEP 1: INPUT (Data comes into the system)
    # ==========================================
    print("\n🔵 STEP 1: INPUT - Data Enters the System")
    print("-" * 70)
    
    # Simulating user input (you could use input() for real interaction)
    raw_data = "john doe, 25, john@example.com"
    print(f"Raw input data: '{raw_data}'")
    print("↓ Data is just a string of text at this point")
    
    # ==========================================
    # STEP 2: PARSING (Transform raw data into structured format)
    # ==========================================
    print("\n🔵 STEP 2: PARSING - Transform Raw Data")
    print("-" * 70)
    
    parsed_data = parse_user_data(raw_data)
    print(f"Parsed data structure:")
    print(f"  Type: {type(parsed_data)}")
    print(f"  Content: {parsed_data}")
    print("↓ Data is now organized into a dictionary")
    
    # ==========================================
    # STEP 3: VALIDATION (Check if data is valid)
    # ==========================================
    print("\n🔵 STEP 3: VALIDATION - Check Data Quality")
    print("-" * 70)
    
    validation_result = validate_user_data(parsed_data)
    print(f"Validation result: {validation_result}")
    
    if not validation_result['valid']:
        print(f"❌ Errors found: {validation_result['errors']}")
        print("↓ Invalid data would be rejected here")
    else:
        print("✅ Data is valid and can proceed")
        print("↓ Data moves to the next stage")
    
    # ==========================================
    # STEP 4: TRANSFORMATION (Modify/enhance data)
    # ==========================================
    print("\n🔵 STEP 4: TRANSFORMATION - Enhance Data")
    print("-" * 70)
    
    enriched_data = enrich_user_data(parsed_data)
    print(f"Enhanced data:")
    for key, value in enriched_data.items():
        print(f"  {key}: {value}")
    print("↓ Data now has additional computed fields")
    
    # ==========================================
    # STEP 5: STORAGE (Store data in a structure)
    # ==========================================
    print("\n🔵 STEP 5: STORAGE - Save to Data Structure")
    print("-" * 70)
    
    # In real apps, this would be a database
    # Here we use a list as our simple "database"
    user_database = []
    user_database.append(enriched_data)
    
    print(f"Data stored in database")
    print(f"Database now contains {len(user_database)} user(s)")
    print("↓ Data is persisted and can be retrieved later")
    
    # ==========================================
    # STEP 6: RETRIEVAL (Get data back from storage)
    # ==========================================
    print("\n🔵 STEP 6: RETRIEVAL - Get Data Back")
    print("-" * 70)
    
    retrieved_user = user_database[0]
    print(f"Retrieved user: {retrieved_user['name']}")
    print("↓ Data is fetched from storage")
    
    # ==========================================
    # STEP 7: FORMATTING (Prepare data for output)
    # ==========================================
    print("\n🔵 STEP 7: FORMATTING - Prepare for Display")
    print("-" * 70)
    
    formatted_output = format_user_display(retrieved_user)
    print("Formatted for display:")
    print(formatted_output)
    print("↓ Data is now human-readable")
    
    # ==========================================
    # STEP 8: OUTPUT (Data leaves the system)
    # ==========================================
    print("\n🔵 STEP 8: OUTPUT - Data Exits the System")
    print("-" * 70)
    
    # Different output formats
    print("As JSON:")
    print(json.dumps(retrieved_user, indent=2))
    
    print("\n" + "=" * 70)
    print("🎯 DATA FLOW COMPLETE!")
    print("=" * 70)
    
    # Show the complete flow
    show_flow_diagram()


def parse_user_data(raw_input):
    """
    Parse raw string input into a structured dictionary
    
    INPUT: "john doe, 25, john@example.com"
    OUTPUT: {'name': 'john doe', 'age': 25, 'email': 'john@example.com'}
    """
    parts = [p.strip() for p in raw_input.split(',')]
    
    return {
        'name': parts[0],
        'age': int(parts[1]),
        'email': parts[2]
    }


def validate_user_data(user_data):
    """
    Validate that user data meets requirements
    
    Returns: {'valid': True/False, 'errors': [...]}
    """
    errors = []
    
    # Check name
    if len(user_data['name']) < 2:
        errors.append("Name too short")
    
    # Check age
    if user_data['age'] < 0 or user_data['age'] > 150:
        errors.append("Invalid age")
    
    # Check email
    if '@' not in user_data['email']:
        errors.append("Invalid email format")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }


def enrich_user_data(user_data):
    """
    Add computed fields to the data
    
    Takes existing data and adds new calculated fields
    """
    enriched = user_data.copy()
    
    # Add computed fields
    enriched['name_capitalized'] = user_data['name'].title()
    enriched['is_adult'] = user_data['age'] >= 18
    enriched['email_domain'] = user_data['email'].split('@')[1]
    enriched['initials'] = ''.join([word[0].upper() for word in user_data['name'].split()])
    
    return enriched


def format_user_display(user_data):
    """
    Format user data for display
    
    Transforms data into a readable format
    """
    output = f"""
    ╔════════════════════════════════╗
    ║        USER PROFILE            ║
    ╠════════════════════════════════╣
    ║ Name:     {user_data['name_capitalized']:<20} ║
    ║ Initials: {user_data['initials']:<20} ║
    ║ Age:      {user_data['age']:<20} ║
    ║ Adult:    {('Yes' if user_data['is_adult'] else 'No'):<20} ║
    ║ Email:    {user_data['email']:<20} ║
    ║ Domain:   {user_data['email_domain']:<20} ║
    ╚════════════════════════════════╝
    """
    return output


def show_flow_diagram():
    """Display a visual diagram of the data flow"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                        DATA FLOW DIAGRAM                         ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║   📥 INPUT                                                       ║
║   └─→ Raw Data: "john doe, 25, john@example.com"               ║
║       │                                                          ║
║       ↓                                                          ║
║   🔧 PARSING                                                     ║
║   └─→ Structured: {'name': 'john doe', 'age': 25, ...}         ║
║       │                                                          ║
║       ↓                                                          ║
║   ✓ VALIDATION                                                   ║
║   └─→ Checks: name length, age range, email format             ║
║       │                                                          ║
║       ↓                                                          ║
║   ⚡ TRANSFORMATION                                              ║
║   └─→ Enhanced: adds initials, domain, is_adult, etc.          ║
║       │                                                          ║
║       ↓                                                          ║
║   💾 STORAGE                                                     ║
║   └─→ Saved: added to database/list                            ║
║       │                                                          ║
║       ↓                                                          ║
║   🔍 RETRIEVAL                                                   ║
║   └─→ Fetched: got data back from storage                      ║
║       │                                                          ║
║       ↓                                                          ║
║   🎨 FORMATTING                                                  ║
║   └─→ Prepared: made human-readable                            ║
║       │                                                          ║
║       ↓                                                          ║
║   📤 OUTPUT                                                      ║
║   └─→ Displayed: shown to user                                 ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    demonstrate_data_flow()

"""
KEY INSIGHTS ABOUT DATA FLOW:
==============================

1. DATA IS TRANSFORMED
   - Starts as one thing (string)
   - Ends as another (formatted display)
   - Each step adds value

2. PIPELINE ARCHITECTURE
   - Data flows through a series of stages
   - Each stage has a specific purpose
   - Output of one stage is input to the next

3. SEPARATION OF CONCERNS
   - Parsing is separate from validation
   - Validation is separate from storage
   - Each function does ONE thing

4. DATA TYPES MATTER
   - String → Dictionary → Enhanced Dictionary → Formatted String
   - Notice how the type changes as data flows

5. ERROR HANDLING
   - Validation catches bad data early
   - Prevents problems downstream
   - Fail fast principle

REAL-WORLD EXAMPLES:
====================

WEB FORM SUBMISSION:
  User fills form → Browser sends data → Server receives
  → Validates → Stores in DB → Sends confirmation → User sees message

E-COMMERCE PURCHASE:
  User clicks buy → Payment info → Validate card → Process payment
  → Update inventory → Send confirmation → Generate receipt

API REQUEST:
  App sends request → Server receives → Authenticates → Processes
  → Queries database → Formats response → Returns JSON → App displays

EXPERIMENT IDEAS:
=================
1. Add more validation rules
2. Add error handling for invalid input
3. Add multiple transformation steps
4. Add different output formats (CSV, XML)
5. Chain multiple data flows together
6. Add logging at each step to trace data
"""
