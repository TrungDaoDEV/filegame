import pygame, sys, random
import os

def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe= pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def create_pipe():
    random_pipe_pos=random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(432+80,random_pipe_pos+100))
    top_pipe = pipe_surface.get_rect(midtop=(432+80,random_pipe_pos-700))
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 4
    return pipes
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False    
        if bird_rect.top <= -75 or bird_rect.bottom >= 650:
            return False
    return True
def rotate_bird(bird1): 
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100,bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,'blue')
        score_rect = score_surface.get_rect(center=(216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f"Score: {int(score)}",True,'blue')
        score_rect = score_surface.get_rect(center=(216,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f"High Score: {int(high_score)}",True,'blue')
        score_rect = high_score_surface.get_rect(center=(216,150))
        screen.blit(high_score_surface,score_rect)
def update_score(score, high_score):
    if score >= high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen=pygame.display.set_mode((432,768))


game_font = pygame.font.Font('D:/LAP_TRINH/PYTHON/Hoc/FileGame/04B_19.TTF',30)
# tạo biến
clock = pygame.time.Clock()
gravity = 0.2
game_active = True
bird_movement = 0
score = 0
high_score = 0
# chèn bg
bg=pygame.image.load('D:/LAP_TRINH/PYTHON/Hoc/FileGame/assets/background-night.png').convert()
bg=pygame.transform.scale2x(bg)
# chèn sàn
floor=pygame.image.load('D:/LAP_TRINH/PYTHON/Hoc/FileGame/assets/floor.png').convert()
floor=pygame.transform.scale2x(floor)
floor_x_pos=0
# tạo chim
bird_down = pygame.image.load('D:/LAP_TRINH/PYTHON/Hoc/FileGame/assets/yellowbird-downflap.png').convert_alpha()
bird_mid = pygame.image.load('D:/LAP_TRINH/PYTHON/Hoc/FileGame/assets/yellowbird-midflap.png').convert_alpha()
bird_up = pygame.image.load('D:/LAP_TRINH/PYTHON/Hoc/FileGame/assets/yellowbird-upflap.png').convert_alpha()
bird_list=[bird_down,bird_mid,bird_up]
bird_index = 2
bird = bird_list[bird_index]
# bird=pygame.image.load('./FileGame/assets/yellowbird-midflap.png').convert_alpha()
# bird=pygame.transform.scale2x(bird)
bird_rect=bird.get_rect(center=(100,384))
# tạo timer cho bird
bird_flap = pygame.USEREVENT+1
pygame.time.set_timer(bird_flap,200)
# tạo ống
pipe_surface = pygame.image.load('D:/LAP_TRINH/PYTHON/Hoc/FileGame/assets/pipe-green.png').convert()
pipe_surface=pygame.transform.scale2x(pipe_surface)
pipe_list=[]
pipe_height = [300,400,500]
# tạo timer 
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1000)
# Tạo màn hình kết thúc
game_over_surface = pygame.image.load('D:/LAP_TRINH/PYTHON/Hoc/FileGame/assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(432/2,768/2))
# chèn âm thanh
flap_sound = pygame.mixer.Sound('D:/LAP_TRINH/PYTHON/Hoc/FileGame/sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('D:/LAP_TRINH/PYTHON/Hoc/FileGame/sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('D:/LAP_TRINH/PYTHON/Hoc/FileGame/sound/sfx_point.wav')
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -5
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active==False:
                game_active=True
                pipe_list.clear()
                bird_rect.center = (100,384)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            # pipe_list.append(create_pipe())
            pipe_list.extend(create_pipe())
            print(create_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else: 
                bird_index = 0
            bird, bird_rect = bird_animation()
    # bg
    screen.blit(bg,(0,0))
    if game_active:
        # chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)
        # ống 
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        check_collision(pipe_list)
        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound_countdown = 100
            score_sound.play()
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score =  update_score(score, high_score)
        score_display('game_over')
    # sàn
    floor_x_pos-=1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos=0    
    pygame.display.update()
    clock.tick(100)

