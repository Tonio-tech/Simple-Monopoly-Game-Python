"""
File:    pyopoly.py
Author:  Toni Olafunmiloye
Date:    10/31/20
Section: 41
E-mail:  oolafun1@umbc.edu
Description: This file is a simplified version of monopoly.
"""

from sys import argv
from random import randint, seed
from board_methods import load_map, display_board

P1 = 0
P2 = 1
PASS_GO_MONEY = 200
STARTING_MONEY = 1500
# there is a bug in this, not sure what the problem is, i tried or and i tried and
BUY_PROPERTY = ["1",  "buy property"]
GET_PROPERTY_INFO = ["2", "get property info"]
YES = 'yes'
GET_PLAYER_INFO = ["3", "get player info"]
BUILD_BUILDING = ["4", "build a building"]
END_TURN = ["5", "end turn"]
BANKRUPTCY = 0
# NO_BUILDING = "no"
BANK = "BANK"



def play_game(starting_money, pass_go_money, board_file):
    """x
    :param starting_money: The money each player starts with, 1500
    :param pass_go_money: 200 every time the player passes go
    :param board_file: any file the user imports
    :return: nothing
    """
    # so switching turns should be taking place in play_game, essentially a condition like
    # while player_not_bankrupt: take_turn for player 1, take_turn for player2
    # and take_should take care of what the player wants to do until they choose to end their turn
    # and then play_game keeps looping until someone has lost

    # if player position greater than 0, += pass_go_money
    # If a player passes the start position (0) then they get the pass-go amount of money,
    # 200 by default, but this should be a constant so that it can be modified for testing.

    players = get_players()
    board = load_map(board_file)
    formatted_board = format_display(players, board)
    display_board(formatted_board)

    # had to make OWNER: BANK, and also had to create key for building so that it may be changed
    for i in range(len(board)):
        board[i]["Building"] = False
        board[i]["Owner"] = BANK

    player = P1
    # basically while the player enough money, keep the game going with the take turn function
    while players[P1]["Current Money"] > BANKRUPTCY and players[P2]["Current Money"] > BANKRUPTCY:
        take_turn(player, players, board)

        if players[P1]["Current Money"] > BANKRUPTCY:
            take_turn(P2, players, board)

    # bankruptcy, when the players have no more money left
    if players[P1]["Current Money"] < BANKRUPTCY:
        print(players[P1]["Player Name"], "has lost.", players[P2]["Player Name"], "you win!")

    if players[P2]["Current Money"] < BANKRUPTCY:
        print(players[P1]["Player Name"], "has won.", players[P2]["Player Name"], "has lost")

    # well you should call play_game with argv
    # but you can leave the parameters in the function as board_file
    # i'm not sure if that would make a difference i haven't worked much with argc
    # but yeah inside of your main I would call the function like this
    # play_game(START_FUNDS, PASS_GO_FUNDS, argv[2])
    # then in the play game function have this: def play_game(starting_money, pass_go_money, board_file):

    # "The general format is:
    # python3 pyopoly.pyc <seed string> <board csv file>
    # You can use any seed value as long as it's a string without spaces.  "
    # argv[1] would be seed, and argv[2] would be file_name

    # Within your main, you should call this function with the constants at the top of the program,
    # and the file name for the map.
    # For testing, you can always make the map-file an input statement.


def take_turn(player, players, board):
    """
    :param player: the current player
    :param players: a list of info about each player
    :param board: the board in which the player move on
    :return:
    """
    # players = [first_player_info, second_player_info]
    YES = 'yes'
    roll = randint(1, 6) + randint(1, 6)
    START_POSITION = 0

    if players[player]["Player position"] < len(board):
        players[player]["Player position"] += roll

    # player passes go
    # display map that shows the players positions
    # display it to the user as well with how far they've traveled + position

    # when the player position is greater than the lenght of the board, its need mod bc of index error
    if players[player]["Player position"] >= len(board):
        players[player]["Player position"] %= len(board)
        # they get 200 when they pass the go
        players[player]["Current Money"] += PASS_GO_MONEY

    display_board((format_display(players, board)))  # updated board showing the movement of players after each roll
    print(players[player]["Player Name"], "rolled a", roll)
    print(players[player]["Player Name"], "landed on", board[players[player]["Player position"]]["Place"])


    # this is for paying rent
    if player == P1:
        # if the player landed on a building
        if board[players[player]["Player position"]]["Building"] == True:
            # if the place is owned by the other player
            if board[players[player]["Player position"]]["Place"] in players[P2]["Properties Owned"]:
                # then subtract building rent from their current money
                players[player]["Current Money"] -= int(board[players[player]["Player position"]]["BuildingRent"])
                # and add the building rent to the money of the player who owns the building
                players[P2]["Current Money"] += int(board[players[player]["Player position"]]["BuildingRent"])
                print("You paid building rent")
        if board[players[player]["Player position"]]["Building"] == False:
            # if player 1 lands on a place owned by player 2, but its not a building
            if board[players[player]["Player position"]]["Place"] in players[P2]["Properties Owned"]:
                # then subtract the price of the place from the players current money
                players[player]["Current Money"] -= int(board[players[player]["Player position"]]["Rent"])
                players[P2]["Current Money"] += int(board[players[player]["Player position"]]["Rent"])
                print("You paid rent")

    if player == P2:
        if board[players[player]["Player position"]]["Building"] == True:
            # if the place is owned by the other player
            if board[players[player]["Player position"]]["Place"] in players[P1]["Properties Owned"]:
                players[player]["Current Money"] -= int(board[players[player]["Player position"]]["BuildingRent"])
                players[P1]["Current Money"] += int(board[players[player]["Player position"]]["BuildingRent"])
                # pay the building cost
                print("You paid building rent")
        if board[players[player]["Player position"]]["Building"] == False:
            if board[players[player]["Player position"]]["Place"] in players[P1]["Properties Owned"]:
                players[player]["Current Money"] -= int(board[players[player]["Player position"]]["Rent"])
                players[P1]["Current Money"] += int(board[players[player]["Player position"]]["Rent"])
                print("You paid rent")



    # this is the menu panel thing, displaying the options the player can shoose from
    print('\n 1) Buy Property \n', '2) Get Property Info \n', '3) Get Player Info \n', "4) Build a Building",
          "\n", '5) End Turn')
    print()
    # the player action will take the number or the name of the action
    player_action = input("What do you want to do? ")

    # as long as the player doesnt end their turn they can keep choosing things from the menu with player action
    while player_action not in END_TURN:
        get_user_input(player, players, board, player_action)
        print('\n 1) Buy Property \n', '2) Get Property Info \n', '3) Get Player Info \n', "4) Build a Building",
              "\n", '5) End Turn')
        print()
        player_action = input("What do you want to do? ")

    # if player action is end turn, is player one was playing, let player two play and vice versa


def get_user_input(player, players, board, player_action):
    """
    :param player:  current player
    :param players: info about players
    :param board: current board
    :param player_action: the player number that shows what action they want to take
    :return:
    """
    # if the inputted player action matched any of the constants, then go to the function
    if player_action in BUY_PROPERTY:
        buy_property(player, players, board)

    elif player_action in GET_PROPERTY_INFO:
        which_property = input("For which property do you want to get information from? ")
        get_property_info(which_property, board)

    elif player_action in GET_PLAYER_INFO:
        get_player_info(players)

    elif player_action in BUILD_BUILDING:
        build_a_building(players, player, board)


def build_a_building(players, player, board):
    """
    :param players: list of dictionary with info about players
    :param player: current player
    :param board: current board
    :return:
    """
    # look through the board and if the place is in the players properties, print out its info
    for i in range(len(board)):
        if board[i]["Place"] in players[player]["Properties Owned"]:
            print(board[i]["Place"], board[i]["Abbrev"], board[i]["BuildingCost"])

    which_property = input("Which property would you like to build a building on? (full name please) ")
    # look through thr board and if the inputted property is in the players properties
    for i in range(len(board)):
        # user can enter the abbreviations or the actual name
        if which_property == board[i]["Place"] or which_property == board[i]["Abbrev"]:
            # then check if the building is owned by the player
            if board[i]["Owner"] == players[player]["Player Name"]:
                # check if they have enough money
                if int(players[player]["Current Money"]) >= int(board[i]["BuildingCost"]):
                    # then check if the place already has a building, if not continue
                    if board[i]["Building"] == False:
                        players[player]["Current Money"] -= int(board[i]["BuildingCost"])
                        board[i]["Building"] = True
                        """if which_property in players[player]["Properties Owned"]:
                            players[player]["Properties Owned"].remove(which_property)"""
                        players[player]["Properties Owned"].append(which_property + " with a building")
                        print("You have built a building on", board[i]["Place"])

                    elif board[i]["Building"] == True:
                            print("This property already has a building")
                else:
                    print("You do not have enough money to build a building on this property")

            if which_property == board[i]["Place"]:
                if board[i]["Owner"] != players[player]["Player Name"]:
                    print("You are not the owner of this property and therefore cannot build a building")



def get_player_info(players):
    """
    :param players: list of dictionaries containing info about players
    :return:
    """
    # this will deplay the name or the players and the user will type in the name
    # if the name match the "Player Name" it'll print the info
    print("The players are: \n", players[P1]["Player Name"], players[P2]["Player Name"])
    which_player = input('Which player do you wish to know about? ')
    if which_player == players[P1]["Player Name"]:
        print(players[P1])
    if which_player == players[P2]["Player Name"]:
        print(players[P2])


def format_display(players, board):
    """
    :param players: list of dictionaries containing info about players
    :param board: board that will be displayed, showing characters and Abbrev of each place
    :return: 
    """
    # this is to print the abbreviations onto the board as places to land in
    abbreviations = []

    first_player_symbol = players[P1]["Player Symbol"]
    second_player_symbol = players[P2]["Player Symbol"]
    for i in range(len(board)):
        location = board[i]
        board_string = location["Abbrev"].ljust(5) + '\n'

        # this makes it so that when the player position (which is original 0)
        # it'll append the players into the list which will be displayed on the board
        if players[P1]["Player position"] == i and players[P2]["Player position"] == i:
            board_string += (first_player_symbol + second_player_symbol).ljust(5)
        elif players[P1]["Player position"] == i:
            board_string += first_player_symbol.ljust(5)
        elif players[P2]["Player position"] == i:
            board_string += (second_player_symbol.ljust(5))
        else:
            board_string += '     '

        abbreviations.append(board_string)

    return abbreviations


def get_property_info(which_property, board):
    """
    :param which_property: an inputted string showing which property the player would like to get info of 
    :param board: current board
    :return: 
    """
    # basically it'll search through the whole board looking for the place that matches
    # when it finds the match it'll print all the necessary info
    for i in range(len(board)):
        if board[i]["Place"] == which_property or board[i]["Abbrev"] == which_property:
            print(board[i]["Place"], "\n", "Price:", board[i]["Price"], "\n", "Owner:", board[i]["Owner"], "\n",
                  "Building:", board[i]["Building"], "\n", "Rent:", board[i]["Rent"], ",", board[i]["BuildingRent"],
                  "(with building)")


def buy_property(player, players, board):
    """
    :param player: current player
    :param players: list of dictionaries containing info about players
    :param board: current board
    :return: 
    """
    CAN_BUY = 0
    NO_BUY = -1
    # there a bug, it is allowing players to buy even when the property is already owned
    # if players[P1]["Properties Owned"] or players[P2]["Properties Owned"] != board[players[player]["Player position"]]["Place"]:
    if board[players[player]["Player position"]]["Place"] not in players[P1]["Properties Owned"] and \
            board[players[player]["Player position"]]["Place"] not in players[P2]["Properties Owned"]:

        want_to_buy = input("The property is unowned, would you like to buy it? (yes or no) ")

        if want_to_buy == YES:
            # if the price of the place the player landed on is greater than -1

            if int(board[players[player]["Player position"]]["Price"]) >= CAN_BUY:
                # if the player's money is greater than or equal to the price of the place they plan to buy

                if int(players[player]["Current Money"]) >= int(board[players[player]["Player position"]]["Price"]):
                    # then subtract the price from the player's money
                    players[player]["Current Money"] -= int(board[players[player]["Player position"]]["Price"])
                    # print(board[players[player]["Player position"]]["Place"])
                    # and then add the place to the dictionary of the player's owned properties
                    players[player]["Properties Owned"].append(board[players[player]["Player position"]]["Place"])
                    board[players[player]["Player position"]]["Owner"] = players[player]["Player Name"]
                    print("You have bought", board[players[player]["Player position"]]["Place"])

                # if the player's money is less than the property price, then they cannot buy it
                elif int(players[player]["Current Money"]) <= int(board[players[player]["Player position"]]["Price"]):
                    print("You do not have enough money to buy this property.")

            elif int(board[players[player]["Player position"]]["Price"]) == NO_BUY:
                print("This property cannot be bought")
        # if the player puts anything other than yes, then they have decided not to buy is
        else:
            print("You have decided not to buy this property")

    elif players[P1]["Properties Owned"] or players[P2]["Properties Owned"] == \
            board[players[player]["Player position"]]["Place"]:
        print("This property is already owned")


def get_players():
    START_POSITION = 0
    # first we gotta get some characters
    first_player = input('First Player, what is your name?: ')
    first_player_symbol = input('First Player, what is your symbol? (a capital letter): ')
    # this is to make sure the symbol is upper case
    while not first_player_symbol.isupper():
        first_player_symbol = input('First Player, what is your symbol? (a capital letter): ')

    second_player = input('Second Player, what is your name?: ')
    second_player_symbol = input('Second Player, what is your symbol? (a capital letter): ')
    while not second_player_symbol.isupper():
        second_player_symbol = input('Second Player, what is your symbol? (a capital letter): ')

    # this is too make sure that the player symbols are not the same
    while first_player_symbol == second_player_symbol:
        print("Please choose a different symbol than first player.")
        second_player_symbol = input('Second Player, what is your symbol? (a capital letter): ')

    # the player info is kept in a dictionary
    first_player_info = {"Player Name": first_player,
                         "Player Symbol": first_player_symbol,
                         "Current Money": STARTING_MONEY,
                         "Properties Owned": [],  # until they buy something
                         "Player position": START_POSITION}

    second_player_info = {"Player Name": second_player,
                          "Player Symbol": second_player_symbol,
                          "Current Money": STARTING_MONEY,
                          "Properties Owned": [],  # until they buy something
                          "Player position": START_POSITION}

    players = [first_player_info, second_player_info]

    return players


# python3 program_name seed file_name
# python3 pyopoly.pyc 12345 proj1_board1.csv


if len(argv) >= 2:
    seed(argv[1])

if __name__ == '__main__':
    play_game(PASS_GO_MONEY, STARTING_MONEY, argv[2])
    # play_game(starting_money, pass_go, argv[2]
    # board = load_map(argv[2])
