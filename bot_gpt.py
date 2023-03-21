import telegram
import random
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# Create an Updater object
updater = Updater(token='YOUR_TELEGRAM_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

# Define a command handler for the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Rock, Paper, Scissors, Lizard, Spock! Type /play to start a game.")

# Define a command handler for the /play command
def play(update, context):
    # Define the options
    options = ["rock", "paper", "scissors", "lizard", "spock"]
    
    # Generate a random choice for the bot
    bot_choice = random.choice(options)
    
    # Send the options to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text="Choose one: rock, paper, scissors, lizard, spock")
    
    # Define a message handler for the user's choice
    def user_choice(update, context):
        user_input = update.message.text.lower()
        if user_input not in options:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid choice. Please choose again.")
            return
        if user_input == bot_choice:
            context.bot.send_message(chat_id=update.effective_chat.id, text="It's a tie!")
        elif (user_input == "rock" and bot_choice == "scissors") or \
             (user_input == "paper" and bot_choice == "rock") or \
             (user_input == "scissors" and bot_choice == "paper") or \
             (user_input == "rock" and bot_choice == "lizard") or \
             (user_input == "lizard" and bot_choice == "spock") or \
             (user_input == "spock" and bot_choice == "scissors") or \
             (user_input == "scissors" and bot_choice == "lizard") or \
             (user_input == "lizard" and bot_choice == "paper") or \
             (user_input == "paper" and bot_choice == "spock") or \
             (user_input == "spock" and bot_choice == "rock"):
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"You chose {user_input}, and I chose {bot_choice}. You win!")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"You chose {user_input}, and I chose {bot_choice}. I win!")
        # Remove the user_choice message handler
        dispatcher.remove_handler(user_choice_handler)
    
    # Add the message handler for the user's choice
    user_choice_handler = MessageHandler(Filters.text & (~Filters.command), user_choice)
    dispatcher.add_handler(user_choice_handler)

# Register the command handlers with the dispatcher
start_handler = CommandHandler('start', start)
play_handler = CommandHandler('play', play)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(play_handler)

# Start the bot
updater.start_polling()
