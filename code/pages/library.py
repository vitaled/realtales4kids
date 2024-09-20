import streamlit as st
import os
import json
import codecs
from utils.story_creator import StoryCreator
from utils.story_creator import StoryCreatorBuilder





# Sidebar content
st.sidebar.title('Menu')
st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/create.py", label="Create")
st.sidebar.page_link("pages/library.py", label="Library")
st.sidebar.page_link("pages/settings.py", label="Settings")

st.title('Library')


story_paths =  os.listdir("code/stories")

for story_path in story_paths:
   with codecs.open(f"code/stories/{story_path}/metadata.json", 'r', encoding='utf-8', errors='ignore') as metadata_file:
      metadata = json.loads(metadata_file.read())
     
      st.write(metadata['page_title']+ " - " + metadata['lang'].upper())
      with codecs.open(metadata['story_path'], 'r', encoding='utf-8', errors='ignore') as story_file:
         story = story_file.read()
         with st.expander("Read Story"):
            st.write(story)
      st.audio(metadata['audio_path'])
