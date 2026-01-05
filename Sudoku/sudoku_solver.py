import pygame
import random
import copy

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 540, 640
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Sudoku: Human vs AI")

# Colors
WHITE, BLACK, BLUE = (255, 255, 255), (0, 0, 0), (50, 100, 255)
RED, GREEN, LIGHT_GRAY = (255, 0, 0), (0, 150, 0), (240, 240, 240)

FONT = pygame.font.SysFont("arial", 40)
SMALL_FONT = pygame.font.SysFont("arial", 18)

# --- AI LOGIC ---
def is_valid(bo, num, pos):
    for i in range(9):
        if bo[pos[0]][i] == num and pos[1] != i: return False
    for i in range(9):
        if bo[i][pos[1]] == num and pos[0] != i: return False
    bx, by = pos[1] // 3, pos[0] // 3
    for i in range(by*3, by*3+3):
        for j in range(bx*3, bx*3+3):
            if bo[i][j] == num and (i, j) != pos: return False
    return True

def generate_new_game():
    base, side = 3, 9
    def pattern(r, c): return (base * (r % base) + r // base + c) % side
    def shuffle(s): return random.sample(s, len(s))
    rBase = range(base)
    rows = [g*base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g*base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, side + 1))
    
    solved_board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    full_solution = copy.deepcopy(solved_board)
    
    # Remove numbers (Difficulty: 45 empties)
    for p in random.sample(range(81), 45):
        solved_board[p // 9][p % 9] = 0
        
    return solved_board, full_solution

# --- UI DRAWING ---
def draw_window(current_board, original_board, solution, selected, status):
    SCREEN.fill(WHITE)
    if selected:
        pygame.draw.rect(SCREEN, (230, 240, 255), (selected[1]*60, selected[0]*60, 60, 60))

    for r in range(9):
        for c in range(9):
            if original_board[r][c] != 0:
                pygame.draw.rect(SCREEN, LIGHT_GRAY, (c*60, r*60, 60, 60))
    
    for i in range(10):
        thick = 4 if i % 3 == 0 else 1
        pygame.draw.line(SCREEN, BLACK, (i*60, 0), (i*60, 540), thick)
        pygame.draw.line(SCREEN, BLACK, (0, i*60), (540, i*60), thick)

    for r in range(9):
        for c in range(9):
            val = current_board[r][c]
            if val != 0:
                if original_board[r][c] != 0: color = BLACK
                else: color = GREEN if val == solution[r][c] else RED
                txt = FONT.render(str(val), True, color)
                SCREEN.blit(txt, (c*60+20, r*60+10))
    
    msg = SMALL_FONT.render(f"Status: {status}", True, BLACK)
    SCREEN.blit(msg, (20, 550))
    instr = SMALL_FONT.render("'A': AI Fix | 'R': New Game | CLICK to edit", True, BLACK)
    SCREEN.blit(instr, (20, 580))

def main():
    board, solution = generate_new_game()
    original = copy.deepcopy(board)
    selected = None
    status = "New Board! Try to solve it."
    
    run = True
    while run:
        # Check for victory condition
        if board == solution:
            status = "SOLVED! Press 'R' for a new puzzle."

        draw_window(board, original, solution, selected, status)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] < 540:
                    selected = (pos[1]//60, pos[0]//60)
            
            if event.type == pygame.KEYDOWN:
                # 1. Reset Board
                if event.key == pygame.K_r:
                    board, solution = generate_new_game()
                    original = copy.deepcopy(board)
                    status = "New Game Started!"
                
                # 2. Number Entry
                if selected and original[selected[0]][selected[1]] == 0:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        board[selected[0]][selected[1]] = int(event.unicode)
                    if event.key == pygame.K_BACKSPACE:
                        board[selected[0]][selected[1]] = 0
                
                # 3. AI Fix Feature
                if event.key == pygame.K_a:
                    board = copy.deepcopy(solution)
                    status = "AI Solved it for you!"

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()