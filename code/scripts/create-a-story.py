import wikipediaapi
import azure.cognitiveservices.speech as speechsdk
import os
import requests
import base64
from dotenv import load_dotenv
# Load the environment variables
load_dotenv("../../.env")


def extract_wikipedia_text(page_title, lang="en"):
    # Initialize the Wikipedia API
    wiki_wiki = wikipediaapi.Wikipedia('Real Tales 4 Kids', lang)

    # Get the page
    page = wiki_wiki.page(page_title)

    # Check if the page exists
    if not page.exists():
        return f"The page '{page_title}' does not exist."

    # Extract the text
    return page.text


def create_story_from_text(text):
    system_prompt = "You are an AI assistant that helps creating educational stories for kids. I will provide you with an Encyclopedia page and you will generate a summary of the topic using the facts in the page but telling them in engaging and funny way that can works for kids. Remember that while you don't have to made up facts you're allowed to do jokes or to make some funny comparison or example to make your story more suitable and engaging for kids. Introduce yourself with a warm greeting to the kids that are going to listen and then start explaining the topic in a funny and engaging way. Dont'use use emoticon and don't say that you're an AI"
    user_prompt = text
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_API_REGION = os.getenv("OPENAI_API_REGION")
    OPENAI_API_ENDPOINT = os.getenv("OPENAI_API_ENDPOINT")
    OPENAI_API_MODEL_DEPLOYMENT_NAME = os.getenv(
        "OPENAI_API_MODEL_DEPLOYMENT_NAME")


    headers = {
        "Content-Type": "application/json",
        "api-key": OPENAI_API_KEY,
    }

    # Payload for the request
    payload = {
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": system_prompt
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt
                    }
                ]
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
    }

    endpoint = f"{OPENAI_API_ENDPOINT}/openai/deployments/{OPENAI_API_MODEL_DEPLOYMENT_NAME}/chat/completions?api-version=2024-02-15-preview"

    # Send request
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

    # Handle the response as needed (e.g., print or process)
    #print(response.json())
    return response.json()["choices"][0]["message"]["content"]

def create_audio_from_text(story):
    SPEECH_REGION = os.getenv("SPEECH_REGION")
    SPEECH_API_KEY = os.getenv("SPEECH_API_KEY")
    SPEECH_API_ENDPOINT = os.getenv("SPEECH_API_ENDPOINT")
    '''
    For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk 
    '''

    import azure.cognitiveservices.speech as speechsdk

    # Creates an instance of a speech config with specified subscription key and service region.
    speech_key = SPEECH_API_KEY
    service_region = SPEECH_REGION

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_language = "it-IT"
    # Note: the voice setting will not overwrite the voice element in input SSML.
    speech_config.speech_synthesis_voice_name = "en-US-AndrewMultilingualNeural"

    text = story

   # Create an audio output stream to store the synthesized speech.
    audio_output = speechsdk.audio.AudioOutputConfig(filename="output2.wav")

    # Create a speech synthesizer with the speech configuration and audio output stream.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

    # Synthesize the text to speech and store it in a file.
    result = speech_synthesizer.speak_text_async(text).get()

    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}] and saved to 'output.wav'".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))




# Example usage
if __name__ == "__main__":
    page_title = "Luna"
    lang = "it"
    text = extract_wikipedia_text(page_title, lang)
    story = create_story_from_text(text)
    create_audio_from_text(story)
    print(story)
    print(len(text))
