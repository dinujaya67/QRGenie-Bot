# Import required libraries
import os
import re
import qrcode
from io import BytesIO
from typing import Final
from dotenv import load_dotenv
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes,CallbackQueryHandler,ConversationHandler

# Load environment variables from a .env file
load_dotenv()

# Retrieve sensitive information securely from environment variables
Token: Final = os.getenv('Api')
Admin_Id: Final = os.getenv('Admin_C_Id')
Bot_Username: Final = os.getenv('Bot_Uname')

# Define handler functions for buttons on the inline keyboard
def handle_help_btn(update:Update, context:ContextTypes.DEFAULT_TYPE) -> str:
    return "Here’s the help you need! Use /help to get detailed instructions."

def handle_create_btn(update:Update, context:ContextTypes.DEFAULT_TYPE) -> str:
    return "Ready to create a QR code? Use /create followed by your data!"

def handle_cancel_btn(update:Update, context:ContextTypes.DEFAULT_TYPE) -> str:
    return "Thank you for using QRGenie! See you next time!"

# Command function that runs when the user starts the bot
async def start_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    f_name: str = update.message.from_user.first_name  # Get the user's first name

    # Send a welcome message with bot usage instructions
    await update.message.reply_text(f"""
*👋🏻 Hi {f_name}!*
I'm *QRGenie*, your personal QR code wizard!🧙🏻‍♂️✨

Ready to transform your text or data into a sleek, high-quality QR code? Just send me what you want to convert, and I'll work my magic in seconds!🪄

*🌟 What can I do for you?*
    • 🔗 *URLs:* Share links effortlessly.
    • 📇 *Contact Info:* Save and share contacts with a scan.
    • 📅 *Event Details:* Make your events scannable.
    • 📜 *And so much more!*

With *QRGenie*, enjoy *secure, private*, and *free* QR code generation, avaliable *24/7*-whenever you need it! 🕒🔒

🚀 *Let's get started!*
Type `/create [your data]` and send it my way. I'll handle the rest!🖼🔍
""",parse_mode='Markdown')
    
    # Create an inline keyboard with multiple options for the user
    keyboard = [
        [InlineKeyboardButton("Create", callback_data='create_btn'), InlineKeyboardButton("Help", callback_data='help_btn')],
        [InlineKeyboardButton("Exit", callback_data='exit_btn')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send a message with the inline keyboard attached
    await update.message.reply_text("*Ready to create some magic?* ✨",parse_mode='Markdown', reply_markup=reply_markup)

# Command function that provides help and instructions
async def help_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # Create an inline keyboard with multiple options for the user
    keyboard = [
        [InlineKeyboardButton("Create", callback_data='create_btn'), InlineKeyboardButton("Exit", callback_data='exit_btn')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send a message with the inline keyboard attached
    await update.message.reply_text("""
*✨ Welcome to QRGenie! ✨*

Unleash the magic of QR codes with QRGenie-your personal QR code creation assistant! 🧙🏻‍♂️ Whether you're sharing links, contact info, or secret messages, QRGenie has got you covered. Here's how to use me:

*Commands🛠*
    • /start - 🌟 Begin Your Journey: Start interacting with QRGenie.
    • /help - 🧩 Need Assistance?: Display this help message anytime.
    • /create [text or data] - 🎨 Create Your QR Code.

Examples:
1. `/create https://example.com`
2. `/create John Doe, John@example.com`
3. `/create Welcome to QRGenie!`

*🧙🏻‍♂️ Why Choose QRGenie?*
    • Ease of Use, Flexibility, Speed, Versatility.
""", parse_mode='Markdown', reply_markup=reply_markup)

# Command function that generates a QR code from the provided data
async def create_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    text: str= update.message.text  # Get the text entered by the user

    # Create an inline keyboard with multiple options for the user
    keyboard = [
        [InlineKeyboardButton("Help", callback_data='help_btn'), InlineKeyboardButton("Exit", callback_data='exit_btn')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if '/create' in text:
        new_text: str=text.replace('/create', '').strip()  # Extract the data after the command
        if new_text != '' :
            img=qrcode.make(new_text)  # Generate the QR code
            bio=BytesIO()
            bio.name='qr_code.png'
            img.save(bio,'PNG')
            bio.seek(0)

            # Send the generated QR code as an image to the user
            await update.message.reply_photo(photo=bio, caption=f'Here’s your magic! ✨ QR code for: {new_text}')
            # Send a message with the inline keyboard attached
            await update.message.reply_text('*Are you need any other help from me?*',parse_mode='Markdown', reply_markup=reply_markup)
        else:
            # Inform the user that no data was found after the command
            await update.message.reply_text("🔍*Oops! Can't find any data here.*📄\nNo worries, just give me some data with the `/create` command!\nExample: `/create some data` 💡", parse_mode='Markdown', reply_markup=reply_markup)

# Command function to handle the exit command
async def cancel_command(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    # Create an inline keyboard with multiple options for the user
    keyboard = [
        [InlineKeyboardButton("Create", callback_data='create_btn'), InlineKeyboardButton("Exit", callback_data='exit_btn')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send a message with the inline keyboard attached
    await update.message.reply_text("👋🏻*Leaving so soon?* Thank you for using QRGenie! 🌟 If you need another sprinkle of QR magic, you know where to find me!🧙🏻‍♂️✨", parse_mode='Markdown', reply_markup=reply_markup)
    return ConversationHandler.END

# Callback function to handle button clicks on the inline keyboard
async def button(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data: str= query.data 

    if data == 'create_btn':
        response: str= handle_create_btn(update, context)
    elif data == 'help_btn':
        response: str= handle_help_btn(update, context)
    elif data == 'exit_btn':
        response: str= handle_cancel_btn(update, context)
    else:
        response: str= "Unknown option selected"

    # Ensure response is not empty before updating the message
    if response.strip():
        await query.edit_message_text(response)
    else:
        await query.edit_message_text("Something went wrong. Please try again.")
        

# Function to handle user messages and provide appropriate responses
def handle_response(text: str, f_name:str) -> str:
    processed: str = text.lower()
    if 'hello' in processed or 'hi' in processed or 'hey' in processed:
        return f"🎨*Hey {f_name},it's time to unleash your creativity!🌟\n\n✨Start your creations now and let your imagination run wild!*🚀"
    else:
        return "🤔*Oops! I didn't quite get that.\nCould you please rephrase or try again?*📝"

# Function to handle incoming messages from users
async def handle_message(update:Update, context:ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type 
    text: str = update.message.text
    f_name: str = update.message.from_user.first_name

    if message_type =='group':
        if Bot_Username in text:
            new_text: str = text.replace(Bot_Username,'').strip()
            if new_text !='':
                response: str = handle_response(new_text, f_name)
            else:
                await start_command(update, context)  # Trigger the start command if the bot's username is mentioned
                return
        else:
            return
    else:
        response: str = handle_response(text, f_name)
    # Create an inline keyboard with multiple options for the user
    keyboard = [
        [InlineKeyboardButton("Create", callback_data='create_btn'), InlineKeyboardButton("Feedback", callback_data='feedback_btn')],
        [InlineKeyboardButton("Help", callback_data='help_btn'), InlineKeyboardButton("Exit", callback_data='exit_btn')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send a message with the inline keyboard attached
    await update.message.reply_text(response, parse_mode='Markdown', reply_markup=reply_markup)

# Function to handle errors that occur during bot operation
async def error(update:Update, context:ContextTypes.DEFAULT_TYPE):
    print(f'Update: {update} caused error {context.error}')
    await update.message.reply_text("An error occurred, please try again later.")

# Main function to set up and run the bot
if __name__=='__main__':
    print('Starting bot......')
    app = Application.builder().token(Token).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('create', create_command))
    app.add_handler(CommandHandler('exit', cancel_command))
    app.add_handler(CallbackQueryHandler(button))

    app.add_error_handler(error)

    print('Polling......')
    app.run_polling(poll_interval=5)