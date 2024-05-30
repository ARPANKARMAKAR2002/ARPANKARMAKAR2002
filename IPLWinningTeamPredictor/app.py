import streamlit as st
import pickle
import pandas as pd
import os

# Define the path to the pickle file
pickle_file_path = 'C:/Users/KIIT/Documents/IPLWinningTeamPredictor/pipe.pkl'

# Check if the file exists
if not os.path.exists(pickle_file_path):
    st.error(f"Model file not found at {pickle_file_path}. Please ensure the file is in the correct location.")
else:
    pipe = pickle.load(open(pickle_file_path, 'rb'))

    # List of IPL teams
    teams = [
        'Sunrisers Hyderabad', 
        'Mumbai Indians',
        'Royal Challengers Bangalore',
        'Kolkata Knight Riders',
        'Kings XI Punjab',
        'Chennai Super Kings',
        'Rajasthan Royals',
        'Delhi Capitals'
    ]

    # List of cities where IPL matches are played
    cities = [
        'Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
        'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
        'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
        'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
        'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
        'Sharjah', 'Mohali', 'Bengaluru'
    ]

    # Title of the Streamlit app
    st.title('IPL Win Predictor')

    # Columns for selecting teams
    col1, col2 = st.columns(2)

    with col1:
        batting_team = st.selectbox('Select the batting team', sorted(teams))
    with col2:
        bowling_team = st.selectbox('Select the bowling team', sorted(teams))

    # Select the host city
    selected_city = st.selectbox('Select host city', sorted(cities))

    # Input the target score
    target = st.number_input('Target')

    # Columns for current match situation
    col3, col4, col5 = st.columns(3)

    with col3:
        score = st.number_input('Score')
    with col4:
        overs = st.number_input('Overs completed', min_value=0.1, max_value=20.0, step=0.1)
    with col5:
        wickets = st.number_input('Wickets out', min_value=0, max_value=10, step=1)

    # Button to predict probability
    if st.button('Predict Probability'):
        runs_left = target - score
        balls_left = 120 - (overs * 6)
        wickets_left = 10 - wickets
        crr = score / overs
        rrr = (runs_left * 6) / balls_left

        # Create input DataFrame for the model
        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets_left],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        # Predict probabilities
        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]

        # Display the probabilities
        st.header(f"{batting_team} - {round(win * 100, 2)}%")
        st.header(f"{bowling_team} - {round(loss * 100, 2)}%")
