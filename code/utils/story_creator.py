import os
import uuid
import wikipediaapi
import requests

class StoryCreator:
    def __init__(self, page_title, lang, open_api_key, open_api_region, open_api_endpoint, open_api_model_deployment_name, speech_region, speech_api_key, speech_api_endpoint):
        self.text = None
        self.audio = None
        self.page_title = page_title
        self.lang = lang
        self.open_api_key = open_api_key
        self.open_api_region = open_api_region
        self.open_api_endpoint = open_api_endpoint
        self.open_api_model_deployment_name = open_api_model_deployment_name
        self.speech_region = speech_region
        self.speech_api_key = speech_api_key
        self.speech_api_endpoint = speech_api_endpoint

    
    def run(self):
        # Initialize the Wikipedia API
        story_id = uuid.uuid4()
        os.mkdir(f"code/stories/{story_id}")

        wiki_wiki = wikipediaapi.Wikipedia('Real Tales 4 Kids', self.lang)

        # Get the page
        page = wiki_wiki.page(self.page_title)

        # Check if the page exists
        if not page.exists():
            return f"The page '{self.page_title}' does not exist."

        text = page.text
        print(text)
        system_prompt = "You are an AI assistant that helps creating educational stories for kids. I will provide you with an Encyclopedia page and you will generate a summary of the topic using the facts in the page but telling them in engaging and funny way that can works for kids. Remember that while you don't have to made up facts you're allowed to do jokes or to make some funny comparison or example to make your story more suitable and engaging for kids. Introduce yourself with a warm greeting to the kids that are going to listen and then start explaining the topic in a funny and engaging way. Dont'use use emoticon and don't say that you're an AI"
        user_prompt = text
        
        headers = {
            "Content-Type": "application/json",
            "api-key": self.open_api_key,
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

        endpoint = f"{self.open_api_endpoint}/openai/deployments/{self.open_api_model_deployment_name}/chat/completions?api-version=2024-02-15-preview"
        print(endpoint)
        # Send request
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
            response.raise_for_status()
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")

        # Handle the response as needed (e.g., print or process)
        #print(response.json())
        text_story = response.json()["choices"][0]["message"]["content"]

        print(text_story)
        self.text = text_story
        # SPEECH_REGION = os.getenv("SPEECH_REGION")
        # SPEECH_API_KEY = os.getenv("SPEECH_API_KEY")
        # SPEECH_API_ENDPOINT = os.getenv("SPEECH_API_ENDPOINT")
        # '''
        # For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk 
        # '''

        import azure.cognitiveservices.speech as speechsdk

        # Creates an instance of a speech config with specified subscription key and service region.
        
        speech_config = speechsdk.SpeechConfig(subscription=self.speech_api_key, region=self.speech_region)
        
        locale ="en-US"

        if self.lang == "it":
            locale = "it-IT"
        if self.lang == "es":
            locale = "es-ES"
        if self.lang == "fr":
            locale = "fr-FR"
        if self.lang == "de":
            locale = "de-DE"
        else:
            locale = "en-US"
        
        
        

        speech_config.speech_synthesis_language = locale
        # Note: the voice setting will not overwrite the voice element in input SSML.
        speech_config.speech_synthesis_voice_name = "en-US-AndrewMultilingualNeural"

        

        # Create an audio output stream to store the synthesized speech.
        audio_output = speechsdk.audio.AudioOutputConfig(filename=f"code/stories/{story_id}/audio.wav")

        self.audio = f"code/stories/{story_id}/audio.wav"


        # Create a speech synthesizer with the speech configuration and audio output stream.
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

        # Synthesize the text to speech and store it in a file.
        result = speech_synthesizer.speak_text_async(text_story).get()

        import codecs
        import json
        with codecs.open(f"code/stories/{story_id}/story.txt", "w") as text_output_file:
            text_output_file.write(text_story)

        metadata = {
            "page_title": self.page_title,
            "lang": self.lang,
            "audio_path": f"code/stories/{story_id}/audio.wav",
            "story_path": f"code/stories/{story_id}/story.txt"
        }
        
        with codecs.open(f"code/stories/{story_id}/metadata.json", "w") as metadata_output_file:
            metadata_output_file.write(json.dumps(metadata))

        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}] and saved to 'output.wav'".format(text))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

    
    def get_audio(self):
        return self.audio
    
    def get_text(self):
        return self.text
    
    # def save_audio(self, path):
    #     pass

    # def save_text(self, path):
    #     pass


class StoryCreatorBuilder:
    def __init__(self):
        self.page_title = None
        self.lang = None
        self.open_api_key = None
        self.open_api_region = None
        self.open_api_endpoint = None
        self.open_api_model_deployment_name = None
        self.speech_region = None
        self.speech_api_key = None
        self.speech_api_endpoint = None
    

    def set_page_title(self, page_title):
        self.page_title = page_title
        return self
    

    def set_lang(self, lang):
        self.lang = lang
        return self
    

    def set_open_api_key(self, open_api_key):
        self.open_api_key = open_api_key
        return self
    

    def set_open_api_region(self, open_api_region):
        self.open_api_region = open_api_region
        return self
    

    def set_open_api_endpoint(self, open_api_endpoint):
        self.open_api_endpoint = open_api_endpoint
        return self
    

    def set_open_api_model_deployment_name(self, open_api_model_deployment_name):
        self.open_api_model_deployment_name = open_api_model_deployment_name
        return self
    

    def set_speech_region(self, speech_region):
        self.speech_region = speech_region
        return self
    

    def set_speech_api_key(self, speech_api_key):
        self.speech_api_key = speech_api_key
        return self

    def set_speech_api_endpoint(self, speech_api_endpoint):
        self.speech_api_endpoint = speech_api_endpoint
        return self

    def build(self):
        story_creator = StoryCreator(self.page_title, self.lang, self.open_api_key, self.open_api_region, self.open_api_endpoint, self.open_api_model_deployment_name, self.speech_region, self.speech_api_key, self.speech_api_endpoint)
        return story_creator
