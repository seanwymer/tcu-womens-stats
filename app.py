import streamlit as st
import pandas as pd
from datetime import date
import os

# List of players and drills
players = ['Select Player', 'Camille Min-Gaultier', 'Charlotte Cattaneo', 'Gracie McGovern', 'Kirstin Angosta', 'Meagan Winans', 'Sofia Barroso Sá', 'Sofie Dimitrova']
drills = ['Tiger 5', 'Combines', 'SIM', 'Up & Downs', '10 Putts']
courses = ['Shady Oaks Country Club', 'Diamond Oaks Country Club', 'Ridglea Country Club', 'Cowboys Golf Club', 'Hawks Creek', 'Other']

# Title and dropdowns
st.title("TCU Women's Golf Stats")
player_name = st.selectbox("Select Player", players)

# Check if a player has been selected (i.e., if the player name is not 'Select Player')
if player_name != 'Select Player':
    # Now allow drill selection
    drill_name = st.selectbox("Select Drill", drills)

    # Form for entering stats if a drill is selected
    with st.form("stats_form"):
        if drill_name == "Tiger 5":
            # Course Name
            course_name = st.selectbox("Course", courses)
        
            # Date (automatically filled with today's date)
            entry_date = st.date_input("Date", value=date.today())

            # 2 Putts or less section with a stronger title
            st.markdown("<h4><b>2 Putts or Less</b></h4>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                two_putts_amount = st.number_input("Amount", min_value=0, step=1)
            with col2:
                two_putts_total = st.number_input("Total", min_value=0, step=1, value=18)

            # Par 5 Scoring (up to 6 par 5's, use dropdowns)
            st.markdown("<h4><b>Par 5 Scoring</b></h4>", unsafe_allow_html=True)
            par_5_scores = []

            # First row for par 5's (4 columns)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                par_5_scores.append(st.selectbox("Par 5 Score 1", ["par", "birdie", "bogey", "double bogey", "n/a"]))
            with col2:
                par_5_scores.append(st.selectbox("Par 5 Score 2", ["par", "birdie", "bogey", "double bogey", "n/a"]))
            with col3:
                par_5_scores.append(st.selectbox("Par 5 Score 3", ["par", "birdie", "bogey", "double bogey", "n/a"]))
            with col4:
                par_5_scores.append(st.selectbox("Par 5 Score 4", ["par", "birdie", "bogey", "double bogey", "n/a"]))
            
            # Second row for par 5's (2 columns)
            col5, col6 = st.columns(2)
            with col5:
                par_5_scores.append(st.selectbox("Par 5 Score 5", ["par", "birdie", "bogey", "double bogey", "n/a"], index=4))
            with col6:
                par_5_scores.append(st.selectbox("Par 5 Score 6", ["par", "birdie", "bogey", "double bogey", "n/a"], index=4))
            
            # No higher than a bogey
            st.markdown("<h4><b>No Higher than a Bogey</b></h4>", unsafe_allow_html=True)
            no_higher_bogey = st.radio("No higher than a bogey?", ("Yes", "No"))

            # Simple U/D (Up and Down)
            st.markdown("<h4><b>Simple U/D</b></h4>", unsafe_allow_html=True)
            ud_amount, ud_total = st.columns(2)
            with ud_amount:
                ud_made = st.number_input("Successful U/D", min_value=0, step=1)
            with ud_total:
                ud_attempts = st.number_input("Total U/D Attempts", min_value=0, step=1)

            # No higher than par with 9i or less
            st.markdown("<h4><b>No Higher than Par w/9i or Less</b></h4>", unsafe_allow_html=True)
            par_9i_amount, par_9i_total = st.columns(2)
            with par_9i_amount:
                shots_made = st.number_input("Successful Attempts", min_value=0, step=1)
            with par_9i_total:
                shots_attempts = st.number_input("Total Attempts", min_value=0, step=1)

        # Submit button for the form
        submit = st.form_submit_button("Submit")

    # Save data to CSV after form submission
    if submit:
        # Create the drill-specific CSV filename
        csv_file = f"{drill_name.lower().replace(' ', '_')}_stats.csv"
        
        if drill_name == "Tiger 5":
            par_5_scores_str = ', '.join(par_5_scores)
            data = {
                'Player': [player_name],
                'Date': [date.today()],
                'Drill': [drill_name],
                'Course': [course_name],
                '2 Putts or Less Amount': [two_putts_amount],
                '2 Putts or Less Total': [two_putts_total],
                'Par 5 Scores': [par_5_scores_str],
                'No Higher than Bogey': [no_higher_bogey],
                'Up & Down Amount': [ud_made],
                'Up & Down Total': [ud_attempts],
                'No Higher than Par w/9i or Less Amount': [shots_made],
                'No Higher than Par w/9i or Less Total': [shots_attempts]
            }
            df = pd.DataFrame(data)

            # Check if the file exists
            file_exists = os.path.isfile(csv_file)

            # Save to the corresponding CSV file
            df.to_csv(csv_file, mode='a', index=False, header=not file_exists)
        
        st.success(f"Data for {player_name} in the '{drill_name}' drill saved to {csv_file}!")
else:
    st.warning("Please select a player to continue.")

