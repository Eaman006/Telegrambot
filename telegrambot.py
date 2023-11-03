import os
import telebot
import requests
import datetime
import pytz
import time
import sympy
import random
import threading
from PIL import Image, ImageDraw, ImageFont
from telebot import types
from telebot import util
from telebot import custom_filters
from telebot.types import Message
import re

Token = ""#enter your bot tocken here 
bot =telebot.TeleBot(Token)



@bot.message_handler(["start" , "Start" , "START"])
def send_welcome(message):
    bot.reply_to(message, "Hello I am Anjan, A virtual assistant designed by Quantum Army. If you want to know about all my commands or about me click here /help")

reminders = {}

class Reminder:
    def __init__(self, text):
        self.text = text
        self.date = None
        self.time = None

    def set_datetime(self, date, time):
        self.date = date
        self.time = time

# Handler for /remind command
@bot.message_handler(commands=['remind'])
def handle_remind_command(message: Message):
    chat_id = message.chat.id
    msg = bot.reply_to(message, "What do you want to be reminded about?")
    bot.register_next_step_handler(msg, ask_date, chat_id)

# Ask for date
def ask_date(message: Message, chat_id):
    text = message.text
    reminder = Reminder(text)
    reminders[chat_id] = reminder
    msg = bot.reply_to(message, "What date do you want to be reminded? (Format: YYYY-MM-DD)")
    bot.register_next_step_handler(msg, ask_time, chat_id)

# Ask for time
def ask_time(message: Message, chat_id):
    text = message.text
    reminder = reminders[chat_id]
    try:
        date = datetime.datetime.strptime(text, '%Y-%m-%d').date()
        reminder.set_datetime(date, None)
        msg = bot.reply_to(message, "What time do you want to be reminded? (Format: HH:MM)")
        bot.register_next_step_handler(msg, set_reminder, chat_id)
    except ValueError:
        bot.reply_to(message, "Invalid date format. Please use YYYY-MM-DD")
        bot.register_next_step_handler(message, ask_date, chat_id)

# Set reminder
def set_reminder(message: Message, chat_id):
    text = message.text
    reminder = reminders[chat_id]
    try:
        time = datetime.datetime.strptime(text, '%H:%M').time()
        reminder.set_datetime(reminder.date, time)
        remind_datetime = datetime.datetime.combine(reminder.date, reminder.time)
        now = datetime.datetime.now()
        if remind_datetime > now:
            bot.reply_to(message, f"Reminder set for {remind_datetime}")
            # schedule reminder
            bot.send_message(chat_id, reminder.text, reply_markup=None, reply_to_message_id=None, disable_notification=False, schedule_date=remind_datetime.timestamp())
        else:
            bot.reply_to(message, "The reminder time is in the past.")
    except ValueError:
        bot.reply_to(message, "Invalid time format. Please use HH:MM")
        bot.register_next_step_handler(message, ask_time, chat_id)



@bot.message_handler(commands=['calculate'])
def calculate_command_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Please enter a mathematical expression:")
    bot.register_next_step_handler(message, calculate_handler)
def calculate(expression):
    try:
        result = sympy.sympify(expression).evalf()
        return f"The result is {result}"
    except:
        return "Sorry, I could not calculate that expression."
def calculate(expression):
    try:
        result = sympy.sympify(expression).evalf()
        return f"The result is {result}"
    except:
        return "Sorry, I could not calculate that expression."

def calculate_handler(message):
    chat_id = message.chat.id
    expression = message.text
    result = calculate(expression)
    bot.send_message(chat_id, result)





# Define the function that creates the invite link
def create_invite_link(chat_id):
    link = bot.create_chat_invite_link(chat_id)
    return link.invite_link

# Define the command handler that generates and sends the invite link
@bot.message_handler(commands=['invite'])
def send_invite_link(message):
    chat_id = message.chat.id
    invite_link = create_invite_link(chat_id)
    bot.send_message(chat_id, f"Here's the invite link for this group: {invite_link}")

@bot.message_handler(["Weather","weather","WEATHER"])
def ask_pincode(message):
    bot.reply_to(message, "Please enter the pincode for the location you want the weather for:")
    bot.register_next_step_handler(message, get_weather)


def get_weather(message):
    try:
        pincode = message.text
        weather_data = get_weather_data(pincode)
        # Extract the weather information from the API response
        city = weather_data['name']
        description = weather_data['weather'][0]['description']
        temperature_kelvin = weather_data['main']['temp']
        temperature_celsius = temperature_kelvin - 273.15
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        response = f"The weather in {city} ({pincode}) is {description}, with a temperature of {temperature_celsius:.1f} °C, a humidity of {humidity}%, and a wind speed of {wind_speed} m/s."
        bot.send_message(message.chat.id, response)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Sorry, I couldn't get the weather information for that location.")


def get_weather_data(pincode):
    url = f"http://api.openweathermap.org/data/2.5/weather?zip={pincode},in&APPID=a17d5a2911e98cfb0f02e65f3f1fd79a"
    response = requests.get(url)
    weather_data = response.json()
    return weather_data



@bot.message_handler(["website" , "Website" , "WEBSITE"])
def send_welcome(message):
    bot.reply_to(message, "our official website is https://shigaraki2005.github.io/army/")
@bot.message_handler(text=["Thank you sir ","THANK YOU SIR","thanks sir","thnx sir","Thank you sir","Thank You Sir","thank you sir", "Thank you anjan ","THANK YOU Anjan","thanks anjan","thnx anjan","Thank you Anjan","Thank You Anjan","thank you Anjan","thank you anjan", "Thank you anjan"])
def text_filter(message):
    bot.send_message(message.chat.id, "Your most welcome!! {name}!".format(name=message.from_user.first_name))
@bot.message_handler(text=["Love you anjan","LOVE YOU ANJAN","Love you sir","Love You sir","Love you Anjan", "I love You Sir" , "I love you sir","love you anjan"])
def text_filter(message):
    bot.send_message(message.chat.id, "Love you too {name}!".format(name=message.from_user.first_name))
@bot.message_handler(text=["OK sir", "Ok sir", "ok sir"])
def text_filter(message):
    bot.send_message(message.chat.id, "I am here to help!!👍 {name}".format(name=message.from_user.first_name) )
@bot.message_handler(['doubt'])
def start(message):
    bot.reply_to(message, "you can ask me but the answer you have to tell")
@bot.message_handler(["help","Help","HELP"])
def help(message):
    bot.reply_to(message,"""😒Hey there, how may I help you?
    Here are the list of commands I can!!!
    /start -> Greeting🙏
    /help -> to find the list of my command🤗
    /developers_details -> to find the developers details👨‍💻
    /sing_a_song -> to listen to my anthem🎧🎤
    /game -> to play a game⚽⚾🥎
    /close -> to close the game
    /invite -> to create group invite link
    /calculate -> for calculation
    /timer -> for setting the timer
    /date -> For knowing the date
    /time -> for knowing the time
    /website -> For directing to our official website
    /weather -> For checking weather""")

@bot.message_handler(['developers_details'])
def start(message):
    bot.reply_to(message, """developers: 1) Nilimesh Roy (Project head)
     2) Anurag Das (R&D)
     3) Eaman Adeep(Software Developer)""")

@bot.message_handler(["sing_a_song" , "Sing"])
def start(message):
    bot.reply_to(message, "e ji o ji lo ji suno ji main huin man mo ji karta huin main jo idhar wo tum bhi karoin ji....1 2 ka 4.... 4 2 ka 1 my name is Anjan My name is Anjan ")
@bot.message_handler(content_types=["photo", "sticker", "document", "hyperlink", "file", "video"])
def send_content_message(msg):
    bot.reply_to(msg, "Alert! that's not a Text message, It may be harmful open it after scanning👍")
@bot.message_handler(commands=["Yes_Sure!!"])
def send_multi_message(msg):
    bot.send_dice(chat_id=msg.chat.id)

@bot.message_handler(commands=["close"])
def send_game_message(msg):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(chat_id=msg.chat.id, text="Better try next Time!!!.....nijer bhaggo ta mathematician Suman ke dekhiye ay🤣😂!!!",
    reply_markup=markup)

@bot.message_handler(commands=["game","Game", "GAME"])
def send_game_message(msg):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton("/Yes_Sure!!")
    btn2 = types.KeyboardButton("/close")
    markup.add(btn1, btn2)
    bot.send_message(chat_id=msg.chat.id, text="Wanna test your luck???",
    reply_markup=markup)

# Check if message starts with @admin tag
@bot.message_handler(text_startswith="@nr1900")
def start_filter(message):
    bot.send_message(message.chat.id, "Looks like you are calling Captain, wait...")
@bot.message_handler(text_startswith="@anurag_nouzen")
def start_filter(message):
    bot.send_message(message.chat.id, "Looks like you are calling our Research Head wait...")
@bot.message_handler(text_startswith="@Eamanhere")
def start_filter(message):
    bot.send_message(message.chat.id, "Looks like you are calling our Tech Support wait...")
# Check if text is hi or hello
@bot.message_handler(text=["hi sir","hello sir","HI sir","Hi sir","Hello sir","HELLO sir", "hi Sir" , "hi" , "HI" , "Hi"])
def text_filter(message):
    bot.send_message(message.chat.id, "Hi, {name}!".format(name=message.from_user.first_name))

@bot.message_handler(text=["Who made you Anjan?","Who made you sir?","who made you anjan", "who made you anjan?","who made you sir","Who made you anjan","who made you anjan", "who are you anjan?", "who are you anjan"])
def text_filter(message):
    bot.send_message(message.chat.id, "I am a bot inspired from a great Teacher and I have been designed by quantum army. If you want to check my developers details please click here /developers_details")


# Do not forget to register filters
bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.TextStartsFilter())

#chat_member_handler. When status changes, telegram gives update. check status from old_chat_member and new_chat_member.
@bot.chat_member_handler()
def chat_m(message: types.ChatMemberUpdated):
    old = message.old_chat_member
    new = message.new_chat_member
    if new.status == "member":
        bot.send_message(message.chat.id,"Hello {name}!. Welcome to our group CRAZY CRATERS. For knowing all my commands click here /help".format(name=new.user.first_name)) # Welcome message
@bot.message_handler(commands=['date', 'time'])
def send_date_time(message):
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(tz)
    if message.text == '/date':
        date_str = now.strftime("%d-%m-%Y")
        bot.reply_to(message, f"Today's date is {date_str}")
    else:
        time_str = now.strftime("%H:%M:%S")
        bot.reply_to(message, f"The current time is {time_str}")




# Handler for the /timer command
@bot.message_handler(commands=['timer'])
def timer_command_handler(message):
    chat_id = message.chat.id
    try:
        timer_duration = int(message.text.split()[1])
        bot.send_message(chat_id, f"Timer set for {timer_duration} seconds. You will receive a notification when the time is up.")
        time.sleep(timer_duration)
        bot.send_message(chat_id, "Time's up!")
    except (IndexError, ValueError):
        bot.send_message(chat_id, "Please specify a timer duration in seconds after the command.")

# define a list of abusive words
abusive_words = ["harami","bhosdike", "bsdk", "baal", "bokachoda","bokichudi", "gandu", "chud", "chuttar", "randa", "lund", "randi", "fuck", "wtf" , "shit" , "choda" , "chodar" "khanki" , "khankir" , "magi","magir","chudi" , "chudir", "marachhe", "gand" , "idiot", "ruskel", "sala" , "suar" , "bustard", "bastard", "gudh" , "guder", "bara"]

# create a function to check if a message contains an abusive word
def has_abusive_word(message):
    text = message.text.lower()
    for word in abusive_words:
        if word in text:
            return True
    return False

# create a function to handle messages containing abusive words
def handle_abusive_word(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    warning_message = "Your message contains abusive language, please maintain your decorum. Mere flat baniye debo jano!!!"
    bot.send_message(chat_id, warning_message, reply_to_message_id=message.message_id)

# handle incoming messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if has_abusive_word(message):
        handle_abusive_word(message)







bot.polling()
