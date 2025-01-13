import random
import string
import logging
from collections import defaultdict
import book_generation

random.seed = 3140701
board_size = 20
logging.basicConfig(filename='word_search.log', encoding='utf-8', level=logging.INFO,
                    format='%(levelname)s:%(message)s')


def word_list_gen() -> dict:
    with open('word_list.txt', 'r') as f:
        lines = f.readlines()
    words_list = []
    active_show = ''
    active_category = ''
    for i, word in enumerate(lines):
        indent_level = len(word) - len(word.lstrip())
        word = word.strip()
        if indent_level == 0:
            active_show = word
        if indent_level == 4:
            active_category = word
        if indent_level == 8:
            words_list.append(':'.join((active_show, active_category, word)))
    result_dict = defaultdict(lambda: defaultdict(list))
    [result_dict[show][category].append(item.split(':')[-1]) for show, category, item in
     map(lambda x: x.split(':'), words_list)]
    result_dict = dict(result_dict)
    return result_dict


def word_list_split(words: list) -> list:
    chunk_size = 15
    return [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]


def clean_words(words: list) -> list:
    words = [x.upper().replace(' ','') for x in words]
    words.sort()
    too_big = [x for x in words if len(x) > board_size]
    if too_big:
        logging.info('The following words are too big for the crossword: %s'.format(too_big))
        words = [x for x in words if x not in too_big]
    words = word_list_split(words)
    return words


def generate_word_search() -> list:
    board = [[0 for x in range(board_size)] for x in range(board_size)]
    return board


def place_word(board: list, word: str) -> list:
    orientation = random.randint(0, 2)
    orientation_map = {0: 'horizontal', 1: 'vertical', 2: 'horizontal'}

    placed = False
    while not placed:
        reverse = random.choice([True, False])
        if reverse:
            word = word[::-1]
        if orientation == 0:
            row = random.randint(0, board_size - 1)
            col = random.randint(0, board_size - len(word))
            space = board[row][col:col + len(word)]
            available = [x == 0 or x == word[i] for i, x in enumerate(space)]
            available = all(available)
            if available:
                for i, letter in enumerate(space):
                    board[row][col + i] = word[i]
                placed = True
        elif orientation == 1:
            row = random.randint(0, board_size - len(word))
            col = random.randint(0, board_size - 1)
            space = [x[col] for x in board[row:row + len(word)]]
            available = [x == 0 or x == word[i] for i, x in enumerate(space)]
            available = all(available)
            if available:
                for i, letter in enumerate(space):
                    board[row + i][col] = word[i]
                placed = True
        elif orientation == 2:
            row = random.randint(0, board_size - len(word))
            col = random.randint(0, board_size - len(word))
            space = [board[row + i][col + i] for i in range(len(word))]
            available = [x == 0 or x == word[i] for i, x in enumerate(space)]
            available = all(available)
            if available:
                for i, letter in enumerate(space):
                    board[row + i][col + i] = word[i]
                placed = True
    return board


def fill_word_search(board: list):
    for i, row in enumerate(board):
        for j, x in enumerate(row):
            if x == 0:
                board[i][j] = random.choice(list(string.ascii_uppercase))
    return board


def create_word_search(words: list) -> list:
    boards = []
    word_list = clean_words(words)
    for page in word_list:
        board = generate_word_search()
        for word in page:
            board = place_word(board, word)
        board = fill_word_search(board)
        boards.append(board)
        boards.append(page)
    return boards


# words_test = ['test', 'testing', 'bryanna', 'kyronn']
full_words_list = word_list_gen()
test_boards = create_word_search(full_words_list['Hunter x Hunter']['Nen'])


for b in test_boards:
    # print(*b, sep='\n')
    print('\n'.join(['\t'.join([str(x) for x in row]) for row in b]) + '\n')
    book_generation.print_word_search(b, book_generation.word_search_book)
