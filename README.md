# QRGenie Bot

QRGenie is a Telegram bot that generates QR codes from user input. It's easy to use and offers a flexible interface for generating QR codes on the fly.

## Features
- Generate QR codes for URLs, contact info, event details, and more.
- Simple and user-friendly commands.
- Available 24/7.

## Requirements
- Python 3.8+
- A Telegram bot token (from [BotFather](https://core.telegram.org/bots#botfather)).

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/your_username/QRGenie-Bot.git
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your bot credentials:
   ```ini
   Api=your_bot_api_token
   Admin_C_Id=your_admin_chat_id
   Bot_Uname=@your_bot_username
   ```

4. Run the bot:
   ```bash
   python qrgenie_bot.py
   ```

## Usage
- `/start` - Start interacting with the bot.
- `/help` - Get help with using the bot.
- `/create [data]` - Create a QR code from the provided data.
