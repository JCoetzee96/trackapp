import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
from deta import Deta
from streamlit_extras.let_it_rain import rain

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
    return [user['key'] for user in db.fetch().items]

def get_usernames():
    """"Fetch usernames"""
    return [user['username'] for user in db.fetch().items]

def validate_email(email):
    """Check email validity"""
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pattern, email):
        return True
    return False

def validate_username(username):
    """Check email validity"""
    pattern = "^[a-zA-Z0-9]*$"
    if re.match(pattern, username):
        return True
    return False

def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader('Sign up')
        email = st.text_input('Email', placeholder='Enter your email')
        username = st.text_input('Username', placeholder='Enter your username')
        password1 = st.text_input('Password', placeholder='Enter your password', type='password')
        password2 = st.text_input('Confirm password', placeholder='Confirm your password', type='password')

        if email:
            if validate_email(email):
                if email not in get_user_emails():
                    if validate_username(username):
                        if username not in get_usernames():
                            if len(username) >= 2:
                                if len(password1) >= 6:
                                    if password1 == password2:
                                        hashed_password = stauth.Hasher([password2]).generate()
                                        insert_user(email, username, hashed_password[0])
                                        st.success('Account has been created')
                                        rain(
                                            emoji="✨",
                                            font_size=54,
                                            falling_speed=5,
                                            animation_length="infinite",
                                        )
                                    else:
                                        st.warning('Passwords do not match')
                                else:
                                    st.warning('Password too short')
                            else:
                                st.warning('Username too short')
                        else:
                            st.warning('Username already exists')
                    else:
                        st.warning('Invalid username')
                else:
                    st.warning('Email already exists')
            else:
                st.warning('Invalid email')

        bt1, bt2, bt3, bt4, bt5 = st.columns(5)

        with bt3:
            st.form_submit_button('Sign up')