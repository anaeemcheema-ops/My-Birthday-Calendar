import streamlit as st
import datetime
import calendar

# Initialize a persistent data store using Streamlit's session state.
# This ensures birthdays_data is not reset every time the app reruns.
if 'birthdays_data' not in st.session_state:
    st.session_state.birthdays_data = []

def add_birthday(name: str, dob_str: str) -> str:
    """
    Adds a new birthday to the session state.
    """
    try:
        dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date()
        st.session_state.birthdays_data.append({'name': name, 'dob': dob})
        return f"Birthday for {name} ({dob_str}) added successfully!"
    except ValueError:
        return "Error: Invalid date format. Please use YYYY-MM-DD."

def get_all_birthdays() -> str:
    """
    Returns a formatted string of all stored birthdays.
    """
    if not st.session_state.birthdays_data:
        return "No birthdays added yet."

    sorted_birthdays = sorted(st.session_state.birthdays_data, key=lambda x: (x['dob'].month, x['dob'].day))
    output = "### All Birthdays\n"
    for bd in sorted_birthdays:
        output += f"- **{bd['name']}**: {bd['dob'].strftime('%B %d, %Y')}\n"
    return output

def get_upcoming_birthdays(days_in_advance: int) -> str:
    """
    Returns a formatted string of upcoming birthdays within a specified number of days.
    """
    if not st.session_state.birthdays_data:
        return "No birthdays added yet."

    today = datetime.date.today()
    upcoming = []

    for bd in st.session_state.birthdays_data:
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

# --- Streamlit App Layout ---

st.title("🎂 Birthday Manager")

# Create a tabbed interface using Streamlit
tab1, tab2, tab3 = st.tabs(["Add Birthday", "All Birthdays", "Upcoming"])

with tab1:
    st.header("Add New Birthday")
    with st.form("add_birthday_form"):
        name_input = st.text_input("Person's Name")
        dob_input = st.text_input("Date of Birth (YYYY-MM-DD)", placeholder="e.g., 1990-05-15")
        submit_button = st.form_submit_button("Add Birthday")

    if submit_button:
        if name_input and dob_input:
            status = add_birthday(name_input, dob_input)
            if "Error" in status:
                st.error(status)
            else:
                st.success(status)
        else:
            st.warning("Please fill in both name and date of birth.")

with tab2:
    st.header("All Birthdays")
    if st.button("View All Birthdays"):
        st.markdown(get_all_birthdays())

with tab3:
    st.header("Upcoming Birthdays")
    days_in_advance_input = st.slider("Select how many days in advance", min_value=7, max_value=180, value=30, step=7)
    if st.button("Check Upcoming Birthdays"):
        st.markdown(get_upcoming_birthdays(days_in_advance_input))
