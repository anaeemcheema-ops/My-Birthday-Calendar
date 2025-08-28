import streamlit as st
import datetime
import calendar

# This list will store all our birthdays.
birthdays_data = []

def add_birthday(name: str, dob_str: str) -> str:
    """
    Adds a new birthday to the list.
    """
    try:
        dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date()
        birthdays_data.append({'name': name, 'dob': dob})
        st.session_state['status_message'] = f"Birthday for {name} ({dob_str}) added successfully!"
        # Clear the input fields after successful addition
        st.session_state['name_input'] = ''
        st.session_state['dob_input'] = ''
        return "Success"
    except ValueError:
        st.session_state['status_message'] = "Error: Invalid date format. Please use YYYY-MM-DD."
        return "Failure"

def get_all_birthdays() -> str:
    """
    Returns a formatted string of all stored birthdays.
    """
    if not birthdays_data:
        return "No birthdays added yet."

    sorted_birthdays = sorted(birthdays_data, key=lambda x: (x['dob'].month, x['dob'].day))

    output = "### All Birthdays\n"
    for bd in sorted_birthdays:
        output += f"- **{bd['name']}**: {bd['dob'].strftime('%B %d, %Y')}\n"
    return output

def get_upcoming_birthdays(days_in_advance: int) -> str:
    """
    Returns a formatted string of upcoming birthdays within a specified number of days.
    """
    if not birthdays_data:
        return "No birthdays added yet."

    today = datetime.date.today()
    upcoming = []

    for bd in birthdays_data:
        birthday_this_year = bd['dob'].replace(year=today.year)

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

# --- Streamlit UI Components ---

# Initialize session state for a persistent data store
if 'birthdays_data' not in st.session_state:
    st.session_state.birthdays_data = []
if 'status_message' not in st.session_state:
    st.session_state.status_message = ''

st.title("🎂 Birthday Manager")

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Add Birthday", "All Birthdays", "Upcoming"])

with tab1:
    st.header("Add New Birthday")
    name = st.text_input("Person's Name", key='name_input')
    dob_str = st.text_input("Date of Birth (YYYY-MM-DD)", placeholder="e.g., 1990-05-15", key='dob_input')
    add_button = st.button("Add Birthday")

    if add_button and name and dob_str:
        status = add_birthday(name, dob_str)
        st.session_state.birthdays_data = birthdays_data
    if st.session_state.status_message:
        if "Error" in st.session_state.status_message:
            st.error(st.session_state.status_message)
        else:
            st.success(st.session_state.status_message)

with tab2:
    st.header("All Birthdays")
    if st.button("View All Birthdays"):
        st.markdown(get_all_birthdays())

with tab3:
    st.header("Upcoming Birthdays")
    days_in_advance = st.slider("Select how many days in advance", min_value=7, max_value=180, value=30, step=7)
    if st.button("Check Upcoming Birthdays"):
        st.markdown(get_upcoming_birthdays(days_in_advance))
