from copy import deepcopy
import time

class GameState:

    def __init__(self, walls, goals, players, reached_goal):
        self.walls = walls
        self.goals = goals
        self.players = players
        self.reached_goal = reached_goal

    def copy(self):
        return deepcopy(self)


class Game:

    def __init__(self, rows, cols, board_details):
        self.rows = rows
        self.cols = cols
        self.state = GameState(
            players=deepcopy(board_details["players"]),
            goals=deepcopy(board_details["goals"]),
            walls=deepcopy(board_details["walls"]),
            reached_goal=[False] * len(board_details["players"])
        )

    def is_won(self):
        return all(self.state.reached_goal)

    def move_players(self, r_row, c_col):
        new_states = []
        cloned_state = self.state.copy()

        for i, player in enumerate(cloned_state.players):
            if cloned_state.reached_goal[i]:
                continue

            current_row, current_col = player["position"]
            while True:
                next_row = current_row + r_row
                next_col = current_col +c_col 
                if not self.is_valid_move(next_row, next_col, i):
                    break
                current_row, current_col = next_row, next_col

                if (current_row, current_col) == cloned_state.goals[i]["position"]:
                    cloned_state.reached_goal[i] = True
                    break

            if (current_row, current_col) != player["position"]:
                cloned_state.players[i]["position"] = (current_row, current_col)
                new_states.append(cloned_state.copy())  

        return new_states

    def is_valid_move(self, row, col, player_):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        if (row, col) in self.state.walls:
            return False

        for j, other_player in enumerate(self.state.players):
            if j != player_ and other_player["position"] == (row, col):
                return False

        if self.state.reached_goal[player_] and (row, col) != self.state.goals[player_]["position"]:
            return False

        return True

    def print_board(self):
        
        for row in range(self.rows):
            line = ""
            for col in range(self.cols):
                if (row, col) in self.state.walls:
                    line += "X "  # Wall
                elif any((row, col) == goal["position"] for goal in self.state.goals):
                    line += "G "  # Goal
                elif any((row, col) == player["position"] for player in self.state.players):
                    line += "P "  # Player
                else:
                    line += ". "  # Empty space
            print(line)
        print()


class GameUI:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.boards = [
            {
                "walls": [
                    (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10),
                    (2, 2), (2, 3), (2, 10), (2, 11),
                    (3, 1), (3, 2), (3, 5), (3, 8), (3, 11), (3, 12),
                    (4, 1), (4, 4), (4, 9), (4, 12),
                    (5, 1), (5, 6), (5, 9), (5, 10), (5, 12),
                    (6, 1), (6, 3), (6, 5), (6, 6), (6, 10), (6, 12),
                    (7, 1), (7, 5), (7, 12),
                    (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12)
                ],
                "players": [
                    {"position": (6, 11), }, {"position": (6, 2), }
                ],
                "goals": [
                    {"position": (3, 7), }, {"position": (4, 6), }
                ]
            },
        ]

        self.current_board = 0
        self.game = Game(rows, cols, deepcopy(self.boards[self.current_board]))

    def run(self):
        states = []  
        while True:
            self.game.print_board()  
            move = input("Enter your move (WASD): ").upper()

            if move == "W":
                new_states = self.game.move_players(-1, 0)
            elif move == "S":
                new_states = self.game.move_players(1, 0)
            elif move == "A":
                new_states = self.game.move_players(0, -1)
            elif move == "D":
                new_states = self.game.move_players(0, 1)
            else:
                print("Wrong! Please enter W, A, S, or D.")
                continue

            
            for state in new_states:
                states.append(state)
                self.game.state = state  

            
            for i, state in enumerate(states):
                print(f"Step {i + 1}:")
                self.game.state = state
                self.game.print_board()
                time.sleep(1) 

            if self.game.is_won():
                print("You Won!")
                break


def main():
    ui = GameUI(15, 15)
    ui.run()


def run():
    main()

run()

