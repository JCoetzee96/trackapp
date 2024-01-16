import streamlit as st
import streamlit_authenticator as stauth
from dependencies import sign_up, fetch_users

st.set_page_config(page_title='Your personalised tracking app', page_icon='✨', initial_sidebar_state='collapsed')

try:
    users = fetch_users()
    emails = [user['key'] for user in users]
    usernames = [user['username'] for user in users]
    passwords = [user['password'] for user in users]

    credentials = {'usernames': {}}

    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

    authenticator = stauth.Authenticate(credentials, cookie_name='OHVFSWBG', key='ecc992ba23ba5c3e', cookie_expiry_days=0)

    email, authentication_status, username = authenticator.login('Login', 'main')

    info, info1 = st.columns(2)

    if not authentication_status:
        sign_up()

    if username:
        if username in usernames:
            if authentication_status:
                st.subheader('Home page')
                st.markdown("""Created with ♥️ by Janke Coetzee""")
                st.sidebar(f'Welcome {username}')
                authenticator.logout('Log out', 'sidebar')
            elif authentication_status == False:
                st.error('Incorrect username or password')
            elif authentication_status == None:
                st.warning('Sign in')
        else:
            st.warning('Username does not exist')

except:
    st.success('Refresh page')