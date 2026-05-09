import streamlit as st
import requests
import json

st.set_page_config(page_title='AI App Compiler', layout='wide')
st.title('AI App Compiler')
st.caption('Natural language → structured config → validation → executable preview')

prompt = st.text_area('Enter app requirement', value='Build a CRM with login, contacts, dashboard, role-based access, and premium plan with payments. Admins can see analytics.', height=120)
api_url = st.text_input('Backend URL', 'http://127.0.0.1:8000/compile')

if st.button('Compile App'):
    with st.spinner('Compiling...'):
        res = requests.post(api_url, json={'prompt': prompt}, timeout=30)
    data = res.json()
    st.subheader('Metrics')
    st.json(data['metrics'])
    st.subheader('Validation Issues')
    st.json(data['validation_issues'])
    left, right = st.columns(2)
    with left:
        st.subheader('Intent')
        st.json(data['intent'])
        st.subheader('Architecture')
        st.json(data['architecture'])
    with right:
        st.subheader('Final App Config')
        st.json(data['config'])
    st.subheader('Executable Preview')
    st.components.v1.html(data['executable_preview_html'], height=450, scrolling=True)
