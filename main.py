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

# --- THE ANT TEMPLATE ---
class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 25 # Click hitbox size
        self.is_squished = False
        self.squish_timer = 30 # How many frames to stay dead before vanishing

    # --- TEAMMATE'S WORK AREA (MOTION) ---
    # Your teammate will add variables like speed and angle here
        self.speed = 2

    def draw(self, surface):
        # --- YOUR WORK AREA (THEME & VISUALS) ---
        # Right now, this draws simple shapes.
        # You will change this to draw images/sprites later today!
        if not self.is_squished:
            pygame.draw.circle(surface, (0, 0, 0), (int(self.x), int(self.y)), self.radius) # Black circle = Live Ant
        else:
            pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), self.radius) # Red circle = Dead Ant

    def update(self):
        if self.is_squished:
            self.squish_timer -= 1
            return

        # --- TEAMMATE'S WORK AREA (MOTION) ---
        # Your teammate will write the movement logic here.
        # Fallback placeholder to show it works:
        self.y += self.speed



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
            ants_list.append(Ant(random.randint(50, SCREEN_WIDTH - 50), 50))

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click or screen tap
            mouse_x, mouse_y = event.pos
            for ant in ants_list:
                if not ant.is_squished:
                    # Math to check if your click hit the circle
                    distance = ((mouse_x - ant.x)**2 + (mouse_y - ant.y)**2)**0.5
                    if distance < ant.radius:
                        ant.is_squished = True
                        score += 10

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