# By submitting this assignment, I agree to the following:
# "Aggies do not lie, cheat, or steal, or tolerate those who do."
# "I have not given or received any unauthorized aid on this assignment."
#
# Names: Aadit Shah
#        Rachel Kwak
#        Lasya Adivi
# Section: 208
# Assignment: Lab 13
# Date: 3 December 2023


import turtle

# Constants
GRID_SIZE = 5
CELL_SIZE = 50
PLAYER1_PIECE = "black"  # Black piece
PLAYER2_PIECE = "red"  # Red piece

def rules():
  '''Prints out the rules and instructions of the game to the user in the console'''
  print('Rules and Instructions: Each player will start with 4 moves, with the player with the black piece (player 1) going first. The objective of the game is to get your 4 pieces into a vertical, horizontal, diagonal, or a 2x2 square formation within the 5x5 board. If no one has won after their first 4 moves, players will be asked to move one of their existing pieces to an adjacent and empty location, till a winning formation has been made.\n')

def draw_board():
  '''Draws the 5x5 board that will be used to place markers during the game'''
  for i in range(GRID_SIZE + 1):
        turtle.penup()
        turtle.goto(-GRID_SIZE * CELL_SIZE / 2, GRID_SIZE * CELL_SIZE / 2 - i * CELL_SIZE)
        turtle.pendown()
        turtle.forward(GRID_SIZE * CELL_SIZE)

        turtle.penup()
        turtle.goto(-GRID_SIZE * CELL_SIZE / 2 + i * CELL_SIZE, GRID_SIZE * CELL_SIZE / 2)
        turtle.pendown()
        turtle.right(90)
        turtle.forward(GRID_SIZE * CELL_SIZE)
        turtle.left(90)

def draw_piece(player, row, col):
    '''Draws the players piece given an inputted row and column'''
    turtle.penup()
    turtle.goto(col * CELL_SIZE - GRID_SIZE * CELL_SIZE / 2 + CELL_SIZE / 2,
                GRID_SIZE * CELL_SIZE / 2 - row * CELL_SIZE - CELL_SIZE / 2 - 20)  # Adjusted y-coordinate to 20
    turtle.pendown()
    turtle.color(player)
    turtle.begin_fill()
    turtle.circle(CELL_SIZE / 2 - 5)
    turtle.end_fill()
    turtle.color("black")  # Reset color to black for the grid

def erase_piece(row, col):
    '''Erases a certain players piece depending on the inputted row and column'''
    turtle.penup()
    turtle.goto(col * CELL_SIZE - GRID_SIZE * CELL_SIZE / 2 + CELL_SIZE / 2,
                GRID_SIZE * CELL_SIZE / 2 - row * CELL_SIZE - CELL_SIZE / 2 - 20)  # Adjusted y-coordinate to 20
    turtle.pendown()
    turtle.color("white")  # Use the background color to "erase" the piece
    turtle.begin_fill()
    turtle.circle(CELL_SIZE / 2 - 5)
    turtle.end_fill()
    turtle.color("black")  # Reset color to black for the grid

def is_empty(board, row, col):
    '''Checks to see if a specific position on the board is empty'''
    return board[row][col] == " "

def is_valid_move(board, row, col):
    '''Checks if the inputted row and column are within the bounds'''
    return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and is_empty(board, row, col)

# Function to check for a win
def check_for_win(board, player):
    '''Checks to see if the player has won, either through horizontal, vertical, diagonal, or square formation'''
    # Check rows
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE - 3):
            if all(board[i][j + k] == player for k in range(4)):
                return True

    # Check columns
    for i in range(GRID_SIZE - 3):
        for j in range(GRID_SIZE):
            if all(board[i + k][j] == player for k in range(4)):
                return True

    # Check diagonals (from top-left to bottom-right)
    for i in range(GRID_SIZE - 3):
        for j in range(GRID_SIZE - 3):
            if all(board[i + k][j + k] == player for k in range(4)):
                return True

    # Check diagonals (from top-right to bottom-left)
    for i in range(GRID_SIZE - 3):
        for j in range(3, GRID_SIZE):
            if all(board[i + k][j - k] == player for k in range(4)):
                return True

    # Check for a square formation
    for i in range(GRID_SIZE - 1):
        for j in range(GRID_SIZE - 1):
            # Check for a square formation in the top-left corner
            if (board[i][j] == board[i][j + 1] == board[i + 1][j] == board[i + 1][j + 1] == player):
                return True
    return False

def move_piece(board, from_row, from_col, to_row, to_col):
    '''Moves the piece from one location to another with two row inputs and two column inputs'''
    if is_valid_move(board, to_row, to_col) and (
        abs(from_row - to_row) == 1 or abs(from_col - to_col) == 1 #Checks to see if it's an adjacent + valid move
    ):
        board[to_row][to_col] = board[from_row][from_col] #Update the location
        board[from_row][from_col] = " " #Reset

        # Erase the original piece at the old position
        erase_piece(from_row, from_col)

        # Draw the player's piece at the new position
        draw_piece(board[to_row][to_col], to_row, to_col)

        return True
    else:
        return False

def get_valid_input(prompt, minval, maxval):
    '''Checks to see if the GUI input is a valid integer input'''
    while True:
        user_input = turtle.numinput(prompt, f"Enter value ({minval}-{maxval}):", minval=minval, maxval=maxval) #GUI input
        if user_input is not None: #If it has a value
            return int(user_input)

def reset_board():
    '''Resets the game board if the players want to play again'''
    return [[" " for y in range(GRID_SIZE)] for z in range(GRID_SIZE)]

def replay():
    '''Asks is the user wants to play the game again or not using a yes or no input'''
    while True:
        replay_input = turtle.textinput("Replay", "Do you want to play again? (yes/no)").lower()
        if replay_input in ["yes", "no"]:
            return replay_input == "yes"

def scores(player_scores):
    '''Updates the scores between the 2 players between the rounds in the console'''
    print("Scores:")
    for player, score in player_scores.items(): #Runs through the dictionary
        print(f"Player {player}: {score}")
        print()
        
def main():
    '''Main game loop that calls all the different functions in order to play a game of Teeko'''
    rules()
    turtle.speed(10)
    turtle.hideturtle()
    turtle.bgcolor("white")
    turtle.title("Teeko Game")

    draw_board()

    # Initialize the game board
    board = reset_board()

    current_player = 1

    # Initialize player scores
    player_scores = {1: 0, 2: 0}

    # Drop phase
    move_num = 0
    while move_num < 8:
        turtle.title(f"Teeko Game - Player {current_player}'s Turn (Drop Phase)")

        # Get player move
        row = get_valid_input(f"Player {current_player}'s Turn: Row", 1, GRID_SIZE) - 1
        col = get_valid_input(f"Player {current_player}'s Turn: Column", 1, GRID_SIZE) - 1

        # Check if the move is valid
        if is_valid_move(board, row, col):
            move_num += 1
            # Place the player's piece on the board
            board[row][col] = PLAYER1_PIECE if current_player == 1 else PLAYER2_PIECE

            # Draw the player's piece on the GUI
            draw_piece(PLAYER1_PIECE if current_player == 1 else PLAYER2_PIECE, row, col)

            # Check for a win
            if check_for_win(board, PLAYER1_PIECE if current_player == 1 else PLAYER2_PIECE):        
                turtle.title(f"Teeko Game - Player {current_player} wins!")
                player_scores[current_player] += 1  # Update player score
                scores(player_scores)  # Print scores
                turtle.done()

                break

            # Switch to the other player
            current_player = 3 - current_player  # Switch between players 1 and 2

    # Movement phase
    check = True
    with open('teeko_congrats.txt', 'w') as congrats:
        congrats.write("Congratulations!")
        
    while check: 
        turtle.title(f"Teeko Game - Player {current_player}'s Turn (Movement Phase)")

        try:
            # Get player move
            from_row = get_valid_input(f"Player {current_player}'s Turn: Row, Original Location", 1, GRID_SIZE) - 1
            from_col = get_valid_input(f"Player {current_player}'s Turn: Column, Original Location", 1, GRID_SIZE) - 1
            to_row = get_valid_input(f"Player {current_player}'s Turn: Row, New Location", 1, GRID_SIZE) - 1
            to_col = get_valid_input(f"Player {current_player}'s Turn: Column, New Location", 1, GRID_SIZE) - 1

            # Check if the move is valid
            if move_piece(board, from_row, from_col, to_row, to_col):
                # Check for a win
                if check_for_win(board, PLAYER1_PIECE if current_player == 1 else PLAYER2_PIECE):
                    turtle.title(f"Teeko Game - Player {current_player} wins!")
                    print(congrats)
                    player_scores[current_player] += 1  # Update player score
                    scores(player_scores)  # Print scores
                    turtle.done()
                    check = False
                    
                    break

                # Switch to the other player
                current_player = 3 - current_player  # Switch between players 1 and 2

        except IndexError:
            turtle.title("Invalid move. Try again")

    # Main game loop with replay logic
    while True:
        draw_board()
        move_num = 0

        # Drop phase
        while move_num < 8:
            turtle.title(f"Teeko Game - Player {current_player}'s Turn (Drop Phase)")

            # Get player move
            row = get_valid_input(f"Player {current_player}'s Turn: Row", 1, GRID_SIZE) - 1
            col = get_valid_input(f"Player {current_player}'s Turn: Column", 1, GRID_SIZE) - 1

            # Check if the move is valid
            if is_valid_move(board, row, col):
                move_num += 1
                # Place the player's piece on the board
                board[row][col] = PLAYER1_PIECE if current_player == 1 else PLAYER2_PIECE

                # Draw the player's piece on the GUI
                draw_piece(PLAYER1_PIECE if current_player == 1 else PLAYER2_PIECE, row, col)

                # Check for a win
                if check_for_win(board, PLAYER1_PIECE if current_player == 1 else PLAYER2_PIECE):
                    turtle.title(f"Teeko Game - Player {current_player} wins!")
                    print(congrats)
                    player_scores[current_player] += 1  # Update player score
                    scores(player_scores)  # Print scores
                    turtle.done()

                    break

                # Switch to the other player
                current_player = 3 - current_player  # Switch between players 1 and 2

        # Movement phase
        check = True
        while check: 
            turtle.title(f"Teeko Game - Player {current_player}'s Turn (Movement Phase)")

            try:
                # Get player move
                from_row = get_valid_input(f"Player {current_player}'s Turn: Row, Original Location", 1, GRID_SIZE) - 1
                from_col = get_valid_input(f"Player {current_player}'s Turn: Column, Original Location", 1, GRID_SIZE) - 1
                to_row = get_valid_input(f"Player {current_player}'s Turn: Row, New Location", 1, GRID_SIZE) - 1
                to_col = get_valid_input(f"Player {current_player}'s Turn: Column, New Location", 1, GRID_SIZE) - 1

                # Check if the move is valid
                if move_piece(board, from_row, from_col, to_row, to_col):
                    # Check for a win
                    if check_for_win(board, PLAYER1_PIECE if current_player == 1 else PLAYER2_PIECE):
                        turtle.title(f"Teeko Game - Player {current_player} wins!")
                        player_scores[current_player] += 1  # Update player score
                        scores(player_scores)  # Print scores
                        turtle.done()
                        check = False
          
                        break

                    # Switch to the other player
                    current_player = 3 - current_player  # Switch between players 1 and 2

            except IndexError:
                turtle.title("Invalid move. Try again")

        # Check for replay after a win
        if replay():
            # If the user wants to replay, reset the game
            turtle.clearscreen()  # Clear the screen before restarting
            board = reset_board()
            current_player = 1
        else:
            # If the user does not want to replay, end the game
            turtle.bye()

if __name__ == "__main__":
    main()
