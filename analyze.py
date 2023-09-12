import pandas as pd
import os
from collections import OrderedDict
from operator import itemgetter
import matplotlib.pyplot as plt
# 32 55 
# Global Variables
DIRECTORY = 'Data'
# ID = "qDZ5ZjSJhA"
# ID = "ozOkFpF87B"
GAME = 81

# ID = "TgbSpva4XT"
# ID = "uJWif_ztls"
# ID = "GpC57e4WHZ"
# ID = "ndZEZ_Th56"
# ID = "s6C0Cpa0sF"
# ID = "y3uC60nHKu"
# ID = "oZJEYxAYTU"
ID = "1WkcOL0Fmx"
# TgbSpva4XT, uJWif_ztls, GpC57e4WHZ, ndZEZ_Th56, s6C0Cpa0sF, y3uC60nHKu, oZJEYxAYTU,1WkcOL0Fmx
# ID = "DO5_qBKPEw"
# ID = "d7EkWI8o2P"
# ID = "JuUMMU8wiU"
# ID = "Q-SW0Q6z3s"
# ID = "Tpn_Cnr1gy"
# ID = "SCoB5LKYVh"
PLAYER_ID = {}
# qDZ5ZjSJhA - David
# ozOkFpF87B - Andrew
# DO5_qBKPEw - Nehamiah
# JuUMMU8wiU - Mega
# Tpn_Cnr1gy - Adi
# SCoB5LKYVh - Isaac
HANDS = []

''' 
For all methods:
shortstacked = true, will remove all hands where you have more than 50bb
noshortstacked = true, will remove all hands where you have less than 50bb
deepstacked = true, will remove all hands where you have less than 250bb
nodeepstacked = true, will remove all hands where you have more than 250bb
(Default false, if all set to false it will look at all hands)

players = n, will remove all hands where there were less than n players
position = [0 - SB, 1 - BB, 2 - UTG, 3 - HiJack, 4 - Cutoff, 5 - Button], will return your stat for that position the positions listed in your list.
pocket_pair = true, will only look at the stat for when you had pocket pairs
top_range = true, will only look at the stat for TT+
meme = true, will only look at the stat for 27o, 2to, 69o, 23o, j4o
suited_connecter = true, will only look at the stat for suited connectors
'''
def prep_helper(shortstacked = False, noshortstacked = False, deepstacked = False, nodeepstacked = False, players = 2, position = [], hand = None):
    seats = []
    exit_hand = False
    for player in hand['players']:
        seats.append(player['seat'])
    button_seat = hand['dealerSeat']
    sb_seat,bb_seat,utg_seat,co_seat = 0,0,0,0
    if button_seat in seats:
        sb_seat = seats[(seats.index(button_seat) + 1) % len(seats)]
        bb_seat = seats[(seats.index(button_seat) + 2) % len(seats)]
        utg_seat = seats[(seats.index(button_seat) + 3) % len(seats)]
        co_seat = seats[(seats.index(button_seat) - 1) % len(seats)]
    for player in hand['players']:
        if player['id'] == ID:
            if shortstacked and player['stack'] >= 50 * hand['bigBlind']:
                exit_hand = True
            if noshortstacked and player['stack'] <= 50 * hand['bigBlind']:
                exit_hand = True
            if deepstacked and player['stack'] <= 250 * hand['bigBlind']:
                exit_hand = True
            if nodeepstacked and player['stack'] >= 250 * hand['bigBlind']:
                exit_hand = True
            seat = player['seat']
            for pos in position:
                # Small blind
                if pos == 0:
                    exit_hand = exit_hand or seat == sb_seat
                # Big blind
                if pos == 1:
                    exit_hand = exit_hand or seat == bb_seat
                # UTG
                if pos == 2:
                    exit_hand = exit_hand or seat == utg_seat
                # Cutoff
                if pos == 4:
                    exit_hand = exit_hand or seat == co_seat
                # Button
                if pos == 5:
                    exit_hand = exit_hand or seat == button_seat
                exit_hand = not exit_hand
    return exit_hand

def find_seat(hand = None):
    for player in hand['players']:
        if player['id'] == ID:
            return player['seat']
    return -1

def print_params(shortstacked = False, noshortstacked = False, deepstacked = False, nodeepstacked = False, players = 2, position = []):
    if shortstacked:
        print("Short stacked", end = " ")
    if noshortstacked:
        print("Not short stacked", end = " ")
    if deepstacked:
        print("Deep stacked", end = " ")
    if nodeepstacked:
        print("Not deep stacked", end = " ")
    for pos in position:
        if pos == 0:
            print("SB", end = " ")
        # Big blind
        if pos == 1:
            print("BB", end = " ")
        # UTG
        if pos == 2:
            print("UTG", end = " ")
        # Cutoff
        if pos == 4:
            print("CO", end = " ")
        # Button
        if pos == 5:
            print("But", end = " ")

def vpip(shortstacked = False, noshortstacked = False, deepstacked = False, nodeepstacked = False, players = 2, position = []):
    vpip_count = 0
    eligible_hands = 0
    print_params(shortstacked=shortstacked, nodeepstacked=nodeepstacked, noshortstacked=noshortstacked, deepstacked=deepstacked, position = position)
    for hand in HANDS:
        # Gets te unique seats
        if prep_helper(shortstacked=shortstacked, nodeepstacked=nodeepstacked, noshortstacked=noshortstacked, deepstacked=deepstacked, position = position, hand = hand):
            continue
        eligible_hands += 1
        seat = find_seat(hand)
        for event in hand['events']:
            if (event['payload']['type'] == 9 and event['payload']['turn'] == 1) or event['payload']['type'] == 15:
                break
            if event['payload']['type'] == 14:
                continue
            if event['payload']['type'] == 11 and event['payload']['seat'] == seat:
                break
            if event['payload']['seat'] == seat and (event['payload']['type'] == 7 or event['payload']['type'] == 8):
                vpip_count += 1
                break
    if eligible_hands == 0:
        print("Not enough data")
        return
    print(f"You had {eligible_hands} eligible hands. You voluntarily put money into the pot {vpip_count} times. This means you have a VPIP of {100*vpip_count/eligible_hands:.2f}%")

def rfi(shortstacked = False, noshortstacked = False, deepstacked = False, nodeepstacked = False, players = 2, position = []):
    print_params(shortstacked=shortstacked, nodeepstacked=nodeepstacked, noshortstacked=noshortstacked, deepstacked=deepstacked, position = position)
    eligible_hands = 0
    rfi_count = 0
    rfi_amount = 0
    for hand in HANDS:
    # Gets te unique seats
        if prep_helper(shortstacked=shortstacked, nodeepstacked=nodeepstacked, noshortstacked=noshortstacked, deepstacked=deepstacked, position = position, hand = hand):
            continue
        eligible_hands += 1
        seat = find_seat(hand)
        for event in hand['events']:
            if (event['payload']['type'] == 9 and event['payload']['turn'] == 1) or event['payload']['type'] == 15:
                break
            if event['payload']['type'] == 14:
                continue
            if event['payload']['type'] == 11 and event['payload']['seat'] == seat:
                break
            if event['payload']['type'] == 8 and event['payload']['seat'] == seat:
                rfi_count += 1
                rfi_amount += (event['payload']['value'])/hand['bigBlind']
                break
    if eligible_hands == 0 or rfi_count == 0:
        print("Not enough data")
        return
    print(f"You had {eligible_hands} eligible hands. You raised preflop {rfi_count} times. This means you have a PFR of {100*rfi_count/eligible_hands:.2f}%. The average amount you raised with is {rfi_amount/rfi_count:.2f}BB")

def threebet():
    pass

def fourbet():
    pass

def allin():
    pass

# The amount of times your hand went to showdown
def showdown_percent():
    pass

def win_graph():
    pass

# How many times you bet on all 3 streets
def triple_barrel():
    pass


# Profit based on what your hand was
def hand_breakdown():
    pass

# Shows the biggest pots (win or lose) that you were part of where number_of_pots is the total number of pots you want displayed 
def biggest_pots(number_of_pots):
    pass

# Tells you how much you made based on the position you were from the big blind, only looks at games that have 5 or more people.
def profit_per_position(shortstacked = False, noshortstacked = False, deepstacked = False, nodeepstacked = False, players = 2, position = []):
    print_params(shortstacked=shortstacked, nodeepstacked=nodeepstacked, noshortstacked=noshortstacked, deepstacked=deepstacked, position = position)
    eligible_hands = 0
    profit = 0
    for hand in HANDS:
    # Gets te unique seats
        if prep_helper(shortstacked=shortstacked, nodeepstacked=nodeepstacked, noshortstacked=noshortstacked, deepstacked=deepstacked, position = position, hand = hand):
            continue
        eligible_hands += 1
        for player in hand['players']:
            if player['id'] == ID:
                try:
                    profit += player['netGain']
                except:
                    continue
    print(f"${profit/100:.2f}")


# The number of times you overbet and the percentage of the amount of times you won when you overbet
# Will also tell you the number of times you called an overbet and the amount of times you won when you called
def overbet_percent():
    pass


def total_profit():
    profit = 0
    graph = []
    for hand in HANDS:
        for player in hand['players']:
            if player['id'] == ID:
                try:
                    profit += int(player['netGain'])
                    graph.append(profit/100)
                except:
                    continue
    plt.plot(graph)
    plt.show()
    print(f"You are currently up/down: ${profit/100:.2f}. This means that you win on average ${(profit/100)/len(HANDS):.2f} per hand")

def unique_hands():
    # Generate the deck to compare to the hands that you've recieved
    suits = ['h', 'd', 'c', 's']
    number = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    cards = []

    All_Hands = set()
    for num in number:
        for suit in suits:
            cards.append(str(num) + str(suit))
    for card1 in cards:
        for card2 in cards:
            if card1 == card2:
                continue
            All_Hands.add((card1, card2))
    hands = set()
    for hand in HANDS:
        for player in hand['players']:
            if player['id'] == ID:
                try:
                    hands.add(tuple(player['hand']))
                except:
                    pass
    missing_hands = list(All_Hands.difference(hands))
    missing_hands.sort()
    print("Missing cards:")
    for hand in missing_hands:
        print(hand[0], hand[1])
    print(f"Out of {len(HANDS)} hands, you have not recieved {len(missing_hands)} as your hole cards as listed above!" )

def load_hands(test = False, game = None):
    if game != None:
        df = pd.read_json(DIRECTORY + "/" + str(game) + ".json")
        for hand in (df['hands']):
            if hand['gameType'] == "th":
                for player in hand['players']:
                    if player['id'] == ID:
                        HANDS.append(hand)
        return
    files = os.listdir(DIRECTORY)
    for file in files:
        if not file.endswith('.json'):
            files.remove(file)
    if test:
        files.sort(key = lambda x:int(x[:-5]))
    else:
        files.sort()
    for filename in files:
        if filename.endswith('.json'):
            df = pd.read_json(DIRECTORY + "/" + filename)
            for hand in (df['hands']):
                if hand['gameType'] == "th":
                    for player in hand['players']:
                        if player['id'] == ID:
                            HANDS.append(hand)
    
def unique_ids(test = False):
    files = os.listdir(DIRECTORY)
    for file in files:
        if not file.endswith('.json'):
            files.remove(file)
    if test:
        files.sort(key = lambda x:int(x[:-5]))
    else:
        files.sort()
    for filename in files:
        if filename.endswith('.json'):
            df = pd.read_json(DIRECTORY + "/" + filename)
            for hand in (df['hands']):
                if hand['gameType'] == "th":
                    for player in hand['players']:
                        if PLAYER_ID.get(player['id']) == None:
                            PLAYER_ID[player['id']] = set()
                            PLAYER_ID[player['id']].add(player['name'])
                        else:
                            PLAYER_ID[player['id']].add(player['name'])

# Gets the names that people have used
def name_count():
    IDS_sorted = sorted(PLAYER_ID, key = lambda x:len(PLAYER_ID[x]))
    for i in IDS_sorted:
        print(i, len(PLAYER_ID[i]), PLAYER_ID[i])
        print()

def main():
    # load_hands(game = GAME)
    load_hands()
    # total_profit()
    # unique_hands()
    vpip(deepstacked=True)
    vpip(shortstacked=True)
    vpip(position = [0])
    vpip(position = [1])
    vpip(position = [2])
    vpip(position = [4])
    vpip(position = [5])
    vpip()
    print()
    rfi(deepstacked=True)
    rfi(shortstacked=True)
    rfi(position = [0])
    rfi(position = [1])
    rfi(position = [2])
    rfi(position = [4])
    rfi(position = [5])
    rfi()
    # profit_per_position(deepstacked=True)
    # profit_per_position(shortstacked=True)
    # profit_per_position(position = [0])
    # profit_per_position(position = [1])
    # profit_per_position(position = [2])
    # profit_per_position(position = [4])
    # profit_per_position(position = [5])
    # profit_per_position()

if __name__ == "__main__":
    main()