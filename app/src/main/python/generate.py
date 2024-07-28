from openai import AzureOpenAI
import azure.cognitiveservices.speech as speechsdk
import tempfile
import os
import json

#config as real time speech to text
client = AzureOpenAI(
    api_key="id",
    api_version="date",
    azure_endpoint="endpoint model"
)
# real time speech to text
def speech_recognition_callback(evt):
    if isinstance(evt, speechsdk.audio.AudioDataReadyEvent):
        print("Received audio data")
    elif isinstance(evt, speechsdk.speech.SpeechRecognitionResult):
        if evt.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"Recognized: {evt.text}")
        elif evt.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized")
        elif evt.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = evt.cancellation_details
            print(f"Speech Recognition canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")

def start_recognition():
    speech_config = create_speech_config()
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    speech_recognizer.recognized.connect(speech_recognition_callback)
    speech_recognizer.canceled.connect(speech_recognition_callback)
    speech_recognizer.session_started.connect(lambda evt: print("Session started"))
    speech_recognizer.session_stopped.connect(lambda evt: print("Session stopped"))

    print("Starting speech recognition...")
    speech_recognizer.start_continuous_recognition()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping...")
        speech_recognizer.stop_continuous_recognition()

if __name__ == "__main__":
    start_recognition()

#config gpt 4 for sentiment analysis
def CustomChatGPT(user_input):
    client = AzureOpenAI(
        api_key="id",
        api_version="date",
        azure_endpoint="endpoint model"
    )
    #Prompt summarize transcription
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """
                You are an AI assistant that evaluate conversation between customer and operator.
    
                please evaluate these point by customer :
                1. Driver sentiment
                2. Passenger sentiment
                3. Call disconnected before conversation ends
                4. Said emergency keyword
    
                please create a flag based on each point above and summarize it into a table
                """,
            },
            {
                "role": "assistant",
                "content": """please format as json with keys  
                Driver sentiment, Passenger sentiment, Call disconnected before conversation ends, Said emergency keyword
                """
            },    
            {
                "role": "user",
                "content": f"conversation between driver and passenger: \n {user_input}"
            }
        ],
        temperature=0
    )
    message = completion.choices[0].message.content
    return message
