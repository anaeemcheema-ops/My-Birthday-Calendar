import streamlit as st
import datetime
import calendar

# Initialize a persistent data store using Streamlit's session state.
# This is crucial for Streamlit apps because the script reruns from top to bottom
# every time there's an interaction. Session state ensures your data (like birthdays)
# doesn't get lost between interactions.
if 'birthdays_data' not in st.session_state:
    st.session_state.birthdays_data = []

# --- Core Logic Functions (mostly unchanged from your original, just refactored for clarity) ---

def add_birthday_logic(name: str, dob_str: str) -> str:
    """
    Adds a new birthday to the session state. This function handles the core logic
    of parsing the date and adding it to our list of birthdays.
    """
    try:
        # Attempt to parse the date string into a datetime.date object
        dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date()
        # Append the new birthday as a dictionary to our list in session state
        st.session_state.birthdays_data.append({'name': name, 'dob': dob})
        return f"Birthday for {name} ({dob_str}) added successfully!"
    except ValueError:
        # If the date format is incorrect, return an error message
        return "Error: Invalid date format. Please use YYYY-MM-DD."

def get_all_birthdays_logic() -> str:
    """
    Generates a formatted string of all stored birthdays, sorted by month and day.
    """
    if not st.session_state.birthdays_data:
        return "No birthdays added yet."

    # Sort birthdays first by month, then by day
    sorted_birthdays = sorted(st.session_state.birthdays_data, key=lambda x: (x['dob'].month, x['dob'].day))

    output = "### All Birthdays\n" # Use Markdown for a nice heading
    for bd in sorted_birthdays:
        # Format each birthday entry
        output += f"- **{bd['name']}**: {bd['dob'].strftime('%B %d, %Y')}\n"
    return output

def get_upcoming_birthdays_logic(days_in_advance: int) -> str:
    """
    Generates a formatted string of upcoming birthdays within a specified number of days
    from today. It also calculates the age they will be turning.
    """
    if not st.session_state.birthdays_data:
        return "No birthdays added yet."

    today = datetime.date.today()
    upcoming = []

    for bd in st.session_state.birthdays_data:
        # Create a birthday for the current year
        birthday_this_year = bd['dob'].replace(year=today.year)

        # Special handling for Leap Year babies (Feb 29th)
        # If the current year is not a leap year, treat Feb 29 as Feb 28 for comparisons
        if bd['dob'].month == 2 and bd['dob'].day == 29 and not calendar.isleap(today.year):
            birthday_this_year = bd['dob'].replace(year=today.year, day=28)

        # If the birthday for the current year has already passed, consider next year's birthday
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        # Calculate how many days are left until the birthday
        time_to_birthday = (birthday_this_year - today).days

        # Check if the birthday falls within our look-ahead window (including today)
        if 0 <= time_to_birthday <= days_in_advance:
            upcoming.append({'name': bd['name'], 'date': birthday_this_year, 'original_dob': bd['dob']})

    if not upcoming:
        return f"No birthdays upcoming in the next {days_in_advance} days."

    # Sort upcoming birthdays chronologically
    sorted_upcoming = sorted(upcoming, key=lambda x: x['date'])

    output = f"### Upcoming Birthdays (next {days_in_advance} days)\n"
    for bd in sorted_upcoming:
        # Calculate the age the person will be turning
        age = bd['date'].year - bd['original_dob'].year
        output += f"- **{bd['name']}**: {bd['date'].strftime('%B %d')} (turning {age})\n"
    return output

# --- Streamlit User Interface Setup ---

# Set the title of your Streamlit application
st.title("🎂 Birthday Manager")

# Streamlit uses `st.tabs` to create a tabbed interface, similar to Gradio's TabbedInterface
tab1, tab2, tab3 = st.tabs(["Add Birthday", "All Birthdays", "Upcoming"])

with tab1:
    st.header("Add New Birthday")
    # Streamlit uses `st.form` to group input widgets. This ensures that
    # the entire form is processed only when the submit button is clicked.
    with st.form("add_birthday_form"):
        # `st.text_input` creates a text input field
        name_input = st.text_input("Person's Name")
        # `placeholder` provides a hint to the user
        dob_input = st.text_input("Date of Birth (YYYY-MM-DD)", placeholder="e.g., 1990-05-15")
        # `st.form_submit_button` is required to submit the form
        submit_button = st.form_submit_button("Add Birthday")

    # This block executes when the submit button is pressed
    if submit_button:
        if name_input and dob_input:
            # Call our logic function to add the birthday
            status_message = add_birthday_logic(name_input, dob_input)
            # Display success or error messages using Streamlit's `st.success` or `st.error`
            if "Error" in status_message:
                st.error(status_message)
            else:
                st.success(status_message)
        else:
            st.warning("Please fill in both name and date of birth.")

with tab2:
    st.header("All Birthdays")
    # A button to trigger viewing all birthdays
    if st.button("View All Birthdays"):
        # Display the result from our logic function using `st.markdown`
        # `st.markdown` is great for rendering formatted text (like headings and lists)
        st.markdown(get_all_birthdays_logic())

with tab3:
    st.header("Upcoming Birthdays")
    # `st.slider` creates an interactive slider for selecting the number of days
    days_in_advance_input = st.slider(
        "Select how many days in advance",
        min_value=7,     # Minimum value for the slider
        max_value=180,   # Maximum value for the slider
        value=30,        # Default value
        step=7           # Increment step
    )
    # A button to trigger checking upcoming birthdays
    if st.button("Check Upcoming Birthdays"):
        # Display the result from our logic function
        st.markdown(get_upcoming_birthdays_logic(days_in_advance_input))

