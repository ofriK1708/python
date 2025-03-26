import json
import sys

def get_round_winner(line):
    """
    input:a line of a round in the game
    return: winner name or tie according to the game rules
    """

    round_lst = line.split()
    player1_choice = round_lst[1]
    player2_choice = round_lst[3]

    rps_rules = {"paper": "rock", "scissors": "paper", "rock": "scissors"}

    if player1_choice == player2_choice:
        return None
    elif player1_choice == rps_rules[player2_choice]:
        return round_lst[2]
    else:
        return round_lst[0]

def game(results_filename):

    game_scores = dict()

    try:
        with open(results_filename, "r",encoding= 'utf8') as res_file:
            res_file.readline()
            num_of_winners = 0

            for line in res_file:
                winner_in_round = get_round_winner(line)
                if winner_in_round:
                    game_scores[winner_in_round] = game_scores.get(winner_in_round, 0) + 1

            if game_scores:
                winner_in_game = max(game_scores, key=game_scores.get)
                num_of_winners = sum(1 for score in game_scores.values() if score == game_scores[winner_in_game])

            if num_of_winners == 1:
                game_result = winner_in_game
            else:
                game_result = "tie"

    except Exception as e:
        sys.exit(f"An error has occurred: {e}")


    print(f'starting the game with {results_filename}')

    # todo: due to possible difference in file encodings between operating systems, you may need to add
    #  utf8 encoding type when opening a file, as an example: with open(<file name>, 'r', encoding='utf8') as fin
    #  python developers plan to make utf8 a default at 3.15 - https://peps.python.org/pep-0686/

    winner = game_result  # todo: assign player name or "tie"
    return winner


# todo: fill in your student ids
students = {'id1': '211440730', 'id2': '208295576'}

if __name__ == '__main__':
    with open('config-rps.json', 'r') as json_file:
        config = json.load(json_file)

    winner = game(config['results_filename'])
    print(f'the winner is: {winner}')
