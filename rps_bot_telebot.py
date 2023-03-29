import telebot
import random
import math

bot_name = 'RPSLSpock'
bot_token = '6170097626:AAF0dCDmWInLrR0zAZ85qMaY_6VQdrVX7mQ'
bot=telebot.TeleBot(bot_token)
players = {}#{'a':1,'b':2,'c':3}
n = 0
y_votes = 0
next_power = 2
g_tournament = []
gmode_selected = 'rpsls'
game_mode_tk = {'rpsls':{'A':'Rock', 'B':'Paper', 'C':'Scissors', 'D':'Lizard', 'E':'Spock'},
            'rpsfwt':{'A':'Rock', 'B':'Paper', 'C':'Scissors', 'D':'Fire', 'E':'Water'},
            'rpsfwl':{'A':'Rock', 'B':'Paper', 'C':'Scissors', 'D':'Fire', 'E':'Well'}}



def joinTournament(message):
    global n
    global players
    global next_power
    n += 1
    if n > next_power:
        next_power <<= 1
    user = message.from_user
    players[user.id] = {}
    players[user.id]['user'] = user
    players[user.id]['vote'] = False
    players[user.id]['gamemode'] = 'rpsls'
    players[user.id]['signal'] = ''
    players[user.id]['adversary'] = ''
    players[user.id]['isWinner'] = False
    bot.send_message(user.id, f"You have successfully joined to the tournament!\nThere are {n - 1} other players in the tournament.")

@bot.message_handler(commands=['join'])
def handleNewUser(message):
    joinTournament(message)
    if isPowerOfTwo(n) and n > 1:
        broadcast("The tournament can start now.")
        broadcast("You can vote to start the tournament:\n/yes\n/no")
    else:
        broadcast(f"There are/is {next_power - n} player(s) left to start the tournament.")



@bot.message_handler(commands=['yes'])
def handleYesVote(message):        
    global y_votes
    print(players)
    if not players[message.chat.id]['vote']:
        players[message.chat.id]['vote'] = True
        y_votes += 1
    if y_votes == n:
        broadcast("Everyone is ready to start the tournament.\nStarting...")
        startTournament()


def isPowerOfTwo(x) -> bool:
    c = 0
    while x:
        if x&1:
            if c == 1:
                return False
            else:
                c = 1
        x>>=1
    return True

def broadcast(message):
    for k in players:
        bot.send_message(k, message)

def pairing(players_dict):
    keys = [k for k in players_dict]
    random.shuffle(keys)
    pairs =[(keys[i], keys[i+1]) for i in range(0, n, 2)]
    for a,b in pairs:
        players[a]['adversary'] = b
        players[b]['adversary'] = a
    return pairs

def playMatch(match):
    a,b = match
    # bot.send_message("907018271", f"What is your signal against {b}?")
    # bot.send_message("907018271",f"/{game_mode_tk[gmode_selected]['A']}\n/{game_mode_tk[gmode_selected]['B']}\n/{game_mode_tk[gmode_selected]['C']}\n/{game_mode_tk[gmode_selected]['D']}\n/{game_mode_tk[gmode_selected]['E']}\n")
    bot.send_message(b, f"What is your signal against {a}?")
    bot.send_message(b,f"/A {game_mode_tk[gmode_selected]['A']}\n/B {game_mode_tk[gmode_selected]['B']}\n/C {game_mode_tk[gmode_selected]['C']}\n/D {game_mode_tk[gmode_selected]['D']}\n/E {game_mode_tk[gmode_selected]['E']}\n")
    bot.send_message(a, f"What is your signal against {b}?")
    bot.send_message(a,f"/A {game_mode_tk[gmode_selected]['A']}\n/B {game_mode_tk[gmode_selected]['B']}\n/C {game_mode_tk[gmode_selected]['C']}\n/D {game_mode_tk[gmode_selected]['D']}\n/E {game_mode_tk[gmode_selected]['E']}\n")

def game(choice_a:str, choice_b:str):
    options = ["A", "B", "C", "D", "E"]

    if choice_a == choice_b:
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
        return 1
    else:
        return 2


@bot.message_handler(commands=['A','B','C','D','E'])
def playSignal(message):
    players[message.chat.id]['signal'] = message.text[1]
    adversary = players[message.chat.id]['adversary']
    print(adversary)
    if players[adversary]['signal'] != '':
        result = game(players[message.chat.id]['signal'], players[adversary]['signal'])
        players[message.chat.id]['signal'] = ''
        players[adversary]['signal'] = ''
        if result == 0:
            bot.send_message(message.chat.id,"There is a tie.\nPlease select again a new signal.")
            bot.send_message(adversary,"There is a tie.\nPlease select again a new signal.")
            playMatch(message.chat.id, adversary)
        elif result == 1:
            players[message.chat.id]["isWinner"] = True
            players[adversary]["isWinner"] = False
            bot.send_message(message.chat.id, f"You have won againts {adversary}")
            bot.send_message(adversary, f"You have lost againts {message.chat.id}")
        else:
            players[message.chat.id]["isWinner"] = False
            players[adversary]["isWinner"] = True
            bot.send_message(adversary, f"You have won againts {message.chat.id}")
            bot.send_message(message.chat.id, f"You have lost againts {adversary}")
            

def startTournament():
    g_tournament = pairing(players)
    broadcast(f"The tournament matches is as follows\n{g_tournament}")
    for p in g_tournament:
        playMatch(p)



bot.polling()

