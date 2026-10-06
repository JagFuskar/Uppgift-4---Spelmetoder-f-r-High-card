import random
from msvcrt import getwch
from bcolors import GREEN, RED, YELLOW, RESET

# Mappning för att kunna jämföra strängar ("J", "Q", "K", "A") med siffror
CARD_RANKS = {
    2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7,
    8: 8, 9: 9, 10: 10, "J": 11, "Q": 12, "K": 13, "A": 14
}


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.suit} {self.value}"

    def __repr__(self):
        return f"Card('{self.suit}', {self.value})"


class Deck:
    def __init__(self, cards=None):
        if cards is None:
            cards = []
        self.cards = cards

    def deal(self, num_cards):
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards left to deal")

        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]

        return dealt_cards

    def shuffle(self, times):
        for _ in range(times):
            random.shuffle(self.cards)

    @staticmethod
    def make_deck():
        cards = []
        suits = ["♠", "♥", "♣", "♦"]
        values = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]

        for suit in suits:
            for value in values:
                cards.append(Card(suit, value))

        return cards


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def take_cards(self, cards):
        self.hand.extend(cards)

    def play_card(self):
        return self.hand.pop()


def read_key():
    key = getwch()
    # Piltangenter och liknande skickar två tecken, det andra ska inte räknas
    if key == "\x00" or key == "\xe0":
        getwch()
        return ""
    return key.lower()


def card_type(card):
    # 2 till 7 är låga kort, 8 till äss är höga kort
    if CARD_RANKS[card.value] >= 8:
        return "högt"
    return "lågt"


def play_game():
    # 1. Skapa kortlek och spelare
    cards = Deck.make_deck()
    deck = Deck(cards)
    deck.shuffle(1)

    player1 = Player("Spelare 1")
    player2 = Player("Spelare 2")

    # 2. Dela ut 1 kort var
    player1.take_cards(deck.deal(1))
    player2.take_cards(deck.deal(1))

    # 3. Spela ut korten
    c1 = player1.play_card()
    c2 = player2.play_card()

    print(f"{player1.name} drog: {c1} ({card_type(c1)} kort)")
    print(f"{player2.name} drog: {c2} ({card_type(c2)} kort)")

    # 4. Hämta numeriskt värde och jämför
    v1 = CARD_RANKS[c1.value]
    v2 = CARD_RANKS[c2.value]

    if v1 > v2:
        print(f"{GREEN}{player1.name} vinner med högst kort!{RESET}")
    elif v2 > v1:
        print(f"{GREEN}{player2.name} vinner med högst kort!{RESET}")
    else:
        print(f"{YELLOW}Det blev oavgjort!{RESET}")


def guess_game():
    cards = Deck.make_deck()
    deck = Deck(cards)
    deck.shuffle(1)

    player = Player("Du")

    print("Gissa lågt (l) eller högt (h): ", end="", flush=True)
    choice = ""
    while choice != "l" and choice != "h":
        choice = read_key()
    print(choice)

    player.take_cards(deck.deal(1))
    card = player.play_card()
    print(f"Du drog: {card} ({card_type(card)} kort)")

    if choice == "l":
        guess = "lågt"
    else:
        guess = "högt"

    if guess == card_type(card):
        print(f"{GREEN}Du gissade rätt, du vinner!{RESET}")
    else:
        print(f"{RED}Du gissade fel, du förlorar!{RESET}")


def main():
    while True:
        print()
        print("1. Spelare mot spelare")
        print("2. Gissa lågt eller högt")
        print("q. Avsluta")
        print("Välj: ", end="", flush=True)
        choice = ""
        while choice not in ["1", "2", "q"]:
            choice = read_key()
        print(choice)

        if choice == "1":
            play_game()
        elif choice == "2":
            guess_game()
        else:
            print("Hej då!")
            break


if __name__ == "__main__":
    main()
