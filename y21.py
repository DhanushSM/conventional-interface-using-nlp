import openai
import pyttsx3
import speech_recognition as sr
import random
from api import api_key
# Set your OpenAI API key here
apikey = api_key
model_id = "gpt-3.5-turbo"
openai.api_key = apikey

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

interaction_counter = 0


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        return user_input
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    return None


def chat_with_gpt(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    api_usage = response['usage']
    print('Total tokens consumed: {0}'.format(api_usage['total_tokens']))
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def welcome_message():
    return "Hello! Welcome to our online shopping assistant. How may I help you today? You can ask about products, fashion trends, or even get styling advice."

def append_to_log(text):
    with open("chat_log.txt", "a") as f:
        f.write(text + "\n")

def process_user_input(user_input):
    # Add logic here to interpret and process user input related to online shopping
    # Example: Guide the user through product search, provide fashion advice, etc.
    if "product" in user_input.lower() or "buy" in user_input.lower():
        return "Sure, let's find the perfect product for you. What are you looking for?"
    elif "fashion" in user_input.lower() or "trends" in user_input.lower():
        return "Fashion is ever-evolving! Would you like to explore the latest trends or get styling advice?"
    else:
        return "I'm here to assist you with your online shopping experience. Feel free to ask anything."


def listen_for_keyword():
    global conversation, interaction_counter

    # Inside the listen_for_keyword function, after getting user input
    user_input = recognize_speech()

    if user_input:
        print(f"You said: {user_input}")
        append_to_log(f"You: {user_input}\n")

        assistant_response = process_user_input(user_input)
        print(f"Assistant: {assistant_response}")
        append_to_log(f"Assistant: {assistant_response}\n")
        speak_text(assistant_response)

        # Additional logic for immersive experiences, e.g., trying out clothes virtually
        if "try out" in user_input.lower() or "virtual fitting room" in user_input.lower():
            print("Initiating virtual fitting room experience...")

            # Example: Suggesting an outfit for virtual try-on
            outfit_suggestion = "How about trying out this stylish outfit? [Image: StylishOutfit.jpg]"

            print(outfit_suggestion)
            append_to_log(f"Assistant: {outfit_suggestion}\n")
            speak_text(outfit_suggestion)


# Call the function to listen for the keyword
while True:
    print("Say 'Assistant' to start...")
    listen_for_keyword()
