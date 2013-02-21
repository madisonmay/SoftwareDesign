import random


suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
ranks = ['', '', '2', '3', '4', '5', '6', '7', '8', '9', '10',
     'Jack', 'Queen', 'King', 'Ace']


"""Card Functions"""
def card(i, j):
    return {'rank': j, 'suit': i}

def printCard(card):
    print(ranks[card['rank']] + ' of ' + suits[card['suit']])

def strCard(card):
    return ranks[card['rank']] + ' of ' + suits[card['suit']]

def lt(c1, c2):
    """For card comparison"""
    return c1['rank'] < c2['rank']


"""Deck functions"""
def Deck():
    return[card(i, j) for i in range(4) for j in range(2, 15)]

def printDeck(deck):
    for i in range(len(deck)):
        print(str(i + 1) + ") " + strCard(deck[i]))

def shuffle(deck):
    random.shuffle(deck)

def sort(deck):
    deck.sort(key= lambda x: x['rank'])

def pop(deck, index=0):
    return deck.pop(index)

def remove(deck, index=0):
    deck.pop(index)

def pop_n(deck, n, start=0):
    res = []
    for i in range(n):
        res.append(pop(deck, start + n))
    return res

def add(deck, card):
    deck.append(card)

def move(deck, target, index=0):
    add(deck, pop(deck, index))

def move_n(deck, target, n, start=0):
    cards = pop_n(deck, n, start)
    for i in range(n):
        add(target, cards[i])

def contains(deck, rank):
    for i in range(len(deck)):
        if rank == deck[i]['rank']:
            return True
    return False

def indexOf(deck, rank):
    for i in range(len(deck)):
        if ranks[deck[i]['rank']] == rank:
            return i

def rank_count(deck, rank):
    count = 0
    for card in deck:
        if card['rank'] == rank:
            count += 1
    return count

def remove_pair(deck, rank):
    for i in range(2):
        for j in range(len(deck)):
            if deck[j]['rank'] == rank:
                remove(deck, j)
                break

def remove_pairs(deck):
    for card in deck:
        if rank_count(deck, card['rank']) > 1:
            remove_pair(deck, card['rank'])


'''Hand constructor'''
def hand():
    return []


'''Player functions'''
def player(name):
    return {'hand': hand(), 'name': name, 'score': 0}

def has(player, rank):
    return contains(player['hand'], rank)

def printPlayer(player):
    print(player['name'])

'''Game functions - Resume conversion to function implementation here'''

def game(players):
    """Prereq: players is a list of names"""
    deck = Deck()
    player_list = []
    shuffle(deck)
    for i in range(len(players)):
        player_x = player(players[i])
        player_list.append(player_x)
        move_n(deck, player_x['hand'], 2)
        sort(player_x['hand'])
        remove_pairs(player_x['hand'])
        if len(player_x['hand']) < 5:
            player_x['score'] += (5 - len(player_x['hand'])) // 2
    return {'deck': deck, 'players': player_list}

def ask(game, player):

    print('Players:')
    for i in range(len(game['players'])):
        print(str(i + 1) + ") " + game['players'][i]['name'])
    #input on following line requires an index
    print('')


    def user_query():
        try:
            k = int(input("%s, which player do you want to ask? "
                        % (player['name']))) - 1
            assert k >= 0
            return k

        except:
            print("Please enter a valid index")
            return user_query()

    k = user_query()

    if k >= len(game['players']):
        print("\nPlease enter a number in the correct range!\n")
        return ask(game, player)

    if game['players'][k] == player:
        print("\nYou can't pick yourself!\n")
        return ask(game, player)

    print('')
    for i in range(2, len(ranks)):
        print(str(i) + ") " + str(ranks[i]))
    print('')

    def rank_query():

        rank = int(input("What card do you want to ask %s for? "
                        % (game['players'][k]['name'])))
        try:
            assert rank >= 2
            return has(game['players'][k], rank), game['players'][k], ranks[rank]
        except:
            print("Please enter a valid index")
            return rank_query()


    return rank_query()

def turn(game, player):

    for person in game['players']:
        if len(person['hand']) == 0:
            return endgame(game)

    if (len(game['deck']) == 0):
        return endgame(game)

    input("Press enter to begin your turn, %s... " % (player['name']))
    print('\nYour hand:')
    printDeck(player['hand'])
    print('\n')
    #Check to see if player guesses correctly
    correct, next_player, rank = ask(game, player)

    #If they did, they go again
    if correct:
        print("\n"*75 + "%s had a %s!\n " % (str(next_player['name']), rank))
        player['score'] += 1
        print("%s's current score: %s\n" % (player['name'], player['score']))
        move(next_player['hand'], player['hand'], indexOf(next_player['hand'], rank))
        remove_pairs(player['hand'])
        if len(player['hand']) != 0:
            return turn(game, player)
        else:
            return endgame(game)

    #Otherwise, the player they asked gets to go
    else:
        print("\n"*75 + "\n%s didn't have that card. Go fish!\n" % (str(next_player['name'])))
        move(game['deck'], player['hand'])
        return turn(game, next_player)

def endgame(self):
    scores = []
    for player in game['players']:
        scores.append((player['score'], player['name']))
    scores.sort(reverse=True)
    print("%s wins with %s points" % (scores[0][1], str(scores[0][0])))
    print("\nScoreboard: \n")
    for score, player in scores:
        print(player + ": " + str(score))

if __name__ == '__main__':
    game = game(['Madison', 'Ben', 'Cullen', "Mac-I"])
    player = random.choice(game['players'])
    turn(game, player)
