import streamlit as st
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import requests
import os

load_dotenv()

llama_key = os.environ.get('LLAMA_API_KEY')


longitude = st.number_input('Longitude', value=-122.42)
latitude = st.number_input('Latitude', value=37.77)
# Load data from CSV
df = pd.read_csv('data/diabetes_binary_5050split_health_indicators_BRFSS2015.csv')

# Create a new column for size, where size is larger for people with diabetes
df['size'] = df['Diabetes_binary'].apply(lambda x: 50 if x == 1 else 10)

# Create a new column for color, where color is different for people with and without diabetes
df['color'] = df['Diabetes_binary'].apply(lambda x: [255, 0, 0, 255] if x == 1 else [0, 255, 0, 255])
df['lat'] = np.random.randn(70692)/latitude + 37.77
df['lon'] = np.random.randn(70692)/longitude - 122.42

# Plot the map
st.map(df,
    latitude='latitude',
    longitude='longitude',
    size='size',
    color='color')

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": f"Bearer {llama_key}"}
st.write("Organisation should follow these steps to reduce the risks of Diabetes in their area")
user_query = "Steps to organise diabetes camp in a community center are"
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

        
output = query({"inputs": user_query,})
output = output[0]["generated_text"]
output = output[len(user_query):]
st.write(output)