import random

'''
Map 1:
- One Wumpus square
- One gold square (out of the remaining squares)
- Chance of a square (out of the remaining squares, except (1, 1)) being a pit: 0.2
- Start at room (1, 1)

Map 2:
- One Wumpus square
- Chance of a square being a gold square (out of the remaining squares): 0.1
- Chance of a square (out of the remaining squares, except (1, 1)) being a pit: 0.3
- Start at a random square (out of the remaining squares)

Map 3:
- Chance of a square being a Wumpus square: 0.1
- One gold square (out of the remaining squares)
- Chance of a square (out of the remaining squares, except (1, 1)) being a pit: 0.2
- Start at a random square (out of the remaining squares)

Map 4:
- Chance of a square being a Wumpus square: 0.1
- Chance of a square being a gold square (out of the remaining squares): 0.1
- Chance of a square (out of the remaining squares, except (1, 1)) being a pit: 0.2
- Start at a random square (out of the remaining squares)

Map 5: Instead of setting probabilities for each square:
- 10 random squares (except (1, 1)) are chosen to be a Wumpus square
- 10 out of the remaining squares (except (1, 1)) are chosen to be gold squares
- 20 out of the remaining squares (except (1, 1)) are chosen to be a pit
- Start at a random square (out of the remaining squares)
- In all maps, the agent does not know in advance how many squares there are of each type
'''

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

def generate_map1(filename):
    '''
    Returns a two-dimensional list of characters and also output the matrix to a textfile
    Map 1:
    - One Wumpus square
    - One gold square (out of the remaining squares)
    - Chance of a square (out of the remaining squares, except (1, 1)) being a pit: 0.2
    - Start at room (1, 1)
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
    sampled_list = [90, 90]
    while 90 in sampled_list: # 90 in the array is (1, 1) in the matrix
        sampled_list = random.sample(rand_nums, 2)
    wumpus_row = int(sampled_list[0] / 10)
    wumpus_col = sampled_list[0] % 10
    gold_row = int(sampled_list[1] / 10)
    gold_col = sampled_list[1] % 10
    resulting_matrix[wumpus_row][wumpus_col] = "W"
    resulting_matrix[gold_row][gold_col] = "G"
    resulting_matrix[9][0] = "A"
    for i in range(len(resulting_matrix)):
        for k in range(len(resulting_matrix)):
            if resulting_matrix[i][k] == "-":
                chance_for_pit = random.choice(range(0, 100))
                if chance_for_pit < 20:
                    resulting_matrix[i][k] = "P"
    convert_matrix_to_file(resulting_matrix, filename)
    return resulting_matrix

def generate_map2(filename):
    '''
    Returns a two-dimensional list of characters and also output the matrix to a textfile
    Map 2:
    - One Wumpus square (except (1, 1))
    - Chance of a square being a gold square (out of the remaining squares): 0.1
    - Chance of a square (out of the remaining squares, except (1, 1)) being a pit: 0.3
    - Start at a random square (out of the remaining squares)
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

    wumpus_square = 90
    while wumpus_square == 90:
        wumpus_square = random.choice(range(0, 100))
    wumpus_row = int(wumpus_square / 10)
    wumpus_col = wumpus_square % 10
    resulting_matrix[wumpus_row][wumpus_col] = "W"

    for i in range(len(resulting_matrix)):
        for k in range(len(resulting_matrix)):
            if resulting_matrix[i][k] == "-":
                chance_for_gold = random.choice(range(0, 100))
                if chance_for_gold < 10:
                    resulting_matrix[i][k] = "G"

    for i in range(len(resulting_matrix)):
        for k in range(len(resulting_matrix)):
            if resulting_matrix[i][k] == "-" and not(i == 9 and k == 0):
                chance_for_pit = random.choice(range(0, 100))
                if chance_for_pit < 30:
                    resulting_matrix[i][k] = "P"

    starting_square = random.choice(range(0, 100))
    while resulting_matrix[int(starting_square / 10)][starting_square % 10] != "-":
        starting_square = random.choice(range(0, 100))
    resulting_matrix[int(starting_square / 10)][starting_square % 10] = "A"

    convert_matrix_to_file(resulting_matrix, filename)
    return resulting_matrix

def generate_map3(filename):
    '''
    Returns a two-dimensional list of characters and also output the matrix to a textfile
    Map 3:
    - Chance of a square being a Wumpus square (except (1, 1)): 0.1
    - One gold square (out of the remaining squares)
    - Chance of a square (out of the remaining squares, except (1, 1)) being a pit: 0.2
    - Start at a random square (out of the remaining squares)
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

    gold_square = 90
    while gold_square == 90:
        gold_square = random.choice(range(0, 100))
    gold_row = int(gold_square / 10)
    gold_col = gold_square % 10
    resulting_matrix[gold_row][gold_col] = "G"

    for i in range(len(resulting_matrix)):
        for k in range(len(resulting_matrix)):
            if resulting_matrix[i][k] == "-" and not(i == 9 and k == 0):
                chance_for_wumpus = random.choice(range(0, 100))
                if chance_for_wumpus < 10:
                    resulting_matrix[i][k] = "W"

    for i in range(len(resulting_matrix)):
        for k in range(len(resulting_matrix)):
            if resulting_matrix[i][k] == "-" and not(i == 9 and k == 0):
                chance_for_pit = random.choice(range(0, 100))
                if chance_for_pit < 20:
                    resulting_matrix[i][k] = "P"

    starting_square = random.choice(range(0, 100))
    while resulting_matrix[int(starting_square / 10)][starting_square % 10] != "-":
        starting_square = random.choice(range(0, 100))
    resulting_matrix[int(starting_square / 10)][starting_square % 10] = "A"

    convert_matrix_to_file(resulting_matrix, filename)
    return resulting_matrix

def generate_map4(filename):
    '''
    Returns a two-dimensional list of characters and also output the matrix to a textfile
    Map 4:
    - Chance of a square being a Wumpus square: 0.1
    - Chance of a square being a gold square (out of the remaining squares): 0.1
    - Chance of a square (out of the remaining squares, except (1, 1)) being a pit: 0.2
    - Start at a random square (out of the remaining squares)
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

    for i in range(len(resulting_matrix)):
        for k in range(len(resulting_matrix)):
            if resulting_matrix[i][k] == "-" and not(i == 9 and k == 0):
                chance_for_wumpus = random.choice(range(0, 100))
                if chance_for_wumpus < 10:
                    resulting_matrix[i][k] = "W"
                    
    for i in range(len(resulting_matrix)):
        for k in range(len(resulting_matrix)):
            if resulting_matrix[i][k] == "-":
                chance_for_gold = random.choice(range(0, 100))
                if chance_for_gold < 10:
                    resulting_matrix[i][k] = "G"

    for i in range(len(resulting_matrix)):
        for k in range(len(resulting_matrix)):
            if resulting_matrix[i][k] == "-" and not(i == 9 and k == 0):
                chance_for_pit = random.choice(range(0, 100))
                if chance_for_pit < 20:
                    resulting_matrix[i][k] = "P"

    starting_square = random.choice(range(0, 100))
    while resulting_matrix[int(starting_square / 10)][starting_square % 10] != "-":
        starting_square = random.choice(range(0, 100))
    resulting_matrix[int(starting_square / 10)][starting_square % 10] = "A"

    convert_matrix_to_file(resulting_matrix, filename)
    return resulting_matrix

def generate_map5(filename):
    '''
    Returns a two-dimensional list of characters and also output the matrix to a textfile
    Map 5: Instead of setting probabilities for each square:
    - 10 random squares (except (1, 1)) are chosen to be a Wumpus square
    - 10 out of the remaining squares (except (1, 1)) are chosen to be gold squares
    - 20 out of the remaining squares (except (1, 1)) are chosen to be a pit
    - Start at a random square (out of the remaining squares)
    - In all maps, the agent does not know in advance how many squares there are of each type
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
        sampled_list = random.sample(rand_nums, 40)
    wumpus_squares = sampled_list[0:10]
    gold_squares = sampled_list[10:20]
    pit_squares = sampled_list[20:40]
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

def Stench(matrix):
    # Given a two-dimensional matrix of rooms, return a two-dimensional boolean list
    # of whether the room has a Stench (is directly adjacent to a wumpus)
    ARRAY_SIZE = len(matrix)
    resulting_array = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
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
    resulting_array = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
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
    resulting_array = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    for i in range(ARRAY_SIZE):
        for k in range(ARRAY_SIZE):
            if matrix[i][k] == 'G':
                resulting_array[i][k] = resulting_array[i][k] + 1
    return resulting_array

def main():
    matrix1 = convert_file_to_matrix("map1.txt")
    matrix2 = convert_file_to_matrix("map2.txt")
    matrix3 = convert_file_to_matrix("map3.txt")
    matrix4 = convert_file_to_matrix("map4.txt")
    matrix5 = convert_file_to_matrix("map5.txt")
    print(matrix1)
    print(Stench(matrix1))
    print(Breeze(matrix1))
    print(Glitter(matrix1))
main()