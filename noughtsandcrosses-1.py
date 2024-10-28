import random
import os.path
import json

random.seed()

def draw_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def welcome(board):
    print("Welcome to Noughts and Crosses!")
    draw_board(board)

def initialise_board(board):
    for i in range(3):
        for j in range(3):
            board[i][j] = ' '
    return board

def get_player_move(board):
    while True:
        try:
            cell = int(input("Enter the cell number to place X (1-9): "))
            if cell < 1 or cell > 9:
                print("Please enter a number between 1 and 9.")
                continue
            row = (cell - 1) // 3
            col = (cell - 1) % 3
            if board[row][col] != ' ':
                print("Cell already occupied. Choose another.")
                continue
            return row, col
        except ValueError:
            print("Invalid input. Please enter a number.")

# Add a little bit of IQ for computer
def choose_computer_move(board):
    available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
    for move in available_moves:
        row, col = move
        # Check if the computer can win in the next move
        board[row][col] = 'O'
        if check_for_win(board, 'O'):
            board[row][col] = ' '
            return row, col
        board[row][col] = ' '  # Reset the board
    
    # Next, check if the player can win in the next move, and block it
    for move in available_moves:
        row, col = move
        board[row][col] = 'X'
        if check_for_win(board, 'X'):
            board[row][col] = ' '
            return row, col
        board[row][col] = ' '  # Reset the board
    
    # If no winning or blocking move, prioritize center, corners, then edges
    center = (1, 1)
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
    
    if center in available_moves:
        return center
    for move in corners:
        if move in available_moves:
            return move
    for move in edges:
        if move in available_moves:
            return move

    # If all else fails (unlikely), choose randomly
    return random.choice(available_moves)


def check_for_win(board, mark):
    for i in range(3):
        if all(board[i][j] == mark for j in range(3)) or \
           all(board[j][i] == mark for j in range(3)) or \
           all(board[i][i] == mark for i in range(3)) or \
           all(board[i][2-i] == mark for i in range(3)):
            return True
    return False

def check_for_draw(board):
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

def play_game(board):
    
    initialise_board(board)
    draw_board(board)
    while True:
        # Player move
        row, col = get_player_move(board)
        board[row][col] = 'X'
        draw_board(board)
        if check_for_win(board, 'X'):
            return 1
        if check_for_draw(board):
            return 0
        
        # Computer move
        row, col = choose_computer_move(board)
        board[row][col] = 'O'
        print("Computer placed O at cell:", row * 3 + col + 1)
        draw_board(board)
        if check_for_win(board, 'O'):
            return -1
        if check_for_draw(board):
            return 0
                    
                
def menu():
    while True:
        choice = input("Enter your choice (1 to play, 2 to save score, 3 to load scores, q to quit): ").lower()
        if choice in ['1', '2', '3', 'q']:
            return choice
        else:
            print("Invalid choice. Please enter again.")

def load_scores():   
    if os.path.exists('leaderboard.txt'):
        with open('leaderboard.txt', 'r') as file:
            leaders = json.load(file)
        return leaders
    else:
        return {}

def save_score(score):
    name = input("Enter your name: ")
    if os.path.exists('leaderboard.txt'):
        with open('leaderboard.txt', 'r') as file:
            leaders = json.load(file)
    else:
        leaders = {}
    leaders[name] = score
    with open('leaderboard.txt', 'w') as file:
        json.dump(leaders, file)

def display_leaderboard(leaders):
    print("Leaderboard:")
    for name, score in leaders.items():
        print(f"{name}: {score}")

