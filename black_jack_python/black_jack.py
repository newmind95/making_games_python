import random, sys

HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)
BACKSIDE = 'backside'


def main():
    print('''Blackjack, by Kristiyan Penev

    Rules:
        Try to get as close to 21 without going over.
        Kings, Queens, and Jacks are worth 10 points.
        Aces are worth 1 or 11 points.
        Cards 2 trough 10 are worth their face value.
        (H)it to take another card.
        (S)tand to stop taking cards.
        On your first play, you can (D)ouble down to increase your bet
        but must hit exactly one more time before standing.
        In case of a tie, the bet is terurnet to the player.
        The dealer stops hitting at 17.''')

    money = 5000
    while True:
        if money <= 0:
            print('You are boke!')
            print('Good think you were not playing with real money.')
            print('Thanks for playing!')
            sys.exit()

        # Let the player enter their bet for this round:
        print(f'Money: {money}')
        bet = get_bet(money)

        # Give the dealer and player two cards from the deck each:
        deck = get_deck()
        dealer_hand = [deck.pop(), deck.pop()]
        player_hand = [deck.pop(), deck.pop()]

        # Handle player actions:
        print(f'Bet: {bet}')
        while True:         # Keep looping until player stands or busts.
            display_hands(player_hand, dealer_hand, False)
            print()

            # Check if the player has bust:
            if get_handle_value(player_hand) > 21:
                break

            # Get the player's move, either H, S, or D:
            move = get_move(player_hand, money - bet)

            # Handle the player actions:
            if move == 'D':
                # Player is doubling down, they can increase their bet:
                additional_bet = get_bet(min(bet, (money-bet)))
                bet += additional_bet
                print(f'Bet increased to {bet}.')
                print(f'Bet: {bet}')

            if move in ('H', 'D'):
                new_card = deck.pop()
                rank, suit = new_card
                print(f'You drew a {rank} of {suit}.')
                player_hand.append(new_card)

                if get_handle_value(player_hand) > 21:
                    # The player has busted:
                    continue

            if move in ('S', 'D'):
                # Stand/doubling down stops the player's trun.
                break

        # Handle the dealer's actions:
        if get_handle_value(player_hand) <= 21:
            while get_handle_value(dealer_hand) < 17:
                # The dealer hits:
                print('Dealer hits...')
                dealer_hand.append(deck.pop())
                display_hands(player_hand, dealer_hand, False)

                if get_handle_value(dealer_hand) > 21:
                    break

                input('Press Enter to continue...')
                print('\n\n')

        # Show the final hands:
        display_hands(player_hand, dealer_hand, True)
        player_value = get_handle_value(player_hand)
        dealer_value = get_handle_value(dealer_hand)
        # Handle whether the player won, lost, or tied:
        if dealer_value > 21:
            print(f'Dealer busts! You win ${bet}')
            money += bet

        elif (player_value > 21) or (player_value < dealer_value):
            print('You lost!')
            money -= bet

        elif player_value > dealer_value:
            print(f'You won ${bet}!')

        elif player_value == dealer_value:
            print('It\'s a tie, the bet is returned to you.')

        input('Press Enter to continue...')
        print('\n\n')


def get_bet(max_bet):
    """ Ask the player how much they want to bet for this round."""

    while True:
        print(f'How much do you bet? (1-{max_bet}, or QUIT)')
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if not bet.isdecimal():
            continue

        bet = int(bet)
        if 1 <= bet <= max_bet:
            return bet


def get_deck():
    """ Return a list of (rank, suit) tuples for all 52 cards."""

    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))

            for rank in ('J', 'Q', 'K', 'A'):
                deck.append((rank, suit))       # Add the face and ace cards.

    random.shuffle(deck)
    return deck


def display_hands(player_hand, dealer_hand, show_dealer_hand):
    """ Show the player's and dealer's crds. Hide the dealer's first
    card if show_dealer_hand is False."""
    print()

    if show_dealer_hand:
        print(f'DEALER: {get_handle_value(dealer_hand)}')
        display_cards(dealer_hand)
    else:
        print('DEALER: ???')
        # Hide the dealer's firs card:
        display_cards([BACKSIDE] + dealer_hand[1:])

    # Show the player's cards:
    print(f'PLAYER: {get_handle_value(player_hand)}')
    display_cards(player_hand)


def get_handle_value(cards):
    """ Returns the value of the cards. Face cards are worth 10, ace are
    worth 11 or 1 (this functions picks the most suitable ace value)."""
    value = 0
    number_of_aces = 0

    # Add the value for the non-ace cards:
    for card in cards:
        rank = card[0]
        if rank == 'A':
            number_of_aces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)      # Numbered cards are worth their number.

    # Add the value for the aces:
    value += number_of_aces     # Add 1 per ace.
    for index in range(number_of_aces):
        # If another 10 can be added with busting, do so:
        if value + 10 <= 21:
            value += 10

    return value


def display_cards(cards):
    """ Display all the cards in the cards list."""
    rows = ['', '', '', '', '']     # The nex to display on each row.

    for i, card in enumerate(cards):
        rows[0] += ' ___  '

        if card == BACKSIDE:
            # Print a card's back:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            # Print the card's font:
            rank, suit = card
            rows[1] += f'|{rank.ljust(2)} | '
            rows[2] += f'| {suit} | '
            rows[3] += f'|_{rank.rjust(2, "_")}| '

    # Print each row on the screen:
    for row in rows:
        print(row)


def get_move(player_hand, money):
    """Asks the player for their move, and returns 'H' for hit, 'S' for
    stand, and 'D' for double down."""
    while True:
        # Determine what moves the player can make:
        moves = ['(H)it', '(S)tand']

        # The player can double down on their first move, which we can
        # tell because they'll have exactly two cards:
        if len(player_hand) == 2 and money > 0:
            moves.append('(D)ouble down')

        # Get the player's move:
        move_prompt = ', '.join(moves) + '> '
        move = input(move_prompt).upper()
        if move in ('H', 'S'):
            return move     # Player has entered a valid move.

        if move == 'D' and '(D)ouble down' in moves:
            return move     # Player has entered a valid move.
    

# If the program is run (insead of imported), run the game:
if __name__ == '__main__':
    main()
