import json


def game(results_filename):
    # todo: implement this function
    print(f'starting the game with {results_filename}')

    # todo: due to possible difference in file encodings between operating systems, you may need to add
    #  utf8 encoding type when opening a file, as an example: with open(<file name>, 'r', encoding='utf8') as fin
    #  python developers plan to make utf8 a default at 3.15 - https://peps.python.org/pep-0686/


    winner = ''  # todo: assign player name or "tie"
    return winner


# todo: fill in your student ids
students = {'id1': '000000000', 'id2': '000000000'}

if __name__ == '__main__':
    with open('config-rps.json', 'r') as json_file:
        config = json.load(json_file)

    winner = game(config['results_filename'])
    print(f'the winner is: {winner}')
