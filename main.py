#BOT CODE, CHANGE TOKEN TO YOUR BOT TOKEN(line: 10) WHAT YOU GOT FROM @BotFather , AND PASTE YOUR TELEGRAM ID IN admins(line: 13) LIST
#Send '/help' command to bot for see all commands

import telebot
from telebot import types
import sqlite3
import json
import os

API_TOKEN = 'PASTE HERE YOUR API KEY'
bot = telebot.TeleBot(API_TOKEN)

admins = [PASTE HERE YOUR TELEGRAM ID]

news_file = 'news.json'

def check_and_add_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user = ?', (user_id,))
    user = cursor.fetchone()
    if user is None:
        cursor.execute('INSERT INTO users (user, areact, messages) VALUES (?, ?, ?)', (user_id, 'Active', 0))
    conn.commit()
    conn.close()
    return user

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    user = check_and_add_user(user_id)
    
    if user_id in admins:
        if user is None:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Add message ✉️', callback_data='add_message'))
            markup.add(types.InlineKeyboardButton('Delete message 🗑️', callback_data='delete_message'))
            markup.add(types.InlineKeyboardButton('Help 📚', callback_data='help'))
            markup.add(types.InlineKeyboardButton('Show all commands 📜', callback_data='show_commands'))

            bot.send_message(user_id, "👨‍💼 *Hello, admin!* Configure your bot using the buttons below:", reply_markup=markup, parse_mode='Markdown')
        else:
            bot.send_message(user_id, "👨‍💼 *Hello, admin!* Type /help to get the admin guide. Type /menu to open the admin panel.", parse_mode='Markdown')
    else:
        if user is None:
            bot.send_message(user_id, "👋 *Hello, user!*\n\nAll phrases: /messagelist", parse_mode='Markdown')
        else:
            bot.send_message(user_id, "👋 *Hello, user!* Type /messagelist to see the list of bot phrases.", parse_mode='Markdown')

@bot.message_handler(commands=['menu'])
def admin_menu(message):
    user_id = message.from_user.id
    if user_id in admins:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Add message ✉️', callback_data='add_message'))
        markup.add(types.InlineKeyboardButton('Delete message 🗑️', callback_data='delete_message'))
        markup.add(types.InlineKeyboardButton('Help 📚', callback_data='help'))
        markup.add(types.InlineKeyboardButton('Show all commands 📜', callback_data='show_commands'))

        bot.send_message(user_id, "👨‍💼 *Admin Menu* 👨‍💼\n\nConfigure your bot using the buttons below:", reply_markup=markup, parse_mode='Markdown')
    else:
        bot.send_message(user_id, "🚫 You are not authorized to access the admin menu.", parse_mode='Markdown')

@bot.message_handler(commands=['list'])
def admin_list(message):
    user_id = message.from_user.id
    if user_id in admins:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE areact = "Active"')
        active_users = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM users WHERE areact = "Disable"')
        inactive_users = cursor.fetchone()[0]
        conn.close()

        bot.send_message(user_id, f"📊 *User List* 📊\n\nActive users: {active_users}\nInactive users: {inactive_users}", parse_mode='Markdown')
    else:
        bot.send_message(user_id, "🚫 You are not authorized to access this command.", parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def admin_help(message):
    user_id = message.from_user.id
    if user_id in admins:
        help_text = """
        📚 *Admin Help* 📚

        **Admin Menu Buttons:**
        - *Add message ✉️*: Click this button to add a new message to which the bot will respond. After clicking the button, enter the message and separate it with a colon (:) from the response. For example: (Message the user will send:Message the bot will respond with).
        - *Delete message 🗑️*: Click this button to delete an existing message from the database. After clicking the button, enter the exact message you want to delete and send it.
        - *Help 📚*: Click this button to get help information on how to use the admin menu.
        - *Show all commands 📜*: Click this button to display a list of all commands available to admins and users.

        **Commands:**
        `/menu` - Send admin menu.
        `/list` - Show the number of active and inactive users.
        `/help` - Show admin help.
        `/statistic` - Show total number of messages for all time, today, week, and month.
        `/localstatistic [user_id]` - Show statistics for a specific user.
        `/addnews` - Add a news item.
        `/seenews` - View all news items.
        `/sendnews` - Send the latest news item to all users.
        `/mystat` - Show user message statistics.
        `/messagelist` - Show a list of all messages that the user can send to the bot to get a response.
        """
        bot.send_message(user_id, help_text, parse_mode='Markdown')
    else:
        bot.send_message(user_id, "🚫 You are not authorized to access this command.", parse_mode='Markdown')


@bot.message_handler(commands=['statistic'])
def admin_statistic(message):
    user_id = message.from_user.id
    if user_id in admins:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(messages) FROM users')
        total_messages = cursor.fetchone()[0] or 0
        cursor.execute('SELECT COUNT(*) FROM statistic WHERE DATE("now") - DATE(time) = 1')
        today_messages = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM statistic WHERE DATE("now") - DATE(time) <= 7')
        week_messages = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM statistic WHERE DATE("now") - DATE(time) <= 30')
        month_messages = cursor.fetchone()[0]
        conn.close()

        bot.send_message(user_id, f"📊 *Statistics* 📊\n\nTotal messages: {total_messages}\nMessages today: {today_messages}\nMessages this week: {week_messages}\nMessages this month: {month_messages}", parse_mode='Markdown')
    else:
        bot.send_message(user_id, "🚫 You are not authorized to access this command.", parse_mode='Markdown')

@bot.message_handler(commands=['localstatistic'])
def admin_localstatistic(message):
    user_id = message.from_user.id
    if user_id in admins:
        try:
            target_user_id = int(message.text.split()[1])
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('SELECT messages FROM users WHERE user = ?', (target_user_id,))
            user_messages = cursor.fetchone()
            conn.close()
            if user_messages:
                bot.send_message(user_id, f"📊 *User {target_user_id} Statistics* 📊\n\nMessages: {user_messages[0]}", parse_mode='Markdown')
            else:
                bot.send_message(user_id, "🚫 User not found.", parse_mode='Markdown')
        except (IndexError, ValueError):
            bot.send_message(user_id, "🚫 Invalid command format. Use /localstatistic [user_id]", parse_mode='Markdown')
    else:
        bot.send_message(user_id, "🚫 You are not authorized to access this command.", parse_mode='Markdown')

@bot.message_handler(commands=['mystat'])
def user_mystat(message):
    user_id = message.from_user.id
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT messages FROM users WHERE user = ?', (user_id,))
    user_messages = cursor.fetchone()
    conn.close()
    if user_messages:
        bot.send_message(user_id, f"📊 *Your Statistics* 📊\n\nMessages: {user_messages[0]}", parse_mode='Markdown')
    else:
        bot.send_message(user_id, "🚫 User not found.", parse_mode='Markdown')

@bot.message_handler(commands=['messagelist'])
def user_messagelist(message):
    user_id = message.from_user.id
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT message FROM messages')
    messages = cursor.fetchall()
    conn.close()
    if messages:
        message_list = "\n".join([msg[0] for msg in messages])
        bot.send_message(user_id, f"📜 *Message List* 📜\n\n{message_list}", parse_mode='Markdown')
    else:
        bot.send_message(user_id, "🚫 No messages found.", parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user_id = call.from_user.id
    if user_id in admins:
        if call.data == 'add_message':
            bot.send_message(user_id, "✉️ *Add Message*\n\nPlease enter the message and the response in the format:\n\n`message:response`", parse_mode='Markdown')
            bot.register_next_step_handler(call.message, add_message)
        elif call.data == 'delete_message':
            bot.send_message(user_id, "🗑️ *Delete Message*\n\nPlease enter the message you want to delete:", parse_mode='Markdown')
            bot.register_next_step_handler(call.message, delete_message)
        elif call.data == 'help':
            admin_help(call.message)
        elif call.data == 'show_commands':
            bot.send_message(user_id, "📜 *All Commands* 📜\n\n**Admin Commands:**\n/menu - Send admin menu.\n/list - Show the number of active and inactive users.\n/help - Show all commands.\n/statistic - Show total number of messages for all time, today, week, and month.\n/localstatistic [user_id] - Show statistics for a specific user.\n/addnews - Add a news item.\n/seenews - View all news items.\n/sendnews - Send the latest news item to all users.\n\n**User Commands:**\n/mystat - Show user message statistics.\n/messagelist - Show a list of all messages that the user can send to the bot to get a response.", parse_mode='Markdown')

def add_message(message):
    user_id = message.from_user.id
    if user_id in admins:
        try:
            msg, response = message.text.split(':')
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages (message, answer) VALUES (?, ?)', (msg, response))
            conn.commit()
            conn.close()
            bot.send_message(user_id, "✅ *Message added successfully!*", parse_mode='Markdown')
        except ValueError:
            bot.send_message(user_id, "🚫 Invalid format. Use `message:response`", parse_mode='Markdown')

def delete_message(message):
    user_id = message.from_user.id
    if user_id in admins:
        msg = message.text
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM messages WHERE message = ?', (msg,))
        conn.commit()
        conn.close()
        bot.send_message(user_id, "✅ *Message deleted successfully!*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_user_message(message):
    user_id = message.from_user.id
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT answer FROM messages WHERE message = ?', (message.text,))
    response = cursor.fetchone()
    if response:
        cursor.execute('UPDATE users SET messages = messages + 1 WHERE user = ?', (user_id,))
        cursor.execute('UPDATE statistic SET allmessages = allmessages + 1, todaymessages = todaymessages + 1, weekmessages = weekmessages + 1, mouthmessages = mouthmessages + 1')
        conn.commit()
        bot.send_message(user_id, response[0])
    conn.close()

def send_message_with_block_check(user_id, text):
    try:
        bot.send_message(user_id, text)
        return True
    except telebot.apihelper.ApiException as e:
        if e.error_code == 403:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET areact = "Disable" WHERE user = ?', (user_id,))
            conn.commit()
            conn.close()
        return False

@bot.message_handler(commands=['addnews'])
def add_news_start(message):
    user_id = message.from_user.id
    if user_id in admins:
        msg = bot.send_message(user_id, "📝 Please write the news:")
        bot.register_next_step_handler(msg, add_news_finish)
    else:
        bot.send_message(user_id, "🚫 You do not have permission to add news.")

def add_news_finish(message):
    user_id = message.from_user.id
    news_text = message.text
    
    if os.path.exists(news_file):
        with open(news_file, 'r') as file:
            news_list = json.load(file)
    else:
        news_list = []

    news_list.append({'text': news_text})
    
    with open(news_file, 'w') as file:
        json.dump(news_list, file, indent=4)

    bot.send_message(user_id, "✅ News added successfully!")


@bot.message_handler(commands=['seenews'])
def see_news(message):
    user_id = message.from_user.id
    if user_id in admins:
        if os.path.exists(news_file):
            with open(news_file, 'r') as file:
                news_list = json.load(file)
            
            if news_list:
                for news in news_list:
                    news_message = f"🗞 {news['text']}"
                    bot.send_message(user_id, news_message)
            else:
                bot.send_message(user_id, "No news available.")
        else:
            bot.send_message(user_id, "No news file found.")
    else:
        bot.send_message(user_id, "🚫 You do not have permission to view news.")


@bot.message_handler(commands=['sendnews'])
def send_news(message):
    user_id = message.from_user.id
    if user_id in admins:
        if os.path.exists(news_file):
            with open(news_file, 'r') as file:
                news_list = json.load(file)
            
            if news_list:
                latest_news = news_list[-1]
                news_message = f"{latest_news['text']}"
                
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute('SELECT user FROM users')
                users = cursor.fetchall()
                conn.close()

                for user in users:
                    user_id = user[0]
                    try:
                        bot.send_message(user_id, news_message)
                    except telebot.apihelper.ApiException as e:
                        print(f"Failed to send message to user {user_id}: {e}")
            else:
                bot.send_message(user_id, "No news available to send.")
        else:
            bot.send_message(user_id, "No news file found.")
    else:
        bot.send_message(user_id, "🚫 You do not have permission to send news.")


if __name__ == '__main__':
    bot.polling(none_stop=True)
