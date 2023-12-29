import random
def convert_file_to_matrix(filename):
    input_file = open(filename, "r")
    text_data = input_file.readlines()
    MAZE_SIZE = int(text_data[0][:-1])
    result = []
    for i in range(1, MAZE_SIZE + 1):
        line = text_data[i].strip().split(".")
        result.append(line)
    input_file.close()
    return result

def convert_matrix_to_file(matrix, filename):
    output_file = open(filename, "w")
    result_str = ""
    result_str += (str(len(matrix)) + "\n")
    for i in range(len(matrix)):
        line_str = ""
        for k in range(len(matrix)):
            line_str = line_str + matrix[i][k]
            if k != len(matrix) - 1:
                line_str = line_str + "."
            else:
                line_str = line_str + "\n"
        result_str += line_str
    output_file.write(result_str)
    output_file.close()
def remove_duplicates(arr):
    result = []
    for i in arr:
        if i not in result:
            result.append(i)
    return result

def Stench(matrix):
    # Given a two-dimensional matrix of rooms, return a two-dimensional boolean list
    # of whether the room has a Breeze (is directly adjacent to a pit square)
    ARRAY_SIZE = len(matrix)
    resulting_array = [[0 for i in range(ARRAY_SIZE)] for j in range(ARRAY_SIZE)]
    for i in range(ARRAY_SIZE):
        for k in range(ARRAY_SIZE):
            if ((i - 1 >= 0 and matrix[i - 1][k] == 'W')
                    or (i + 1 < ARRAY_SIZE and matrix[i + 1][k] == 'W')
                    or (k - 1 >= 0 and matrix[i][k - 1] == 'W')
                    or (k + 1 < ARRAY_SIZE and matrix[i][k + 1] == 'W')):
                resulting_array[i][k] = resulting_array[i][k] + 1
    return resulting_array

def Breeze(matrix):
    # Given a two-dimensional matrix of rooms, return a two-dimensional boolean list
    # of whether the room has a Breeze (is directly adjacent to a pit square)
    ARRAY_SIZE = len(matrix)
    resulting_array = [[0 for i in range(ARRAY_SIZE)] for j in range(ARRAY_SIZE)]
    for i in range(ARRAY_SIZE):
        for k in range(ARRAY_SIZE):
            if ((i - 1 >= 0 and matrix[i - 1][k] == 'P')
                    or (i + 1 < ARRAY_SIZE and matrix[i + 1][k] == 'P')
                    or (k - 1 >= 0 and matrix[i][k - 1] == 'P')
                    or (k + 1 < ARRAY_SIZE and matrix[i][k + 1] == 'P')):
                resulting_array[i][k] = resulting_array[i][k] + 1
    return resulting_array

def Glitter(matrix):
    # Given a two-dimensional matrix of rooms, return a two-dimensional boolean list
    # of whether the room has a Glitter (is a gold square)
    ARRAY_SIZE = len(matrix)
    resulting_array = [[0 for i in range(ARRAY_SIZE)] for j in range(ARRAY_SIZE)]
    for i in range(ARRAY_SIZE):
        for k in range(ARRAY_SIZE):
            if matrix[i][k] == 'G':
                resulting_array[i][k] = resulting_array[i][k] + 1
    return resulting_array

def isWall(coords, KB_walls):
    # coords: a list with exactly two elements, the coordinates like [3, 2]
    # KB_walls = [[3, 'r'], [-4, 'r'], [5, 'c'], [-2, 'c']]
    left_bound = -999999999
    right_bound = 999999999
    top_bound = -999999999 # Top is negative, because in array order, the top value has a smaller position.
    bottom_bound = 999999999
    for i in range(len(KB_walls)):
        if KB_walls[i][1] == 'c' and KB_walls[i][0] < 0:
            left_bound = left_bound - left_bound + KB_walls[i][0]
        if KB_walls[i][1] == 'c' and KB_walls[i][0] > 0:
            right_bound = right_bound - right_bound + KB_walls[i][0]
        if KB_walls[i][1] == 'r' and KB_walls[i][0] < 0:
            top_bound = top_bound - top_bound + KB_walls[i][0]
        if KB_walls[i][1] == 'r' and KB_walls[i][0] > 0:
            bottom_bound = bottom_bound - bottom_bound + KB_walls[i][0]
    if top_bound < coords[0] < bottom_bound and left_bound < coords[1] < right_bound:
        return False
    else:
        return True
class Agent:
    def __init__(self, matrix):
        self.matrix = matrix
        self.Breeze = Breeze(self.matrix)
        self.Glitter = Glitter(self.matrix)
        self.Stench = Stench(self.matrix)
        self.hidden_len = len(self.matrix)
        self.starting_row = 0
        self.starting_col = 0
        for i in range(len(matrix)):
            for k in range(len(matrix)):
                if matrix[i][k] == 'A':
                    self.starting_row += i
                    self.starting_col += k
                    self.matrix[i][k] = '-'
        self.accepted_move()
    # Matrix, starting_row, starting_col are hidden (not known) constants to the agent, used for checking walls.
    # But the agent knows the following:
    KB_current_pos = [0, 0] # Current relative position to the starting square, with (0, 0) being the start
    KB_walls = [] # Relative coordinates of known walls
    KB_no_pits = [] # Relative coordinates of known safe squares, those that do not have pits
    KB_no_wumpus = [] # Squares that do not have wumpus. Helpful to avoid wasting arrows
    KB_visited = [[0, 0]] # Relative coordinates of visited squares
    KB_current_path = [] # Stack of current path relative to the starting square
    KB_full_path = []
    # "Accepted move" is used at the beginning before actually moving to check for safe squares around
    # the starting square. Each accepted move costs 10 points, but because the agent does not move yet while checking
    # the starting square, 10 points are awarded from the start to make it free.
    KB_score = 10
    def print_knowledge(self):
        print("- Current relative position: " + str(self.KB_current_pos))
        print("- Relative coordinates of known walls: " + str(self.KB_walls))
        print("- Relative coordinates of known squares to not have pits: " + str(self.KB_no_pits))
        print("- Relative coordinates of known squares to not have wumpus: " + str(self.KB_no_wumpus))
        print("- Relative coordinates of visited squares: " + str(self.KB_visited))
        print("- Stack of moves in the current path: " + str(self.KB_current_path))
        print("- Entire path so far: " + str(self.KB_full_path))
        print("- Current score: " + str(self.KB_score))

    def accepted_move(self):
        print("Success, -10 pts")
        self.KB_score -= 10
        if not self.Breeze[self.starting_row + self.KB_current_pos[0]][self.starting_col + self.KB_current_pos[1]]:
            if not isWall([self.KB_current_pos[0], self.KB_current_pos[1] + 1], self.KB_walls):
                self.KB_no_pits.append([self.KB_current_pos[0], self.KB_current_pos[1] + 1])
            if not isWall([self.KB_current_pos[0], self.KB_current_pos[1] - 1], self.KB_walls):
                self.KB_no_pits.append([self.KB_current_pos[0], self.KB_current_pos[1] - 1])
            if not isWall([self.KB_current_pos[0] - 1, self.KB_current_pos[1]], self.KB_walls):
                self.KB_no_pits.append([self.KB_current_pos[0] - 1, self.KB_current_pos[1]])
            if not isWall([self.KB_current_pos[0] + 1, self.KB_current_pos[1]], self.KB_walls):
                self.KB_no_pits.append([self.KB_current_pos[0] + 1, self.KB_current_pos[1]])
            self.KB_no_pits = remove_duplicates(self.KB_no_pits)
        else:
            print("Breeze perceived. Neighboring squares of "
                  + str([self.KB_current_pos[0], self.KB_current_pos[1]]) + " may have pits.")
        if self.Glitter[self.starting_row + self.KB_current_pos[0]][self.starting_col + self.KB_current_pos[1]]:
            print("Glitter perceived. Picking up gold, +1000 pts")
            self.KB_score += 1000
            self.matrix[self.starting_row + self.KB_current_pos[0]][self.starting_col + self.KB_current_pos[1]] = "-"
            self.Glitter[self.starting_row + self.KB_current_pos[0]][self.starting_col + self.KB_current_pos[1]] \
                = not self.Glitter[self.starting_row + self.KB_current_pos[0]][self.starting_col + self.KB_current_pos[1]]

        # Shoot one arrow to the right, only if it is not known to be the wall
        # and not known to be safe from wumpus. Kill the wumpus (if there is one on that square). -100 pts
        if self.Stench[self.starting_row + self.KB_current_pos[0]][self.starting_col + self.KB_current_pos[1]]:
            shooting_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1] + 1]
            shooting_absolute_pos = [self.starting_row + shooting_relative_pos[0],
                                     self.starting_col + shooting_relative_pos[1]]
            print("Stench perceived, attempting to shoot to the right, "
                  + str(shooting_relative_pos))
            if (not isWall(shooting_relative_pos, self.KB_walls)
                    and shooting_relative_pos not in self.KB_no_wumpus):
                print("Successfully shoot to the right, -100 pts")
                self.KB_score -= 100
                if 0 <= shooting_absolute_pos[0] < self.hidden_len and 0 <= shooting_absolute_pos[1] < self.hidden_len:
                    if self.matrix[self.starting_row + shooting_relative_pos[0]][self.starting_col + shooting_relative_pos[1]] == 'W':
                        print("Scream perceived. The wumpus at "
                              + str(shooting_relative_pos) + " is killed.")
                        self.matrix[self.starting_row + shooting_relative_pos[0]][self.starting_col + shooting_relative_pos[1]] = '-'
                        self.Stench = Stench(self.matrix)
                    else:
                        print("No scream is perceived. This square does not have a wumpus.")
                    self.KB_no_wumpus.append(shooting_relative_pos)
                else:
                    print("The arrow hits a wall. Under the problem rules, this information is hidden to the agent.")
            elif isWall(shooting_relative_pos, self.KB_walls):
                print("Shooting is not allowed because this is a known wall")
            else:
                print("Shooting is not allowed because this square is confirmed to not have a wumpus")
        # Similar for down
        if self.Stench[self.starting_row + self.KB_current_pos[0]][self.starting_col + self.KB_current_pos[1]]:
            shooting_relative_pos = [self.KB_current_pos[0] + 1, self.KB_current_pos[1]]
            shooting_absolute_pos = [self.starting_row + shooting_relative_pos[0],
                                     self.starting_col + shooting_relative_pos[1]]
            print("Stench perceived, attempting to shoot down, "
                  + str(shooting_relative_pos))
            if (not isWall(shooting_relative_pos, self.KB_walls)
                    and shooting_relative_pos not in self.KB_no_wumpus):
                print("Successfully shoot down, -100 pts")
                self.KB_score -= 100
                if 0 <= shooting_absolute_pos[0] < self.hidden_len and 0 <= shooting_absolute_pos[1] < self.hidden_len:
                    if self.matrix[self.starting_row + shooting_relative_pos[0]][self.starting_col + shooting_relative_pos[1]] == 'W':
                        print("Scream perceived. The wumpus at "
                              + str(shooting_relative_pos) + " is killed.")
                        self.matrix[self.starting_row + shooting_relative_pos[0]][self.starting_col + shooting_relative_pos[1]] = '-'
                        self.Stench = Stench(self.matrix)
                    else:
                        print("No scream is perceived. This square does not have a wumpus.")
                    self.KB_no_wumpus.append(shooting_relative_pos)
                else:
                    print("The arrow hits a wall. Under the problem rules, this information is hidden to the agent.")
        # Similar for left
        if self.Stench[self.starting_row + self.KB_current_pos[0]][self.starting_col + self.KB_current_pos[1]]:
            shooting_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1] - 1]
            shooting_absolute_pos = [self.starting_row + shooting_relative_pos[0],
                                     self.starting_col + shooting_relative_pos[1]]
            print("Stench perceived, attempting to shoot to the left, "
                  + str(shooting_relative_pos))
            if (not isWall(shooting_relative_pos, self.KB_walls)
                    and shooting_relative_pos not in self.KB_no_wumpus):
                print("Successfully shoot to the left, -100 pts")
                self.KB_score -= 100
                if 0 <= shooting_absolute_pos[0] < self.hidden_len and 0 <= shooting_absolute_pos[1] < self.hidden_len:
                    if self.matrix[self.starting_row + shooting_relative_pos[0]][self.starting_col + shooting_relative_pos[1]] == 'W':
                        print("Scream perceived. The wumpus at "
                              + str(shooting_relative_pos) + " is killed.")
                        self.matrix[self.starting_row + shooting_relative_pos[0]][self.starting_col + shooting_relative_pos[1]] = '-'
                        self.Stench = Stench(self.matrix)
                    else:
                        print("No scream is perceived. This square does not have a wumpus.")
                    self.KB_no_wumpus.append(shooting_relative_pos)
                else:
                    print("The arrow hits a wall. Under the problem rules, this information is hidden to the agent.")
        # Similar for up
        if self.Stench[self.starting_row + self.KB_current_pos[0]][self.starting_col + self.KB_current_pos[1]]:
            shooting_relative_pos = [self.KB_current_pos[0] - 1, self.KB_current_pos[1]]
            shooting_absolute_pos = [self.starting_row + shooting_relative_pos[0],
                                     self.starting_col + shooting_relative_pos[1]]
            print("Stench perceived, attempting to shoot up, "
                  + str(shooting_relative_pos))
            if (not isWall(shooting_relative_pos, self.KB_walls)
                    and shooting_relative_pos not in self.KB_no_wumpus):
                print("Successfully shoot up, -100 pts")
                self.KB_score -= 100
                if 0 <= shooting_absolute_pos[0] < self.hidden_len and 0 <= shooting_absolute_pos[1] < self.hidden_len:
                    if self.matrix[self.starting_row + shooting_relative_pos[0]][self.starting_col + shooting_relative_pos[1]] == 'W':
                        print("Scream perceived. The wumpus at "
                              + str(shooting_relative_pos) + "is killed.")
                        self.matrix[self.starting_row + shooting_relative_pos[0]][self.starting_col + shooting_relative_pos[1]] = '-'
                        self.Stench = Stench(self.matrix)
                    else:
                        print("No scream is perceived. This square does not have a wumpus.")
                    self.KB_no_wumpus.append(shooting_relative_pos)
                else:
                    print("The arrow hits a wall. Under the problem rules, this information is hidden to the agent.")

    def move_deeper_template(self, direction_str, opposite_direction_str, wall_char, index_of_changed_coord,
                             next_coord, next_relative_pos, next_absolute_pos):
        print("Attempt to move " + str(direction_str) + " to:")
        print("- Known relative position: " + str(next_relative_pos))
        print("- Hidden absolute position: " + str(next_absolute_pos))
        if isWall(next_relative_pos, self.KB_walls):
            print("Failed: This is a known wall")
            return
        elif not ((0 <= next_absolute_pos[0] < self.hidden_len) and (0 <= next_absolute_pos[1] < self.hidden_len)):
            print("Failed: Bumped to a wall. Bump perceived.")
            self.KB_walls.append([next_coord, wall_char])
            self.KB_walls = remove_duplicates(self.KB_walls)
            return
        elif len(self.KB_current_path) > 0 and self.KB_current_path[-1] == opposite_direction_str:
            print(
                "Failed: While searching deeper, going the opposite direction of previous move is not allowed")
            return
        elif next_relative_pos in self.KB_visited:
            print("Failed: While searching deeper, each square can only be visited once")
            return
        elif next_relative_pos not in self.KB_no_pits:
            print("Failed: This is not a known square to be safe from pits")
            return
        else:
            self.KB_current_pos[index_of_changed_coord] = next_coord
            self.KB_visited.append(next_relative_pos)
            self.KB_current_path.append(direction_str)
            self.KB_full_path.append(direction_str)
            self.accepted_move()

    def move_right_deeper(self):
        direction_str = "right"
        opposite_direction_str = "left"
        wall_char = 'c'
        index_of_changed_coord = 1
        next_coord = self.KB_current_pos[index_of_changed_coord] + 1
        next_relative_pos = [self.KB_current_pos[0], next_coord]
        next_absolute_pos = [self.starting_row + next_relative_pos[0], self.starting_col + next_relative_pos[1]]
        self.move_deeper_template(direction_str, opposite_direction_str, wall_char, index_of_changed_coord, next_coord,
                                  next_relative_pos, next_absolute_pos)
    def move_left_deeper(self):
        direction_str = "left"
        opposite_direction_str = "right"
        wall_char = 'c'
        index_of_changed_coord = 1
        next_coord = self.KB_current_pos[index_of_changed_coord] - 1
        next_relative_pos = [self.KB_current_pos[0], next_coord]
        next_absolute_pos = [self.starting_row + next_relative_pos[0], self.starting_col + next_relative_pos[1]]
        self.move_deeper_template(direction_str, opposite_direction_str, wall_char, index_of_changed_coord, next_coord,
                                  next_relative_pos, next_absolute_pos)
    def move_up_deeper(self):
        direction_str = "up"
        opposite_direction_str = "down"
        wall_char = 'r'
        index_of_changed_coord = 0
        next_coord = self.KB_current_pos[index_of_changed_coord] - 1
        next_relative_pos = [next_coord, self.KB_current_pos[1]]
        next_absolute_pos = [self.starting_row + next_relative_pos[0], self.starting_col + next_relative_pos[1]]
        self.move_deeper_template(direction_str, opposite_direction_str, wall_char, index_of_changed_coord, next_coord,
                                  next_relative_pos, next_absolute_pos)
    def move_down_deeper(self):
        direction_str = "down"
        opposite_direction_str = "up"
        wall_char = 'r'
        index_of_changed_coord = 0
        next_coord = self.KB_current_pos[index_of_changed_coord] + 1
        next_relative_pos = [next_coord, self.KB_current_pos[1]]
        next_absolute_pos = [self.starting_row + next_relative_pos[0], self.starting_col + next_relative_pos[1]]
        self.move_deeper_template(direction_str, opposite_direction_str, wall_char, index_of_changed_coord, next_coord,
                                  next_relative_pos, next_absolute_pos)
    def undo_previous_move(self):
        if len(self.KB_current_path) <= 0:
            return
        log_str = "Undo previous move (-10 pts): "
        if self.KB_current_path[-1] == "left":
            log_str += "Going right"
            self.KB_current_pos[1] += 1
            self.KB_full_path.append("right")
        elif self.KB_current_path[-1] == "right":
            log_str += "Going left"
            self.KB_current_pos[1] -= 1
            self.KB_full_path.append("left")
        elif self.KB_current_path[-1] == "up":
            log_str += "Going down"
            self.KB_current_pos[0] += 1
            self.KB_full_path.append("down")
        elif self.KB_current_path[-1] == "down":
            log_str += "Going up"
            self.KB_current_pos[0] -= 1
            self.KB_full_path.append("up")
        print(log_str)
        self.KB_score -= 10
        self.KB_current_path.pop()
    def climb(self):
        # Final action to exit the cave.
        # Boolean variable, returns true if the agent is currently at absolute position (1, 1).
        # The agent does not know if it is currently on (1, 1), so it has to try this for every square it travels to.
        if (self.starting_row + self.KB_current_pos[0] == self.hidden_len - 1
                and self.starting_col + self.KB_current_pos[1] == 0):
            # (1, 1) in the wumpus problem is (hidden_len, 0) in array order
            return True
        return False
    def solve_problem(self):
        # Phase 1: Find gold
        neighbor_available = True
        while neighbor_available:
            current_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1]]
            hidden_agent_matrix = [['-' for i in range(len(self.matrix))] for j in range(len(self.matrix))]
            for i in range(len(hidden_agent_matrix)):
                for j in range(len(hidden_agent_matrix)):
                    hidden_agent_matrix[i][j] = self.matrix[i][j]
            hidden_agent_matrix[self.starting_row + current_relative_pos[0]][self.starting_col + current_relative_pos[1]] = 'A'
            print("Current top-view matrix (hidden from agent):")
            for i in range(len(hidden_agent_matrix)):
                print(hidden_agent_matrix[i])
            print("Current knowledge base of the agent:")
            self.print_knowledge()
            print()
            self.move_right_deeper()
            next_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1]]
            if current_relative_pos[0] == next_relative_pos[0] and current_relative_pos[1] == next_relative_pos[1]:
                current_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1]]
                self.move_down_deeper()
                next_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1]]
                if current_relative_pos[0] == next_relative_pos[0] and current_relative_pos[1] == next_relative_pos[1]:
                    current_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1]]
                    self.move_left_deeper()
                    next_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1]]
                    if current_relative_pos[0] == next_relative_pos[0] and current_relative_pos[1] == next_relative_pos[1]:
                        current_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1]]
                        self.move_up_deeper()
                        next_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1]]
                        if current_relative_pos[0] == next_relative_pos[0] and current_relative_pos[1] == next_relative_pos[1]:
                            if len(self.KB_current_path) > 0:
                                self.undo_previous_move()
                            else:
                                neighbor_available = False
                                print("Finish searching for gold")
                                print(self.KB_full_path)
        print("Final score: " + str(self.KB_score))
        self.print_knowledge()
        # Phase 2: Exit the cave
        neighbor_available = True
        self.KB_visited.clear()
        while neighbor_available:
            current_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1]]
            hidden_agent_matrix = [['-' for i in range(len(self.matrix))] for j in range(len(self.matrix))]
            for i in range(len(hidden_agent_matrix)):
                for j in range(len(hidden_agent_matrix)):
                    hidden_agent_matrix[i][j] = self.matrix[i][j]
            hidden_agent_matrix[self.starting_row + current_relative_pos[0]][
                self.starting_col + current_relative_pos[1]] = 'A'
            print("Current top-view matrix (hidden from agent):")
            for i in range(len(hidden_agent_matrix)):
                print(hidden_agent_matrix[i])
            print("Current knowledge base of the agent:")
            self.print_knowledge()
            print()
            if self.climb():
                print("Successfully escaped")
                break
            self.move_right_deeper()
            next_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1]]
            if current_relative_pos[0] == next_relative_pos[0] and current_relative_pos[1] == next_relative_pos[1]:
                current_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1]]
                self.move_down_deeper()
                next_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1]]
                if current_relative_pos[0] == next_relative_pos[0] and current_relative_pos[1] == next_relative_pos[1]:
                    current_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1]]
                    self.move_left_deeper()
                    next_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1]]
                    if current_relative_pos[0] == next_relative_pos[0] and current_relative_pos[1] == next_relative_pos[1]:
                        current_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1]]
                        self.move_up_deeper()
                        next_relative_pos = [self.KB_current_pos[0], self.KB_current_pos[1]]
                        if current_relative_pos[0] == next_relative_pos[0] and current_relative_pos[1] == next_relative_pos[1]:
                            if len(self.KB_current_path) > 0:
                                self.undo_previous_move()
                            else:
                                neighbor_available = False
                                print("No exit path exists")
                                print(self.KB_full_path)
        print("Final score: " + str(self.KB_score))
def generate_map(filename):
    '''
    Returns a two-dimensional list of characters and also output the matrix to a textfile
    - 5 random squares (except (1, 1) in the wumpus problem, or [9, 0] in array order)
    are chosen to be a Wumpus square
    - 10 out of the remaining squares (except (1, 1)) are chosen to be gold squares
    - 10 out of the remaining squares (except (1, 1)) are chosen to be a pit
    - Start at a random square (out of the remaining squares)
    - In all maps, the agent does not know in advance how many squares there are of each type
    - All maps are possible to escape.
    '''
    resulting_matrix = [['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']]
    rand_nums = []
    for i in range(100):
        rand_nums.append(i)
    sampled_list = [90]
    while 90 in sampled_list:
        sampled_list = random.sample(rand_nums, 25)
    wumpus_squares = sampled_list[0:5]
    gold_squares = sampled_list[5:15]
    pit_squares = sampled_list[15:25]
    for i in range(len(wumpus_squares)):
        wumpus_row = int(wumpus_squares[i] / 10)
        wumpus_col = wumpus_squares[i] % 10
        resulting_matrix[wumpus_row][wumpus_col] = "W"
    for i in range(len(gold_squares)):
        gold_row = int(gold_squares[i] / 10)
        gold_col = gold_squares[i] % 10
        resulting_matrix[gold_row][gold_col] = "G"
    for i in range(len(pit_squares)):
        pit_row = int(pit_squares[i] / 10)
        pit_col = pit_squares[i] % 10
        resulting_matrix[pit_row][pit_col] = "P"
    starting_square = random.choice(range(0, 100))
    while starting_square in sampled_list:
        starting_square = random.choice(range(0, 100))
    starting_row = int(starting_square / 10)
    starting_col = starting_square % 10
    resulting_matrix[starting_row][starting_col] = "A"
    convert_matrix_to_file(resulting_matrix, filename)
    return resulting_matrix
def main():
    matrix5 = convert_file_to_matrix("map5.txt")
    agent5 = Agent(matrix5)
    agent5.solve_problem()
main()