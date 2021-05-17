import streamlit as st
import requests
import json
import pydeck as pdk
import urllib.request
import pandas as pd

response = requests.get("http://api.open-notify.org/astros.json")
astro = json.loads(response.text)
number_space = astro["number"]
name_space = [astro["people"][i]["name"] for i in range(len(astro["people"]))]

# iss 
response = urllib.request.urlopen("http://api.open-notify.org/iss-now.json")
obj = json.loads(response.read())

# list of strings
lst2 = [float(obj['iss_position']['latitude'])]
  
# list of int
lst = [float(obj['iss_position']['longitude'])]
  
df = pd.DataFrame(list(zip(lst, lst2)),
               columns =['lon', 'lat'])

# visualization 

st.title('Web API exercise')
st.text('This exercise uses randomly generated astro data. \nThe purpose of this exercise is it to use requests to get data \nand then create a Streamlit app which will be deployed at the end.')
st.subheader('Some figures')
st.text('Total number of people in space: {}'.format(len(astro["people"])))
st.text('The following people are in space:\n\n{}'.format(' \n'.join(name_space)))

st.subheader('The red dot marks where the ISS is currently located')
st.map(df)