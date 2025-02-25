import openai
import pyttsx3
import speech_recognition as sr
import streamlit as st
from api import apikey

# Set your OpenAI API key here
api_key = apikey
model_id = "gpt-3.5-turbo"
openai.api_key = api_key

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

interaction_counter = 0


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        return user_input
    except sr.UnknownValueError:
        st.write("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        st.write(f"Could not request results from Google Speech Recognition service; {e}")
    return None


def chat_with_gpt(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    api_usage = response['usage']
    st.write('Total tokens consumed: {0}'.format(api_usage['total_tokens']))
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


def suggest_outfit():
    # Example logic for suggesting outfits based on user preferences or trends
    return "How about trying out this trendy outfit? [Image: TrendyOutfit.jpg]"


def virtual_try_on():
    # Example logic for virtual try-on, such as displaying virtual clothes or using AR technology
    return "Initiating virtual fitting room experience... You can now virtually try on different outfits."


def process_user_input(user_input):
    # Additional logic for immersive experiences and online shopping guidance
    if "product" in user_input.lower() or "buy" in user_input.lower():
        return "Sure, let's find the perfect product for you. What are you looking for?"
    elif "fashion" in user_input.lower() or "trends" in user_input.lower():
        return "Fashion is ever-evolving! Would you like to explore the latest trends or get styling advice?"
    elif "try out" in user_input.lower() or "virtual fitting room" in user_input.lower():
        return virtual_try_on()
    elif "suggest outfit" in user_input.lower() or "what to wear" in user_input.lower():
        return suggest_outfit()
    else:
        return "I'm here to assist you with your online shopping experience. Feel free to ask anything."


def main():
    st.title("Online Shopping Assistant")
    # User input text box with a unique key
    user_input_key = "assistant_input"
    user_input = st.text_input("Say 'Assistant' to start...", key=user_input_key)

    if user_input and user_input.lower() == "assistant":
        # Additional logic for processing user input
        st.write("Initiating the assistant...")
    st.write(welcome_message())

    while True:
        user_input = st.text_input("Say 'Assistant' to start...")

        if user_input:
            st.write(f"You said: {user_input}")
            append_to_log(f"You: {user_input}\n")

            assistant_response = process_user_input(user_input)
            st.write(f"Assistant: {assistant_response}")
            append_to_log(f"Assistant: {assistant_response}\n")
            speak_text(assistant_response)

            if "try out" in user_input.lower() or "virtual fitting room" in user_input.lower():
                st.write("Initiating virtual fitting room experience...")
                outfit_suggestion = "How about trying out this stylish outfit? [Image: StylishOutfit.jpg]"
                st.write(outfit_suggestion)
                append_to_log(f"Assistant: {outfit_suggestion}\n")
                speak_text(outfit_suggestion)



if __name__ == "__main__":
    main()
