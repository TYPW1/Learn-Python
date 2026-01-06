import asyncio  # <--- NEW: Required for Web
import pygame

# --- GLOBAL DATA (Kept outside so it's easy to edit) ---
quiz_data = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Paris", "Berlin", "Rome"],
"correct_index": 1
},
    {
        "question": "Which animal barks?",
        "options": ["Cat", "Dog", "Fish", "Bird"],
"correct_index": 1
},
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "22"],
        "correct_index": 1
    }
]

class Button:
    def __init__(self, x, y, image, text):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.text = text
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
        font = pygame.font.SysFont(None, 40)
        img = font.render(self.text, True, (255, 255, 255))
        surface.blit(img, (self.rect.x + 10, self.rect.y + 10))

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        return action

class Player:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_y = 0
        self.is_jumping = False
    
    def jump(self):
        if not self.is_jumping:
            self.vel_y = -18
            self.is_jumping = True
            
    def update(self):
        self.vel_y += 1
        self.rect.y += self.vel_y
        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.is_jumping = False
            
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# --- THE MAIN ASYNC FUNCTION ---
async def main():
    pygame.init()
    pygame.mixer.init()

    # --- SETUP SCREEN ---
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Quiz Quest: Final Web Version")
    clock = pygame.time.Clock()

    # --- LOAD ASSETS ---
    try:
        dog_img = pygame.image.load("assets/dog.png")
        virus_img = pygame.image.load("assets/virus.png")
        btn_img = pygame.image.load("assets/button.png")
        sfx_correct = pygame.mixer.Sound("assets/correct.wav")
        sfx_wrong = pygame.mixer.Sound("assets/wrong.wav")
    except (FileNotFoundError, pygame.error):
        print("Warning: Assets missing. Using placeholders.")
        dog_img = pygame.Surface((50, 50)); dog_img.fill((255, 200, 0))
        virus_img = pygame.Surface((40, 40)); virus_img.fill((0, 255, 0))
        btn_img = pygame.Surface((200, 50)); btn_img.fill((100, 100, 255))
        class DummySound:
            def play(self): pass
        sfx_correct = DummySound(); 
        sfx_wrong = DummySound()

    # --- INSTANCES & VARIABLES ---
    player = Player(100, 450, dog_img)
    option_buttons = [
        Button(150, 200, btn_img, ""), 
        Button(450, 200, btn_img, ""),
        Button(150, 350, btn_img, ""), 
        Button(450, 350, btn_img, "")
    ]
    
    obstacle_x = 800
    obstacle_y = 460
    score = 0
    current_q_index = 0
    game_state = "PLAYING"
    
    feedback_timer = 0
    feedback_message = ""
    feedback_color = (0,0,0)

    # --- GAME LOOP ---
    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state == "PLAYING":
                    player.jump()

        screen.fill((255, 255, 255)) # Clear Screen

        # 2. Logic Branching
        if game_state == "PLAYING":
            player.update()
            player.draw(screen)
            
            obstacle_x -= 6
            if obstacle_x < -50: obstacle_x = 800
            screen.blit(virus_img, (obstacle_x, obstacle_y))
            
            obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, 40, 40)
            if player.rect.colliderect(obstacle_rect):
                game_state = "QUIZ"
                current_data = quiz_data[current_q_index]
                for i in range(4):
                    option_buttons[i].text = current_data["options"][i]

        elif game_state == "QUIZ":
            player.draw(screen)
            screen.blit(virus_img, (obstacle_x, obstacle_y))
            
            # Draw Overlay
            overlay = pygame.Surface((800, 600))
            overlay.set_alpha(128); overlay.fill((0,0,0))
            screen.blit(overlay, (0,0))
            
            # Draw Question
            current_data = quiz_data[current_q_index]
            font = pygame.font.SysFont(None, 50)
            q_surf = font.render(current_data["question"], True, (255, 255, 255))
            screen.blit(q_surf, (800//2 - q_surf.get_width()//2, 100))

            # Draw Buttons
            for i in range(4):
                if option_buttons[i].draw(screen):
                    if i == current_data["correct_index"]:
                        score += 10
                        feedback_message = "CORRECT!"
                        feedback_color = (0, 255, 0)
                        sfx_correct.play()
                    else:
                        score -= 5
                        feedback_message = "WRONG!"
                        feedback_color = (255, 0, 0)
                        sfx_wrong.play()
                    
                    game_state = "RESULT"
                    feedback_timer = 60

        elif game_state == "RESULT":
            screen.fill(feedback_color)
            player.draw(screen)
            font_big = pygame.font.SysFont(None, 80)
            msg_surf = font_big.render(feedback_message, True, (255, 255, 255))
            screen.blit(msg_surf, (800//2 - msg_surf.get_width()//2, 250))
            
            feedback_timer -= 1
            if feedback_timer <= 0:
                if current_q_index < len(quiz_data) - 1:
                    current_q_index += 1
                    obstacle_x = 800
                    game_state = "PLAYING"
                else:
                    game_state = "GAME_OVER"

        elif game_state == "GAME_OVER":
            screen.fill((50, 50, 100))
            font_huge = pygame.font.SysFont(None, 100)
            end_surf = font_huge.render("GAME OVER", True, (255, 255, 255))
            screen.blit(end_surf, (200, 150))
            font_med = pygame.font.SysFont(None, 60)
            score_surf = font_med.render(f"Final Score: {score}", True, (255, 200, 0))
            screen.blit(score_surf, (250, 300))

        pygame.display.flip()
        clock.tick(60)
        
        # --- THE WEB SECRET ---
        await asyncio.sleep(0) # Lets the browser breathe

pygame.quit()

# --- EXECUTE THE GAME ---
asyncio.run(main())