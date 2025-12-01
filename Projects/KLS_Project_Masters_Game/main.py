# main.py
import asyncio # Essential for the web!
import pygame
import random

# Initialize Pygame
pygame.init()

# --- SETUP ---
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Potato Dog Web Adventure")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 50)

# --- LOAD IMAGES (Make sure these are in the same folder!) ---
# If you don't have images yet, we will draw colorful rectangles instead
try:
    dog_img = pygame.image.load("images/dog.png")
    virus_img = pygame.image.load("images/virus.png")
    num67_img = pygame.image.load("images/num67.png")
except:
    # Fallback if images are missing: Draw rectangles
    dog_img = pygame.Surface((50, 30)); dog_img.fill((200, 150, 100))
    virus_img = pygame.Surface((40, 40)); virus_img.fill((0, 255, 0))
    num67_img = pygame.Surface((40, 40)); num67_img.fill((255, 0, 0))

# Game Variables
dog_rect = dog_img.get_rect(topleft=(100, 300))
virus_rect = virus_img.get_rect(topleft=(900, 200))
enemy67_rect = num67_img.get_rect(topleft=(1000, 400))

marbles = 10
game_state = "play"
current_q = {}

# Quiz Data
quiz_data = [
    {"q": "What has keys but no locks?", "a": "Piano", "b": "Banana", "correct": "a"},
    {"q": "Is a tomato a fruit?", "a": "No", "b": "Yes", "correct": "b"},
    {"q": "Why is 6 afraid of 7?", "a": "7 8 9", "b": "7 is mean", "correct": "a"}
]

# --- MAIN LOOP ---
# The 'async' keyword is the magic that lets it run in a browser
async def main():
    global marbles, game_state, current_q
    
    running = True
    while running:
        # 1. Handle Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state == "quiz" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if current_q["correct"] == "a": marbles += 5
                    else: marbles -= 5
                    game_state = "play"
                if event.key == pygame.K_2:
                    if current_q["correct"] == "b": marbles += 5
                    else: marbles -= 5
                    game_state = "play"

        # 2. Movement (Only in play mode)
        if game_state == "play":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: dog_rect.x -= 5
            if keys[pygame.K_RIGHT]: dog_rect.x += 5
            if keys[pygame.K_UP]: dog_rect.y -= 5
            if keys[pygame.K_DOWN]: dog_rect.y += 5

            # Move Enemies
            virus_rect.x -= 4
            enemy67_rect.x -= 6

            # Reset Enemies
            if virus_rect.right < 0:
                virus_rect.x = WIDTH + random.randint(0, 200)
                virus_rect.y = random.randint(50, 500)
            if enemy67_rect.right < 0:
                enemy67_rect.x = WIDTH + random.randint(0, 200)
                enemy67_rect.y = random.randint(50, 500)

            # Check Collisions
            if dog_rect.colliderect(virus_rect) or dog_rect.colliderect(enemy67_rect):
                game_state = "quiz"
                current_q = random.choice(quiz_data)
                # Reset positions so we don't hit immediately again
                virus_rect.x += 300
                enemy67_rect.x += 300

        # 3. Draw Everything
        screen.fill((210, 180, 140)) # Paper color background

        if game_state == "play":
            screen.blit(dog_img, dog_rect)
            screen.blit(virus_img, virus_rect)
            screen.blit(num67_img, enemy67_rect)
            
            score_text = font.render(f"Marbles: {marbles}", True, (0,0,0))
            screen.blit(score_text, (WIDTH - 180, 20))

        elif game_state == "quiz":
            # Draw simple quiz box
            pygame.draw.rect(screen, (50, 50, 50), (100, 100, 600, 400))
            
            title = big_font.render("QUIZ TIME!", True, (255, 255, 0))
            q_text = font.render(current_q["q"], True, (255, 255, 255))
            a_text = font.render(f"[1] {current_q['a']}", True, (0, 255, 255))
            b_text = font.render(f"[2] {current_q['b']}", True, (255, 165, 0))
            
            screen.blit(title, (300, 120))
            screen.blit(q_text, (150, 200))
            screen.blit(a_text, (150, 300))
            screen.blit(b_text, (150, 350))

        pygame.display.update()
        clock.tick(60)
        
        # This line is REQUIRED for the web browser to breathe!
        await asyncio.sleep(0)

# Run the magic
asyncio.run(main())