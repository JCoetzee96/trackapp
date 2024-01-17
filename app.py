import streamlit as st
import streamlit_authenticator as stauth
from dependencies import sign_up, fetch_users

st.set_page_config(page_title='Your personalised tracking app', page_icon='👾', initial_sidebar_state='collapsed',)

try:
    users = fetch_users()
    emails = []
    usernames = []
    passwords = []

    for user in users:
        emails.append(user['key'])
        usernames.append(user['username'])
        passwords.append(user['password'])

    credentials = {'usernames': {}}
    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

    Authenticator = stauth.Authenticate(credentials, cookie_name='OHVFSWBG', key='ecc992ba23ba5c3e', cookie_expiry_days=0)
    st.title('Your personalised tracking app')
    st.divider()
    email, authentication_status, username = Authenticator.login('Login', 'main')

    info, info1 = st.columns(2)

    if not authentication_status:
        sign_up()
        ## add function for forgotten username
        ## add function for forgotten password

    if username:
        if username in usernames:
            if authentication_status:
                st.sidebar.subheader(f'Welcome {username}')
                ## add option to reset password
                ## add option to update personal info
                Authenticator.logout('Log out', 'sidebar')

                st.subheader('Home page')
                st.markdown("""Created with ♥️ by Janke Coetzee""")

            elif authentication_status == False:
                with info:
                    st.error('Incorrect username or password')
            elif authentication_status == None:
                with info:
                    st.warning('Sign in')
        else:
            with info:
                st.warning('Username does not exist')

except:
    st.success('Refresh page')