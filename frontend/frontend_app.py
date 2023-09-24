import streamlit as st
import requests 

# FastAPI server URL
SERVER_URL = "http://backend:8000/recommendations/" # Replace with localhost if running locally

st.title('Movie Recommendation System')

# User Inputs
query = st.text_input('Enter a movie title:')  # Create a search bar
num_rec = st.number_input('Number of Recommendations:', min_value=1, value=10)  # Number of recommendations

# Get Recommendations Button
if st.button('Get Recommendations'):
    if query:
        st.subheader('Recommendations for "{}":'.format(query))
        
        # Prepare payload
        payload = {"movie": query, "num_rec": num_rec}
        
        try:
            # Send POST request to FastAPI server
            response = requests.post(SERVER_URL, json=payload)
            
            if response.status_code == 200:
                recommendations = response.json()  # Parse JSON response
                
                if recommendations:
                    # Display recommended movies
                    st.write('Recommended Movies:')
                    for rec in recommendations.get('recommendations', []):
                        st.write('- ' + rec)
                    
                    # Display metrics
                    metrics = recommendations.get('metrics', {})
                    st.write('Metrics:')
                    st.write(f"Popularity: {metrics.get('popularity', 'N/A')}")
                    st.write(f"Average Vote: {metrics.get('vote_avg', 'N/A')}")
                    st.write(f"Vote Count: {metrics.get('vote_count', 'N/A')}")
                else:
                    st.write('No recommendations available for this movie.')
            
            else:
                st.write('Error occurred:', response.text)  # Display error message from server
            
        except Exception as e:
            st.write('Error occurred:', e)  # In case of an error, display it
    else:
        st.write('Please enter a movie title.')