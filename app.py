import datetime
import calendar

# This list will store all our birthdays.
# Each birthday will be a dictionary with 'name' and 'dob' (Date of Birth).
birthdays_data = []

def add_birthday(name: str, dob_str: str) -> str:
    """
    Adds a new birthday to the list.
    Args:
        name (str): The name of the person.
        dob_str (str): The date of birth in 'YYYY-MM-DD' format.
    Returns:
        str: A message indicating success or failure.
    """
    try:
        # Parse the date string into a datetime object
        dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date()
        birthdays_data.append({'name': name, 'dob': dob})
        return f"Birthday for {name} ({dob_str}) added successfully!"
    except ValueError:
        return "Error: Invalid date format. Please use YYYY-MM-DD."

def get_all_birthdays() -> str:
    """
    Returns a formatted string of all stored birthdays.
    Returns:
        str: A string listing all birthdays, or a message if none are found.
    """
    if not birthdays_data:
        return "No birthdays added yet."

    # Sort birthdays by month and then day
    sorted_birthdays = sorted(birthdays_data, key=lambda x: (x['dob'].month, x['dob'].day))

    output = "--- All Birthdays ---\n"
    for bd in sorted_birthdays:
        # Format the date nicely for display
        output += f"{bd['name']}: {bd['dob'].strftime('%B %d, %Y')}\n"
    return output

def get_upcoming_birthdays(days_in_advance: int = 30) -> str:
    """
    Returns a formatted string of upcoming birthdays within a specified number of days.
    Args:
        days_in_advance (int): Number of days to look ahead for upcoming birthdays.
    Returns:
        str: A string listing upcoming birthdays, or a message if none are found.
    """
    if not birthdays_data:
        return "No birthdays added yet."

    today = datetime.date.today()
    upcoming = []

    for bd in birthdays_data:
        # Get the birthday for the current year
        birthday_this_year = bd['dob'].replace(year=today.year)

        # Handle leap year birthdays (Feb 29th) when the current year is not a leap year
        if bd['dob'].month == 2 and bd['dob'].day == 29 and not calendar.isleap(today.year):
            # If current year is not a leap year, treat Feb 29 as Feb 28 for comparison
            birthday_this_year = bd['dob'].replace(year=today.year, day=28)


        # If the birthday has already passed this year, check for next year
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        # Calculate the difference in days
        time_to_birthday = (birthday_this_year - today).days

        # If it's within our look-ahead window and not today (today will be covered by "all birthdays")
        # Let's adjust this to include today if it's an upcoming birthday
        if 0 <= time_to_birthday <= days_in_advance:
            upcoming.append({'name': bd['name'], 'date': birthday_this_year, 'original_dob': bd['dob']})

    if not upcoming:
        return f"No birthdays upcoming in the next {days_in_advance} days."

    # Sort upcoming birthdays chronologically
    sorted_upcoming = sorted(upcoming, key=lambda x: x['date'])

    output = f"--- Upcoming Birthdays (next {days_in_advance} days) ---\n"
    for bd in sorted_upcoming:
        # Calculate age
        age = bd['date'].year - bd['original_dob'].year
        output += f"{bd['name']}: {bd['date'].strftime('%B %d')} (turning {age})\n"
    return output

# Example Usage (you can run these in a separate cell to test the logic)
# print(add_birthday("Alice", "1990-08-30"))
# print(add_birthday("Bob", "1985-01-15"))
# print(add_birthday("Charlie", "1992-12-25"))
# print(add_birthday("Diana", "1995-02-29")) # Leap year baby
# print(add_birthday("Eve", datetime.date.today().strftime('%Y-%m-%d'))) # Today's birthday
# print("\n" + get_all_birthdays())
# print("\n" + get_upcoming_birthdays(60))

import gradio as gr
import datetime
import calendar # Make sure to import calendar if not already in the previous cell

# Re-define or ensure these are accessible from the previous cell if you restart the kernel
# For simplicity, I'm including them here again, but in a real scenario, you'd define them once.
birthdays_data = []

def add_birthday(name: str, dob_str: str) -> str:
    """
    Adds a new birthday to the list.
    Args:
        name (str): The name of the person.
        dob_str (str): The date of birth in 'YYYY-MM-DD' format.
    Returns:
        str: A message indicating success or failure.
    """
    try:
        dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date()
        birthdays_data.append({'name': name, 'dob': dob})
        return f"Birthday for {name} ({dob_str}) added successfully!"
    except ValueError:
        return "Error: Invalid date format. Please use YYYY-MM-DD."

def get_all_birthdays() -> str:
    """
    Returns a formatted string of all stored birthdays.
    Returns:
        str: A string listing all birthdays, or a message if none are found.
    """
    if not birthdays_data:
        return "No birthdays added yet."

    sorted_birthdays = sorted(birthdays_data, key=lambda x: (x['dob'].month, x['dob'].day))

    output = "### All Birthdays\n" # Using Markdown for a nicer heading
    for bd in sorted_birthdays:
        output += f"- **{bd['name']}**: {bd['dob'].strftime('%B %d, %Y')}\n"
    return output

def get_upcoming_birthdays(days_in_advance_str: str = "30") -> str:
    """
    Returns a formatted string of upcoming birthdays within a specified number of days.
    Gradio passes strings, so we convert it to int.
    Args:
        days_in_advance_str (str): Number of days to look ahead for upcoming birthdays (as a string).
    Returns:
        str: A string listing upcoming birthdays, or a message if none are found.
    """
    try:
        days_in_advance = int(days_in_advance_str)
    except ValueError:
        return "Error: Please enter a valid number for days in advance."

    if not birthdays_data:
        return "No birthdays added yet."

    today = datetime.date.today()
    upcoming = []

    for bd in birthdays_data:
        birthday_this_year = bd['dob'].replace(year=today.year)

        # Handle leap year birthdays (Feb 29th) when the current year is not a leap year
        if bd['dob'].month == 2 and bd['dob'].day == 29 and not calendar.isleap(today.year):
            birthday_this_year = bd['dob'].replace(year=today.year, day=28)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        time_to_birthday = (birthday_this_year - today).days

        if 0 <= time_to_birthday <= days_in_advance:
            upcoming.append({'name': bd['name'], 'date': birthday_this_year, 'original_dob': bd['dob']})

    if not upcoming:
        return f"No birthdays upcoming in the next {days_in_advance} days."

    sorted_upcoming = sorted(upcoming, key=lambda x: x['date'])

    output = f"### Upcoming Birthdays (next {days_in_advance} days)\n"
    for bd in sorted_upcoming:
        age = bd['date'].year - bd['original_dob'].year
        output += f"- **{bd['name']}**: {bd['date'].strftime('%B %d')} (turning {age})\n"
    return output

# --- Gradio Interface Setup ---

# Define the input components for adding a birthday
name_input = gr.Textbox(label="Person's Name")
dob_input = gr.Textbox(label="Date of Birth (YYYY-MM-DD)", placeholder="e.g., 1990-05-15")

# Output components
add_output = gr.Markdown(label="Add Birthday Status")
display_output = gr.Markdown(label="Birthday List")
upcoming_output = gr.Markdown(label="Upcoming Birthdays")

# Interface for adding a birthday
add_interface = gr.Interface(
    fn=add_birthday,
    inputs=[name_input, dob_input],
    outputs=add_output,
    title="Add New Birthday",
    description="Enter the name and Date of Birth (YYYY-MM-DD) to add a new birthday.",
    allow_flagging="never"
)

# Interface for viewing all birthdays
all_birthdays_interface = gr.Interface(
    fn=get_all_birthdays,
    inputs=[],
    outputs=display_output,
    title="View All Birthdays",
    description="Click the button to see all stored birthdays.",
    allow_flagging="never"
)

# Interface for viewing upcoming birthdays
upcoming_days_input = gr.Slider(minimum=7, maximum=180, step=7, value=30, label="Days in Advance")
upcoming_birthdays_interface = gr.Interface(
    fn=get_upcoming_birthdays,
    inputs=upcoming_days_input,
    outputs=upcoming_output,
    title="View Upcoming Birthdays",
    description="Select how many days in advance you want to check for birthdays.",
    allow_flagging="never"
)

# Combine all interfaces into a single Gradio tabbed interface
demo = gr.TabbedInterface(
    [add_interface, all_birthdays_interface, upcoming_birthdays_interface],
    ["Add Birthday", "All Birthdays", "Upcoming"]
)

# Launch the Gradio app
# The `share=True` option will generate a public link you can share.
# This link is temporary and will expire after some time.
demo.launch(share=True)