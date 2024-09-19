import streamlit as st
import os
from utils.story_creator import StoryCreator
from utils.story_creator import StoryCreatorBuilder


from dotenv import load_dotenv
# Load the environment variables
load_dotenv()

print(os.listdir())

def create_story():
    story_creator = StoryCreatorBuilder()\
        .set_page_title(page_title)\
        .set_lang(lang)\
        .set_open_api_key(os.getenv("OPENAI_API_KEY"))\
        .set_open_api_region(os.getenv("OPENAI_API_REGION"))\
        .set_open_api_endpoint(os.getenv("OPENAI_API_ENDPOINT"))\
        .set_open_api_model_deployment_name(os.getenv("OPENAI_API_MODEL_DEPLOYMENT_NAME"))\
        .set_speech_region(os.getenv("SPEECH_REGION"))\
        .set_speech_api_key(os.getenv("SPEECH_API_KEY"))\
        .set_speech_api_endpoint(os.getenv("SPEECH_API_ENDPOINT"))\
        .build()
    
    story_creator.run()

    st.session_state['story_created'] = True
    st.session_state['story'] =  story_creator.get_text()
    st.session_state['story_audio'] =  story_creator.get_audio()
    

if 'story_created' not in st.session_state:
    st.session_state['story_created'] = False

# Sidebar content
st.sidebar.title('Menu')
st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/create.py", label="Create")
st.sidebar.page_link("pages/library.py", label="Library")
st.sidebar.page_link("pages/settings.py", label="Settings")


st.title('Real Tales 4 Kids: Creation Page')
st.write("Select the Wikipedia page you want to create a story from.")
page_title = st.text_input("Page Title")
lang = st.selectbox("Language",["en","it"])


st.button("Create Story", key="create_story",on_click=create_story)


if st.session_state['story_created']:
    st.write("Story created successfully!")
    st.write(st.session_state['story'])
    st.audio(st.session_state['story_audio'])
    #st.audio("output.mp3")
    #st.write("Story created successfully!")