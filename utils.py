import random
import numpy

def generate_map(width, height, bombs):
    map = numpy.zeros((width, height), dtype=int)
    for i in range(bombs):
        map[i // width][i % width] = -1
    numpy.random.seed()
    numpy.random.shuffle(map.flat)
    for i in range(height):
        for j in range(width):
            if map[i][j] > -1:
                if i > 0:
                    if (j > 0) and (map[i-1][j-1] == -1): map[i][j] += 1
                    if (map[i-1][j] == -1): map[i][j] += 1
                    if (j < (width - 1)) and (map[i-1][j+1] == -1): map[i][j] += 1
                    
                if (j > 0) and (map[i][j-1] == -1): map[i][j] += 1
                if (map[i][j] == -1): map[i][j] += 1
                if (j < (width - 1)) and (map[i][j+1] == -1): map[i][j] += 1
                
                if i < (height - 1):
                    if (j > 0) and (map[i+1][j-1] == -1): map[i][j] += 1
                    if (map[i+1][j] == -1): map[i][j] += 1
                    if (j < (width - 1)) and (map[i+1][j+1] == -1): map[i][j] += 1
                
    return map
            
print(generate_map(10, 10, 22))