import pyttsx3 
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
import os
import smtplib
import requests
import yfinance as yfp
from pytube import Search

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.setProperty('voice', voices[1].id)
    engine.say(audio)   
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am obligued Sir. Please tell me how may I help you")       

def takeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-us')
        print(f"User said: {query}\n")

    except Exception as e: 
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('sahilakash2264@gmail.com', 'Samsung@m01')
    server.sendmail('sahilakash22264@gmail.com', to, content)
    server.close()
    
def getStockPrice(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    stock_info = stock.info
    current_price = stock_info.get('currentPrice', 'N/A')
    return f"The current price of {stock_symbol} is {current_price}"

def showYouTubeResults(song_name):
    search = Search(song_name)
    results = search.results
    if results:
        video_url = results[0].watch_url
        webbrowser.open(video_url)
        speak(f"Showing results for {song_name} on YouTube")
    else:
        speak("Song not found on YouTube")
    
def getWeather(city):
    api_key = "2a1b67d9c312d584b7b0bb2ab988d956"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data.get("main", {})
        weather = data.get("weather", [{}])[0]
        temperature = main.get("temp", "N/A")
        pressure = main.get("pressure", "N/A")
        humidity = main.get("humidity", "N/A")
        description = weather.get("description", "N/A")
        weather_report = f"Temperature: {temperature}K\nPressure: {pressure}hPa\nHumidity: {humidity}%\nDescription: {description}"
        return weather_report
    else:
        return "City not found."
    

if __name__ == "__main__":
    wishMe()
    while True:
    
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "").strip()
            print(f"Search term: {query}")  # Debugging statement
            if query:
                try:
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                except wikipedia.exceptions.DisambiguationError as e:
                    speak("There are multiple results for your query, please be more specific.")
                    print(e.options)
                except wikipedia.exceptions.PageError:
                    speak("The page does not exist.")
                except wikipedia.exceptions.WikipediaException as e:
                    speak("An error occurred while searching Wikipedia.")
                    print(e)
            else:
                speak("Please provide a search term.")
                      
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
            
        elif 'search google for' in query:
            search_term = query.replace("search google for", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={search_term}")
            speak(f"Searching Google for {search_term}")   


        elif 'play youtube video' in query:
            speak("Which YouTube video?")
            song_name = takeCommand().lower()
            showYouTubeResults(song_name)


        elif 'what is the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")
            
        elif 'what is the weather' in query:
            speak('Which city?')
            city = takeCommand().lower()
            weather_report = getWeather(city)
            speak(weather_report)
            print(weather_report)

        elif 'open code' in query:
            codePath = "C:\\Users\\Haris\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
            
        elif 'send email' in query:
            try:
                speak("To whom should I send the email?")
                to = takeCommand().lower()
                speak("What should I say?")
                content = takeCommand()
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry SIR. I am not able to send this email") 

        elif 'stock price' in query:
            speak("Which stock?")
            stock_symbol = takeCommand().upper()
            stock_price = getStockPrice(stock_symbol)
            speak(stock_price)
            print(stock_price)  
            
        elif "end" or "break" or "stop" in query:
            print("User ended the program")
            # break

        else:
            print("No query matched")