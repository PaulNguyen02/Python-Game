import pygame
import os
pygame.init()

WIDTH, HEIGHT = 900, 500        
pygame.display.set_caption("Đối kháng")     #hiện thị dòng chữ đối kháng

WHITE, BLACK, RED, GREEN, BLUE = (255, 255, 255), (0, 0, 0), (255, 0, 0), (34, 177, 76), (0, 162, 232)      #đặt cac biến màu

WINDOWS = pygame.display.set_mode((WIDTH, HEIGHT))  #set kích thước khung nhìn

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)       #chia biên giới với độ rộng là 10

BULLET_HIT_SOUND = pygame.mixer.Sound('sounds/bumm1.mp3') 
BULLET_FIRE_SOUND = pygame.mixer.Sound('sounds/gun1.mp3')
SOUND_TRACK = pygame.mixer.Sound('sounds/astro1.mp3')

MANG_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

MAX_vien_dan = 3 # Số lượng đạn tối đa có thể bắn trong 1 đợt
TANK_WIDTH, TANK_HEIGHT = 55, 40

GREEN_HIT = pygame.USEREVENT + 1 # Mã sự kiện 1
RED_HIT = pygame.USEREVENT + 2 # Mã sự kiện 2

# Gán hình ảnh cho các biến để dễ dàng thao tác
GREEN_TANK_IMAGE = pygame.image.load(os.path.join('images', 'tankplayer1.png')) # loadhình xe tăng
GREEN_TANK = pygame.transform.rotate(pygame.transform.scale(GREEN_TANK_IMAGE, (TANK_WIDTH, TANK_HEIGHT)), 90) #hình chuyển động của xe tăng 

RED_TANK_IMAGE = pygame.image.load(os.path.join('images', 'tankdich1.png')) # loadhình xe tăng địch
RED_TANK = pygame.transform.rotate(pygame.transform.scale(RED_TANK_IMAGE, (TANK_WIDTH, TANK_HEIGHT)), 270)

BGWAR = pygame.transform.scale(pygame.image.load(os.path.join('images', 'chientruong1.png')), (WIDTH, HEIGHT))

# Đưa các đối tượng và vật thể lên màn hình
def draw_window(red, green, red_vien_dan, green_vien_dan, red_mang, green_mang):
    
    WINDOWS.blit(BGWAR, (0, 0)) #set hình nền ở vị trí mặc định 0,0

    # Ranh giới phân chia hai chiến tuyến
    pygame.draw.rect(WINDOWS, BLUE, BORDER)

    red_mang_text = MANG_FONT.render("Mang Song: " + str(red_mang), 1, RED)     #Chữ mạng sống
    green_mang_text = MANG_FONT.render("Mang Song: " + str(green_mang), 1, GREEN)
    WINDOWS.blit(red_mang_text, (WIDTH - red_mang_text.get_width() - 10, 10))   #Set vị trí của chữ mạng
    WINDOWS.blit(green_mang_text, (10, 10))

    WINDOWS.blit(GREEN_TANK, (green.x, green.y))    #set vị trí cho 2 xe tăng
    WINDOWS.blit(RED_TANK, (red.x, red.y))

    for dan in red_vien_dan:
        pygame.draw.rect(WINDOWS, RED, dan)     #xe tăng bắn 1 lượt 3 viên, mỗi viên là hình chữ nhật

    for dan in green_vien_dan:
        pygame.draw.rect(WINDOWS, GREEN, dan)

    pygame.display.update()                     #animation 

# Cơ chế điều khiển của xe tăng XANH
def dieu_khien_tank_green(phimDK, green):
    if phimDK[pygame.K_a] and green.x - 5 > 0:  # TRÁI
        green.x -= 5 # Tốc độ di chuyển bằng 5
    if phimDK[pygame.K_d] and green.x + 5 + green.width < BORDER.x:  # PHẢI
        green.x += 5
    if phimDK[pygame.K_w] and green.y - 5 > 0:  # LÊN
        green.y -= 5
    if phimDK[pygame.K_s] and green.y + 5 + green.height < HEIGHT - 15:  # XUỐNG
        green.y += 5

# Cơ chế điều khiển của xe tăng ĐỎ
def dieu_khien_tank_red(phimDK, red):
    if phimDK[pygame.K_LEFT] and red.x - 5 > BORDER.x + BORDER.width:  # TRÁI 
        red.x -= 5
    if phimDK[pygame.K_RIGHT] and red.x + 5 + red.width < WIDTH:  # PHẢI
        red.x += 5
    if phimDK[pygame.K_UP] and red.y - 5 > 0:  # LÊN
        red.y -= 5
    if phimDK[pygame.K_DOWN] and red.y + 5 + red.height < HEIGHT - 15:  # XUỐNG
        red.y += 5

# Cơ chế bắn đạn của cả hai xe tăng
def xu_li_ban_dan(green_vien_dan, red_vien_dan, green, red):
    for dan in green_vien_dan:
        dan.x += 7      # Tốc độ đạn đi
        if red.colliderect(dan):
            pygame.event.post(pygame.event.Event(RED_HIT))
            green_vien_dan.remove(dan) # Xóa đạn khi bắn trúng kẻ địch
        elif dan.x > WIDTH:
            green_vien_dan.remove(dan) # Xóa đạn khi ra khỏi bản đồ

    for dan in red_vien_dan:
        dan.x -= 7
        if green.colliderect(dan):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            red_vien_dan.remove(dan)
        elif dan.x < 0:
            red_vien_dan.remove(dan)

# In ra thông báo thông báo thắng hoặc thua

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOWS.blit(draw_text, (WIDTH/2 - draw_text.get_width() /2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000) # Đấu lại sau khoảng thời gian


# Hàm Main gọi lại các cơ chế xử lí phía trên và thêm các chức năng phụ
def main():

    green = pygame.Rect(100, 300, TANK_WIDTH, TANK_HEIGHT)
    red = pygame.Rect(700, 300, TANK_WIDTH, TANK_HEIGHT)

    red_vien_dan = []
    green_vien_dan = []

    red_mang = 10
    green_mang = 10

    SOUND_TRACK.play()
    SOUND_TRACK.set_volume(0.5)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60) # FPS: 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(green_vien_dan) < MAX_vien_dan:
                    dan = pygame.Rect(green.x + green.width, green.y + green.height//2 - 2, 10, 5)
                    green_vien_dan.append(dan)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(red_vien_dan) < MAX_vien_dan:
                    dan = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_vien_dan.append(dan)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_mang -= 1
                BULLET_HIT_SOUND.play()

            if event.type == GREEN_HIT:
                green_mang -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_mang <= 0:
            winner_text = "GREEN WIN !"
            SOUND_TRACK.stop()

        if green_mang <= 0:
            winner_text = "RED WIN !"
            SOUND_TRACK.stop()

        if winner_text != "":
            draw_winner(winner_text)
            break

        phimDK = pygame.key.get_pressed()
        dieu_khien_tank_green(phimDK, green)
        dieu_khien_tank_red(phimDK, red)

        xu_li_ban_dan(green_vien_dan, red_vien_dan, green, red)

        draw_window(red, green, red_vien_dan, green_vien_dan, red_mang, green_mang)

    main()

if __name__ == "__main__":
    main()