import pygame
import asyncio  # <--- NEW: Required for Web

# --- VARIABLES ---
# NEW: The Quiz Data
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

current_q_index = 0  # Tracks which question we are on

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

        # Draw button
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
        # Draw Text (Simple Font)
        font = pygame.font.SysFont(None, 40)
        img = font.render(self.text, True, (255, 255, 255))
        surface.blit(img, (self.rect.x + 10, self.rect.y + 10))

        # Check for Clicks
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
            self.vel_y = -25  # Jump Power
            self.is_jumping = True
            
    def update(self):
        # Gravity
        self.vel_y += 1
        self.rect.y += self.vel_y
        
        # Floor (Ground is at 500)
        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.is_jumping = False
            
    def draw(self, surface):
        surface.blit(self.image, self.rect)

async def main():        
    # 1. Initialize Pygame (Start the engine)
    pygame.init()
    pygame.mixer.init() # NEW: Initialize the Sound System

    # --- LOAD SOUNDS (With Safety Check) ---
    try:
        # If you have files, name them correct.wav and wrong.wav
        sfx_correct = pygame.mixer.Sound("assets/correct.wav")
        sfx_wrong = pygame.mixer.Sound("assets/wrong.wav")
    except (FileNotFoundError, pygame.error):
        print("Warning: Sound files not found. Sounds will be silent.")
        # We create a "dummy" sound object so the code doesn't crash later
        class DummySound:
            def play(self): pass
        sfx_correct = DummySound()
        sfx_wrong = DummySound()


    # 2. Set up the Screen
    # We create a window that is 800 pixels wide and 600 pixels tall
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    # 3. Name the Window
    pygame.display.set_caption("My Awesome Quiz")

    # --- LOAD ASSETS SECTION ---
    try:
        # Attempt to load ALL images from the disk
        dog_img = pygame.image.load("assets/dog.png")
        virus_img = pygame.image.load("assets/virus.png")
        btn_img = pygame.image.load("assets/button.png")
        print("Success: All images loaded from file.")

    except (FileNotFoundError, pygame.error):
        # If ANY image fails, fallback to placeholders for ALL of them
        print("Warning: One or more files missing. Using ALL color placeholders.")
        
        dog_img = pygame.Surface((50, 50))
        dog_img.fill((255, 200, 0)) # Yellow Dog

        virus_img = pygame.Surface((40, 40))
        virus_img.fill((0, 255, 0)) # Green Virus

        btn_img = pygame.Surface((200, 50))
        btn_img.fill((100, 100, 255)) # Blue Button



    # --- INSTANCES ---
    player = Player(100, 450, dog_img)

    # NEW: Create 4 buttons in a list
    # We use empty text "" for now, because the code will fill it in later!
    option_buttons = [
        Button(150, 200, btn_img, ""), # Top Left
        Button(450, 200, btn_img, ""), # Top Right
        Button(150, 350, btn_img, ""), # Bottom Left
        Button(450, 350, btn_img, "")  # Bottom Right
    ]



    # --- GAME LOOP ---
    obstacle_x = 600
    obstacle_y = 460
    score = 0
    current_q_index = 0
    game_state = "PLAYING"
        
    feedback_timer = 0
    feedback_message = ""
    feedback_color = (0,0,0)
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(60) # FPS Lock
        screen.fill((255, 255, 255)) # White Background  
    
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # NEW CONDITION
            # Jump Controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state == "PLAYING":
                    player.jump()
        
        # --- LOGIC BRANCHING ---
        
        if game_state == "PLAYING":
            # 1. Update Player
            player.update()
            player.draw(screen)
            
            # 2. Update Obstacle
            obstacle_x -= 6 # Speed
            if obstacle_x < -50:
                obstacle_x = 800 # Reset
                
            # Draw Obstacle
            screen.blit(virus_img, (obstacle_x, obstacle_y))
            
            # 3. Check Collision
            obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, 40, 40)
            
            # CHANGED: When we hit the obstacle
            if player.rect.colliderect(obstacle_rect):
                game_state = "QUIZ"
                
                # 1. Get the data for the current question
                current_data = quiz_data[current_q_index]
                
                # 2. Update the buttons with new text!
                # We use a loop to update all 4 buttons at once
                for i in range(4):
                    option_buttons[i].text = current_data["options"][i]

        elif game_state == "QUIZ":
            # Draw background elements (Player, Virus, Overlay) - SAME AS BEFORE
            player.draw(screen)
            screen.blit(virus_img, (obstacle_x, obstacle_y))
            
            overlay = pygame.Surface((800, 600))
            overlay.set_alpha(128)
            overlay.fill((0,0,0))
            screen.blit(overlay, (0,0))
            
            # NEW: Draw the Question Text at the top
            current_data = quiz_data[current_q_index]
            question_font = pygame.font.SysFont(None, 50)
            # Render the text (White color)
            q_surf = question_font.render(current_data["question"], True, (255, 255, 255))
            # Center the text
            screen.blit(q_surf, (800//2 - q_surf.get_width()//2, 100))

            # NEW: Draw Buttons and Check Answers
            # We assume the variable 'i' is the answer the user clicked (0, 1, 2, or 3)
            # NEW: Draw Buttons and Check Answers
            for i in range(4):
                if option_buttons[i].draw(screen):
                    
                    # 1. CHECK ANSWER
                    if i == current_data["correct_index"]:
                        score += 10
                        feedback_message = "CORRECT!"
                        feedback_color = (0, 255, 0) # Green
                        sfx_correct.play() # Play Sound
                    else:
                        score -= 5
                        feedback_message = "WRONG!"
                        feedback_color = (255, 0, 0) # Red
                        sfx_wrong.play() # Play Sound
                    
                    # 2. SWITCH TO RESULT STATE (The Delay)
                    game_state = "RESULT"
                    feedback_timer = 60 # Wait for 60 frames (approx 1 second)
            
        # --- NEW STATE: THE RESULT DELAY ---
        elif game_state == "RESULT":
            # 1. Draw the feedback background
            screen.fill(feedback_color)
            
            # 2. Draw the Player (so they don't disappear)
            player.draw(screen)
            
            # 3. Draw the big message
            font_big = pygame.font.SysFont(None, 80)
            msg_surf = font_big.render(feedback_message, True, (255, 255, 255))
            screen.blit(msg_surf, (800//2 - msg_surf.get_width()//2, 250))
            
            # 4. Count down the timer
            feedback_timer -= 1
            
            # 5. When time is up... move on!
            if feedback_timer <= 0:
                
                # Check if we have more questions?
                if current_q_index < len(quiz_data) - 1:
                    current_q_index += 1      # Next Question
                    obstacle_x = 800          # Reset Obstacle
                    game_state = "PLAYING"    # Resume Game
                else:
                    game_state = "GAME_OVER"  # No more questions!

        # --- NEW STATE: GAME OVER ---
        elif game_state == "GAME_OVER":
            screen.fill((50, 50, 100)) # Dark Blue background
            
            # Title
            font_huge = pygame.font.SysFont(None, 100)
            end_surf = font_huge.render("GAME OVER", True, (255, 255, 255))
            screen.blit(end_surf, (200, 150))
            
            # Final Score
            font_med = pygame.font.SysFont(None, 60)
            score_surf = font_med.render(f"Final Score: {score}", True, (255, 200, 0))
            screen.blit(score_surf, (250, 300))
            
            # Optional: Code to restart? (Extension Task)


        
        # 3. Update Display
        pygame.display.flip()

    pygame.quit()
    
asyncio.run(main())