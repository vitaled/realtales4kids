import streamlit as st
import os
from utils.story_creator import StoryCreator
from utils.story_creator import StoryCreatorBuilder





# Sidebar content
st.sidebar.title('Menu')
st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/create.py", label="Create")
st.sidebar.page_link("pages/library.py", label="Library")
st.sidebar.page_link("pages/settings.py", label="Settings")

st.title('Real Tales 4 Kids: Library Page')


for story_path in os.listdir("code/stories"):
    st.write(f"code/stories/{story_path}")
