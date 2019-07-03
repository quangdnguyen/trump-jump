## Quang Nguyen qdn8mj Edward Radion er2cg; FINAL SUBMISSION
# game description:
# goal is to survive as long as possible against the numerous impediments to Trump's Mission while making big bucks
# Mission Trump has: user input, graphics, start screen, animation, enemies, collectables, scrolling level, timer, health meter, music/sounds

import pygame
import gamebox
import random
camera = gamebox.Camera(1000, 600)
show_splash = True
game_on = False
ticks = 0
wait_before_flap = 0
timer = 0
jump_clock = 0

donald = gamebox.load_sprite_sheet("http://tinyurl.com/y88svru3", 4, 6)
me = gamebox.from_image(200, 200, donald[2])
collectibles = [
    gamebox.from_image(random.randrange(100, 900), random.randrange(0, 100), "money.png"),
    gamebox.from_image(random.randrange(100, 900), random.randrange(-100, 0), "money.png"),
    gamebox.from_image(random.randrange(100, 900), random.randrange(-200, -100), "money.png"),
    gamebox.from_image(random.randrange(100, 900), random.randrange(-300, -200), "money.png"),
    gamebox.from_image(random.randrange(100, 900), random.randrange(-400, -300), "money.png"),
    gamebox.from_image(random.randrange(100, 900), random.randrange(-500, -400), "money.png"),
    gamebox.from_image(random.randrange(100, 900), random.randrange(-50, 0), "money.png"),
    gamebox.from_image(random.randrange(100, 900), random.randrange(0, 50), "money.png"),
    gamebox.from_image(random.randrange(100, 900), random.randrange(350, 400), "money.png"),
    gamebox.from_image(random.randrange(100, 900), random.randrange(-300, -200), "money.png"),
    gamebox.from_image(random.randrange(100, 900), random.randrange(-400, -300), "money.png"),
]
money_collected = 0
fake_news = [
    gamebox.from_image(random.randrange(100, 900), random.randrange(600, 800), "cnbc.png"),
    gamebox.from_image(random.randrange(100, 900), random.randrange(800, 1000), "new_york_times.png"),
    gamebox.from_image(random.randrange(100, 900), random.randrange(1200, 1400), "washington_post.png"),
    gamebox.from_image(random.randrange(0, 1000), random.randrange(0, 1000), "cnn.png")
]
# cnn = gamebox.from_image(random.randrange(0, 1000), random.randrange(0, 1000), "cnn.png")
# cnn.height = 40

hearts = [
    gamebox.from_image(camera.left + 70, camera.top + 12, 'heart.png'),
    gamebox.from_image(camera.left + 45, camera.top + 12, 'heart.png'),
    gamebox.from_image(camera.left + 20, camera.top + 12, 'heart.png')

]

platforms_moving_left = [
    gamebox.from_image(random.randrange(0, 200), random.randrange(200,300), "brickfloor.png"),
    gamebox.from_image(random.randrange(300,500), random.randrange(300,400), "brickfloor.png"),
    gamebox.from_image(random.randrange(600,900), random.randrange(400,500), "brickfloor.png")
]

platforms_moving_right = [
    gamebox.from_image(random.randrange(0, 200), random.randrange(200,300), "brickfloor.png"),
    gamebox.from_image(random.randrange(300,500), random.randrange(300,400), "brickfloor.png"),
    gamebox.from_image(random.randrange(600,900), random.randrange(400,500), "brickfloor.png")
]


backgrounds = [
    gamebox.from_image(camera.x, camera.y, "background1.png"),
    gamebox.from_image(3.552*camera.x, camera.y, "background1.png")
]

background_music = gamebox.load_sound("backgroundmusic.wav")
menu_music = gamebox.load_sound("menumusic.wav")
jump_sound = gamebox.load_sound("jumpsound.wav")
getting_hit_sound = gamebox.load_sound("hit.wav")

def splash(keys):
    global show_splash
    camera.clear('black')
    white_house = gamebox.from_image(camera.x, camera.bottom - 190, "http://www.pngmart.com/files/4/White-House-PNG-HD.png")
    face = gamebox.from_image(830, 240, "http://tinyurl.com/y86pwv9o")
    title = gamebox.from_text(350, 100, "MISSION TRUMP", 'sys', 100, 'white')
    white_house.width = 1000
    camera.draw(white_house)
    camera.draw(face)
    camera.draw(title)
    camera.draw(gamebox.from_text(350, 150, "Press SPACE to start", 'sys', 30, 'white'))
    camera.draw(gamebox.from_text(100, 170, "Controls:", 'sys', 30, 'white'))
    camera.draw(gamebox.from_text(166, 190, "SPACE - Jump", 'sys', 30, 'white'))
    camera.draw(gamebox.from_text(240, 210, "Right and Left Arrows - Move", 'sys', 30, 'white'))
    camera.draw(gamebox.from_text(855, 90, "- Avoid FAKE NEWS", 'sys', 30, 'red'))
    camera.draw(gamebox.from_text(820, 115, "- Collect $$$", 'sys', 30, 'red'))
    camera.draw(gamebox.from_text(camera.left + 170, camera.bottom - 20, "Quang Nguyen (qdn8mj), Edward Radion (er2cg)", 'sys', 20, 'white'))
    menu_music.play(loops=-1)

    if pygame.K_SPACE in keys:
        show_splash = False
        menu_music.stop()
        background_music.play(loops=-1)
    camera.display()

def tick(keys):
    global money_collected
    global timer
    global ticks
    global game_on
    global ground
    global wait_before_flap
    global jump_clock
    ticks += 1
    camera.clear('black')
# splash screen
    if show_splash:
        splash(keys)
        return

    for background in backgrounds:
         camera.draw(background)

    for bill in collectibles:
        camera.draw(bill)
        bill.y += 5
        bill.move_speed()
        if me.touches(bill):
            bill.y -= 700
            bill.x = random.randrange(0, 1000)
            money_collected += 1
        if bill.top >= camera.bottom:
            bill.y -= 700
            bill.x = random.randrange(0, 1000)
        if pygame.K_RIGHT in keys:
            bill.x -= 10
        if pygame.K_LEFT in keys:
            bill.x += 10


        # Score is based on how long the player lasts before the game ends
    game_score = (ticks // 60) + money_collected
    score = gamebox.from_text(200, 0, "Score: " + str(game_score), "sys", 40, "black")
    score.top = camera.top + 10
    score.right = camera.right - 10

    # if me.x < cnn.x:
    #     cnn.speedx -= 1.5
    # if me.y < cnn.y:
    #     cnn.speedy -= 1.5
    # if me.x > cnn.x:
    #     cnn.speedx += 1.5
    # if me.y > cnn.y:
    #     cnn.speedy += 1.5
    # cnn.speedx *= .4
    # cnn.speedy *= .4
    # cnn.move_speed()

    for news in fake_news:
        news.height = 50
        camera.draw(news)
        news.y -= 10
        news.move_speed()
        if news.bottom <= camera.top:
            news.y += 1000
            news.x = random.randrange(0, 1000)
        if pygame.K_RIGHT in keys:
            news.x -= 10
        if pygame.K_LEFT in keys:
            news.x += 10
        for heart in hearts:
            if me.touches(news):
                news.y += 1000
                news.x = random.randrange(0, 1000)
                hearts.remove(heart)
                getting_hit_sound.play()
            # if me.touches(cnn) and timer <= 0:
            #     timer = 120
            #     hearts.remove(heart)
            #     getting_hit_sound.play()
            timer -= 1


    # Movement on platforms moving left
    for ground in platforms_moving_left:
        camera.draw(ground)
        ground.x -= 3
        if ground.right <= camera.left:
            ground.x += 1200
            ground.y = random.randrange(camera.top, camera.bottom)
            ground.width = random.randrange(50, 200)
        # Controls - Pressing down on a platform allows you do fall
        if me.bottom_touches(ground) and pygame.K_DOWN not in keys:
            me.move_to_stop_overlapping(ground, 0, -10)
        # if me.top_touches(ground):
        #     me.move_to_stop_overlapping(ground, 0, 11)
        if pygame.K_RIGHT in keys:
            ground.x -= 10
        if pygame.K_LEFT in keys:
            ground.x += 10
        if pygame.K_SPACE in keys and me.bottom_touches(ground) and jump_clock <= 0:
            me.speedy = -25
            jump_clock = 50
            jump_sound.play()
        jump_clock -= 1

    # Movement on platforms moving right
    for ground in platforms_moving_right:
        camera.draw(ground)
        ground.x += 3
        if ground.left >= camera.right:
            ground.x -= 1200
            ground.y = random.randrange(camera.top, camera.bottom)
            ground.width = random.randrange(50, 200)
        # Controls - Pressing down on a platform allows you to fall
        if me.bottom_touches(ground) and pygame.K_DOWN not in keys:
            me.move_to_stop_overlapping(ground, 0, -10)
        if pygame.K_RIGHT in keys:
            ground.x -= 10
        if pygame.K_LEFT in keys:
            ground.x += 10
        if pygame.K_SPACE in keys and me.bottom_touches(ground) and jump_clock <= 0:
            me.speedy = -25
            jump_clock = 50
            jump_sound.play()
        jump_clock -= 1

    # Movement midair
    if pygame.K_LEFT in keys:
        me.x -= 10
    if pygame.K_RIGHT in keys:
        me.x += 10
    me.image = donald[(ticks // 3) % 6]

    # Gravity
    me.speedy += 2
    me.move_speed()

    # camera.draw(cnn)
    camera.draw(score)

    for heart in hearts:
        camera.draw(heart)
    camera.draw(me)

    # end screen
    has_collision = False
    if me.y > 700:
        has_collision = True
    if has_collision or hearts == []:
        camera.draw(gamebox.from_color(camera.x, camera.y, "black", 790, 400))
        camera.draw(gamebox.from_text(camera.x, camera.y - 80, "GAME OVER", 'sys', 170, 'white'))
        camera.draw(gamebox.from_text(camera.x, camera.y + 20, "You scored "+str(game_score), "sys", 50, "white"))
        # below are end messages based on player score
        if ticks // 30 < 5:
            camera.draw(gamebox.from_text(camera.x, camera.y + 110, "FAKE NEWS!", 'sys', 100, 'white'))
        elif 5 <= ticks // 30 < 30:
            camera.draw(gamebox.from_text(camera.x, camera.y + 110, "Weak, very weak", 'sys', 100, 'white'))
        elif 30 <= ticks // 30 <= 100:
            camera.draw(gamebox.from_text(camera.x, camera.y + 110, "Not too bad", 'sys', 100, 'white'))
        elif 30 <= ticks // 30 <= 100:
            camera.draw(gamebox.from_text(camera.x, camera.y + 110, "BIGLY!", 'sys', 100, 'white'))
        gamebox.pause()

    camera.draw(score)
    camera.display()


gamebox.timer_loop(30, tick)