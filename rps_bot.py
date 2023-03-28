import math
import random
import telebot

bot_name = 'RPSLSpock'
bot_token = '6170097626:AAF0dCDmWInLrR0zAZ85qMaY_6VQdrVX7mQ'

players = {}
n = 0



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(
        f"Type /join to join to the tournament",
        reply_markup=ForceReply(selective=True),
    )
    # await update.message.reply_html(
    #     "Type /rpsfwl to vote for Rock, Paper, Scissors, Fire, Well\nType /rpsls to vote for Rock, Paper, Scissors, Lizard, Spock\nType /rpsfwt to vote for Rock, Paper, Scissors, Fire, Water",
    #     reply_markup=ForceReply(selective=True),
    # )
    # Send game options


def pairing(players_dict):
    keys = [k for k in players_dict]
    random.shuffle(keys)
    return [(keys[i], keys[i+1]) for i in range(0, len(keys), 2)]


def main() -> None:
    f = open('botConf.json')
    botConfData = json.load(f)

    print("Running bot: ", botConfData["bot_name"])

    """Start the bot."""
    TOKEN=botConfData["bot_token"]
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on game command - answer

    application.add_handler(CommandHandler("rpsfwl", rpsfwl))
    application.add_handler(CommandHandler("rpsls", rpsls))
    application.add_handler(CommandHandler("rpsfwt", rpsfwt))
    application.add_handler(CommandHandler("join", joinTournament))
    application.add_handler(CommandHandler("startTournament", startTournament))
    application.add_handler(CommandHandler("resetTournament", resetTournament))
    application.add_handler(CommandHandler("players", showPlayers))
    application.add_handler(CommandHandler("pairing", randomPairs))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

async def rpsfwl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("rpsfwl selected")
    game_vote(0)

async def rpsls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("rpsls selected")
    game_vote(1)

async def rpsfwt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("rpsfwt selected")
    game_vote(2)


async def joinTournament(update: Update, context: ContextTypes.DEFAULT_TYPE):
    players[update.message.from_user.id]=update.message.from_user.username
    user = update.effective_user
    await update.message.reply_text(f"Hi {user.mention_html()}!. You have successfully joined to the tournament!\n{players}")

async def startTournament(update: Update, context: ContextTypes.DEFAULT_TYPE):
    players[update.message.id]=update.message.username
    await update.message.reply_text(f"You have successfully joined to the tournament!\n{players}")

async def resetTournament(update: Update, context: ContextTypes.DEFAULT_TYPE):
    players = {}
    await update.message.reply_text("The tournament has been succesfully reseted!")

async def showPlayers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"The current list of players is:\n{players}")

async def randomPairs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Random pairing:\n{pairing({'a':'v1', 'b':'v2', 'c':'v3', 'd':'v4'})}")

async def notifyNewPlayer(user_id: Update, context: ContextTypes.DEFAULT_TYPE):
    to_notify = [k for k in players]
    for k in players:
        


def game_vote(opt: str):
    print("VOTE: ",opt)

def game(choice_a:str):
    options = ["A", "B", "C", "D", "E"]
    choice_a = ''
    choice_b = ''

    if choice_a not in options or  choice_b not in options:
        print("Not an option") # Replace this to send the bot message
        return -1
    elif choice_a == choice_b:
        print("It's a tie!") # Replace this to send the bot message
        return 0
    # We should not know the user's input
    elif (choice_a == "A" and choice_b == "C") or \
    (choice_a == "B" and choice_b == "A") or \
    (choice_a == "C" and choice_b == "B") or \
    (choice_a == "A" and choice_b == "D") or \
    (choice_a == "D" and choice_b == "E") or \
    (choice_a == "E" and choice_b == "C") or \
    (choice_a == "C" and choice_b == "D") or \
    (choice_a == "D" and choice_b == "B") or \
    (choice_a == "B" and choice_b == "E") or \
    (choice_a == "E" and choice_b == "A"):
        print("Player A won!") # Replace this to send the bot message
        return 1
    else:
        print("Player B won!") # Replace this to send the bot message
        return 2


if __name__ == "__main__":
    main()

gmode_selected = 'rpsls'
game_mode_tk = {'rpsls':{'A':'Rock', 'B':'Paper', 'C':'Scissors', 'D':'Lizard', 'E':'Spock'},
            'rpsfwt':{'A':'Rock', 'B':'Paper', 'C':'Scissors', 'D':'Fire', 'E':'Water'},
            'rpsfwl':{'A':'Rock', 'B':'Paper', 'C':'Scissors', 'D':'Fire', 'E':'Well'}}


def generate_tournament():
    n = len(players)
    if math.log(n) != math.trunc(n):
        print("The number of players must be power of 2") #Replace this to use the bot
        return
    pairs = pairing(players)
    