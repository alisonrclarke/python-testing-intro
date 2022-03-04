import math
import random
import sys
import time


def main():
    """Function to put data into a square grid and do something complicated
    with it"""
    # Determine length of data from input parameter
    # TODO: add input validation
    data_size = int(sys.argv[1])

    # Generate some data
    data = random.sample(range(1, 100), data_size)
    print(f"Data: {data}")

    # Put the data in a grid
    grid_size = int(math.sqrt(data_size))
    grid = []
    i = 0
    for r in range(grid_size):
        row = []
        for c in range(grid_size):
            row.append(data[i])
            i += 1
        grid.append(row)

    # Do some really complex calculations...
    print("Working...")
    time.sleep(5)

    # Display the grid
    print("Grid:")
    for row in grid:
        print('\t'.join([str(i) for i in row]))


if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    main()
