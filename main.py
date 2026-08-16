import pygame
import random
import sys

# --- GAME ENGINE INITIALIZATION ---
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ant Smasher")
clock = pygame.time.Clock()

# --- GAME STATE DATA ---
score = 0
font = pygame.font.SysFont("Arial", 36)
ants_list = []
base_ant_speed = 2.0  # Start with a speed of 2. Use a float for smoother increases.
score_for_next_speed_increase = 20 # Increase speed every 100 points

# --- THE ANT TEMPLATE ---
class Ant:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.radius = 25 # Click hitbox size
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
            pygame.draw.circle(surface, (0, 0, 0), (int(self.x), int(self.y)), self.radius) # Black circle = Live Ant
        else:
            pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), self.radius) # Red circle = Dead Ant

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


# --- GAME MANAGEMENT EVENTS ---
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1500) # Spawn a temporary ant every 1.5 seconds

# --- THE MAIN GAME LOOP ---
running = True
while running:
    # 1. CHECK FOR INPUT / TAPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == SPAWN_EVENT and len(ants_list) < 8:
            ants_list.append(Ant(random.randint(50, SCREEN_WIDTH - 50), 50, base_ant_speed))

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click or screen tap
            mouse_x, mouse_y = event.pos
            for ant in ants_list:
                if not ant.is_squished:
                    # Math to check if your click hit the circle
                    distance = ((mouse_x - ant.x)**2 + (mouse_y - ant.y)**2)**0.5
                    if distance < ant.radius:
                        ant.is_squished = True
                        score += 10
    if(score >= score_for_next_speed_increase):
        base_ant_speed += 0.125
        score_for_next_speed_increase += 10
    # 2. MOVE THINGS
    for ant in ants_list[:]:
        ant.update()
        if ant.is_squished and ant.squish_timer <= 0:
            ants_list.remove(ant)

    # 3. DRAW EVERYTHING (YOUR THEME LAYER)
    screen.fill((215, 161, 92)) # Default background color (Sandy Picnic Table Wood)

# Draw all ants
    for ant in ants_list:
        ant.draw(screen)

    # Draw Score UI text
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (20, 20))

    pygame.display.flip()
    clock.tick(60) # Run at 60 frames per second

pygame.quit()
sys.exit()