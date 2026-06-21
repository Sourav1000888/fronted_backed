import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()

st.title('testing')

username = st.text_input('enter username : ')
password = st.text_input('enter password : ')


endpoint1 = os.environ.get("post_url")
endpoint2 = os.environ.get("get_url")

if st.button('save data'):
    data = {'username' : username, 'password' : password}
    res = requests.post(url=f'{endpoint1}', json=data)
    st.write(res.text)
    

user = st.text_input('enrte name : ')
if st.button('show data'):
    param = {'username' : user}
    res = requests.get(url=f'{endpoint2}', params=param)
    st.text('users data')
    st.dataframe(res.json())



