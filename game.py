from dawg import *
from board import ScrabbleBoard
import pygame 
import sys
import random
import pickle
from player import *

# Track player turns and scores
current_player = 1  # Start with Player 1
player_scores = {1: 0, 2: 0}  # Player 1 and Player 2 scores
player_words = {1: [], 2: []}

# returns a list of all words played on the board
def all_board_words(board):
    board_words = []

    # check regular board
    for row in range(0, 15):
        temp_word = ""
        for col in range(0, 16):
            letter = board[row][col].letter
            if letter:
                temp_word += letter
            else:
                if len(temp_word) > 1:
                    board_words.append(temp_word)
                temp_word = ""

    # check transposed board
    for col in range(0, 16):
        temp_word = ""
        for row in range(0, 16):
            letter = board[row][col].letter
            if letter:
                temp_word += letter
            else:
                if len(temp_word) > 1:
                    board_words.append(temp_word)
                temp_word = ""

    return board_words


def refill_word_rack(rack, tile_bag):
    to_add = min([7 - len(rack), len(tile_bag)])
    new_letters = random.sample(tile_bag, to_add)
    rack = rack + new_letters
    return rack, new_letters

def is_rack_empty(player):
    return len(player_racks[player]) == 0


def draw_board(board):
    for y in range(15):
        for x in range(15):
            if board[x][y].letter:
                if board[x][y].letter == "I":
                    letter_x_offset = 15
                else:
                    letter_x_offset = 7
                pygame.draw.rect(screen, (255, 215, 0), [(margin + square_width) * x + margin + x_offset,
                                                         (margin + square_height) * y + margin + y_offset,
                                                         square_width, square_height])

                letter = tile_font.render(board[x][y].letter, True, (0, 0, 0))
                screen.blit(letter, ((margin + square_width) * x + margin + x_offset + letter_x_offset,
                                     (margin + square_height) * y + margin + y_offset + 7))

                letter_score = modifier_font.render(str(game.point_dict[board[x][y].letter]), True, (0, 0, 0))
                screen.blit(letter_score, ((margin + square_width) * x + margin + x_offset + 31,
                                           (margin + square_height) * y + margin + y_offset + 30))

            elif "3LS" in board[x][y].modifier:
                pygame.draw.rect(screen, (0, 100, 200), [(margin + square_width) * x + margin + x_offset,
                                                         (margin + square_height) * y + margin + y_offset,
                                                         square_width, square_height])
                text_top = modifier_font.render("TRIPLE", True, (0, 0, 0))
                text_mid = modifier_font.render("LETTER", True, (0, 0, 0))
                text_bot = modifier_font.render("SCORE", True, (0, 0, 0))
                screen.blit(text_top, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 7))
                screen.blit(text_mid, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 17))
                screen.blit(text_bot, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 27))

            elif "2LS" in board[x][y].modifier:
                pygame.draw.rect(screen, (173, 216, 230), [(margin + square_width) * x + margin + x_offset,
                                                           (margin + square_height) * y + margin + y_offset,
                                                           square_width, square_height])
                text_top = modifier_font.render("DOUBLE", True, (0, 0, 0))
                text_mid = modifier_font.render("LETTER", True, (0, 0, 0))
                text_bot = modifier_font.render("SCORE", True, (0, 0, 0))
                screen.blit(text_top, ((margin + square_width) * x + margin + x_offset + 3,
                                       (margin + square_height) * y + margin + y_offset + 7))
                screen.blit(text_mid, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 17))
                screen.blit(text_bot, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 27))

            elif "2WS" in board[x][y].modifier:
                pygame.draw.rect(screen, (255, 204, 203), [(margin + square_width) * x + margin + x_offset,
                                                           (margin + square_height) * y + margin + y_offset,
                                                           square_width, square_height])
                text_top = modifier_font.render("DOUBLE", True, (0, 0, 0))
                text_mid = modifier_font.render("WORD", True, (0, 0, 0))
                text_bot = modifier_font.render("SCORE", True, (0, 0, 0))
                screen.blit(text_top, ((margin + square_width) * x + margin + x_offset + 3,
                                       (margin + square_height) * y + margin + y_offset + 7))
                screen.blit(text_mid, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 17))
                screen.blit(text_bot, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 27))

            elif "3WS" in board[x][y].modifier:
                pygame.draw.rect(screen, (237, 28, 36), [(margin + square_width) * x + margin + x_offset,
                                                         (margin + square_height) * y + margin + y_offset,
                                                         square_width, square_height])
                text_top = modifier_font.render("TRIPLE", True, (0, 0, 0))
                text_mid = modifier_font.render("WORD", True, (0, 0, 0))
                text_bot = modifier_font.render("SCORE", True, (0, 0, 0))
                screen.blit(text_top, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 7))
                screen.blit(text_mid, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 17))
                screen.blit(text_bot, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 27))

            else:
                pygame.draw.rect(screen, (210, 180, 140), [(margin + square_width) * x + margin + x_offset,
                                                           (margin + square_height) * y + margin + y_offset,
                                                           square_width, square_height])
                                                           


def draw_start_screen():
    screen.fill((255, 255, 255))
    intro_text = tile_font.render(f"Scrabble Solver Demonstration", True, (0, 0, 0))
    intro_rect = intro_text.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(intro_text, intro_rect)

    info_text = tile_font.render(f"Press Space to Generate New Game Once Game is Finished", True, (0, 0, 0))
    info_rect = info_text.get_rect(center=(screen_width // 2, screen_height // 4 + 100))
    screen.blit(info_text, info_rect)

    space_text = tile_font.render("Press Space to Start", True, (0, 0, 0))
    space_rect = space_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(space_text, space_rect)

def draw_rack():
    rack = player_racks[current_player]  # Show current player's rack
    for i, letter in enumerate(rack):
        if letter == "I":
            letter_x_offset = 15
        else:
            letter_x_offset = 7
        pygame.draw.rect(screen, (255, 215, 0), [(margin + square_width) * (i + 4) + margin + x_offset,
                                                 700,
                                                 square_width, square_height])

        if letter == "%":
            tile_letter = tile_font.render(" ", True, (0, 0, 0))
        else:
            tile_letter = tile_font.render(letter, True, (0, 0, 0))
        screen.blit(tile_letter, ((margin + square_width) * (i + 4) + margin + x_offset + letter_x_offset,
                                  700 + 7))

        letter_score = modifier_font.render(str(game.point_dict[letter]), True, (0, 0, 0))
        screen.blit(letter_score, ((margin + square_width) * (i + 4) + margin + x_offset + 31,
                                   700 + 30))

'''
def draw_rack(rack):
    for i, letter in enumerate(rack):
        if letter == "I":
            letter_x_offset = 15
        else:
            letter_x_offset = 7
        pygame.draw.rect(screen, (255, 215, 0), [(margin + square_width) * (i + 4) + margin + x_offset,
                                                 700,
                                                 square_width, square_height])

        if letter == "%":
            tile_letter = tile_font.render(" ", True, (0, 0, 0))
        else:
            tile_letter = tile_font.render(letter, True, (0, 0, 0))
        screen.blit(tile_letter, ((margin + square_width) * (i + 4) + margin + x_offset + letter_x_offset,
                                  700 + 7))

        letter_score = modifier_font.render(str(game.point_dict[letter]), True, (0, 0, 0))
        screen.blit(letter_score, ((margin + square_width) * (i + 4) + margin + x_offset + 31,
                                   700 + 30))
'''
'''
def draw_computer_score(word_score_dict):
    x_start = 700
    y_start = 50
    total = 0
    pygame.draw.rect(screen, (210, 180, 140), [x_start, 25, 255, 50])
    score_title = score_font.render("Computer Score", True, (0, 0, 0))
    screen.blit(score_title, (x_start + 50, 25))
    pygame.draw.rect(screen, (210, 180, 140), [x_start, y_start, 255, 700])
    i = 0
    for word, score in word_score_dict.items():
        if y_start * (i+1) > 665:
            x_start += 130
            i = 0
        total += score
        word = score_font.render(word, True, (0, 0, 0))
        score = score_font.render(str(score), True, (0, 0, 0))
        screen.blit(word, (x_start + 2, y_start * (i+1)))
        screen.blit(score, (x_start + 105, y_start * (i+1)))

        i += .35

    total_score = score_font.render(f"Total Score: {total}", True, (0, 0, 0))
    screen.blit(total_score, (705, 700))
'''

def draw_computer_score(word_score_dict):
    x_start = 700
    y_start = 50
    #total = 0
    column_spacing = 120 # Space between word list s

    pygame.draw.rect(screen, (210, 180, 140), [x_start, 25, 255, 50])
    #score_title = score_font.render("Player Scores", True, (0, 0, 0))
    #screen.blit(score_title, (x_start + 50, 45))

    pygame.draw.rect(screen, (210, 180, 140), [x_start, y_start, 255, 700])

    # Display Player 1 Score
    player1_score_text = score_font.render(f"Player 1: {player_scores[1]}", True, (0, 0, 0))
    screen.blit(player1_score_text, (x_start + 20, y_start + 30))

    # Display Player 1 Words
    y_offset = y_start + 90
    screen.blit(score_font.render("P1 Words:", True, (0, 0, 0)), (x_start + 20, y_offset))
    y_offset += 25
    for word in player_racks[1]:
        screen.blit(score_font.render(word, True, (0, 0, 0)), (x_start + 30, y_offset))
        y_offset += 20

    # Display Player 2 Score
    player2_score_text = score_font.render(f"Player 2: {player_scores[2]}", True, (0, 0, 0))
    screen.blit(player2_score_text, (x_start + 20, y_start + 60))

    # Display Player 2 Words
    y_offset = y_start + 90
    screen.blit(score_font.render("P2 Words:", True, (0, 0, 0)), (x_start + 20 + column_spacing, y_offset))
    y_offset += 25
    for word in player_racks[2]:
        screen.blit(score_font.render(word, True, (0, 0, 0)), (x_start + 30 + column_spacing, y_offset))
        y_offset += 20


    # Display Whose Turn it is
    turn_text = score_font.render(f"Player {current_player}'s Turn", True, (255, 0, 0))
    screen.blit(turn_text, (x_start + 50, 30))

if __name__ == "__main__":

    pygame.init()

    # Game-level variables
    screen_width = 1000
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    square_width = 40
    square_height = 40
    margin = 3
    mouse_x = 0
    mouse_y = 0
    x_offset = 20
    y_offset = 20
    modifier_font = pygame.font.Font(None, 12)
    tile_font = pygame.font.Font(None, 45)
    score_font = pygame.font.Font(None, 25)
    game_state = "start_screen"
    first_move = True  # Track if the first move has been made

    tile_bag = ["A"] * 9 + ["B"] * 2 + ["C"] * 2 + ["D"] * 4 + ["E"] * 12 + ["F"] * 2 + ["G"] * 3 + \
               ["H"] * 2 + ["I"] * 9 + ["J"] * 1 + ["K"] * 1 + ["L"] * 4 + ["M"] * 2 + ["N"] * 6 + \
               ["O"] * 8 + ["P"] * 2 + ["Q"] * 1 + ["R"] * 6 + ["S"] * 4 + ["T"] * 6 + ["U"] * 4 + \
               ["V"] * 2 + ["W"] * 2 + ["X"] * 1 + ["Y"] * 2 + ["Z"] * 1 + ["%"] * 2

    #to_load = open("lexicon/scrabble_words_complete.pickle", "rb")
    to_load = open("lexicon/grade5.pickle", "rb")
    root = pickle.load(to_load)
    #print(f"✅ Root-level letters in DAWG: {list(root.children.keys())}")
    to_load.close()
    #tile_rack = random.sample(tile_bag, 7)
    #[tile_bag.remove(letter) for letter in tile_rack]

    # Create separate racks for each player
    player_racks = {
        1: random.sample(tile_bag, 7),
        2: random.sample(tile_bag, 7)
    }

    # Remove drawn tiles from the tile bag
    for rack in player_racks.values():
        for letter in rack:
            tile_bag.remove(letter)
    game = ScrabbleBoard(root)
    #tile_rack = game.get_start_move(tile_rack)
    player_racks[current_player] = game.get_best_move(player_racks[current_player])
    
    #tile_rack, new_letters = refill_word_rack(tile_rack, tile_bag)
    #[tile_bag.remove(letter) for letter in new_letters]

    player_racks[current_player], new_letters = refill_word_rack(player_racks[current_player], tile_bag)
    [tile_bag.remove(letter) for letter in new_letters]

    pygame.display.set_caption("Scrabble")

    turn_in_progress = False  # ensures moves only happen when space is pressed

    while True:
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Start the game from the start screen
                    if game_state == "start_screen":
                        game_state = "game_screen"

                        # Reset tile bag
                        tile_bag = ["A"] * 9 + ["B"] * 2 + ["C"] * 2 + ["D"] * 4 + ["E"] * 12 + ["F"] * 2 + ["G"] * 3 + \
                                ["H"] * 2 + ["I"] * 9 + ["J"] * 1 + ["K"] * 1 + ["L"] * 4 + ["M"] * 2 + ["N"] * 6 + \
                                ["O"] * 8 + ["P"] * 2 + ["Q"] * 1 + ["R"] * 6 + ["S"] * 4 + ["T"] * 6 + ["U"] * 4 + \
                                ["V"] * 2 + ["W"] * 2 + ["X"] * 1 + ["Y"] * 2 + ["Z"] * 1 + ["%"] * 2

                        # Create separate racks for each player
                        player_racks = {
                            1: random.sample(tile_bag, 7),
                            2: random.sample(tile_bag, 7)
                        }

                        for rack in player_racks.values():
                            for letter in rack:
                                tile_bag.remove(letter)

                        game = ScrabbleBoard(root)

                        # Reset scores and words
                        player_scores = {1: 0, 2: 0}
                        player_words = {1: [], 2: []}

                        # Start with Player 1
                        current_player = 1

                # Player 1's Turn (Press "1")
                if event.key == pygame.K_1 and game_state == "game_screen":
                    if not turn_in_progress and current_player == 1:
                        turn_in_progress = True

                        # Player 1 plays from their own rack
                        #player_racks[1] = game.get_best_move(player_racks[1])
                        if first_move:
                            #print("🔵 Player 1 (First Move): Attempting to place a word...")
                            player_racks[1] = game.get_start_move(player_racks[1])
                            placed_word = game.best_word
                            first_move = False
                        else:
                            #print("🔵 Player 1: Attempting to play a move...")
                            player_racks[1] = game.get_best_move(player_racks[1])
                            #print(f"Player 1 placed '{game.best_word}' at {word_coords}")
                            placed_word = game.best_word

                        # Log the move
                        if placed_word:
                            #print(f"✅ Player 1 placed: {placed_word}")
                            player_words[1].append(placed_word)
                        else:
                            print("❌ Player 1 couldn't find a valid word.") 

                        # Update score log
                        previous_score = player_scores[1]
                        player_scores[1] += game.word_score_dict.get(game.best_word, 0)
                        #print(f"🏆 Player 1 Score: {previous_score} ➝ {player_scores[1]}")

                        # Log the updated tile rack
                        #print(f"🎭 Player 1 New Rack: {player_racks[1]}")

                        # Refill Player 1's rack
                        player_racks[1], new_letters = refill_word_rack(player_racks[1], tile_bag)
                        [tile_bag.remove(letter) for letter in new_letters]

                        # Switch to Player 2
                        current_player = 2
                        turn_in_progress = False

                # Player 2's Turn (Press "2")
                elif event.key == pygame.K_2 and game_state == "game_screen":
                    if not turn_in_progress and current_player == 2:
                        turn_in_progress = True

                        # Player 2 plays from their own rack
                        #print("🔴 Player 2: Attempting to play a move...")
                        player_racks[2], word_coords = game.get_best_move(player_racks[2])
                        #print(f"Player 2 placed '{game.best_word}' at {word_coords}")
                        placed_word = game.best_word

                        # Log the move
                        if placed_word:
                            #print(f"✅ Player 2 placed: {placed_word}")
                            player_words[2].append(placed_word)
                        else:
                            print("❌ Player 2 couldn't find a valid word.")

                        # Update score log
                        previous_score = player_scores[2]
                        player_scores[2] += game.word_score_dict.get(game.best_word, 0)
                        #print(f"🏆 Player 2 Score: {previous_score} ➝ {player_scores[2]}")

                        # Log the updated tile rack
                        #print(f"🎭 Player 2 New Rack: {player_racks[2]}")

                        # Refill Player 2's rack
                        player_racks[2], new_letters = refill_word_rack(player_racks[2], tile_bag)
                        [tile_bag.remove(letter) for letter in new_letters]

                        # Switch back to Player 1
                        current_player = 1
                        turn_in_progress = False

                # Reset Game on "end_screen"
                elif game_state == "end_screen":
                    game_state = "game_screen"

                    # Reset tile bag
                    tile_bag = ["A"] * 9 + ["B"] * 2 + ["C"] * 2 + ["D"] * 4 + ["E"] * 12 + ["F"] * 2 + ["G"] * 3 + \
                            ["H"] * 2 + ["I"] * 9 + ["J"] * 1 + ["K"] * 1 + ["L"] * 4 + ["M"] * 2 + ["N"] * 6 + \
                            ["O"] * 8 + ["P"] * 2 + ["Q"] * 1 + ["R"] * 6 + ["S"] * 4 + ["T"] * 6 + ["U"] * 4 + \
                            ["V"] * 2 + ["W"] * 2 + ["X"] * 1 + ["Y"] * 2 + ["Z"] * 1 + ["%"] * 2

                    # Reset both racks
                    player_racks = {
                        1: random.sample(tile_bag, 7),
                        2: random.sample(tile_bag, 7)
                    }

                    for rack in player_racks.values():
                        for letter in rack:
                            tile_bag.remove(letter)

                    game = ScrabbleBoard(root)

                    # Reset player scores and words
                    player_scores = {1: 0, 2: 0}
                    player_words = {1: [], 2: []}

                    # Reset to Player 1
                    current_player = 1
                    first_move = True

        # Handle Screens
        if game_state == "start_screen":
            screen.fill((255, 255, 255))
            intro_text = tile_font.render("Scrabble Solver", True, (0, 0, 0))
            intro_rect = intro_text.get_rect(center=(screen_width // 2, screen_height // 4))
            screen.blit(intro_text, intro_rect)

            info_text = tile_font.render("Press SPACE to Start", True, (0, 0, 0))
            info_rect = info_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(info_text, info_rect)

            player1_text = tile_font.render("Player 1: Press '1' to Play", True, (0, 0, 255))
            player1_rect = player1_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
            screen.blit(player1_text, player1_rect)

            player2_text = tile_font.render("Player 2: Press '2' to Play", True, (255, 0, 0))
            player2_rect = player2_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
            screen.blit(player2_text, player2_rect)

            pygame.display.update()

            #continue

        elif game_state == "game_screen":
            screen.fill((0, 0, 0))  # Clear screen for game
            draw_board(game.board)
            draw_rack()
            draw_computer_score(game.word_score_dict)

        '''
        # Draw Board and UI
        draw_board(game.board)
        draw_rack()
        draw_computer_score(game.word_score_dict)

        pygame.time.wait(75)
        '''


    '''
    while True:
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if event.key == pygame.K_1:  # Player 1's turn
                    if game_state == "game_screen" and not turn_in_progress:
                        current_player = 1
                        turn_in_progress = True

                        # Player 1 plays from their own rack
                        player_racks[1] = game.get_best_move(player_racks[1])

                        # Update Player 1's score and words
                        player_scores[1] += game.word_score_dict.get(game.best_word, 0)
                        if game.best_word:
                            player_words[1].append(game.best_word)

                        # Refill Player 1's rack
                        player_racks[1], new_letters = refill_word_rack(player_racks[1], tile_bag)
                        [tile_bag.remove(letter) for letter in new_letters]

                        # Switch to Player 2
                        current_player = 2
                        turn_in_progress = False

                elif event.key == pygame.K_2:  # Player 2's turn
                    if game_state == "game_screen" and not turn_in_progress:
                        current_player = 2
                        turn_in_progress = True

                        # Player 2 plays from their own rack
                        player_racks[2] = game.get_best_move(player_racks[2])

                        # Update Player 2's score and words
                        player_scores[2] += game.word_score_dict.get(game.best_word, 0)
                        if game.best_word:
                            player_words[2].append(game.best_word)

                        # Refill Player 2's rack
                        player_racks[2], new_letters = refill_word_rack(player_racks[2], tile_bag)
                        [tile_bag.remove(letter) for letter in new_letters]

                        # Switch back to Player 1
                        current_player = 1
                        turn_in_progress = False

                elif game_state == "end_screen":
                    game_state = "game_screen"
                    
                    # Reset tile bag and rack
                    tile_bag = ["A"] * 9 + ["B"] * 2 + ["C"] * 2 + ["D"] * 4 + ["E"] * 12 + ["F"] * 2 + ["G"] * 3 + \
                            ["H"] * 2 + ["I"] * 9 + ["J"] * 1 + ["K"] * 1 + ["L"] * 4 + ["M"] * 2 + ["N"] * 6 + \
                            ["O"] * 8 + ["P"] * 2 + ["Q"] * 1 + ["R"] * 6 + ["S"] * 4 + ["T"] * 6 + ["U"] * 4 + \
                            ["V"] * 2 + ["W"] * 2 + ["X"] * 1 + ["Y"] * 2 + ["Z"] * 1 + ["%"] * 2

                    # Reset both racks
                    player_racks = {
                        1: random.sample(tile_bag, 7),
                        2: random.sample(tile_bag, 7)
                    }

                    for rack in player_racks.values():
                        for letter in rack:
                            tile_bag.remove(letter)

                    game = ScrabbleBoard(root)

                    # Reset player scores
                    player_scores = {1: 0, 2: 0}

                    # Reset player words
                    player_words = {1: [], 2: []}

                    # Reset to Player 1
                    current_player = 1

                
                elif game_state == "game_screen" and not turn_in_progress:
                    turn_in_progress = True  # Lock the turn to prevent looping

                    # Clear the screen
                    screen.fill((0, 0, 0))

                    # Play one move only when space is pressed
                    tile_rack = game.get_best_move(tile_rack)

                    # Update current player's score
                    player_scores[current_player] += game.word_score_dict.get(game.best_word, 0)

                    if game.best_word:
                        player_words[current_player].append(game.best_word)

                    # Refill the tile rack
                    tile_rack, new_letters = refill_word_rack(tile_rack, tile_bag)
                    [tile_bag.remove(letter) for letter in new_letters]

                    # If no valid words are left, check for game end
                    if game.best_word == "":
                        if len(tile_bag) >= 7:
                            tile_rack, new_letters = refill_word_rack([], tile_bag)
                            [tile_bag.remove(letter) for letter in new_letters]
                        else:
                            game_state = "end_screen"
                            for word in all_board_words(game.board):
                                if not find_in_dawg(word, root) and word:
                                    raise Exception(f"Invalid word on board: {word}")

                    # Switch player after move
                    current_player = 2 if current_player == 1 else 1

                    turn_in_progress = False  # Unlock turn for next space press

                
                
                

        # Handle Screens
        if game_state == "start_screen":
            draw_start_screen()
            continue

        if game_state == "end_screen":
            draw_board(game.board)
            draw_rack(tile_rack)
            draw_computer_score(game.word_score_dict)
            continue

        # Draw Board
        draw_board(game.board)
        draw_rack(tile_rack)
        draw_computer_score(game.word_score_dict)

        pygame.time.wait(75)
    '''


'''
elif game_state == "game_screen" and not turn_in_progress:
                    turn_in_progress = True  # Lock the turn to prevent looping
                    
                    # Clear the screen
                    screen.fill((0, 0, 0))
                    
                    # Play one move only when space is pressed
                    tile_rack = game.get_best_move(tile_rack)

                    tile_rack, new_letters = refill_word_rack(tile_rack, tile_bag)
                    [tile_bag.remove(letter) for letter in new_letters]

                    # If no valid words are left, check for game end
                    if game.best_word == "":
                        if len(tile_bag) >= 7:
                            tile_rack, new_letters = refill_word_rack([], tile_bag)
                            [tile_bag.remove(letter) for letter in new_letters]
                        else:
                            game_state = "end_screen"
                            for word in all_board_words(game.board):
                                if not find_in_dawg(word, root) and word:
                                    raise Exception(f"Invalid word on board: {word}")

                    turn_in_progress = False  # Unlock turn for next space press
'''

'''
while True:
        pygame.display.update()
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if game_state == "start_screen":
                    game_state = "game_screen"
                    
                    # Initialize new game setup
                    tile_rack = random.sample(tile_bag, 7)
                    [tile_bag.remove(letter) for letter in tile_rack]
                    game = ScrabbleBoard(root)
                    game.get_start_move(tile_rack)
                    tile_rack, new_letters = refill_word_rack(tile_rack, tile_bag)
                    [tile_bag.remove(letter) for letter in new_letters]

                elif game_state == "end_screen":
                    game_state = "game_screen"
                    
                    # Reset tile bag and rack
                    tile_bag = ["A"] * 9 + ["B"] * 2 + ["C"] * 2 + ["D"] * 4 + ["E"] * 12 + ["F"] * 2 + ["G"] * 3 + \
                            ["H"] * 2 + ["I"] * 9 + ["J"] * 1 + ["K"] * 1 + ["L"] * 4 + ["M"] * 2 + ["N"] * 6 + \
                            ["O"] * 8 + ["P"] * 2 + ["Q"] * 1 + ["R"] * 6 + ["S"] * 4 + ["T"] * 6 + ["U"] * 4 + \
                            ["V"] * 2 + ["W"] * 2 + ["X"] * 1 + ["Y"] * 2 + ["Z"] * 1 + ["%"] * 2

                    tile_rack = random.sample(tile_bag, 7)
                    [tile_bag.remove(letter) for letter in tile_rack]
                    game = ScrabbleBoard(root)
                    game.get_start_move(tile_rack)
                    tile_rack, new_letters = refill_word_rack(tile_rack, tile_bag)
                    [tile_bag.remove(letter) for letter in new_letters]

                    # Reset player scores
                    player_scores = {1: 0, 2: 0}

                    # Reset player words
                    player_words = {1: [], 2: []}

                    # Reset to Player 1
                    current_player = 1

                
                elif game_state == "game_screen" and not turn_in_progress:
                    turn_in_progress = True  # Lock the turn to prevent looping

                    # Clear the screen
                    screen.fill((0, 0, 0))

                    # Play one move only when space is pressed
                    tile_rack = game.get_best_move(tile_rack)

                    # Update current player's score
                    player_scores[current_player] += game.word_score_dict.get(game.best_word, 0)

                    if game.best_word:
                        player_words[current_player].append(game.best_word)

                    # Refill the tile rack
                    tile_rack, new_letters = refill_word_rack(tile_rack, tile_bag)
                    [tile_bag.remove(letter) for letter in new_letters]

                    # If no valid words are left, check for game end
                    if game.best_word == "":
                        if len(tile_bag) >= 7:
                            tile_rack, new_letters = refill_word_rack([], tile_bag)
                            [tile_bag.remove(letter) for letter in new_letters]
                        else:
                            game_state = "end_screen"
                            for word in all_board_words(game.board):
                                if not find_in_dawg(word, root) and word:
                                    raise Exception(f"Invalid word on board: {word}")

                    # Switch player after move
                    current_player = 2 if current_player == 1 else 1

                    turn_in_progress = False  # Unlock turn for next space press
'''
                    



        