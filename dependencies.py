import bcrypt
import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
from deta import Deta
from streamlit_extras.let_it_rain import rain
import secrets
import string

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
    st.warning('Invalid email')
    return False

def validate_username(username):
    """Check username validity"""
    pattern = "^[a-zA-Z0-9]*$"
    if re.match(pattern, username) and len(username) >= 4:
        return True
    elif re.match(pattern, username) and len(username) <= 4:
        st.warning('Username too short')
    else:
        st.warning('Invalid username')
    return False

def validate_password(password):
    """Check password validity"""
    if len(password) >= 8:
        if any(char.isdigit() for char in password):
            if any(char.isupper() for char in password):
                if any(char.islower() for char in password):
                    if any(char in "±§!@€#$%^&*()_-+={}[]:;|\\<>,.?/" for char in password):
                        return True
                    else:
                        st.warning('Password must contain a special character')
                else:
                    st.warning('Password must contain at least one lowercase letter')
            else:
                st.warning('Password must contain at least one capital letter')
        else:
            st.warning('Password must contain a number')
    else:
        st.warning('Password too short')
    return False

def sign_up():
    """Sign up new user"""
    with st.form(key='signup', clear_on_submit=True):
        st.subheader('Sign up')
        email = st.text_input('Email', placeholder='Enter your email')
        username = st.text_input('Username', placeholder='Enter your username')
        password1 = st.text_input('Password', placeholder='Enter your password', type='password')
        password2 = st.text_input('Confirm password', placeholder='Confirm your password', type='password')

        if email:
            if validate_email(email):
                if email not in get_user_emails():
                    if username:
                        if validate_username(username):
                            if username not in get_usernames():
                                if password1:
                                    if password2:
                                        if password1 == password2:
                                            if validate_password(password2):
                                                hashed_password = stauth.Hasher([password2]).generate()
                                                insert_user(email, username, hashed_password[0])
                                                st.success('Account has been created')
                                                rain(
                                                    emoji="✨",
                                                    font_size=54,
                                                    falling_speed=5,
                                                    animation_length=5,
                                                )
                                        else:
                                            st.warning('Passwords do not match')
                                    else:
                                        st.warning('Confirm your password')
                                else:
                                    st.warning('Enter a password')
                            else:
                                st.warning('Username already exists')
                    else:
                        st.warning('Enter a username')
                else:
                    st.warning('Email already exists')

        bt1, bt2, bt3, bt4, bt5 = st.columns(5)

        with bt3:
            st.form_submit_button('Sign up')

def forgotten_username():
    """Retrieve username with email"""
    with st.form(key='forgotusername', clear_on_submit=True):
        st.subheader('Forgot username')
        email = st.text_input('Email', placeholder='Enter your email')

        if email:
            if email in get_user_emails():
                username = ' '.join(get_usernames())
            else:
                st.warning('The is no account with this email')

        if st.form_submit_button('Submit'):
            st.success(f'Your username is {username}')

def generate_random_password(length=8):
    password = (secrets.choice(string.ascii_uppercase) +
                secrets.choice(string.ascii_lowercase) +
                secrets.choice(string.digits) +
                secrets.choice("±§!@€#$%^&*()_-+={}[]:;|\\<>,.?/"))
    return ''.join(secrets.choice(password) for _ in range(length))

def forgotten_password():
    """Set a random password if forgotten"""
    with st.form(key='forgotpassword', clear_on_submit=True):
        st.subheader('Forgot password')
        email = st.text_input('Email', placeholder='Enter your email')
        username = st.text_input('Username', placeholder='Enter your username')

        if email or username:
            if email in get_user_emails() or username in get_usernames():
                random_password = generate_random_password()
                hashed_random_password = stauth.Hasher([random_password]).generate()

                if email:
                    username = ''.join(get_usernames())
                    insert_user(email, username, hashed_random_password[0])
                elif username:
                    email = ''.join(get_user_emails())
                    insert_user(email, username, hashed_random_password[0])

            else:
                st.error('Email or username invalid')

        if st.form_submit_button('Submit'):

            st.success(f'Your password has been reset to: {random_password}. \n'
                       f'You can change your password after logging in.')

def reset_password(username, email):
    """Reset password"""
    with st.expander("Reset password"):
        with st.form('Reset password'):
            st.subheader('Reset password')
            current_password = st.text_input('Current password', placeholder='Enter your current password', type='password')
            new_password1 = st.text_input('New password', placeholder='Enter your new password', type='password')
            new_password2 = st.text_input('Confirm new password', placeholder='Confirm your new password', type='password')

            if current_password:
                if bcrypt.checkpw("3kk$33kk".encode('utf-8'), [user['password'] for user in db.fetch().items][0].encode()):
                    if new_password1 == new_password2:
                        if validate_password(new_password2):
                            hashed_password = stauth.Hasher([new_password2]).generate()
                            insert_user(email, username, hashed_password[0])
                            st.success('Password has been reset')
                    else:
                        st.warning("New passwords don't match")
                else:
                    st.warning('Password incorrect')

            st.form_submit_button('Submit')