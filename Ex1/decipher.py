import json
import pickle as pkl
import sys


def decipher_phrase(phrase, lexicon_filename, abc_filename):

    print(f'starting deciphering using {lexicon_filename} and {abc_filename}')

    try:
        with open(abc_filename, 'r') as abc_file, open(lexicon_filename, 'rb') as lex_file:
            lexicon = pkl.load(lex_file)
            abc_data = abc_file.read().split('\n')
            phrase_encoded = phrase.split()

            if not phrase_encoded:
                return {"status": 0, "orig_phrase": '', "K": -1}

            for k in range(0,len(abc_data)):
                temp_sentence = []
                for encoded_word in phrase_encoded:
                    temp_word = "".join(map(lambda s: abc_data[(abc_data.index(s) - k) % len(abc_data)], encoded_word))
                    if temp_word not in lexicon:
                        break
                    else:
                        temp_sentence.append(temp_word)
                if len(temp_sentence) == len(phrase_encoded):
                    real_sentence = " ".join(temp_sentence)
                    return {"status": 1, "orig_phrase": real_sentence, "K" : k}


    except Exception as e:
        sys.exit(f"An error has occurred: {e}")

    # todo: due to possible difference in file encodings between operating systems, make sure to add
    #  utf8 encoding type when opening a file, as an example: with open(<file name>, 'r', encoding='utf8') as fin
    #  python developers plan to make utf8 a default at 3.15 - https://peps.python.org/pep-0686/

    result = {"status": -1, "orig_phrase": '', "K": -1}
    return result


# todo: fill in your student ids
students = {'id1': '2114407030', 'id2': '208295576'}

if __name__ == '__main__':
    with open('config-decipher.json', 'r') as json_file:
        config = json.load(json_file)

    # note that lexicon.pkl is a serialized list of 10,000 most common English words
    result = decipher_phrase(config['secret_phrase'],
                             config['lexicon_filename'],
                             config['abc_filename'])

    assert result["status"] in {1, -1, 0}

    if result["status"] == 1:
        print(f'deciphered phrase: {result["orig_phrase"]}, K: {result["K"]}')
    elif result["status"] == -1:
        print("cannot decipher the phrase!")
    else:  # result["status"] == 0:
        print("empty phrase")
