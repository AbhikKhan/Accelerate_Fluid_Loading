
import pygame
import os

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set the size of the window and grid
WINDOW_SIZE = (600, 600)
GRID_SIZE = 15

# Set the size of each cell in the grid
CELL_SIZE = WINDOW_SIZE[0] // GRID_SIZE

# Create the window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Grid")

# Create a font object to write alphabets
FONT_SIZE = CELL_SIZE // 2 + 10  # Modified font size
font = pygame.font.SysFont(None, FONT_SIZE, bold=True)

# Create a font object to write subscript
SUBSCRIPT_FONT_SIZE = CELL_SIZE // 3  # Modified subscript font size
subscript_font = pygame.font.SysFont(None, SUBSCRIPT_FONT_SIZE, bold=True)

# Create the grid
grid = []
for row in range(GRID_SIZE):
    grid.append([])
    for column in range(GRID_SIZE):
        grid[row].append("")


# Draw the grid and save the image to a file
def draw_grid(foldername, filename,highlighted_cells=None,color=None):
    # Fill the background with black
    screen.fill(BLACK)

    # Draw the grid lines in white
    for x in range(0, WINDOW_SIZE[0], CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, WINDOW_SIZE[1]), 3)
    for y in range(0, WINDOW_SIZE[1], CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WINDOW_SIZE[0], y), 3)

    # Write the alphabet and subscript in each cell
    for row in range(GRID_SIZE):
        for column in range(GRID_SIZE):
            cell_text = font.render(grid[row][column], True, WHITE)
            text="["+str(row)+" "+str(column)+"]"
            subscript_text = subscript_font.render(text, True,
                                                   WHITE)  # add subscript text
            screen.blit(cell_text, (column * CELL_SIZE + CELL_SIZE // 4,
                                    row * CELL_SIZE + CELL_SIZE // 4))
            screen.blit(subscript_text,
                        (column * CELL_SIZE + CELL_SIZE // 8, row * CELL_SIZE))

    
    # Highlight the cells if specified
    if highlighted_cells is not None:
        for cell in highlighted_cells:
            row, column = cell
            rect = pygame.Rect(column * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            highlight_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
            highlight_surface.set_alpha(128)  # Set opacity of highlight to 50%
            highlight_surface.fill(color)
            screen.blit(highlight_surface, (column * CELL_SIZE, row * CELL_SIZE))
            
    # Update the display
    pygame.display.update()

    # Create the folder if it doesn't exist
    if not os.path.exists(foldername):
        os.makedirs(foldername)

    # Save the grid image to a file inside the folder
    pygame.image.save(screen, os.path.join(foldername, filename))


# Set the alphabet for a specific cell
def set_cell_alphabet(row, column, alphabet, foldername, filename):
    grid[row][column] = alphabet

    # Draw the grid again with the updated alphabet and save the image to a file
    draw_grid(foldername, filename)


# Load the alphabets at specific cells
def load(cells, alphabets, foldername, filename):
    for i in range(len(cells)):
        row, column = cells[i]
        alphabet = alphabets[i].upper()
        set_cell_alphabet(row, column, alphabet, foldername, filename)
    # pygame.quit()
    # get_matrix()
    
    
def get_matrix():
    matrix = []
    for row in range(GRID_SIZE):
        matrix.append([])
        for column in range(GRID_SIZE):
            if grid[row][column] == "":
                matrix[row].append(0)
            else:
                matrix[row].append(1)
    return matrix

from collections import deque


def is_valid(coord, rows, cols):
    row, col = coord
    return 0 <= row < rows and 0 <= col < cols



def shortest_path(matrix, start, end): 
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))
    # print("from:",start," to:",end)
    
    # Define helper function to get neighboring cells
    def get_neighbors(cell):
        row, col = cell
        candidates = [
            (row-1, col), # up
            (row+1, col), # down
            (row, col-1), # left
            (row, col+1), # right
        ]
        return [(r, c) for r, c in candidates if 0 <= r < len(matrix) and 0 <= c < len(matrix[0]) and matrix[r][c] == 0]

    # Convert start and end coordinates to tuples
    start = tuple(start)
    end = tuple(end)

    # Initialize variables
    queue = deque([start])
    visited = {start: None}

    # BFS algorithm to find shortest path
    while queue:
        current = queue.popleft()
        if current == end:
            break
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited[neighbor] = current
                queue.append(neighbor)

    # Reconstruct path from start to end
    path = [end]
    while path[-1] != start:
        if path[-1] not in visited:
            return [] # Path not found
        path.append(visited[path[-1]])
    path.reverse()

    return path



# Blink the cells at specific coordinates
# def blink_cells(cells, duration, foldername, filename):
#     for i in range(duration):
#         draw_grid(foldername, filename)
#         for cell in cells:
#             row, column = cell
#             rect = pygame.Rect(column * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
#             pygame.draw.rect(screen, RED, rect)
#         pygame.display.update()
#         pygame.time.wait(200)
        
        
# def blink_cells(cells, duration, foldername, filename):
#     for i in range(duration):
#         draw_grid(foldername, filename)
#         for cell in cells:
#             row, column = cell
#             rect = pygame.Rect(column * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
#             pygame.draw.rect(screen, RED, rect)
#         pygame.display.update()
#         pygame.time.wait(200)
#         draw_grid(foldername, filename)
#         pygame.display.update()
#         pygame.time.wait(200)
        
        
# def highlight_cells(cells, foldername, filename):
#     for cell in cells:
#         row, column = cell
#         rect = pygame.Rect(column * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
#         pygame.draw.rect(screen, RED, rect)
#     pygame.display.update()
#     pygame.time.wait(2000)
#     draw_grid(foldername, filename)


##okcode
###############################################################################
# import pygame
# import os

# # Initialize Pygame
# pygame.init()

# # Define colors
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)

# # Set the size of the window and grid
# WINDOW_SIZE = (500, 500)
# GRID_SIZE = 10

# # Set the size of each cell in the grid
# CELL_SIZE = WINDOW_SIZE[0] // GRID_SIZE

# # Create the window
# screen = pygame.display.set_mode(WINDOW_SIZE)
# pygame.display.set_caption("Grid")

# # Create a font object to write alphabets
# FONT_SIZE = CELL_SIZE // 2 + 10 # Modified font size
# font = pygame.font.SysFont(None, FONT_SIZE, bold=True)

# # Create the grid
# grid = []
# for row in range(GRID_SIZE):
#     grid.append([])
#     for column in range(GRID_SIZE):
#         grid[row].append("")

# # Draw the grid and save the image to a file
# def draw_grid(foldername, filename):
#     # Fill the background with black
#     screen.fill(BLACK)

#     # Draw the grid lines in white
#     for x in range(0, WINDOW_SIZE[0], CELL_SIZE):
#         pygame.draw.line(screen, WHITE, (x, 0), (x, WINDOW_SIZE[1]), 3)
#     for y in range(0, WINDOW_SIZE[1], CELL_SIZE):
#         pygame.draw.line(screen, WHITE, (0, y), (WINDOW_SIZE[0], y), 3)

#     # Write the alphabet in each cell
#     for row in range(GRID_SIZE):
#         for column in range(GRID_SIZE):
#             cell_text = font.render(grid[row][column], True, WHITE)
#             screen.blit(cell_text, (column * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 4))

#     # Update the display
#     pygame.display.update()

#     # Create the folder if it doesn't exist
#     if not os.path.exists(foldername):
#         os.makedirs(foldername)

#     # Save the grid image to a file inside the folder
#     pygame.image.save(screen, os.path.join(foldername, filename))

# # Set the alphabet for a specific cell
# def set_cell_alphabet(row, column, alphabet, foldername, filename):
#     grid[row][column] = alphabet

#     # Draw the grid again with the updated alphabet and save the image to a file
#     draw_grid(foldername, filename)

# # Load the alphabets at specific cells
# def load(cells, alphabets, foldername, filename):
#     for i in range(len(cells)):
#         row, column = cells[i]
#         alphabet = alphabets[i].upper()
#         set_cell_alphabet(row, column, alphabet, foldername, filename)
#     # pygame.quit()

# # Blink the cells at specific coordinates
# def blink_cells(cells, duration, foldername, filename):
#     for i in range(duration):
#         draw_grid(foldername, filename)
#         for cell in cells:
#             row, column = cell
#             rect = pygame.Rect(column * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
#             pygame.draw.rect(screen, RED, rect)
#         pygame.display.update()
#         pygame.time.wait(200)
#         draw_grid(foldername, filename)
#         pygame.display.update()
#         pygame.time.wait(200)
#     # pygame.quit()

# # Get the folder name and filename to save the grid image
# # foldername = input("Enter the folder name to save the grid image: ")
# # filename = input("Enter the filename to save the grid image: ")

# # # cells = [(2, 3), (5, 6), (8, 1)]
# # # alphabets = ["a", "b", "c"]
# # # load(cells, alphabets, foldername, filename)
# # cells_to_blink = [[4, 6], [4, 7], [5, 7], [5, 6]]
# # blink_cells(cells_to_blink, 5, foldername, filename)

# # Quit Pygame
# # pygame.quit()
# ############################################################################################








# import pygame
# import os

# # Initialize Pygame
# pygame.init()

# # Define colors
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)

# # Set the size of the window and grid
# WINDOW_SIZE = (500, 500)
# GRID_SIZE = 10

# # Set the size of each cell in the grid
# CELL_SIZE = WINDOW_SIZE[0] // GRID_SIZE

# # Create the window
# screen = pygame.display.set_mode(WINDOW_SIZE)
# pygame.display.set_caption("Grid")

# # Create a font object to write alphabets
# FONT_SIZE = CELL_SIZE // 2 + 10 # Modified font size
# font = pygame.font.SysFont(None, FONT_SIZE, bold=True)

# # Create the grid
# grid = []
# for row in range(GRID_SIZE):
#     grid.append([])
#     for column in range(GRID_SIZE):
#         grid[row].append("")

# # Draw the grid and save the image to a file
# def draw_grid(foldername, filename):
#     # Fill the background with black
#     screen.fill(BLACK)

#     # Draw the grid lines in white
#     for x in range(0, WINDOW_SIZE[0], CELL_SIZE):
#         pygame.draw.line(screen, WHITE, (x, 0), (x, WINDOW_SIZE[1]), 3)
#     for y in range(0, WINDOW_SIZE[1], CELL_SIZE):
#         pygame.draw.line(screen, WHITE, (0, y), (WINDOW_SIZE[0], y), 3)

#     # Write the alphabet in each cell
#     for row in range(GRID_SIZE):
#         for column in range(GRID_SIZE):
#             cell_text = font.render(grid[row][column], True, WHITE)
#             screen.blit(cell_text, (column * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 4))

#     # Update the display
#     pygame.display.update()

#     # Create the folder if it doesn't exist
#     if not os.path.exists(foldername):
#         os.makedirs(foldername)

#     # Save the grid image to a file inside the folder
#     pygame.image.save(screen, os.path.join(foldername, filename))

# # Set the alphabet for a specific cell
# def set_cell_alphabet(row, column, alphabet, foldername, filename):
#     grid[row][column] = alphabet

#     # Draw the grid again with the updated alphabet and save the image to a file
#     draw_grid(foldername, filename)

# # Get the folder name and filename to save the grid image
# # foldername = input("Enter the folder name to save the grid image: ")
# # filename = input("Enter the filename to save the grid image: ")

# # Draw the initial grid and save the image to a file
# # draw_grid(foldername, filename)

# # Set the alphabet for a specific cell
# # alphabet = input("Enter alphabet for cell (row, column): ")
# # row, column = map(int, input("Enter row and column of the cell (separated by space): ").split())
# # set_cell_alphabet(row, column, alphabet.upper(), foldername, filename)

