import random


suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
ranks = ['', '', '2', '3', '4', '5', '6', '7', '8', '9', '10',
     'Jack', 'Queen', 'King', 'Ace']


"""Card Functions"""
def card(i, j):
    return {'rank': i, 'suit': j}

def printCard(card):
    print(ranks[card['rank']] + ' of ' + suits[card['suit']])

def lt(c1, c2):
    """For card comparison"""
    return c1['rank'] < c2['rank']


"""Deck functions"""
def deck():
    return[card(i, j) for i in range(4) for j in range(2, 15)]

def printDeck(deck):
    for i in range(len(deck)):
        print(str(i + 1) + ") " + str(deck[i]))

def shuffle(deck):
    random.shuffle(deck)

def sort(deck):
    deck.sort()

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
        if rank == deck[i][rank]:
            return True
    return False

def indexOf(deck, rank):
    for i in range(len(deck)):
        if ranks[deck[i][rank]] == rank:
            return i

def rank_count(deck, rank):
    count = 0
    for card in deck:
        if card[rank] == rank:
            count += 1
    return count

def remove_pair(deck, rank):
    for i in range(2):
        for j in range(len(deck)):
            if deck[j][rank] == rank:
                remove(deck, j)
                break

def remove_pairs(deck):
    for card in deck:
        if rank_count(deck, card[rank]) > 1:
            remove_pair(deck, card[rank])


'''Hand constructor'''
def hand():
    return []


'''Player functions'''
def player(name):
    return {'hand': Hand(), 'name': name, 'score': 0}

def has(player, rank):
    return contains(player['hand'], rank)

def printPlayer(player):
    print(player['name'])

'''Game functions - Resume conversion to function implementation here'''
class GoFish():

    def __init__(self, players):
        """Prereq: players is a list of names"""
        self.suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        self.ranks = ['', '', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  'Jack', 'Queen', 'King', 'Ace']
        self.deck = Deck()
        self.players = []
        self.deck.shuffle()
        for i in range(len(players)):
            player = Player(players[i])
            self.players.append(player)
            self.deck.move_n(player.hand, 5)
            player.hand.sort()
            player.hand.remove_pairs()
            if len(player.hand.cards) < 5:
                player.score += (5 - len(player.hand.cards)) / 2

    def ask(self, player):

        print('Players:')
        for i in range(len(self.players)):
            print(str(i + 1) + ") " + str(self.players[i]))
        #input on following line requires an index
        print('')


        def user_query():
            try:
                k = int(input("%s, which player do you want to ask? "
                            % (player.name))) - 1
                return k

            except:
                print("Please enter a valid index")
                return user_query()

        k = user_query()

        if k >= len(self.players):
            print("\nPlease enter a number in the correct range!\n")
            return self.ask(player)

        if self.players[k] == player:
            print("\nYou can't pick yourself!\n")
            return self.ask(player)

        print('')
        for i in range(2, len(self.ranks)):
            print(str(i) + ") " + str(self.ranks[i]))
        print('')

        def rank_query():

            rank = int(input("What card do you want to ask %s for? "
                            % (self.players[k].name)))
            try:
                return self.players[k].has(rank), self.players[k], self.ranks[rank]
            except:
                print("Please enter a valid index")
                return rank_query()


        return rank_query()

    def turn(self, player):

        for person in self.players:
            if len(person.hand.cards) == 0:
                return self.endgame()

        if (len(self.deck.cards) == 0):
            return self.endgame()

        input("Press enter to begin your turn, %s... " % (player.name))
        print('\nYour hand:')
        for person in self.players:
            print(person.name)
            person.hand.printDeck()
        print('\n')
        #Check to see if player guesses correctly
        correct, next_player, rank = self.ask(player)

        #If they did, they go again
        if correct:
            print("\n%s had a %s!\n " % (str(next_player), rank))
            player.score += 1
            print("%s's current score: %s\n" % (player.name, player.score))
            next_player.hand.move(player.hand, next_player.hand.indexOf(rank))
            player.hand.remove_pairs()
            if len(player.hand.cards) != 0:
                return self.turn(player)
            else:
                return self.endgame()

        #Otherwise, the player they asked gets to go
        else:
            print("\n%s didn't have that card. Go fish!\n" % (str(next_player)))
            game.deck.move(player.hand)
            return self.turn(next_player)

    def endgame(self):
        scores = []
        for player in self.players:
            scores.append((player.score, player.name))
        scores.sort(reverse=True)
        print("%s wins with %s points" % (scores[0][1], str(scores[0][0])))
        print("\nScoreboard: \n")
        for score, player in scores:
            print(player + ": " + str(score))

if __name__ == '__main__':
    game = GoFish(['Madison', 'Ben', 'Cullen'])
    player = random.choice(game.players)
    game.turn(player)
