import random


class Card():

    def __init__(self, suit=None, rank=None):
        self.suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        self.ranks = ['', '', '2', '3', '4', '5', '6', '7', '8', '9', '10',
             'Jack', 'Queen', 'King', 'Ace']

        self.suit = suit
        self.rank = rank

    def printCard(self):
        print(self.ranks[self.rank] + ' of ' + self.suits[self.suit])

    def __str__(self):
        return(self.ranks[self.rank] + ' of ' + self.suits[self.suit])

    def __lt__(self, other):
        """For card comparison"""
        return self.rank < other.rank


class Deck():

    def __init__(self):
        self.cards = [Card(i, j) for i in range(4) for j in range(2, 15)]

    def printDeck(self):
        for i in range(len(self.cards)):
            print(str(i + 1) + ") " + str(self.cards[i]))

    def shuffle(self):
        random.shuffle(self.cards)

    def sort(self):
        self.cards = sorted(self.cards)

    def pop(self, index=0):
        return self.cards.pop(index)

    def remove(self, index=0):
        self.cards.pop(index)

    def pop_n(self, n, start=0):
        res = []
        for i in range(n):
            res.append(self.cards.pop(start + n))
        return res

    def add(self, card):
        self.cards.append(card)

    def move(self, target, index=0):
        target.add(self.pop(index))

    def move_n(self, target, n, start=0):
        cards = self.pop_n(n, start)
        for i in range(n):
            target.add(cards[i])

    def contains(self, rank):
        for i in range(len(self.cards)):
            if rank == self.cards[i].rank:
                return True
        return False

    def indexOf(self, rank):
        for i in range(len(self.cards)):
            print(self.cards[i].rank, rank)
            if self.ranks[self.cards[i].rank] == rank:
                return i

    def rank_count(self, rank):
        count = 0
        for card in self.cards:
            if card.rank == rank:
                count += 1
        return count

    def remove_pair(self, rank):
        for i in range(2):
            for j in range(len(self.cards)):
                if self.cards[j].rank == rank:
                    self.remove(j)
                    break

    def remove_pairs(self):
        for card in self.cards:
            if self.rank_count(card.rank) > 1:
                self.remove_pair(card.rank)


class Hand(Deck):

    def __init__(self):
        self.suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        self.ranks = ['', '', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  'Jack', 'Queen', 'King', 'Ace']
        self.cards = []


class Player():

    def __init__(self, name):
        self.hand = Hand()
        self.name = name
        self.score = 0

    def has(self, rank):
        return self.hand.contains(rank)

    def __str__(self):
        return self.name


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

        k = int(input("%s, which player do you want to ask? "
                      % (player.name))) - 1

        if self.players[k] == player:
            print("You can't pick yourself!")
            return self.ask(player)

        if k > len(self.players):
            print("Please enter a number in the correct range")
            return self.ask(player)

        print('')
        for i in range(2, len(self.ranks)):
            print(str(i) + ") " + str(self.ranks[i]))
        print('')

        rank = int(input("What card do you want to ask %s for? "
                         % (self.players[k].name)))
        return self.players[k].has(rank), self.players[k], self.ranks[rank]

    def turn(self, player):

        for person in self.players:
            if len(person.hand.cards) == 0:
                return self.endgame()

        if (len(self.deck.cards) == 0):
            return self.endgame()

        input("Press enter to begin your turn, %s... " % (player.name))
        print('\nYour hand:')
        player.hand.printDeck()
        print('\n')
        #Check to see if player guesses correctly
        correct, next_player, rank = self.ask(player)

        #If they did, they go again
        if correct:
            print("\n%s had a %s!\n " % (str(next_player), rank))
            player.score += 1
            print("%s's current score: %s" % (player.name, player.score))
            next_player.hand.move(player.hand, player.hand.indexOf(rank))
            player.hand.remove_pairs()
            if len(player.hand.cards):
                return self.turn(player)

        #Otherwise, the player they asked gets to go
        else:
            print("\n%s didn't have a %s.\n " % (str(next_player), rank))
            game.deck.move(player.hand)
            return self.turn(next_player)

    def endgame(self):
        scores = []
        for player in self.players:
            scores.append((player.score, player.name))
        scores.sort(reverse=True)
        print("%s wins with %s points" % (scores[0][1], str(scores[0][0])))
        print("\n Scoreboard: \n")
        for score, player in scores:
            print(player + ": " + score)

if __name__ == '__main__':
    game = GoFish(['Madison', 'Ben', 'Cullen'])
    for player in game.players:
        print(player.name)
        player.hand.printDeck()
    player = random.choice(game.players)
    game.turn(player)
