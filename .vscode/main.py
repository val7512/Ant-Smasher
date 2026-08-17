import pygame
import random
import sys
import math

# --- 1. GAME ENGINE INITIALIZATION ---
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ant Smasher - Working UI Background")
clock = pygame.time.Clock()

# --- 2. GAME STATE DATA ---
score = 0
lives = 3
game_state = "MENU"  # Tracks current screen: MENU, PLAYING, GAMEOVER

# Fixed Font System (Guaranteed no syntax crashes)
font_large = pygame.font.Font(None, 70)
font_medium = pygame.font.Font(None, 45)
font_small = pygame.font.Font(None, 36)

ants_list = []
base_ant_speed = 2.0  # Start with a speed of 2. Use a float for smoother increases.
score_for_next_speed_increase = 20 # Increase speed every 100 points

# --- 3. UI MAIN MENU BACKGROUND DATA ---
# Using flat lists so Python reads the syntax perfectly
leaf_x = []
leaf_y = []
leaf_speed = []
leaf_sway = []

for i in range(15):
    leaf_x.append(random.randint(0, SCREEN_WIDTH))
    leaf_y.append(random.randint(0, SCREEN_HEIGHT))
    leaf_speed.append(random.uniform(1.0, 2.5))
    leaf_sway.append(random.uniform(0, 100))

bug_x = []
bug_y = []
bug_speed = []

for i in range(20):
    bug_x.append(random.randint(0, SCREEN_WIDTH))
    bug_y.append(random.randint(0, SCREEN_HEIGHT))
    bug_speed.append(random.uniform(2.0, 4.0))


# --- 4. THE ANT TEMPLATE ---
class Ant:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.radius = 25  
        self.is_squished = False
        self.squish_timer = 30 # How many frames to stay dead before vanishing

        # --- Movement Parameters ---
        self.vertical_speed = speed # Use the passed-in speed for downward movement
        self.horizontal_speed = speed * 0.75 # Make horizontal speed a bit slower than vertical
        
        # --- Ant's "Brain" for Zigzag Movement ---
        self.direction_timer = random.randint(40, 80) # Start with an initial timer
        # -1 for left, 1 for right. Starts randomly.
        self.horizontal_direction_multiplier = random.choice([-1, 1])

    def draw(self, surface):
        # --- YOUR WORK AREA (THEME & VISUALS) ---
        if not self.is_squished:
            pygame.draw.circle(surface, (0, 0, 0), (int(self.x), int(self.y)), self.radius)  
        else:
            pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), self.radius)  

    def update(self):
        if self.is_squished:
            self.squish_timer -= 1
            return

        # --- New, Smooth Movement Logic ---
        # 1. Always move down
        self.y += self.vertical_speed
        
        # 2. Check the timer to see if we should change horizontal direction
        self.direction_timer -= 1
        if self.direction_timer <= 0:
            # Time to change direction!
            self.direction_timer = random.randint(40, 80) # Reset timer for the next segment
            # Flip direction: if it was 1, it becomes -1. If -1, it becomes 1.
            self.horizontal_direction_multiplier *= -1
            
        # 3. Always apply horizontal movement every frame
        self.x += self.horizontal_speed * self.horizontal_direction_multiplier
        
        # --- Optional: Boundary Check ---
        # Bounce off side walls
        if self.x < self.radius or self.x > SCREEN_WIDTH - self.radius:
            self.horizontal_direction_multiplier *= -1

# --- 5. GAME MANAGEMENT EVENTS ---
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1200)  


# --- 6. THE MAIN GAME LOOP ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False

    # Check for Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == SPAWN_EVENT and len(ants_list) < 8:
            ants_list.append(Ant(random.randint(50, SCREEN_WIDTH - 50), 50, base_ant_speed))

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click or screen tap
            mouse_clicked = True
            mouse_x, mouse_y = event.pos
            
            # Only squish ants if we're in PLAYING mode
            if game_state == "PLAYING":
                for ant in ants_list:
                    if not ant.is_squished:
                        # Math to check if your click hit the circle
                        distance = ((mouse_x - ant.x)**2 + (mouse_y - ant.y)**2)**0.5
                        if distance < ant.radius:
                            ant.is_squished = True
                            score += 10
    
    if score >= score_for_next_speed_increase:
        base_ant_speed += 0.125
        score_for_next_speed_increase += 10
    
    # 2. MOVE THINGS
    for ant in ants_list[:]:
        ant.update()
        if ant.is_squished and ant.squish_timer <= 0:
            ants_list.remove(ant)

    # --- 7. RENDERING LAYER & STATE MACHINE ---
    
    # --- SCREEN A: MAIN MENU ---
    if game_state == "MENU":
        screen.fill((173, 216, 230))  # Clear sky blue base background
        
        # Animate Falling Leaves
        for i in range(15):
            leaf_y[i] += leaf_speed[i]  # Move down
            leaf_sway[i] += 0.03        # Advance sway math
            
            # Wiggle left and right using sine waves
            display_x = leaf_x[i] + (math.sin(leaf_sway[i]) * 20)
            
            pygame.draw.ellipse(screen, (34, 139, 34), (int(display_x), int(leaf_y[i]), 25, 15))
            
            # Reset if it hits bottom edge
            if leaf_y[i] > SCREEN_HEIGHT:
                leaf_y[i] = -20
                leaf_x[i] = random.randint(0, SCREEN_WIDTH)

        # Animate Falling Background Bugs
        for i in range(20):
            bug_y[i] += bug_speed[i]
            
            pygame.draw.circle(screen, (75, 75, 75), (int(bug_x[i]), int(bug_y[i])), 4)
            
            # Reset if it hits bottom edge
            if bug_y[i] > SCREEN_HEIGHT:
                bug_y[i] = -10
                bug_x[i] = random.randint(0, SCREEN_WIDTH)

        # Draw UI Text
        title_surf = font_large.render("ANT SMASHER", True, (0, 0, 0))
        screen.blit(title_surf, (240, 150))
        
        # Draw Start Button Box
        start_btn = pygame.Rect(300, 320, 200, 50)
        pygame.draw.rect(screen, (34, 139, 34), start_btn, border_radius=10)
        
        btn_surf = font_small.render("START GAME", True, (255, 255, 255))
        screen.blit(btn_surf, (325, 332)) 
        
        if mouse_clicked and start_btn.collidepoint(mouse_pos):
            score = 0
            lives = 3
            ants_list.clear()
            game_state = "PLAYING"

    # --- SCREEN B: ACTIVE GAMEPLAY ---
    elif game_state == "PLAYING":
        screen.fill((215, 161, 92))  

        for ant in ants_list[:]:
            ant.update()
            
            if ant.y > SCREEN_HEIGHT and not ant.is_squished:
                lives -= 1
                ants_list.remove(ant)
            elif ant.is_squished and ant.squish_timer <= 0:
                ants_list.remove(ant)

        for ant in ants_list:
            ant.draw(screen)

        # UI HUD Overlay Top Bar
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, SCREEN_WIDTH, 60))
        pygame.draw.line(screen, (0, 0, 0), (0, 60), (SCREEN_WIDTH, 60), 2)
        
        score_surf = font_small.render(f"Score: {score}", True, (0, 0, 0))
        lives_surf = font_small.render(f"Lives: {lives}", True, (200, 0, 0))
        screen.blit(score_surf, (20, 15))
        screen.blit(lives_surf, (SCREEN_WIDTH - 150, 15))

        if lives <= 0:
            game_state = "GAMEOVER"

    # --- SCREEN C: GAME OVER SCREEN ---
    elif game_state == "GAMEOVER":
        screen.fill((15, 15, 15))  
        
        go_surf = font_large.render("GAME OVER", True, (200, 0, 0))
        screen.blit(go_surf, (260, 150))
        
        score_surf = font_medium.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(score_surf, (290, 250))
        
        retry_btn = pygame.Rect(300, 360, 200, 50)
        pygame.draw.rect(screen, (34, 139, 34), retry_btn, border_radius=10)
        
        retry_surf = font_small.render("PLAY AGAIN", True, (255, 255, 255))
        screen.blit(retry_surf, (330, 372))
        
        if mouse_clicked and retry_btn.collidepoint(mouse_pos):
            game_state = "MENU"

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
