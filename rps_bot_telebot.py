import telebot
import random
from pedersen import prover, verifier

bot_name = 'RPSLSpock'
bot_token = '6170097626:AAF0dCDmWInLrR0zAZ85qMaY_6VQdrVX7mQ'
bot=telebot.TeleBot(bot_token)
players = {}#{'a':1,'b':2,'c':3}
n = 0
gamemode_votes = [0,0,0]
next_power = 2
g_tournament = []
stage_matches_finished = 0
gmode_selected = 'rpsfwl'
game_mode_tk = {'rpsls':{'A':'Rock', 'B':'Paper', 'C':'Scissors', 'D':'Lizard', 'E':'Spock'},
                'rpsfwt':{'A':'Rock', 'B':'Paper', 'C':'Scissors', 'D':'Fire', 'E':'Water'},
                'rpsfwl':{'A':'Rock', 'B':'Paper', 'C':'Scissors', 'D':'Fire', 'E':'Well'}}

p = prover()
v = verifier()
security = 80
public_params = v.setup(security)

def joinTournament(message):
    global n
    global players
    global next_power
    n += 1
    if n > next_power:
        next_power <<= 1
    user = message.from_user
    players[user.id] = {}
    players[user.id]['adversary'] = ''
    players[user.id]['commitment'] = None
    players[user.id]['gamemode'] = 'rpsls'
    players[user.id]['isWinner'] = False
    players[user.id]['signal'] = ''
    players[user.id]['user'] = user
    players[user.id]['vote'] = None 
    bot.send_message(user.id, f"You have successfully joined to the tournament!\nThere are {n - 1} other players in the tournament.")

@bot.message_handler(commands=['join'])
def handleNewUser(message):
    global players

    if message.chat.id not in players.keys():
        joinTournament(message)
        if isPowerOfTwo(n) and n > 1:
            broadcast("The tournament can start now.")
            broadcast("Select the game mode:\n/rpsls to play Rock, Paper, Scissors, Lizard, Spock\n/rpsfwt to play Rock, Paper, Scissors, Fire, Water\n/rpsfwl to play Rock, Paper, Scissors, Fire, Well")
        else:
            broadcast(f"There are/is {next_power - n} player(s) left to start the tournament.")
    else:
        bot.send_message(message.chat.id, f"You have already joined the tournament, you must wait until other participants join the tournament.")

def voteIndex(vote):
    global game_mode_tk
    return list(game_mode_tk.keys()).index(vote) if vote in game_mode_tk else 2 

def votesCast(key):
    global players
    
    return sum([1 if value[key] != None else 0 for _, value in players.items()])


@bot.message_handler(commands=['rpsls', 'rpsfwt', 'rpsfwl'])
def handleCommitment(message):
    global gamemode_votes
    global gmode_selected
    global public_params
    global p
    if players[message.chat.id]['commitment'] == None:
        selected = message.text[1:]
        idx = voteIndex(selected) 
        gamemode_votes[idx] += 1
        c, r = p.commit(public_params, idx)
        players[message.chat.id]['commitment'] = c
        bot.send_message(message.chat.id, f"The commitment for the vote <code>{selected}</code> has been submitted.\n. Please make sure you remember the vote selected and the random value to verify your vote in the next state.\n\nvote: <code>{selected}</code>\nrandom value: <code>{r}</code>\ncommitment: <code>{c}</code>.\n\n Once all players have submitted their commitments, you must verify your vote by sending the following message:\n<code>verify {selected} {r}</code>", parse_mode='html')
        totalVotesCast = votesCast('commitment')

        broadcast(f"{totalVotesCast}/{n} players have submitted their commitments.")

        if totalVotesCast == n:
            broadcast("All players have submitted their commitments, the verification stage is starting now...")
            broadcast("Now all participants must send the vote and the random value that generate the commitment by using the keyword <code>verify</code>. Please make sure you send the values in the following format:\n\n <code>verify {vote} {random value}</code>.")
    else:
        bot.send_message(message.chat.id, f"You have already published your commitment, you must wait until all participants submit their commitments to start the verification stage.")


def verifyRequest(message):
    request = message.text.split()
    return len(request) >= 3 and request[0].lower() == "verify" and request[2].isnumeric()

def verify_vote(player_id, vote, r):
    global players
    global v

    player = players[player_id]
    return v.open(public_params, player['commitment'], vote, r)

@bot.message_handler(func=verifyRequest)
def tallyVotes(message):
    global gmode_selected
    global players

    if players[message.chat.id]['vote'] != None:
        request = message.text.split()
        selected_vote = request[1]
        idx = voteIndex(selected_vote)
        r = int(request[2])
        is_valid = verify_vote(message.chat.id, idx, r)

        if is_valid:
            gamemode_votes[idx] += 1
            bot.send_message(message.chat.id, f"Your vote has been verified succefully!")
        else:
            selected_vote = 'invalid'
            bot.send_message(message.chat.id, "Your vote is invalid because the verification of your vote has failed.")

        players[message.chat.id]['vote'] = selected_vote 

        totalVotesCast = votesCast('vote')
        broadcast(f"{totalVotesCast}/{n} players have verified their commitments.")
        
        if totalVotesCast == n:
            selected_idx = gamemode_votes.index(max(gamemode_votes))
            gmode_selected = list(game_mode_tk.keys())[selected_idx]
            broadcast("Everyone is ready to start the tournament.\nStarting...")
            startTournament()


def isPowerOfTwo(x):
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
        bot.send_message(k, message, parse_mode='html')

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
    global stage_matches_finished
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
            bot.send_message(adversary, f"Thanks for playing. Better luck the next one!")
            stage_matches_finished += 1
        else:
            players[message.chat.id]["isWinner"] = False
            players[adversary]["isWinner"] = True
            bot.send_message(adversary, f"You have won againts {message.chat.id}")
            bot.send_message(message.chat.id, f"You have lost againts {adversary}")
            bot.send_message(message.chat.id, f"Thanks for playing. Better luck the next one!")
            stage_matches_finished += 1
    if stage_matches_finished == len():
        nextStage()


def startTournament():
    global g_tournament
    g_tournament = pairing(players)
    broadcast(f"The tournament matches is as follows\n{g_tournament}")
    for p in g_tournament:
        playMatch(p)

def nextStage():
    global g_tournament
    # Check the winners and remove the losers from `players`
    players = {k:p for k,p in players if p['isWinner']}

    # Check if there is already a winner
    if len(players) == 1:
        key = 0
        winner = 0
        for k,p in players:
            key = k
            winner = p
        broadcast(f"There is a winner! {key}")
        return

    # Announce the next round
    broadcast("The next round is about to start")
    g_tournament = pairing(players)
    broadcast(f"The tournament matches is as follows\n{g_tournament}")
    for p in g_tournament:
        playMatch(p)

bot.polling()

