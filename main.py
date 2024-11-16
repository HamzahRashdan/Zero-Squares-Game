import time
from copy import deepcopy
from collections import deque


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
            walls=deepcopy(board_details["walls"]),
            goals=deepcopy(board_details["goals"]),
            players=deepcopy(board_details["players"]),
            reached_goal=[False] * len(board_details["players"])
        )

    def is_won(self):
        return all(self.state.reached_goal)

    def is_valid_move(self, row, col, player_i):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        if (row, col) in self.state.walls:
            return False
        for j, other_player in enumerate(self.state.players):
            if j != player_i and other_player["position"] == (row, col):
                return False
        if self.state.reached_goal[player_i] and (row, col) != self.state.goals[player_i]["position"]:
            return False
        return True

    def simulate_move(self, current_state, r_row, c_col):
        cloned_state = deepcopy(current_state)
        new_states = []

        for i, player in enumerate(cloned_state.players):
            if cloned_state.reached_goal[i]:
                continue

            current_row, current_col = player["position"]

            while True:
                next_row = current_row + r_row
                next_col = current_col + c_col

                if not self.is_valid_move(next_row, next_col, i):
                    break

                current_row, current_col = next_row, next_col

                if (current_row, current_col) == cloned_state.goals[i]["position"]:
                    cloned_state.reached_goal[i] = True
                    break

            if (current_row, current_col) != player["position"]:
                cloned_state.players[i]["position"] = (current_row, current_col)
                new_states.append(deepcopy(cloned_state))

        return new_states

    def dfs(self):
        initial_state = self.state.copy()
        stack = [(initial_state, [])]  
        visited = set()
        visited_states = [] 
        nodes_visited = 0

        while stack:
            current_state, path = stack.pop()  
            nodes_visited += 1

            visited_states.append(deepcopy(current_state)) 

            if all(current_state.reached_goal):
                return path + [current_state], nodes_visited, visited_states

            state_hash = self.get_state_hash(current_state)
            if state_hash in visited:
                continue
            visited.add(state_hash)

            for move_row, move_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_states = self.simulate_move(current_state, move_row, move_col)
                for new_state in new_states:
                    stack.append((new_state, path + [current_state]))  

        return None, nodes_visited, visited_states  

    def get_state_hash(self, state):
        players_positions = tuple(player["position"] for player in state.players)
        return (players_positions, tuple(state.reached_goal))


if __name__ == "__main__":
    board_details = {

        "walls": [
                    (1, 2), (1, 3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9),(1,10),(1,11),(1,12),
                    (2,2),(2,12),
                    (3, 0),(3,1),(3,2),(3, 5),(3, 6),(3, 7),(3, 8),(3, 9),(3, 10),(3, 12),
                    (4, 0),(4, 10),(4,12),
                    (5, 0),(5, 2),(5, 10),(5, 12),
                    (6,0),(6, 12),
                    (7,0), (7,1), (7,2), (7,3),(7,12),
                    (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12),
                ],
        "players": [
            {"position": (2, 3), }
        ],
        "goals": [
            {"position": (4, 6), }
        ]
    }

    
    rows, cols = 15, 14
    game = Game(rows, cols, board_details)

    
    solution_path, nodes_visited, visited_states = game.dfs()

    if solution_path:
        print(f"Solution found in {len(solution_path) - 1} steps!")
        print(f"Total nodes visited: {nodes_visited}")
        for step, state in enumerate(solution_path):
            print(f"Step {step}:")
            for row in range(rows):
                row_str = ""
                for col in range(cols):
                    if (row, col) in state.walls:
                        row_str += "# "
                    elif any(goal["position"] == (row, col) for goal in state.goals):
                        row_str += "G "
                    elif any(player["position"] == (row, col) for player in state.players):
                        row_str += "P "
                    else:
                        row_str += ". "
                print(row_str)
            print()
            time.sleep(1)  

    
        print("\nVisited Nodes:")
        for i, state in enumerate(visited_states):
            print(f"Node #{i + 1}:")
            for row in range(rows):
                row_str = ""
                for col in range(cols):
                    if (row, col) in state.walls:
                        row_str += "# "
                    elif any(goal["position"] == (row, col) for goal in state.goals):
                        row_str += "G "
                    elif any(player["position"] == (row, col) for player in state.players):
                        row_str += "P "
                    else:
                        row_str += ". "
                print(row_str)
            print()
    else:
        print("No solution")
