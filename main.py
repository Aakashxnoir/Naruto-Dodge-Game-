import pygame
import random
import sys
import math
import json
import os

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
DARK_GREEN = (0, 100, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

class Particle:
    def __init__(self, x, y, color, velocity, life):
        self.x = x
        self.y = y
        self.color = color
        self.vx, self.vy = velocity
        self.life = life
        self.max_life = life
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.vx *= 0.98  # Friction
        self.vy *= 0.98
    
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            size = max(1, int(3 * (self.life / self.max_life)))
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

class PowerUp:
    def __init__(self, x, y, power_type):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.type = power_type  # 'speed', 'shield', 'slow_time'
        self.animation = 0
        self.colors = {
            'speed': CYAN,
            'shield': BLUE,
            'slow_time': PURPLE
        }
    
    def update(self):
        self.animation += 0.3
    
    def draw(self, screen):
        center_x = self.rect.x + self.rect.width // 2
        center_y = self.rect.y + self.rect.height // 2
        
        # Pulsing effect
        size = int(15 + 5 * math.sin(self.animation))
        pygame.draw.circle(screen, self.colors[self.type], (center_x, center_y), size)
        pygame.draw.circle(screen, WHITE, (center_x, center_y), size - 5)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 6
        self.color = ORANGE  # Naruto's orange color
        self.animation_frame = 0
        self.shield_active = False
        self.shield_timer = 0
        self.speed_boost = False
        self.speed_timer = 0
        self.slow_time = False
        self.slow_timer = 0
    
    def move(self, keys):
        current_speed = self.speed
        if self.speed_boost:
            current_speed *= 1.5
        
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= current_speed
        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.rect.width:
            self.rect.x += current_speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= current_speed
        if keys[pygame.K_DOWN] and self.rect.y < SCREEN_HEIGHT - self.rect.height:
            self.rect.y += current_speed
    
    def update_powerups(self):
        # Update shield timer
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False
        
        # Update speed boost timer
        if self.speed_boost:
            self.speed_timer -= 1
            if self.speed_timer <= 0:
                self.speed_boost = False
        
        # Update slow time timer
        if self.slow_time:
            self.slow_timer -= 1
            if self.slow_timer <= 0:
                self.slow_time = False
    
    def draw(self, screen):
        # Draw ninja body with animation
        self.animation_frame += 0.2
        center_x = self.rect.x + self.rect.width // 2
        center_y = self.rect.y + self.rect.height // 2
        
        # Draw shield effect
        if self.shield_active:
            shield_radius = 25 + int(5 * math.sin(self.animation_frame * 2))
            pygame.draw.circle(screen, BLUE, (center_x, center_y), shield_radius, 3)
        
        # Main body
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Head
        head_radius = 12
        head_y_offset = int(math.sin(self.animation_frame) * 2)
        pygame.draw.circle(screen, WHITE, (center_x, center_y - 15 + head_y_offset), head_radius)
        
        # Eyes
        eye_offset = 3
        pygame.draw.circle(screen, BLACK, (center_x - eye_offset, center_y - 15 + head_y_offset), 2)
        pygame.draw.circle(screen, BLACK, (center_x + eye_offset, center_y - 15 + head_y_offset), 2)
        
        # Ninja headband
        pygame.draw.rect(screen, BLUE, (center_x - 8, center_y - 20 + head_y_offset, 16, 3))
        
        # Arms (simple lines)
        arm_length = 15
        pygame.draw.line(screen, WHITE, (center_x, center_y), 
                        (center_x - arm_length, center_y + 10), 3)
        pygame.draw.line(screen, WHITE, (center_x, center_y), 
                        (center_x + arm_length, center_y + 10), 3)
        
        # Speed boost effect
        if self.speed_boost:
            for i in range(3):
                trail_x = center_x + random.randint(-20, 20)
                trail_y = center_y + random.randint(-20, 20)
                pygame.draw.circle(screen, CYAN, (trail_x, trail_y), 2)

class Projectile:
    def __init__(self, x, y, direction, speed, color, projectile_type):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.direction = direction  # 'down', 'left', 'right'
        self.speed = speed
        self.color = color
        self.type = projectile_type  # 'kunai', 'fireball', 'shuriken'
        self.rotation = 0
    
    def update(self):
        if self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
        
        # Rotate projectiles for visual effect
        self.rotation += 10
    
    def draw(self, screen):
        center_x = self.rect.x + self.rect.width // 2
        center_y = self.rect.y + self.rect.height // 2
        
        if self.type == 'kunai':
            # Draw kunai (throwing knife)
            pygame.draw.polygon(screen, self.color, [
                (center_x, self.rect.y),
                (self.rect.x, center_y),
                (center_x, self.rect.y + self.rect.height),
                (self.rect.x + self.rect.width, center_y)
            ])
        elif self.type == 'fireball':
            # Draw fireball
            pygame.draw.circle(screen, self.color, (center_x, center_y), 10)
            # Add flame effect
            for i in range(3):
                flame_x = center_x + random.randint(-5, 5)
                flame_y = center_y + random.randint(-5, 5)
                pygame.draw.circle(screen, YELLOW, (flame_x, flame_y), 3)
        elif self.type == 'shuriken':
            # Draw shuriken (star)
            points = []
            for i in range(8):
                angle = (self.rotation + i * 45) * math.pi / 180
                radius = 8 if i % 2 == 0 else 4
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((x, y))
            pygame.draw.polygon(screen, self.color, points)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dodge Like Naruto")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.title_font = pygame.font.Font(None, 96)
        
        self.state = MENU
        self.high_score = self.load_high_score()
        self.particles = []
        self.powerups = []
        self.powerup_timer = 0
        self.powerup_delay = 300  # frames between powerup spawns
        
        self.reset_game()
    
    def load_high_score(self):
        try:
            if os.path.exists('high_score.json'):
                with open('high_score.json', 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except:
            pass
        return 0
    
    def save_high_score(self):
        try:
            with open('high_score.json', 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except:
            pass
    
    def reset_game(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.projectiles = []
        self.score = 0
        self.game_over = False
        self.spawn_timer = 0
        self.spawn_delay = 60  # frames between spawns
        self.particles = []
        self.powerups = []
        self.powerup_timer = 0
    
    def spawn_projectile(self):
        direction = random.choice(['down', 'left', 'right'])
        projectile_type = random.choice(['kunai', 'fireball', 'shuriken'])
        
        # Assign colors based on projectile type
        if projectile_type == 'kunai':
            color = random.choice([RED, BLUE])
        elif projectile_type == 'fireball':
            color = random.choice([RED, ORANGE, YELLOW])
        else:  # shuriken
            color = random.choice([PURPLE, CYAN, DARK_GREEN])
        
        speed = random.randint(3, 8)
        
        if direction == 'down':
            x = random.randint(0, SCREEN_WIDTH - 20)
            y = -20
        elif direction == 'left':
            x = SCREEN_WIDTH
            y = random.randint(0, SCREEN_HEIGHT - 20)
        else:  # right
            x = -20
            y = random.randint(0, SCREEN_HEIGHT - 20)
        
        self.projectiles.append(Projectile(x, y, direction, speed, color, projectile_type))
    
    def spawn_powerup(self):
        powerup_type = random.choice(['speed', 'shield', 'slow_time'])
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        self.powerups.append(PowerUp(x, y, powerup_type))
    
    def create_particles(self, x, y, color, count=5):
        for _ in range(count):
            vx = random.randint(-5, 5)
            vy = random.randint(-5, 5)
            life = random.randint(20, 40)
            self.particles.append(Particle(x, y, color, (vx, vy), life))
    
    def update(self):
        if self.state != PLAYING:
            return
        
        # Spawn projectiles
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_projectile()
            self.spawn_timer = 0
            # Increase difficulty over time
            if self.spawn_delay > 20:
                self.spawn_delay -= 1
        
        # Spawn powerups
        self.powerup_timer += 1
        if self.powerup_timer >= self.powerup_delay:
            self.spawn_powerup()
            self.powerup_timer = 0
        
        # Update player
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.player.update_powerups()
        
        # Update projectiles with slow time effect
        speed_multiplier = 0.5 if self.player.slow_time else 1.0
        for projectile in self.projectiles[:]:
            projectile.update()
            
            # Apply slow time effect
            if self.player.slow_time:
                projectile.speed = max(1, projectile.speed * 0.5)
            
            # Remove projectiles that are off-screen
            if (projectile.rect.y > SCREEN_HEIGHT or 
                projectile.rect.x > SCREEN_WIDTH or 
                projectile.rect.x < -20):
                self.projectiles.remove(projectile)
            
            # Check collision with player
            if self.player.rect.colliderect(projectile.rect):
                if self.player.shield_active:
                    # Shield absorbs the hit
                    self.create_particles(projectile.rect.centerx, projectile.rect.centery, BLUE, 8)
                    self.projectiles.remove(projectile)
                else:
                    self.game_over = True
                    self.state = GAME_OVER
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.save_high_score()
        
        # Update powerups
        for powerup in self.powerups[:]:
            powerup.update()
            if self.player.rect.colliderect(powerup.rect):
                self.collect_powerup(powerup)
                self.powerups.remove(powerup)
        
        # Update particles
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
        
        # Update score
        self.score += 1
    
    def collect_powerup(self, powerup):
        self.create_particles(powerup.rect.centerx, powerup.rect.centery, GOLD, 10)
        
        if powerup.type == 'speed':
            self.player.speed_boost = True
            self.player.speed_timer = 300  # 5 seconds at 60 FPS
        elif powerup.type == 'shield':
            self.player.shield_active = True
            self.player.shield_timer = 600  # 10 seconds at 60 FPS
        elif powerup.type == 'slow_time':
            self.player.slow_time = True
            self.player.slow_timer = 300  # 5 seconds at 60 FPS
    
    def draw_menu(self):
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.title_font.render("DODGE LIKE NARUTO", True, ORANGE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(title_text, title_rect)
        
        # High score
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, GOLD)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(high_score_text, high_score_rect)
        
        # Instructions
        start_text = self.font.render("Press SPACE to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        self.screen.blit(start_text, start_rect)
        
        controls_text = self.font.render("Arrow Keys: Move | Collect Power-ups!", True, YELLOW)
        controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
        self.screen.blit(controls_text, controls_rect)
        
        # Power-up descriptions
        powerup_text = self.font.render("Power-ups: Speed (Cyan) | Shield (Blue) | Slow Time (Purple)", True, CYAN)
        powerup_rect = powerup_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        self.screen.blit(powerup_text, powerup_rect)
    
    def draw_game(self):
        # Draw animated background
        self.screen.fill(BLACK)
        
        # Add some background stars for atmosphere
        for i in range(20):
            x = (i * 40 + self.score // 10) % SCREEN_WIDTH
            y = (i * 30 + self.score // 5) % SCREEN_HEIGHT
            pygame.draw.circle(self.screen, WHITE, (x, y), 1)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw powerups
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw score with better styling
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect()
        pygame.draw.rect(self.screen, (0, 0, 0, 128), score_rect.inflate(10, 5))
        self.screen.blit(score_text, (10, 10))
        
        # Draw high score
        high_score_text = self.font.render(f"High: {self.high_score}", True, GOLD)
        self.screen.blit(high_score_text, (10, 50))
        
        # Draw power-up status
        if self.player.shield_active:
            shield_text = self.font.render(f"Shield: {self.player.shield_timer//60}s", True, BLUE)
            self.screen.blit(shield_text, (10, 90))
        if self.player.speed_boost:
            speed_text = self.font.render(f"Speed Boost: {self.player.speed_timer//60}s", True, CYAN)
            self.screen.blit(speed_text, (10, 130))
        if self.player.slow_time:
            slow_text = self.font.render(f"Slow Time: {self.player.slow_timer//60}s", True, PURPLE)
            self.screen.blit(slow_text, (10, 170))
        
        # Draw instructions
        if self.score < 100:  # Show instructions for first 100 points
            instruction_text = self.font.render("Use Arrow Keys to Move!", True, YELLOW)
            self.screen.blit(instruction_text, (10, 210))
    
    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.big_font.render("GAME OVER", True, RED)
        final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        
        # Check if new high score
        if self.score >= self.high_score:
            new_high_text = self.font.render("NEW HIGH SCORE!", True, GOLD)
            new_high_rect = new_high_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
            self.screen.blit(new_high_text, new_high_rect)
        
        restart_text = self.font.render("Press R to Restart or ESC to Quit", True, YELLOW)
        menu_text = self.font.render("Press M for Main Menu", True, CYAN)
        
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(final_score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(menu_text, menu_rect)
    
    def draw(self):
        if self.state == MENU:
            self.draw_menu()
        elif self.state == PLAYING:
            self.draw_game()
        elif self.state == GAME_OVER:
            self.draw_game_over()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE and self.state == MENU:
                    self.state = PLAYING
                    self.reset_game()
                elif event.key == pygame.K_r and self.state == GAME_OVER:
                    self.state = PLAYING
                    self.reset_game()
                elif event.key == pygame.K_m and self.state == GAME_OVER:
                    self.state = MENU
        return True
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
