import streamlit as st
from dotenv import load_dotenv
# Load the environment variables
load_dotenv()

# st.title('Real Tales 4 Kids')
# st.write("""
#     Welcome to Real Tales 4 Kids! This is a platform where kids can read and listen to stories.
#          """)
# Sidebar content
st.sidebar.title('Menu')
st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/create.py", label="Create")
st.sidebar.page_link("pages/library.py", label="Library")
st.sidebar.page_link("pages/settings.py", label="Settings")


st.image("code/images/realtales.jpeg", use_column_width=True)