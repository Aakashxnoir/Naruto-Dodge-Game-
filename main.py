import pygame
import random
import sys
import math
import json
import os
import time

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Game constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
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
DARK_BLUE = (0, 0, 139)
LIGHT_BLUE = (173, 216, 230)
PINK = (255, 192, 203)
DARK_RED = (139, 0, 0)
LIGHT_GREEN = (144, 238, 144)
DARK_PURPLE = (75, 0, 130)
LIGHT_YELLOW = (255, 255, 224)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
PAUSED = 3
SETTINGS = 4
LEVEL_SELECT = 5
SPLASH = 6

# Sound system
class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_enabled = True
        self.sound_enabled = True
        self.init_sounds()
    
    def init_sounds(self):
        """Initialize sound effects (placeholder for actual sound files)"""
        # In a real implementation, you would load actual sound files here
        # For now, we'll create placeholder sounds using pygame's built-in sounds
        try:
            # Create simple beep sounds for different events
            self.sounds['collect'] = self.create_beep_sound(440, 0.1)  # A note
            self.sounds['hit'] = self.create_beep_sound(220, 0.2)      # Low A
            self.sounds['dash'] = self.create_beep_sound(880, 0.05)    # High A
            self.sounds['level_up'] = self.create_beep_sound(660, 0.3) # E note
            self.sounds['game_over'] = self.create_beep_sound(110, 0.5) # Very low A
        except:
            # If sound creation fails, disable sounds
            self.sound_enabled = False
    
    def create_beep_sound(self, frequency, duration):
        """Create a simple beep sound"""
        try:
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                time = float(i) / sample_rate
                wave = 4096 * math.sin(frequency * 2 * math.pi * time)
                arr.append([int(wave), int(wave)])
            sound = pygame.sndarray.make_sound(pygame.array.array('i', arr))
            return sound
        except:
            return None
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if self.sound_enabled and sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except:
                pass
    
    def toggle_sound(self):
        """Toggle sound effects on/off"""
        self.sound_enabled = not self.sound_enabled
    
    def toggle_music(self):
        """Toggle background music on/off"""
        self.music_enabled = not self.music_enabled

# Global sound manager
sound_manager = SoundManager()

class Particle:
    def __init__(self, x, y, color, velocity, life, particle_type="circle", size=3):
        self.x = x
        self.y = y
        self.color = color
        self.vx, self.vy = velocity
        self.life = life
        self.max_life = life
        self.type = particle_type
        self.size = size
        self.rotation = 0
        self.gravity = 0.1 if particle_type == "spark" else 0
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.vx *= 0.98  # Friction
        self.vy *= 0.98
        self.vy += self.gravity  # Gravity for sparks
        self.rotation += 5
    
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            size = max(1, int(self.size * (self.life / self.max_life)))
            
            if self.type == "circle":
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)
            elif self.type == "spark":
                # Draw spark as a line
                end_x = self.x + math.cos(self.rotation * math.pi / 180) * size
                end_y = self.y + math.sin(self.rotation * math.pi / 180) * size
                pygame.draw.line(screen, self.color, (int(self.x), int(self.y)), 
                               (int(end_x), int(end_y)), 2)
            elif self.type == "star":
                # Draw star particle
                points = []
                for i in range(5):
                    angle = (self.rotation + i * 72) * math.pi / 180
                    radius = size if i % 2 == 0 else size // 2
                    x = self.x + radius * math.cos(angle)
                    y = self.y + radius * math.sin(angle)
                    points.append((x, y))
                if len(points) >= 3:
                    pygame.draw.polygon(screen, self.color, points)

class PowerUp:
    def __init__(self, x, y, power_type):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.type = power_type  # 'speed', 'shield', 'slow_time', 'multi_shot', 'health', 'invincible'
        self.animation = 0
        self.rotation = 0
        self.colors = {
            'speed': CYAN,
            'shield': BLUE,
            'slow_time': PURPLE,
            'multi_shot': YELLOW,
            'health': GREEN,
            'invincible': GOLD
        }
        self.symbols = {
            'speed': '⚡',
            'shield': '🛡️',
            'slow_time': '⏰',
            'multi_shot': '💥',
            'health': '❤️',
            'invincible': '✨'
        }
    
    def update(self):
        self.animation += 0.3
        self.rotation += 2
    
    def draw(self, screen):
        center_x = self.rect.x + self.rect.width // 2
        center_y = self.rect.y + self.rect.height // 2
        
        # Pulsing effect
        size = int(18 + 6 * math.sin(self.animation))
        
        # Draw outer glow
        pygame.draw.circle(screen, self.colors[self.type], (center_x, center_y), size + 3)
        pygame.draw.circle(screen, WHITE, (center_x, center_y), size)
        
        # Draw inner symbol area
        inner_size = size - 8
        pygame.draw.circle(screen, BLACK, (center_x, center_y), inner_size)
        
        # Draw rotating symbol
        if self.type in ['speed', 'multi_shot']:
            # Draw lightning bolt for speed
            points = [
                (center_x - 3, center_y - 8),
                (center_x + 3, center_y - 8),
                (center_x + 1, center_y - 2),
                (center_x + 4, center_y - 2),
                (center_x - 2, center_y + 8),
                (center_x - 4, center_y + 2),
                (center_x - 1, center_y + 2)
            ]
            pygame.draw.polygon(screen, self.colors[self.type], points)
        elif self.type == 'shield':
            # Draw shield
            pygame.draw.circle(screen, self.colors[self.type], (center_x, center_y), inner_size - 2, 3)
            pygame.draw.circle(screen, self.colors[self.type], (center_x, center_y), inner_size - 6)
        elif self.type == 'slow_time':
            # Draw clock
            pygame.draw.circle(screen, self.colors[self.type], (center_x, center_y), inner_size - 2, 3)
            # Clock hands
            hand_length = inner_size - 4
            pygame.draw.line(screen, self.colors[self.type], (center_x, center_y), 
                           (center_x, center_y - hand_length), 2)
            pygame.draw.line(screen, self.colors[self.type], (center_x, center_y), 
                           (center_x + hand_length//2, center_y), 2)
        elif self.type == 'health':
            # Draw heart
            heart_points = [
                (center_x, center_y + 6),
                (center_x - 6, center_y),
                (center_x - 3, center_y - 3),
                (center_x, center_y),
                (center_x + 3, center_y - 3),
                (center_x + 6, center_y)
            ]
            pygame.draw.polygon(screen, self.colors[self.type], heart_points)
        elif self.type == 'invincible':
            # Draw star
            points = []
            for i in range(8):
                angle = (self.rotation + i * 45) * math.pi / 180
                radius = inner_size - 2 if i % 2 == 0 else inner_size - 6
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((x, y))
            pygame.draw.polygon(screen, self.colors[self.type], points)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.speed = 6
        self.color = ORANGE  # Naruto's orange color
        self.animation_frame = 0
        self.shield_active = False
        self.shield_timer = 0
        self.speed_boost = False
        self.speed_timer = 0
        self.slow_time = False
        self.slow_timer = 0
        self.multi_shot = False
        self.multi_shot_timer = 0
        self.health = 3
        self.max_health = 3
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_flash = 0
        self.dash_cooldown = 0
        self.dash_timer = 0
        self.is_dashing = False
        self.special_attack_cooldown = 0
        self.special_attack_timer = 0
        self.is_using_special = False
        self.dash_count = 0
    
    def move(self, keys):
        current_speed = self.speed
        if self.speed_boost:
            current_speed *= 1.5
        if self.is_dashing:
            current_speed *= 2.0
        
        # Handle dash
        if keys[pygame.K_SPACE] and self.dash_cooldown <= 0 and not self.is_dashing:
            self.is_dashing = True
            self.dash_timer = 10  # Dash for 10 frames
            self.dash_cooldown = 60  # 1 second cooldown
            # Track dash count for achievements
            self.dash_count += 1
            sound_manager.play_sound('dash')
        
        # Update dash
        if self.is_dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
        
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        
        # Handle special attack
        if keys[pygame.K_x] and self.special_attack_cooldown <= 0 and not self.is_using_special:
            self.is_using_special = True
            self.special_attack_timer = 30  # Special attack lasts 30 frames
            self.special_attack_cooldown = 300  # 5 second cooldown
        
        # Update special attack
        if self.is_using_special:
            self.special_attack_timer -= 1
            if self.special_attack_timer <= 0:
                self.is_using_special = False
        
        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1
        
        # Movement with diagonal support
        dx = 0
        dy = 0
        
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            dx -= current_speed
        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.rect.width:
            dx += current_speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            dy -= current_speed
        if keys[pygame.K_DOWN] and self.rect.y < SCREEN_HEIGHT - self.rect.height:
            dy += current_speed
        
        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.707  # 1/sqrt(2)
            dy *= 0.707
        
        self.rect.x += dx
        self.rect.y += dy
    
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
        
        # Update multi shot timer
        if self.multi_shot:
            self.multi_shot_timer -= 1
            if self.multi_shot_timer <= 0:
                self.multi_shot = False
        
        # Update invincible timer
        if self.invincible:
            self.invincible_timer -= 1
            self.invincible_flash += 1
            if self.invincible_timer <= 0:
                self.invincible = False
    
    def draw(self, screen):
        # Draw ninja body with animation
        self.animation_frame += 0.2
        center_x = self.rect.x + self.rect.width // 2
        center_y = self.rect.y + self.rect.height // 2
        
        # Invincible flash effect
        if self.invincible and self.invincible_flash % 10 < 5:
            return  # Skip drawing during flash
        
        # Draw shield effect
        if self.shield_active:
            shield_radius = 30 + int(8 * math.sin(self.animation_frame * 3))
            pygame.draw.circle(screen, BLUE, (center_x, center_y), shield_radius, 4)
            pygame.draw.circle(screen, LIGHT_BLUE, (center_x, center_y), shield_radius - 4, 2)
        
        # Dash effect
        if self.is_dashing:
            for i in range(5):
                trail_x = center_x + random.randint(-30, 30)
                trail_y = center_y + random.randint(-30, 30)
                pygame.draw.circle(screen, WHITE, (trail_x, trail_y), 3)
        
        # Special attack effect
        if self.is_using_special:
            # Create a powerful aura around the player
            aura_radius = 40 + int(10 * math.sin(self.animation_frame * 5))
            pygame.draw.circle(screen, GOLD, (center_x, center_y), aura_radius, 4)
            pygame.draw.circle(screen, YELLOW, (center_x, center_y), aura_radius - 8, 2)
            
            # Energy particles
            for i in range(8):
                angle = (self.animation_frame * 2 + i * 45) * math.pi / 180
                particle_x = center_x + math.cos(angle) * (aura_radius + 10)
                particle_y = center_y + math.sin(angle) * (aura_radius + 10)
                pygame.draw.circle(screen, YELLOW, (int(particle_x), int(particle_y)), 3)
        
        # Main body with gradient effect
        body_rect = self.rect.copy()
        body_rect.inflate(-5, -5)
        pygame.draw.rect(screen, self.color, body_rect)
        pygame.draw.rect(screen, LIGHT_YELLOW, body_rect, 2)
        
        # Head with better proportions
        head_radius = 15
        head_y_offset = int(math.sin(self.animation_frame) * 3)
        head_center = (center_x, center_y - 18 + head_y_offset)
        pygame.draw.circle(screen, WHITE, head_center, head_radius)
        pygame.draw.circle(screen, LIGHT_GRAY, head_center, head_radius - 2)
        
        # Eyes with expression
        eye_offset = 4
        eye_y = head_center[1] - 2
        pygame.draw.circle(screen, BLACK, (head_center[0] - eye_offset, eye_y), 3)
        pygame.draw.circle(screen, BLACK, (head_center[0] + eye_offset, eye_y), 3)
        pygame.draw.circle(screen, WHITE, (head_center[0] - eye_offset + 1, eye_y - 1), 1)
        pygame.draw.circle(screen, WHITE, (head_center[0] + eye_offset + 1, eye_y - 1), 1)
        
        # Ninja headband with symbol
        headband_rect = pygame.Rect(head_center[0] - 12, head_center[1] - 18, 24, 4)
        pygame.draw.rect(screen, DARK_BLUE, headband_rect)
        pygame.draw.rect(screen, BLUE, headband_rect, 1)
        
        # Headband symbol (leaf village)
        symbol_points = [
            (head_center[0] - 3, head_center[1] - 16),
            (head_center[0], head_center[1] - 12),
            (head_center[0] + 3, head_center[1] - 16),
            (head_center[0] + 1, head_center[1] - 14),
            (head_center[0] - 1, head_center[1] - 14)
        ]
        pygame.draw.polygon(screen, WHITE, symbol_points)
        
        # Arms with better positioning
        arm_length = 18
        arm_angle = math.sin(self.animation_frame * 2) * 0.3
        left_arm_end = (center_x - arm_length * math.cos(arm_angle), 
                       center_y + 8 + arm_length * math.sin(arm_angle))
        right_arm_end = (center_x + arm_length * math.cos(arm_angle), 
                        center_y + 8 + arm_length * math.sin(arm_angle))
        
        pygame.draw.line(screen, WHITE, (center_x, center_y + 5), left_arm_end, 4)
        pygame.draw.line(screen, WHITE, (center_x, center_y + 5), right_arm_end, 4)
        
        # Legs
        leg_length = 20
        pygame.draw.line(screen, self.color, (center_x - 8, center_y + 20), 
                        (center_x - 8, center_y + 20 + leg_length), 4)
        pygame.draw.line(screen, self.color, (center_x + 8, center_y + 20), 
                        (center_x + 8, center_y + 20 + leg_length), 4)
        
        # Speed boost effect
        if self.speed_boost:
            for i in range(5):
                trail_x = center_x + random.randint(-25, 25)
                trail_y = center_y + random.randint(-25, 25)
                pygame.draw.circle(screen, CYAN, (trail_x, trail_y), 2)
        
        # Health indicator
        for i in range(self.health):
            heart_x = self.rect.x + 5 + i * 12
            heart_y = self.rect.y - 15
            heart_points = [
                (heart_x, heart_y + 3),
                (heart_x - 3, heart_y),
                (heart_x - 1.5, heart_y - 1.5),
                (heart_x, heart_y),
                (heart_x + 1.5, heart_y - 1.5),
                (heart_x + 3, heart_y)
            ]
            pygame.draw.polygon(screen, RED, heart_points)

class Enemy:
    def __init__(self, x, y, enemy_type):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.type = enemy_type  # 'ninja', 'boss', 'assassin'
        self.speed = 2
        self.health = 1
        self.animation = 0
        self.attack_timer = 0
        self.attack_delay = 120  # frames between attacks
        self.color = RED
        
        if enemy_type == 'ninja':
            self.speed = 2
            self.health = 1
            self.color = DARK_GREEN
        elif enemy_type == 'boss':
            self.rect = pygame.Rect(x, y, 60, 60)
            self.speed = 1
            self.health = 3
            self.color = DARK_RED
        elif enemy_type == 'assassin':
            self.speed = 4
            self.health = 1
            self.color = PURPLE
    
    def update(self, player_pos):
        # Move towards player
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed
            self.rect.x += dx
            self.rect.y += dy
        
        self.animation += 0.2
        self.attack_timer += 1
    
    def can_attack(self):
        return self.attack_timer >= self.attack_delay
    
    def attack(self):
        self.attack_timer = 0
        return True
    
    def draw(self, screen):
        center_x = self.rect.x + self.rect.width // 2
        center_y = self.rect.y + self.rect.height // 2
        
        # Draw enemy body
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Draw enemy head
        head_radius = 12
        head_y_offset = int(math.sin(self.animation) * 2)
        pygame.draw.circle(screen, WHITE, (center_x, center_y - 15 + head_y_offset), head_radius)
        
        # Draw eyes (angry)
        eye_offset = 3
        pygame.draw.circle(screen, RED, (center_x - eye_offset, center_y - 15 + head_y_offset), 2)
        pygame.draw.circle(screen, RED, (center_x + eye_offset, center_y - 15 + head_y_offset), 2)
        
        # Health indicator for bosses
        if self.type == 'boss' and self.health < 3:
            for i in range(self.health):
                health_x = self.rect.x + 5 + i * 15
                health_y = self.rect.y - 10
                pygame.draw.rect(screen, RED, (health_x, health_y, 10, 3))

class Projectile:
    def __init__(self, x, y, direction, speed, color, projectile_type):
        self.rect = pygame.Rect(x, y, 25, 25)
        self.direction = direction  # 'down', 'left', 'right'
        self.speed = speed
        self.color = color
        self.type = projectile_type  # 'kunai', 'fireball', 'shuriken', 'lightning', 'ice_shard', 'wind_blade'
        self.rotation = 0
        self.animation = 0
        self.trail = []  # For trail effects
    
    def update(self):
        # Store previous position for trail
        prev_pos = (self.rect.centerx, self.rect.centery)
        
        if self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
        
        # Update trail
        self.trail.append(prev_pos)
        if len(self.trail) > 5:
            self.trail.pop(0)
        
        # Rotate projectiles for visual effect
        self.rotation += 10
        self.animation += 0.3
    
    def draw(self, screen):
        center_x = self.rect.x + self.rect.width // 2
        center_y = self.rect.y + self.rect.height // 2
        
        # Draw trail effect
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            trail_size = max(1, int(3 * (i / len(self.trail))))
            pygame.draw.circle(screen, self.color, (int(trail_x), int(trail_y)), trail_size)
        
        if self.type == 'kunai':
            # Draw kunai (throwing knife) with better detail
            points = [
                (center_x, self.rect.y + 2),
                (center_x - 8, center_y),
                (center_x, self.rect.y + self.rect.height - 2),
                (center_x + 8, center_y)
            ]
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, DARK_GRAY, points, 2)
            # Blade tip
            pygame.draw.circle(screen, SILVER, (center_x, center_y), 3)
            
        elif self.type == 'fireball':
            # Draw fireball with better flame effects
            base_radius = 12
            pygame.draw.circle(screen, self.color, (center_x, center_y), base_radius)
            pygame.draw.circle(screen, YELLOW, (center_x, center_y), base_radius - 3)
            
            # Animated flame effect
            for i in range(6):
                angle = (self.animation * 2 + i * 60) * math.pi / 180
                flame_x = center_x + math.cos(angle) * (base_radius + 3)
                flame_y = center_y + math.sin(angle) * (base_radius + 3)
                flame_size = 4 + int(2 * math.sin(self.animation + i))
                pygame.draw.circle(screen, YELLOW, (int(flame_x), int(flame_y)), flame_size)
                
        elif self.type == 'shuriken':
            # Draw shuriken (star) with better detail
            points = []
            for i in range(8):
                angle = (self.rotation + i * 45) * math.pi / 180
                radius = 10 if i % 2 == 0 else 5
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((x, y))
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, DARK_GRAY, points, 2)
            # Center circle
            pygame.draw.circle(screen, DARK_GRAY, (center_x, center_y), 3)
            
        elif self.type == 'lightning':
            # Draw lightning bolt
            points = [
                (center_x - 6, self.rect.y),
                (center_x + 2, center_y - 5),
                (center_x - 2, center_y),
                (center_x + 6, center_y + 5),
                (center_x - 2, center_y + 10),
                (center_x + 2, center_y + 15),
                (center_x - 6, self.rect.y + self.rect.height)
            ]
            pygame.draw.lines(screen, self.color, False, points, 4)
            pygame.draw.lines(screen, YELLOW, False, points, 2)
            
        elif self.type == 'ice_shard':
            # Draw ice shard
            points = [
                (center_x, self.rect.y),
                (center_x - 6, center_y),
                (center_x, self.rect.y + self.rect.height),
                (center_x + 6, center_y)
            ]
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, WHITE, points, 2)
            # Ice sparkles
            for i in range(3):
                sparkle_x = center_x + random.randint(-8, 8)
                sparkle_y = center_y + random.randint(-8, 8)
                pygame.draw.circle(screen, WHITE, (sparkle_x, sparkle_y), 1)
                
        elif self.type == 'wind_blade':
            # Draw wind blade
            blade_length = 15
            angle = self.rotation * math.pi / 180
            end_x = center_x + blade_length * math.cos(angle)
            end_y = center_y + blade_length * math.sin(angle)
            pygame.draw.line(screen, self.color, (center_x, center_y), (end_x, end_y), 6)
            pygame.draw.line(screen, WHITE, (center_x, center_y), (end_x, end_y), 3)
            # Wind particles
            for i in range(4):
                wind_x = center_x + random.randint(-10, 10)
                wind_y = center_y + random.randint(-10, 10)
                pygame.draw.circle(screen, LIGHT_BLUE, (wind_x, wind_y), 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dodge Like Naruto - Enhanced Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)  # Increased from 36
        self.big_font = pygame.font.Font(None, 84)  # Increased from 72
        self.title_font = pygame.font.Font(None, 120)  # Increased from 96
        self.small_font = pygame.font.Font(None, 32)  # Increased from 24
        self.medium_font = pygame.font.Font(None, 40)  # New medium font
        self.large_font = pygame.font.Font(None, 60)  # New large font
        
        self.state = SPLASH
        self.splash_timer = 0
        self.high_score = self.load_high_score()
        self.particles = []
        self.powerups = []
        self.powerup_timer = 0
        self.powerup_delay = 300  # frames between powerup spawns
        self.enemies = []
        self.enemy_timer = 0
        self.enemy_delay = 180  # frames between enemy spawns
        self.level = 1
        self.experience = 0
        self.achievements = self.load_achievements()
        self.settings = self.load_settings()
        self.background_offset = 0
        self.stage = 1  # Different visual themes per stage
        self.stage_colors = {
            1: {'bg': (20, 20, 40), 'stars': (100, 100, 200), 'accent': CYAN},
            2: {'bg': (40, 20, 20), 'stars': (200, 100, 100), 'accent': RED},
            3: {'bg': (20, 40, 20), 'stars': (100, 200, 100), 'accent': GREEN},
            4: {'bg': (40, 20, 40), 'stars': (200, 100, 200), 'accent': PURPLE},
            5: {'bg': (40, 40, 20), 'stars': (200, 200, 100), 'accent': YELLOW}
        }
        
        # Sound system
        self.sound_enabled = True
        self.music_enabled = True
        
        # Performance tracking
        self.frame_count = 0
        self.fps_counter = 0
        self.fps_timer = 0
        self.current_fps = 0
        
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
    
    def load_achievements(self):
        try:
            if os.path.exists('achievements.json'):
                with open('achievements.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return {
            'first_game': False,
            'score_1000': False,
            'score_5000': False,
            'score_10000': False,
            'survive_60s': False,
            'collect_10_powerups': False,
            'perfect_dash': False,
            'no_damage_run': False
        }
    
    def save_achievements(self):
        try:
            with open('achievements.json', 'w') as f:
                json.dump(self.achievements, f)
        except:
            pass
    
    def load_settings(self):
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return {
            'sound_enabled': True,
            'music_enabled': True,
            'difficulty': 'normal',
            'particle_effects': True,
            'show_fps': False
        }
    
    def save_settings(self):
        try:
            with open('settings.json', 'w') as f:
                json.dump(self.settings, f)
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
        self.enemies = []
        self.enemy_timer = 0
        self.level = 1
        self.experience = 0
        self.powerups_collected = 0
        self.damage_taken = 0
        self.dash_count = 0
        self.start_time = time.time()
        self.background_offset = 0
    
    def spawn_projectile(self):
        direction = random.choice(['down', 'left', 'right'])
        
        # More projectile types at higher levels and stages
        if self.stage >= 4:
            projectile_types = ['kunai', 'fireball', 'shuriken', 'lightning', 'ice_shard', 'wind_blade']
        elif self.stage >= 3:
            projectile_types = ['kunai', 'fireball', 'shuriken', 'lightning', 'ice_shard']
        elif self.stage >= 2:
            projectile_types = ['kunai', 'fireball', 'shuriken', 'lightning']
        else:
            projectile_types = ['kunai', 'fireball', 'shuriken']
        
        projectile_type = random.choice(projectile_types)
        
        # Assign colors based on projectile type
        if projectile_type == 'kunai':
            color = random.choice([RED, BLUE, DARK_GRAY])
        elif projectile_type == 'fireball':
            color = random.choice([RED, ORANGE, YELLOW])
        elif projectile_type == 'shuriken':
            color = random.choice([PURPLE, CYAN, DARK_GREEN])
        elif projectile_type == 'lightning':
            color = random.choice([YELLOW, WHITE, LIGHT_YELLOW])
        elif projectile_type == 'ice_shard':
            color = random.choice([CYAN, LIGHT_BLUE, WHITE])
        elif projectile_type == 'wind_blade':
            color = random.choice([LIGHT_GREEN, WHITE, LIGHT_GRAY])
        
        # Speed increases with level and stage
        base_speed = 3 + self.level + (self.stage - 1)
        speed = random.randint(base_speed, base_speed + 3)
        
        if direction == 'down':
            x = random.randint(0, SCREEN_WIDTH - 25)
            y = -25
        elif direction == 'left':
            x = SCREEN_WIDTH
            y = random.randint(0, SCREEN_HEIGHT - 25)
        else:  # right
            x = -25
            y = random.randint(0, SCREEN_HEIGHT - 25)
        
        self.projectiles.append(Projectile(x, y, direction, speed, color, projectile_type))
    
    def spawn_enemy(self):
        """Spawn enemies based on level and stage"""
        if self.level >= 2:
            enemy_types = ['ninja', 'assassin']
            
            # Stage-specific enemy types
            if self.stage >= 2:
                enemy_types.append('ninja')  # More ninjas in later stages
            if self.stage >= 3:
                enemy_types.append('assassin')  # More assassins
            if self.level >= 4:
                enemy_types.append('boss')
            
            # Stage 5 gets special boss spawns
            if self.stage >= 5 and random.random() < 0.3:
                enemy_types = ['boss']
            
            enemy_type = random.choice(enemy_types)
            
            # Spawn from edges
            side = random.choice(['top', 'left', 'right'])
            if side == 'top':
                x = random.randint(0, SCREEN_WIDTH - 40)
                y = -40
            elif side == 'left':
                x = -40
                y = random.randint(0, SCREEN_HEIGHT - 40)
            else:  # right
                x = SCREEN_WIDTH
                y = random.randint(0, SCREEN_HEIGHT - 40)
            
            enemy = Enemy(x, y, enemy_type)
            
            # Stage-specific enemy buffs
            if self.stage >= 3:
                enemy.speed += 1
            if self.stage >= 4:
                enemy.health += 1
                enemy.attack_delay = max(60, enemy.attack_delay - 30)
            
            self.enemies.append(enemy)
    
    def spawn_powerup(self):
        # More powerup types at higher levels and stages
        if self.stage >= 4:
            powerup_types = ['speed', 'shield', 'slow_time', 'multi_shot', 'health', 'invincible']
        elif self.stage >= 3:
            powerup_types = ['speed', 'shield', 'slow_time', 'multi_shot', 'health']
        elif self.stage >= 2:
            powerup_types = ['speed', 'shield', 'slow_time', 'health']
        else:
            powerup_types = ['speed', 'shield', 'slow_time']
        
        powerup_type = random.choice(powerup_types)
        x = random.randint(60, SCREEN_WIDTH - 60)
        y = random.randint(60, SCREEN_HEIGHT - 60)
        self.powerups.append(PowerUp(x, y, powerup_type))
    
    def create_particles(self, x, y, color, count=5, particle_type="circle", size=3):
        for _ in range(count):
            vx = random.randint(-8, 8)
            vy = random.randint(-8, 8)
            life = random.randint(20, 40)
            self.particles.append(Particle(x, y, color, (vx, vy), life, particle_type, size))
    
    def create_explosion(self, x, y, color, count=15):
        """Create a large explosion effect"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            life = random.randint(30, 60)
            particle_type = random.choice(["circle", "spark", "star"])
            self.particles.append(Particle(x, y, color, (vx, vy), life, particle_type, 4))
    
    def create_trail(self, x, y, color, count=3):
        """Create a trail effect"""
        for _ in range(count):
            vx = random.randint(-3, 3)
            vy = random.randint(-3, 3)
            life = random.randint(10, 20)
            self.particles.append(Particle(x, y, color, (vx, vy), life, "spark", 2))
    
    def update(self):
        # Update splash screen
        if self.state == SPLASH:
            self.splash_timer += 1
            self.background_offset += 0.5
            if self.splash_timer >= 180:  # 3 seconds at 60 FPS
                self.state = MENU
            return
        
        if self.state != PLAYING:
            return
        
        # Update performance tracking
        self.frame_count += 1
        self.fps_timer += 1
        if self.fps_timer >= 60:  # Update FPS every second
            self.current_fps = self.fps_counter
            self.fps_counter = 0
            self.fps_timer = 0
        self.fps_counter += 1
        
        # Update background offset for scrolling effect
        self.background_offset += 0.5
        
        # Level progression
        new_level = (self.score // 1000) + 1
        if new_level > self.level:
            self.level = new_level
            self.stage = ((self.level - 1) // 3) + 1  # New stage every 3 levels
            self.create_explosion(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, GOLD, 20)
            sound_manager.play_sound('level_up')
            
            # Level up effects
            for i in range(10):
                angle = (i * 36) * math.pi / 180
                x = SCREEN_WIDTH // 2 + math.cos(angle) * 100
                y = SCREEN_HEIGHT // 2 + math.sin(angle) * 100
                self.create_explosion(x, y, GOLD, 5)
        
        # Spawn projectiles
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_projectile()
            self.spawn_timer = 0
            # Increase difficulty over time and with stages
            if self.spawn_delay > 15:
                self.spawn_delay -= 1
            if self.stage >= 3 and self.spawn_delay > 10:
                self.spawn_delay -= 1
        
        # Spawn powerups
        self.powerup_timer += 1
        if self.powerup_timer >= self.powerup_delay:
            self.spawn_powerup()
            self.powerup_timer = 0
        
        # Spawn enemies
        self.enemy_timer += 1
        if self.enemy_timer >= self.enemy_delay:
            self.spawn_enemy()
            self.enemy_timer = 0
            # Increase enemy spawn rate over time and with stages
            if self.enemy_delay > 60:
                self.enemy_delay -= 2
            if self.stage >= 3 and self.enemy_delay > 30:
                self.enemy_delay -= 1
        
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
                    self.create_explosion(projectile.rect.centerx, projectile.rect.centery, BLUE, 10)
                    self.projectiles.remove(projectile)
                elif self.player.invincible:
                    # Invincible - no damage
                    self.create_particles(projectile.rect.centerx, projectile.rect.centery, GOLD, 5)
                    self.projectiles.remove(projectile)
                else:
                    # Take damage
                    self.player.health -= 1
                    self.damage_taken += 1
                    self.create_explosion(projectile.rect.centerx, projectile.rect.centery, RED, 12)
                    sound_manager.play_sound('hit')
                    self.projectiles.remove(projectile)
                    
                    if self.player.health <= 0:
                        self.game_over = True
                        self.state = GAME_OVER
                        sound_manager.play_sound('game_over')
                        if self.score > self.high_score:
                            self.high_score = self.score
                            self.save_high_score()
                        self.check_achievements()
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.player.rect.center)
            
            # Check special attack damage to enemies
            if self.player.is_using_special:
                distance = math.sqrt((enemy.rect.centerx - self.player.rect.centerx)**2 + 
                                   (enemy.rect.centery - self.player.rect.centery)**2)
                if distance < 50:  # Special attack range
                    enemy.health -= 1
                    self.create_explosion(enemy.rect.centerx, enemy.rect.centery, GOLD, 15)
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.score += 100  # Bonus points for defeating enemies
            
            # Check if enemy attacks
            if enemy.can_attack() and self.player.rect.colliderect(enemy.rect):
                if self.player.shield_active:
                    # Shield blocks enemy attack
                    self.create_explosion(enemy.rect.centerx, enemy.rect.centery, BLUE, 10)
                    enemy.health -= 1
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                elif self.player.invincible:
                    # Invincible - no damage
                    self.create_particles(enemy.rect.centerx, enemy.rect.centery, GOLD, 5)
                else:
                    # Take damage from enemy
                    self.player.health -= 1
                    self.damage_taken += 1
                    self.create_explosion(enemy.rect.centerx, enemy.rect.centery, RED, 12)
                    sound_manager.play_sound('hit')
                    
                    if self.player.health <= 0:
                        self.game_over = True
                        self.state = GAME_OVER
                        sound_manager.play_sound('game_over')
                        if self.score > self.high_score:
                            self.high_score = self.score
                            self.save_high_score()
                        self.check_achievements()
            
            # Remove enemies that are off-screen
            if (enemy.rect.y > SCREEN_HEIGHT + 50 or 
                enemy.rect.x > SCREEN_WIDTH + 50 or 
                enemy.rect.x < -50):
                self.enemies.remove(enemy)
        
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
        self.create_explosion(powerup.rect.centerx, powerup.rect.centery, GOLD, 15)
        self.powerups_collected += 1
        sound_manager.play_sound('collect')
        
        if powerup.type == 'speed':
            self.player.speed_boost = True
            self.player.speed_timer = 300  # 5 seconds at 60 FPS
        elif powerup.type == 'shield':
            self.player.shield_active = True
            self.player.shield_timer = 600  # 10 seconds at 60 FPS
        elif powerup.type == 'slow_time':
            self.player.slow_time = True
            self.player.slow_timer = 300  # 5 seconds at 60 FPS
        elif powerup.type == 'multi_shot':
            self.player.multi_shot = True
            self.player.multi_shot_timer = 450  # 7.5 seconds at 60 FPS
        elif powerup.type == 'health':
            if self.player.health < self.player.max_health:
                self.player.health += 1
        elif powerup.type == 'invincible':
            self.player.invincible = True
            self.player.invincible_timer = 300  # 5 seconds at 60 FPS
    
    def check_achievements(self):
        """Check and unlock achievements"""
        if not self.achievements['first_game']:
            self.achievements['first_game'] = True
        
        if self.score >= 1000 and not self.achievements['score_1000']:
            self.achievements['score_1000'] = True
        
        if self.score >= 5000 and not self.achievements['score_5000']:
            self.achievements['score_5000'] = True
        
        if self.score >= 10000 and not self.achievements['score_10000']:
            self.achievements['score_10000'] = True
        
        if time.time() - self.start_time >= 60 and not self.achievements['survive_60s']:
            self.achievements['survive_60s'] = True
        
        if self.powerups_collected >= 10 and not self.achievements['collect_10_powerups']:
            self.achievements['collect_10_powerups'] = True
        
        if self.player.dash_count >= 20 and not self.achievements['perfect_dash']:
            self.achievements['perfect_dash'] = True
        
        if self.damage_taken == 0 and self.score >= 1000 and not self.achievements['no_damage_run']:
            self.achievements['no_damage_run'] = True
        
        self.save_achievements()
    
    def draw_menu(self):
        # Animated background
        self.screen.fill(BLACK)
        
        # Moving stars
        for i in range(50):
            x = (i * 20 + self.background_offset) % SCREEN_WIDTH
            y = (i * 15 + self.background_offset * 0.5) % SCREEN_HEIGHT
            brightness = int(255 * (0.5 + 0.5 * math.sin(self.background_offset * 0.01 + i)))
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, (int(x), int(y)), 1)
        
        # Title with gradient effect
        title_text = self.title_font.render("DODGE LIKE NARUTO", True, ORANGE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 180))
        
        # Title shadow
        shadow_text = self.title_font.render("DODGE LIKE NARUTO", True, DARK_GRAY)
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH//2 + 4, SCREEN_HEIGHT//2 - 176))
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.large_font.render("Enhanced Edition", True, GOLD)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 120))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # High score with better styling
        high_score_text = self.font.render(f"High Score: {self.high_score:,}", True, GOLD)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
        self.screen.blit(high_score_text, high_score_rect)
        
        # Level indicator
        level_text = self.font.render(f"Level: {self.level}", True, CYAN)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
        self.screen.blit(level_text, level_rect)
        
        # Instructions
        start_text = self.large_font.render("Press SPACE to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        self.screen.blit(start_text, start_rect)
        
        # Controls
        controls_text = self.medium_font.render("Arrow Keys: Move | SPACE: Dash | X: Special Attack", True, YELLOW)
        controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70))
        self.screen.blit(controls_text, controls_rect)
        
        # Additional controls
        controls2_text = self.medium_font.render("Collect Power-ups! Defeat Enemies!", True, CYAN)
        controls2_rect = controls2_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 110))
        self.screen.blit(controls2_text, controls2_rect)
        
        # Power-up descriptions
        powerup_text = self.small_font.render("Power-ups: Speed | Shield | Slow Time | Multi-Shot | Health | Invincible", True, CYAN)
        powerup_rect = powerup_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 150))
        self.screen.blit(powerup_text, powerup_rect)
        
        # Additional controls
        extra_text = self.small_font.render("Press P to Pause | ESC to Quit | S to Toggle Sound | O for Settings | A for Achievements", True, LIGHT_GRAY)
        extra_rect = extra_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 190))
        self.screen.blit(extra_text, extra_rect)
        
        # Sound status
        sound_status = "ON" if sound_manager.sound_enabled else "OFF"
        sound_text = self.small_font.render(f"Sound: {sound_status}", True, LIGHT_GREEN if sound_manager.sound_enabled else LIGHT_GRAY)
        sound_rect = sound_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 230))
        self.screen.blit(sound_text, sound_rect)
    
    def draw_game(self):
        # Draw animated background with stage colors
        stage_color = self.stage_colors.get(self.stage, self.stage_colors[1])
        self.screen.fill(stage_color['bg'])
        
        # Enhanced background with parallax scrolling
        for i in range(100):
            x = (i * 10 + self.background_offset) % SCREEN_WIDTH
            y = (i * 8 + self.background_offset * 0.3) % SCREEN_HEIGHT
            brightness = int(100 + 155 * (0.5 + 0.5 * math.sin(self.background_offset * 0.02 + i)))
            # Ensure color values are within valid range (0-255)
            r = max(0, min(255, int(brightness * stage_color['stars'][0] / 255)))
            g = max(0, min(255, int(brightness * stage_color['stars'][1] / 255)))
            b = max(0, min(255, int(brightness * stage_color['stars'][2] / 255)))
            color = (r, g, b)
            pygame.draw.circle(self.screen, color, (int(x), int(y)), 1)
        
        # Additional star layer
        for i in range(30):
            x = (i * 33 + self.background_offset * 1.5) % SCREEN_WIDTH
            y = (i * 25 + self.background_offset * 0.8) % SCREEN_HEIGHT
            brightness = int(200 * (0.3 + 0.7 * math.sin(self.background_offset * 0.015 + i)))
            # Ensure color values are within valid range (0-255)
            r = max(0, min(255, int(brightness * stage_color['stars'][0] / 255)))
            g = max(0, min(255, int(brightness * stage_color['stars'][1] / 255)))
            b = max(0, min(255, int(brightness * stage_color['stars'][2] / 255)))
            color = (r, g, b)
            pygame.draw.circle(self.screen, color, (int(x), int(y)), 2)
        
        # Stage-specific background elements
        if self.stage >= 2:
            # Add some atmospheric elements
            for i in range(5):
                x = (i * 200 + self.background_offset * 0.5) % SCREEN_WIDTH
                y = (i * 150 + self.background_offset * 0.2) % SCREEN_HEIGHT
                pygame.draw.circle(self.screen, stage_color['accent'], (int(x), int(y)), 3, 1)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw powerups
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Enhanced HUD with better styling and spacing
        hud_y = 15
        hud_x = 15
        hud_spacing = 60  # Increased spacing between elements
        
        # Score with background
        score_text = self.font.render(f"Score: {self.score:,}", True, WHITE)
        score_rect = score_text.get_rect()
        score_bg = pygame.Rect(hud_x - 8, hud_y - 8, score_rect.width + 16, score_rect.height + 16)
        pygame.draw.rect(self.screen, (0, 0, 0, 200), score_bg)
        pygame.draw.rect(self.screen, WHITE, score_bg, 3)
        self.screen.blit(score_text, (hud_x, hud_y))
        hud_y += hud_spacing
        
        # High score
        high_score_text = self.font.render(f"High: {self.high_score:,}", True, GOLD)
        high_score_rect = high_score_text.get_rect()
        high_score_bg = pygame.Rect(hud_x - 8, hud_y - 8, high_score_rect.width + 16, high_score_rect.height + 16)
        pygame.draw.rect(self.screen, (0, 0, 0, 200), high_score_bg)
        pygame.draw.rect(self.screen, GOLD, high_score_bg, 3)
        self.screen.blit(high_score_text, (hud_x, hud_y))
        hud_y += hud_spacing
        
        # Level and Stage
        level_text = self.font.render(f"Level: {self.level}", True, CYAN)
        level_rect = level_text.get_rect()
        level_bg = pygame.Rect(hud_x - 8, hud_y - 8, level_rect.width + 16, level_rect.height + 16)
        pygame.draw.rect(self.screen, (0, 0, 0, 200), level_bg)
        pygame.draw.rect(self.screen, CYAN, level_bg, 3)
        self.screen.blit(level_text, (hud_x, hud_y))
        hud_y += hud_spacing
        
        # Stage
        stage_text = self.font.render(f"Stage: {self.stage}", True, stage_color['accent'])
        stage_rect = stage_text.get_rect()
        stage_bg = pygame.Rect(hud_x - 8, hud_y - 8, stage_rect.width + 16, stage_rect.height + 16)
        pygame.draw.rect(self.screen, (0, 0, 0, 200), stage_bg)
        pygame.draw.rect(self.screen, stage_color['accent'], stage_bg, 3)
        self.screen.blit(stage_text, (hud_x, hud_y))
        hud_y += hud_spacing
        
        # Health bar with better spacing
        health_text = self.medium_font.render("Health:", True, WHITE)
        self.screen.blit(health_text, (hud_x, hud_y))
        hud_y += 35
        
        for i in range(self.player.max_health):
            if i < self.player.health:
                color = RED
            else:
                color = DARK_GRAY
            heart_x = hud_x + i * 20
            heart_y = hud_y
            heart_points = [
                (heart_x, heart_y + 3),
                (heart_x - 3, heart_y),
                (heart_x - 1.5, heart_y - 1.5),
                (heart_x, heart_y),
                (heart_x + 1.5, heart_y - 1.5),
                (heart_x + 3, heart_y)
            ]
            pygame.draw.polygon(self.screen, color, heart_points)
        hud_y += 30
        
        # Power-up status with better spacing
        powerup_y = hud_y + 10
        powerup_spacing = 35  # Increased spacing between power-up items
        
        if self.player.shield_active:
            shield_text = self.medium_font.render(f"Shield: {self.player.shield_timer//60}s", True, BLUE)
            self.screen.blit(shield_text, (hud_x, powerup_y))
            powerup_y += powerup_spacing
        if self.player.speed_boost:
            speed_text = self.medium_font.render(f"Speed: {self.player.speed_timer//60}s", True, CYAN)
            self.screen.blit(speed_text, (hud_x, powerup_y))
            powerup_y += powerup_spacing
        if self.player.slow_time:
            slow_text = self.medium_font.render(f"Slow Time: {self.player.slow_timer//60}s", True, PURPLE)
            self.screen.blit(slow_text, (hud_x, powerup_y))
            powerup_y += powerup_spacing
        if self.player.multi_shot:
            multi_text = self.medium_font.render(f"Multi-Shot: {self.player.multi_shot_timer//60}s", True, YELLOW)
            self.screen.blit(multi_text, (hud_x, powerup_y))
            powerup_y += powerup_spacing
        if self.player.invincible:
            inv_text = self.medium_font.render(f"Invincible: {self.player.invincible_timer//60}s", True, GOLD)
            self.screen.blit(inv_text, (hud_x, powerup_y))
            powerup_y += powerup_spacing
        
        # Dash cooldown
        if self.player.dash_cooldown > 0:
            dash_text = self.medium_font.render(f"Dash: {self.player.dash_cooldown//60}s", True, LIGHT_GRAY)
            self.screen.blit(dash_text, (hud_x, powerup_y))
            powerup_y += powerup_spacing
        
        # Special attack cooldown
        if self.player.special_attack_cooldown > 0:
            special_text = self.medium_font.render(f"Special: {self.player.special_attack_cooldown//60}s", True, LIGHT_GRAY)
            self.screen.blit(special_text, (hud_x, powerup_y))
        
        # Mini-map/Radar
        self.draw_minimap(hud_x, SCREEN_HEIGHT - 150)
        
        # Instructions
        if self.score < 100:  # Show instructions for first 100 points
            instruction_text = self.medium_font.render("Arrow Keys: Move | SPACE: Dash | X: Special Attack", True, YELLOW)
            self.screen.blit(instruction_text, (hud_x, SCREEN_HEIGHT - 40))
        
        # Draw FPS counter
        self.draw_fps()
    
    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Get stage color for display
        stage_color = self.stage_colors.get(self.stage, self.stage_colors[1])
        
        # Game over text with shadow
        game_over_text = self.big_font.render("GAME OVER", True, RED)
        game_over_shadow = self.big_font.render("GAME OVER", True, DARK_GRAY)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 180))
        shadow_rect = game_over_shadow.get_rect(center=(SCREEN_WIDTH//2 + 4, SCREEN_HEIGHT//2 - 176))
        self.screen.blit(game_over_shadow, shadow_rect)
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        final_score_text = self.large_font.render(f"Final Score: {self.score:,}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 120))
        self.screen.blit(final_score_text, final_score_rect)
        
        # Level and Stage reached
        level_text = self.font.render(f"Level Reached: {self.level}", True, CYAN)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 70))
        self.screen.blit(level_text, level_rect)
        
        stage_text = self.font.render(f"Stage Reached: {self.stage}", True, stage_color['accent'])
        stage_rect = stage_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
        self.screen.blit(stage_text, stage_rect)
        
        # Time survived
        time_survived = int(time.time() - self.start_time)
        time_text = self.font.render(f"Time Survived: {time_survived}s", True, YELLOW)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 10))
        self.screen.blit(time_text, time_rect)
        
        # Check if new high score
        if self.score >= self.high_score:
            new_high_text = self.font.render("NEW HIGH SCORE!", True, GOLD)
            new_high_rect = new_high_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            self.screen.blit(new_high_text, new_high_rect)
        
        # Statistics
        stats_text = self.small_font.render(f"Power-ups Collected: {self.powerups_collected} | Damage Taken: {self.damage_taken}", True, LIGHT_GRAY)
        stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
        self.screen.blit(stats_text, stats_rect)
        
        # Controls
        restart_text = self.font.render("Press R to Restart", True, YELLOW)
        menu_text = self.font.render("Press M for Main Menu", True, CYAN)
        quit_text = self.small_font.render("Press ESC to Quit", True, LIGHT_GRAY)
        
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 140))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 180))
        
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(menu_text, menu_rect)
        self.screen.blit(quit_text, quit_rect)
    
    def draw_pause(self):
        """Draw pause screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.big_font.render("PAUSED", True, YELLOW)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(pause_text, pause_rect)
        
        # Instructions
        resume_text = self.font.render("Press SPACE to Resume", True, WHITE)
        quit_text = self.font.render("Press ESC to Quit", True, LIGHT_GRAY)
        
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
        
        self.screen.blit(resume_text, resume_rect)
        self.screen.blit(quit_text, quit_rect)
    
    def draw_settings(self):
        """Draw settings screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Settings title
        title_text = self.big_font.render("SETTINGS", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 150))
        self.screen.blit(title_text, title_rect)
        
        # Sound settings
        sound_text = self.font.render(f"Sound Effects: {'ON' if sound_manager.sound_enabled else 'OFF'}", True, LIGHT_GREEN if sound_manager.sound_enabled else LIGHT_GRAY)
        sound_rect = sound_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80))
        self.screen.blit(sound_text, sound_rect)
        
        # Music settings
        music_text = self.font.render(f"Background Music: {'ON' if sound_manager.music_enabled else 'OFF'}", True, LIGHT_GREEN if sound_manager.music_enabled else LIGHT_GRAY)
        music_rect = music_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
        self.screen.blit(music_text, music_rect)
        
        # Difficulty settings
        difficulty_text = self.font.render(f"Difficulty: {self.settings['difficulty'].title()}", True, CYAN)
        difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(difficulty_text, difficulty_rect)
        
        # Particle effects
        particles_text = self.font.render(f"Particle Effects: {'ON' if self.settings['particle_effects'] else 'OFF'}", True, LIGHT_GREEN if self.settings['particle_effects'] else LIGHT_GRAY)
        particles_rect = particles_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
        self.screen.blit(particles_text, particles_rect)
        
        # FPS display
        fps_text = self.font.render(f"Show FPS: {'ON' if self.settings.get('show_fps', False) else 'OFF'}", True, LIGHT_GREEN if self.settings.get('show_fps', False) else LIGHT_GRAY)
        fps_rect = fps_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
        self.screen.blit(fps_text, fps_rect)
        
        # Controls
        controls_text = self.small_font.render("S: Toggle Sound | M: Toggle Music | D: Change Difficulty | P: Toggle Particles | F: Toggle FPS", True, LIGHT_GRAY)
        controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        self.screen.blit(controls_text, controls_rect)
        
        # Back to menu
        back_text = self.font.render("Press ESC to Return to Menu", True, YELLOW)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 150))
        self.screen.blit(back_text, back_rect)
    
    def draw_achievements(self):
        """Draw achievements screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Achievements title
        title_text = self.big_font.render("ACHIEVEMENTS", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 200))
        self.screen.blit(title_text, title_rect)
        
        # Achievement list
        achievement_data = [
            ("First Game", "Play your first game", self.achievements['first_game']),
            ("Score 1000", "Reach a score of 1000", self.achievements['score_1000']),
            ("Score 5000", "Reach a score of 5000", self.achievements['score_5000']),
            ("Score 10000", "Reach a score of 10000", self.achievements['score_10000']),
            ("Survive 60s", "Survive for 60 seconds", self.achievements['survive_60s']),
            ("Collect 10 Power-ups", "Collect 10 power-ups in one game", self.achievements['collect_10_powerups']),
            ("Perfect Dash", "Use dash 20 times in one game", self.achievements['perfect_dash']),
            ("No Damage Run", "Reach 1000 points without taking damage", self.achievements['no_damage_run'])
        ]
        
        y_offset = -120
        for name, description, unlocked in achievement_data:
            color = GOLD if unlocked else LIGHT_GRAY
            status = "✓" if unlocked else "✗"
            
            achievement_text = self.font.render(f"{status} {name}", True, color)
            achievement_rect = achievement_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + y_offset))
            self.screen.blit(achievement_text, achievement_rect)
            
            desc_text = self.small_font.render(description, True, LIGHT_GRAY)
            desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + y_offset + 25))
            self.screen.blit(desc_text, desc_rect)
            
            y_offset += 50
        
        # Back to menu
        back_text = self.font.render("Press ESC to Return to Menu", True, YELLOW)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 250))
        self.screen.blit(back_text, back_rect)
    
    def draw_splash(self):
        """Draw splash screen"""
        # Animated background
        self.screen.fill(BLACK)
        
        # Moving stars
        for i in range(100):
            x = (i * 20 + self.background_offset) % SCREEN_WIDTH
            y = (i * 15 + self.background_offset * 0.5) % SCREEN_HEIGHT
            brightness = int(255 * (0.5 + 0.5 * math.sin(self.background_offset * 0.01 + i)))
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, (int(x), int(y)), 1)
        
        # Title with pulsing effect
        pulse = int(10 * math.sin(self.splash_timer * 0.1))
        title_text = self.title_font.render("DODGE LIKE NARUTO", True, ORANGE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50 + pulse))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font.render("Enhanced Edition", True, GOLD)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20 + pulse))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Loading text
        loading_text = self.small_font.render("Loading...", True, WHITE)
        loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
        self.screen.blit(loading_text, loading_rect)
        
        # Progress bar
        progress_width = 200
        progress_height = 20
        progress_x = SCREEN_WIDTH // 2 - progress_width // 2
        progress_y = SCREEN_HEIGHT // 2 + 120
        
        # Background
        pygame.draw.rect(self.screen, DARK_GRAY, (progress_x, progress_y, progress_width, progress_height))
        
        # Progress
        progress = min(1.0, self.splash_timer / 180)  # 3 seconds at 60 FPS
        fill_width = int(progress_width * progress)
        pygame.draw.rect(self.screen, ORANGE, (progress_x, progress_y, fill_width, progress_height))
        
        # Border
        pygame.draw.rect(self.screen, WHITE, (progress_x, progress_y, progress_width, progress_height), 2)
    
    def draw_minimap(self, x, y):
        """Draw a mini-map showing enemies and power-ups"""
        map_size = 120
        map_rect = pygame.Rect(x, y, map_size, map_size)
        
        # Draw map background
        pygame.draw.rect(self.screen, (0, 0, 0, 180), map_rect)
        pygame.draw.rect(self.screen, WHITE, map_rect, 2)
        
        # Draw player position (center of map)
        player_x = x + map_size // 2
        player_y = y + map_size // 2
        pygame.draw.circle(self.screen, ORANGE, (player_x, player_y), 3)
        
        # Draw enemies
        for enemy in self.enemies:
            # Convert world coordinates to map coordinates
            rel_x = (enemy.rect.centerx - self.player.rect.centerx) * map_size // (SCREEN_WIDTH * 2)
            rel_y = (enemy.rect.centery - self.player.rect.centery) * map_size // (SCREEN_HEIGHT * 2)
            
            map_enemy_x = player_x + rel_x
            map_enemy_y = player_y + rel_y
            
            # Only draw if within map bounds
            if (map_enemy_x >= x and map_enemy_x <= x + map_size and 
                map_enemy_y >= y and map_enemy_y <= y + map_size):
                pygame.draw.circle(self.screen, enemy.color, (int(map_enemy_x), int(map_enemy_y)), 2)
        
        # Draw power-ups
        for powerup in self.powerups:
            # Convert world coordinates to map coordinates
            rel_x = (powerup.rect.centerx - self.player.rect.centerx) * map_size // (SCREEN_WIDTH * 2)
            rel_y = (powerup.rect.centery - self.player.rect.centery) * map_size // (SCREEN_HEIGHT * 2)
            
            map_powerup_x = player_x + rel_x
            map_powerup_y = player_y + rel_y
            
            # Only draw if within map bounds
            if (map_powerup_x >= x and map_powerup_x <= x + map_size and 
                map_powerup_y >= y and map_powerup_y <= y + map_size):
                pygame.draw.circle(self.screen, GOLD, (int(map_powerup_x), int(map_powerup_y)), 2)
        
        # Draw map label
        label_text = self.small_font.render("RADAR", True, WHITE)
        self.screen.blit(label_text, (x, y - 20))
    
    def draw_fps(self):
        """Draw FPS counter"""
        if self.settings.get('show_fps', False):
            fps_text = self.small_font.render(f"FPS: {self.current_fps}", True, LIGHT_GREEN)
            self.screen.blit(fps_text, (SCREEN_WIDTH - 80, 10))
    
    def draw(self):
        if self.state == SPLASH:
            self.draw_splash()
        elif self.state == MENU:
            self.draw_menu()
        elif self.state == PLAYING:
            self.draw_game()
        elif self.state == PAUSED:
            self.draw_game()  # Draw game in background
            self.draw_pause()  # Draw pause overlay
        elif self.state == SETTINGS:
            self.draw_settings()
        elif self.state == LEVEL_SELECT:
            self.draw_achievements()  # Using achievements screen for now
        elif self.state == GAME_OVER:
            self.draw_game_over()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == PLAYING:
                        self.state = PAUSED
                    else:
                        return False
                elif event.key == pygame.K_SPACE:
                    if self.state == MENU:
                        self.state = PLAYING
                        self.reset_game()
                    elif self.state == PAUSED:
                        self.state = PLAYING
                elif event.key == pygame.K_p and self.state == PLAYING:
                    self.state = PAUSED
                elif event.key == pygame.K_r and self.state == GAME_OVER:
                    self.state = PLAYING
                    self.reset_game()
                elif event.key == pygame.K_m and self.state == GAME_OVER:
                    self.state = MENU
                elif event.key == pygame.K_s:
                    sound_manager.toggle_sound()
                elif event.key == pygame.K_o and self.state == MENU:
                    self.state = SETTINGS
                elif event.key == pygame.K_a and self.state == MENU:
                    self.state = LEVEL_SELECT
                elif event.key == pygame.K_m and self.state == SETTINGS:
                    sound_manager.toggle_music()
                elif event.key == pygame.K_d and self.state == SETTINGS:
                    # Cycle through difficulty levels
                    difficulties = ['easy', 'normal', 'hard']
                    current_idx = difficulties.index(self.settings['difficulty'])
                    self.settings['difficulty'] = difficulties[(current_idx + 1) % len(difficulties)]
                    self.save_settings()
                elif event.key == pygame.K_p and self.state == SETTINGS:
                    self.settings['particle_effects'] = not self.settings['particle_effects']
                    self.save_settings()
                elif event.key == pygame.K_f and self.state == SETTINGS:
                    self.settings['show_fps'] = not self.settings.get('show_fps', False)
                    self.save_settings()
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
