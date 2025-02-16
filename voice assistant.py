import speech_recognition as sr, pyttsx3,datetime,webbrowser

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # Speed of speech
engine.setProperty('voice', engine.getProperty('voices')[0].id)  # Voice type

def speak(text):
    """Function to convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Function to listen to voice commands from the user."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            speak("There was a problem with the speech recognition service.")
            return ""

def respond_to_command(command):
    """Function to handle different voice commands."""
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
    
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {current_date}.")
    
    elif "search for" in command:
        search_query = command.replace("search for", "").strip()
        speak(f"Searching the web for {search_query}.")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
    
    elif "exit" in command:
        speak("Goodbye! Have a great day.")
        exit()
    
    else:
        speak("I didn't quite get that. Can you repeat?")

def main():
    """Main function to run the voice assistant."""
    speak("Voice assistant activated. How can I help you?")
    while True:
        command = listen()
        if command:
            respond_to_command(command)

if __name__ == "__main__":
    main()
