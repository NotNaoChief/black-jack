"""
Black Jack

- 1 player
- 1 AI dealer
- 1 Deck
- Bankroll for betting.

- The goal is to get 21 or be closer to the dealer to 21.

-- Starting
- Player places bet.
- Player starts 2 cards face up.
- Dealer starts 1 card face up, 1 card face down.
- Player goes first.

-- Turn Options
- 'Hit', receive another card.
- 'Stay', stop receiving cards.
- **For ease of programming, don't worry about 'Insurance', 'Split', or
    'Double Down'**

-- On Dealers Turn
- If player is under 21, dealer must hit until they either:
    1. beat the player, or
    2. bust.

-- Ways for hand to end. **Alert Player of all instances.**
- 1. Player goes over 21. Player Busts! Dealer Wins!
- 2. Dealers total > player total & Dealer total <= 21. Dealer wins!
- 3. Dealer Busts! Player Wins!

-- Special Rules
- Face Cards = 10
- Aces = 1 or 11, whichever is preferable to the player.


"""
import random
import time

playing = True


# A way to clear the screen
def clear_screen():

    try:

        from IPython import get_ipython

        ip = get_ipython()

        if ip is None:

            raise ImportError

        else:

            from IPython.display import clear_output as clear

            clear()

    except ImportError:

        from os import name, system

        # for windows
        if name == 'nt':

            _ = system('cls')

        # for mac and linux('posix')
        else:

            _ = system('clear')


class Card():
    """A playing card."""
    def __init__(self, rank: str, value: int, suit: str):
        self.rank = rank
        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck():
    """52 playing cards, no jokers."""
    def __init__(self):
        self.ranks = (
            'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
            'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace'
        )
        self.values = (
            2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11
        )
        self.suits = (
            'Hearts', 'Diamonds', 'Clubs', 'Spades'
        )

        # Hold all cards.
        self.all_cards = []

        # Build Deck
        for suit in self.suits:
            for idx, value in enumerate(self.values):
                new_card = Card(self.ranks[idx], value, suit)
                self.all_cards.append(new_card)

    def shuffle_deck(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()


class Player():
    def __init__(self):
        self.name = 'Player'
        self.bank = 100
        self.all_cards = []
        self.card_total = 0
        self.aces = 0
        self.bet_amount = 0

    def add_card(self, new_card):
        self.all_cards.append(new_card)
        self.card_total += new_card.value
        if new_card.rank == 'Ace':
            self.aces += 1
        if self.card_total > 21 and self.aces:
            self.card_total -= 10
            self.aces -= 1

    def clear_hand(self):
        self.all_cards = []
        self.card_total = 0

    def bet(self):
        msg = (
            'How much would you like to bet?\n'
            f'You currently have {self.bank} chips.: '
        )
        while True:
            self.bet_amount = input(msg)
            if self.bet_amount.isnumeric():
                # Convert to integer.
                self.bet_amount = int(self.bet_amount)
                if self.bet_amount > 0 and self.bet_amount <= self.bank:
                    # Balance out bank.
                    self.bank -= self.bet_amount
                    return

    def win(self):
        self.bank += (self.bet_amount * 2)

    def __str__(self):
        return f"{self.name} has {self.bank} chips!"


class Dealer():
    def __init__(self):
        self.all_cards = []
        self.name = 'Dealer'
        self.card_total = 0

    def add_card(self, new_card):
        self.all_cards.append(new_card)
        self.card_total += new_card.value

    def clear_hand(self):
        self.all_cards = []
        self.card_total = 0


def show_cards(who: str):
    cards_to_show = []
    for i in who.all_cards:
        cards_to_show.append(f"{i.__str__()}")
    return ', '.join(cards_to_show)


def setup():
    # Initialize & shuffle deck.
    deck = Deck()
    deck.shuffle_deck()

    # Initialize player and dealer.
    player = Player()
    dealer = Dealer()

    return (deck, player, dealer)


deck, player, dealer = setup()


def start():
    # Greet player.
    print("Welcome to BlackJack!")
    time.sleep(2)

    # Player places bet, bet amount is announced.
    player.bet()
    print(
        f"Player has bet {player.bet_amount} chips!"
    )
    time.sleep(1)

    # Simulate dealing time.
    print('Dealing...')
    time.sleep(2)

    for i in range(2):
        player.add_card(deck.deal_one())
        dealer.add_card(deck.deal_one())

    dealer_shown = dealer.all_cards[1]
    player_shown = show_cards(player)

    # Announce 1 card for dealer, and both cards for player.
    print(
        f"Dealer: One card down with {dealer_shown} showing."
    )
    time.sleep(1)
    print(
        f"Player: {player_shown} showing."
    )


def rounds():
    while True:
        answer = input("Press '1' to hit, '2' to stay: ")
        if answer == '1':
            player.add_card(deck.deal_one())
            print(show_cards(player))
        elif answer == '2':
            break
        if player.card_total > 21:
            print("Player busts! Dealer Wins!")
            return

    print(f"{show_cards(dealer)}")
    print(dealer.card_total)
    while dealer.card_total <= 17:

        dealer.add_card(deck.deal_one())
        print("Dealer hits.")
        time.sleep(1)
        print(f"{show_cards(dealer)}")
        if dealer.card_total > 21:
            print('Dealer busts! Player Wins!')
            player.win()
            return
        elif dealer.card_total == 21:
            print("BlackJack! Dealer Wins!")
            return

    if player.card_total > dealer.card_total:
        print("Player Wins!")
        player.win()
        return
    elif player.card_total == dealer.card_total:
        print("Dealer Wins")
        return
    else:
        print("Dealer Wins!")
        return


while playing is True:
    clear_screen()
    start()
    rounds()
    if player.bank == 0:
        print("Game Over, out of chips!")
        playing = False
        break
    while True:
        answer = input("Continue Playing? (y)es or (n)o: ")
        if answer in ['Y', 'y']:
            player.clear_hand()
            dealer.clear_hand()
            print("\n\n")
            break
        elif answer in ['N', 'n']:
            playing = False
            break
