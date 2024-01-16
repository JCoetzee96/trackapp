import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
from deta import Deta

deta_key = "a0hkj1bnvev_7P3cA3n5tmGqFMu4zrqEHKrah9su9hJQ"
deta = Deta(deta_key)
db = deta.Base('Authentication')

def insert_user(email, username, password):
    """Insert users to DB"""
    date_joined = str(datetime.datetime.now())
    return db.put({'key':email, 'username':username, 'password': password, 'date_joined':date_joined})

def fetch_users():
    """Fetch users"""
    return db.fetch().items

def get_user_emails():
    """Fetch user emails"""
    users = db.fetch()
    return [user['key'] for user in users.items]

print(get_user_emails())

def sign_uo():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader('Sign up')
        email = st.text_input('Email', placeholder='Enter your email')
        username = st.text_input('Username', placeholder='Enter your username')
        password1 = st.text_input('Password', placeholder='Enter your password', type='password')
        password2 = st.text_input('Confirm password', placeholder='Confirm your password', type='password')