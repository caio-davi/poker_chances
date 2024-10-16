import random
from sys import exit
from typing import List

N_SIMULATIONS = 1000

class Card:
    def __init__(self, suit: str, number: int):
        self.suit = suit
        self.number = number
    
    def same(self, other):
        return self.suit == other.suit and self.number == other.number

    def __repr__(self):
        return f"{self.number}{self.suit}"

class Deck:
    def __init__(self):
        self.cards = self.generate_deck()
    
    def generate_deck(self):
        suits = ['H', 'D', 'C', 'S']
        numbers = list(range(2, 15))  # 2-10, J=11, Q=12, K=13, A=14
        return [Card(suit, number) for suit in suits for number in numbers]
    
    def remove_cards(self, cards_to_remove):
        self.cards = [card for card in self.cards if not any(card.same(c) for c in cards_to_remove)]

    def shuffle(self):
        random.shuffle(self.cards)

def reverse_dict(dictionary):
    reverse = {} 
    for k, v in dictionary.items():
        if v not in reverse:
            reverse[v] = 1
        else:
            reverse[v] = reverse[v] + 1
    return reverse

def poker_chances(on_table: List[Card], player_hand: List[Card], other_players: List[List[Card]]) -> int:

    def fill_cards(deck, cards, total_cards):
        deck.remove_cards(cards)
        remaining_table_cards = total_cards - len(cards)
        return cards + deck.cards[:remaining_table_cards], deck.cards[remaining_table_cards:]

    def simulate_game(on_table, player_hand, other_players):
        deck = Deck()
        deck.shuffle()
        table_cards, deck.cards = fill_cards(deck, on_table, 5)
        player_hand, deck.cards = fill_cards(deck, player_hand, 3)
        other_players_hand = []
        for hand in other_players:
            other_players_cards, _ = fill_cards(deck, hand, 3)
            other_players_hand.append(other_players_cards)

        player_best_hand = evaluate_hand(player_hand + table_cards)
        other_best_hands = [evaluate_hand(hand + table_cards) for hand in other_players_hand]

        return player_best_hand > max(other_best_hands)
    
    # Return a dict with:
    # reverse=True: the amount (key) of of pairs (value), three (value), fours (value)...
    # reverse=False: return the number of cards (value) for each number (key)
    def count_same_numbers(cards, reverse=True):
        numbers = [card.number for card in cards]
        numbers_dict = {number: numbers.count(number) for number in numbers}
        if (reverse):
            return reverse_dict(numbers_dict)
        return numbers_dict
    
    def evaluate_hand(cards):
        same_numbers_count = count_same_numbers(cards)
        if is_royal_flush(cards):
            return 900
        elif is_straight_flush(cards):
            return 800
        elif is_four_of_a_kind(same_numbers_count):
            return 700
        elif is_full_house(same_numbers_count):
            return 600
        elif is_flush(cards):
            return 500
        elif is_straight(cards):
            return 400  
        elif is_three_of_a_kind(same_numbers_count):
            return 300
        elif is_two_pair(same_numbers_count):
            return 200
        elif is_pair(same_numbers_count):
            return 100
        else:   
            return max(card.number for card in cards)
    
    def is_royal_flush(cards):
        royal_flush_numbers = {10, 11, 12, 13, 14}  # 10, J, Q, K, A
        suits = {}
        for card in cards:
            if card.suit not in suits:
                suits[card.suit] = []
            suits[card.suit].append(card.number)
        for suit, numbers in suits.items():
            if royal_flush_numbers.issubset(set(numbers)):
                return True
        return False

    def is_straight_flush(cards):
        return is_flush(cards) and is_straight(cards)   

    def is_flush(cards):
        suits = [card.suit for card in cards]
        suits_cout = list({suit: suits.count(suit) for suit in suits}.values())
        return any(num >= 5 for num in suits_cout)
    
    def is_straight(cards: List[Card]) -> bool:
        numbers = [card.number for card in cards]
        numbers = sorted(set(numbers))
        for i in range(len(numbers) - 4):
            if numbers[i + 4] == numbers[i] + 4:
                return True
        # Special case for Ace-low straight (A, 2, 3, 4, 5)
        if set([14, 2, 3, 4, 5]).issubset(numbers):
            return True
        return False

    def is_four_of_a_kind(same_numbers_count):
        return 4 in same_numbers_count

    def is_full_house(same_numbers_count):
        return 2 in same_numbers_count and 3 in same_numbers_count   
    
    def is_three_of_a_kind(same_numbers_count):
        return 3 in same_numbers_count

    def is_two_pair(same_numbers_count):    
        return 2 in same_numbers_count and same_numbers_count[2] == 2

    def is_pair(same_numbers_count):
        return 2 in same_numbers_count

    wins = 0
    for _ in range(N_SIMULATIONS):
        if simulate_game(on_table, player_hand, other_players):
            wins += 1

    chances = (wins / N_SIMULATIONS) * 100
    return chances

# Example usage
on_table = [Card('D', 12)]
player_hand = [Card('D', 11), Card('D', 10)]
other_players = [[Card('S', 2), Card('S', 3)], [Card('H', 14), Card('H', 13)]]

print("Setting:")
print(f"On table: {on_table}")
print(f"Player hand: {player_hand}")
print(f"Other players: {other_players}")
print("======================================")

print(f"Chances: {poker_chances(on_table, player_hand, other_players)}%")