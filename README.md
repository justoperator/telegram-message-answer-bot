# Telegram Bot for Message Management

This Telegram bot allows you to create a message-based assistant. It can respond to specific messages with predefined responses, manage users, and handle news updates. This bot supports administrative commands and can be customized according to your needs.

## Features

- **User Management**: Adds new users and tracks their activity.
- **Message Management**: Admins can add or delete predefined messages that the bot will respond to.
- **Admin Menu**: Provides a menu for admins to manage the bot.
- **Statistics**: Displays statistics about messages and users.
- **News Management**: Allows admins to add, view, and send news updates.

## Setup

### Prerequisites

- Python 3.x
- Telegram Bot Token (get it from [BotFather](https://t.me/botfather))

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/justoperator/telegram-message-answer-bot.git
    ```

2. **Install Dependencies**: Ensure you have the necessary Python packages installed. You can use pip to install them:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Bot**:
    - Open the `bot_code.py` file.
    - Replace `PASTE HERE YOUR API KEY` with your bot token.
    - Replace `PASTE HERE YOUR TELEGRAM ID` with your Telegram ID in the `admins` list.

4. **Run the Bot**:
    ```bash
    python main.py
    ```

## Commands

- `/start` - Starts the bot and shows a welcome message based on user or admin status.
- `/menu` - Displays the admin menu with options to manage messages and view help. (Admin only).
- `/list` - Shows the number of active and inactive users (Admin only).
- `/help` - Provides help information for admins (Admin only).
- `/statistic` - Shows message statistics (Admin only).
- `/localstatistic [user_id]` - Shows statistics for a specific user (Admin only).
- `/mystat` - Displays the user's message statistics.
- `/messagelist` - Shows a list of all messages that the user can send to the bot.
- `/addnews` - Starts the process to add a news item (Admin only).
- `/seenews` - Views all news items (Admin only).
- `/sendnews` - Sends the latest news item to all users (Admin only).

## Admin Functions

Admins can access additional commands and features:

- **Add Message**: Adds a new message to the database. Format: `message:response`.
- **Delete Message**: Deletes an existing message from the database.
- **Help**: Provides detailed help information on admin commands.
- **Show All Commands**: Displays a list of all available commands.

## Notes

- Make sure to replace placeholder values with actual data before running the bot.
- Use the `/help` command to get a detailed guide on how to use the bot’s features.

