import streamlit as st
import requests
from google import genai

client = genai.Client(api_key="AIzaSyCDN3mnTyhAA6X0WN5MGx5nn3fjoCMkkDw")

def gemini(query):
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=query,
    )
    
    # # Inspect the API response
    # print("API Response:", response.text)
    # print("API Response JSON:", response.json())
    
    try:
        return response.text
    except KeyError as e:
        print(f"Error: {e}")

# Create a Streamlit app
st.title("Gemini Chatbot")

# User input form
query = st.text_input("What would you like to ask the chatbot?", value="")

if query:
    # Call Gemini API with user's query
    response = gemini(query)
    
    # Display chatbot response
    st.write(response)