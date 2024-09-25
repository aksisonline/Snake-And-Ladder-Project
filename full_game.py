import random
import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 10
CELL_SIZE = HEIGHT // GRID_SIZE
BOARD_SIZE = CELL_SIZE * GRID_SIZE
INFO_WIDTH = WIDTH - BOARD_SIZE

PLAYERS=2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class SnakeAndLadderGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake and Ladder Game")
        
        self.board = {4: 14, 9: 31, 17: 7, 20: 38, 28: 84, 40: 59, 51: 67, 54: 34, 62: 19, 63: 81, 64: 60, 71: 91, 87: 24, 93: 73, 95: 75, 99: 78}
        self.players = []
        self.current_player = 0
        self.colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]
        self.dice_value = None
        
        self.font = pygame.font.Font(None, 24)
        self.roll_button = Button(BOARD_SIZE + 10, HEIGHT - 60, 100, 40, "Roll Dice", GREEN, WHITE)
        
        self.animation_frames = 60
        self.current_frame = 0
        self.path = []
        self.animating = False
        self.animation_delay = 16  # Delay between frames in milliseconds (60 FPS)
        self.last_animation_time = 0
        
    def draw_board(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * CELL_SIZE
                y = (GRID_SIZE - 1 - row) * CELL_SIZE
                color = WHITE if (row + col) % 2 == 0 else GRAY
                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                
                number = row * GRID_SIZE + col + 1
                text = self.font.render(str(number), True, BLACK)
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                self.screen.blit(text, text_rect)
    
    def draw_snakes_and_ladders(self):
        for start, end in self.board.items():
            start_pos = self.get_position_coordinates(start)
            end_pos = self.get_position_coordinates(end)
            
            if start < end:  # Ladder
                pygame.draw.line(self.screen, GREEN, start_pos, end_pos, 5)
            else:  # Snake
                pygame.draw.line(self.screen, RED, start_pos, end_pos, 5)
                # Draw snake head
                pygame.draw.circle(self.screen, RED, end_pos, 10)
    
    def get_position_coordinates(self, position):
        row = (position - 1) // GRID_SIZE
        col = (position - 1) % GRID_SIZE
        if row % 2 == 1:
            col = GRID_SIZE - 1 - col
        x = col * CELL_SIZE + CELL_SIZE // 2
        y = (GRID_SIZE - 1 - row) * CELL_SIZE + CELL_SIZE // 2
        return (x, y)
    
    def draw_players(self):
        for i, player in enumerate(self.players):
            if i == self.current_player and self.animating:
                pos = self.path[min(self.current_frame, len(self.path) - 1)]
            else:
                pos = self.get_position_coordinates(player["position"])
            
            pygame.draw.circle(self.screen, player["color"], pos, 15)
            
            player_text = self.font.render(f"P{i+1}", True, WHITE)
            player_rect = player_text.get_rect(center=pos)
            self.screen.blit(player_text, player_rect)
    
    def draw_info(self):
        info_x = BOARD_SIZE
        pygame.draw.rect(self.screen, (240, 240, 240), (info_x, 0, INFO_WIDTH, HEIGHT))
        
        for i, player in enumerate(self.players):
            text = f"Player {i+1}: Position {player['position']}"
            player_text = self.font.render(text, True, player["color"])
            self.screen.blit(player_text, (info_x + 10, 10 + i * 30))
        
        if self.dice_value:
            dice_text = self.font.render(f"Dice: {self.dice_value}", True, BLACK)
            self.screen.blit(dice_text, (info_x + 10, HEIGHT - 100))
        
        self.roll_button.draw(self.screen)
    
    def roll_dice(self):
        if self.animating:
            return
        
        self.dice_value = random.randint(1, 6)
        player = self.players[self.current_player]
        start_position = player["position"]
        end_position = min(start_position + self.dice_value, 100)
        
        self.path = self.generate_bezier_path(start_position, end_position)
        
        if end_position in self.board:
            snake_or_ladder_end = self.board[end_position]
            self.path += self.generate_bezier_path(end_position, snake_or_ladder_end, is_snake_or_ladder=True)
            end_position = snake_or_ladder_end
        
        player["position"] = end_position
        self.animating = True
        self.current_frame = 0
        self.last_animation_time = pygame.time.get_ticks()
        
        if end_position == 100:
            print(f"Player {self.current_player + 1} wins!")
            pygame.quit()
            sys.exit()
    
    def generate_bezier_path(self, start, end, is_snake_or_ladder=False):
        start_pos = self.get_position_coordinates(start)
        end_pos = self.get_position_coordinates(end)
        
        if is_snake_or_ladder:
            control_point = ((start_pos[0] + end_pos[0]) // 2, min(start_pos[1], end_pos[1]) - 50)
        else:
            mid_x = (start_pos[0] + end_pos[0]) // 2
            mid_y = (start_pos[1] + end_pos[1]) // 2
            control_point = (mid_x, mid_y - 50)
        
        path = []
        for i in range(self.animation_frames):
            t = i / (self.animation_frames - 1)
            x = (1 - t)**2 * start_pos[0] + 2 * (1 - t) * t * control_point[0] + t**2 * end_pos[0]
            y = (1 - t)**2 * start_pos[1] + 2 * (1 - t) * t * control_point[1] + t**2 * end_pos[1]
            path.append((int(x), int(y)))
        
        return path
    
    def start_game(self):
        num_players = PLAYERS  # You can modify this to ask for user input
        
        for i in range(num_players):
            color = self.colors[i]
            self.players.append({"position": 1, "color": color})
    
    def run(self):
        self.start_game()
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.roll_button.is_clicked(event.pos):
                            self.roll_dice()
            
            self.screen.fill(WHITE)
            self.draw_board()
            self.draw_snakes_and_ladders()
            self.draw_players()
            self.draw_info()
            
            if self.animating:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_animation_time >= self.animation_delay:
                    self.current_frame += 1
                    self.last_animation_time = current_time
                    if self.current_frame >= len(self.path):
                        self.animating = False
                        self.current_player = (self.current_player + 1) % len(self.players)
            
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = SnakeAndLadderGame()
    game.run()