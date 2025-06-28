import numpy

def generate_map(width=10, height=10, bombs=10):
    map = numpy.zeros((height, width), dtype=int)
    for i in range(bombs):
        map[i // width][i % width] = -1
    numpy.random.seed()
    numpy.random.shuffle(map.ravel())
    for i in range(height):
        for j in range(width):
            if map[i][j] > -1:
                if i > 0:
                    if (j > 0) and (map[i-1][j-1] == -1): map[i][j] += 1
                    if (map[i-1][j] == -1): map[i][j] += 1
                    if (j < (width - 1)) and (map[i-1][j+1] == -1): map[i][j] += 1
                    
                if (j > 0) and (map[i][j-1] == -1): map[i][j] += 1
                if (j < (width - 1)) and (map[i][j+1] == -1): map[i][j] += 1
                
                if i < (height - 1):
                    if (j > 0) and (map[i+1][j-1] == -1): map[i][j] += 1
                    if (map[i+1][j] == -1): map[i][j] += 1
                    if (j < (width - 1)) and (map[i+1][j+1] == -1): map[i][j] += 1

    return map