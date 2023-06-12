import pgzrun, random, pygame

WIDTH, HEIGHT = 800, 600
BLACK, WHITE, GREEN, RED = (0,0,0), (255,255,255), (0,255,0), (255,0,0)

SIZE_TANK = 25 # Kích thước xe tăng bằng 1 nửa ô tường
bucTuong = []
danPlayer = []
danDich = []
playerNapDan = 0
dichNapDan = 0
dichDiChuyen = 0
ketThuc = False
keDich = []

# ĐỊNH DẠNG XE TĂNG BÊN PLAYER
tank = Actor("tankplayer2")
tank.pos = (WIDTH/2, HEIGHT - SIZE_TANK)
tank.angle = 90 

# ĐỊNH DẠNG XE TĂNG BÊN KẺ ĐỊCH 
for i in range (6): 
    dich = Actor("tankdich2")
    dich.x = i * 100 + 100 # Khoang cach = 100
    dich.y = SIZE_TANK
    dich.angle = 270
    keDich.append(dich)

# ĐỊNH DẠNG NỀN VÀ CÁC TƯỜNG CHẮN
background = Actor("chientruong2")
for x in range(16):
    for y in range(10):
        if random.randint(0,100) < 50:
            tuong = Actor("tuong2")
            tuong.x = x * 50  + SIZE_TANK
            tuong.y = y * 50 + SIZE_TANK*3
            bucTuong.append(tuong)

def tank_set(): # TANK PLAYER
    pos_x, pos_y = tank.x, tank.y

    # MOVE TANK PLAYER
    if keyboard.a:
        # Ở đây tốc độ xe tăng là 2
        tank.x = tank.x - 2  
        tank.angle = 180
    elif keyboard.d:
        tank.x = tank.x + 2
        tank.angle = 0
    elif keyboard.w:
        tank.y = tank.y - 2
        tank.angle = 90
    elif keyboard.s:
        tank.y = tank.y + 2
        tank.angle = 270    
    
    # ĐIỀU KIỆN để tank không đi qua được tường
    if tank.collidelist(bucTuong) != -1:
        tank.x = pos_x
        tank.y = pos_y
        
    # ĐIỀU KIỆN để tank không đi ra khỏi map
    if tank.x < SIZE_TANK or tank.x > WIDTH - SIZE_TANK or tank.y > HEIGHT - SIZE_TANK:
        tank.x = pos_x
        tank.y = pos_y

def tank_bullet_set(): # CƠ CHẾ DI CHUYỂN VÀ BẮN CỦA PLAYER
    global playerNapDan # Delay sau mỗi lần bắn
    if playerNapDan == 0:
        if keyboard.space:
            # Định dạng đạn của player
            dan = Actor("dan2")
            dan.angle = tank.angle

            if dan.angle == 0:
                dan.pos = (tank.x + SIZE_TANK, tank.y)
            if dan.angle == 90:
                dan.pos = (tank.x, tank.y + SIZE_TANK)
            if dan.angle == 180:
                dan.pos = (tank.x - SIZE_TANK, tank.y)
            if dan.angle == 270:
                dan.pos = (tank.x, tank.y + SIZE_TANK)

            danPlayer.append(dan)
            playerNapDan = 150
    else:
        playerNapDan -= 1

        # Đường di chuyển của đạn người chơi
        for dan in danPlayer:
            if dan.angle == 0:
                dan.x += 5
            if dan.angle == 90:
                dan.y -= 5
            if dan.angle == 180:
                dan.x -= 5
            if dan.angle == 270:
                dan.y += 5

        # Phá hủy tường bằng đạn
        for dan in danPlayer:
            bucTuong_index = dan.collidelist(bucTuong)
            if bucTuong_index != -1:
                sounds.fire2.play()
                del bucTuong[bucTuong_index]
                danPlayer.remove(dan)

            # XÓA ĐẠN KHI CHẠM RÌA MAP --> GIẢM DUNG LƯỢNG RAM
            if dan.x < 0 or dan.x > WIDTH or dan.y < 0 or dan.y > HEIGHT:
                danPlayer.remove(dan)

            # Khi đạn của người chơi va chạm với xe tăng địch
            dich_index = dan.collidelist(keDich)
            sounds.bumm2.play()
            if dich_index != -1:
                danPlayer.remove(dan)
                del keDich[dich_index]
                
def enemy_set(): # THIẾT LẬP CƠ CHẾ DI CHUYỂN TỰ ĐỘNG VÀ BẮN ĐẠN TỰ ĐỘNG CHO KẺ ĐỊCH
    global dichDiChuyen, dichNapDan

    for dich in keDich:
        pre_x, pre_y = dich.x, dich.y
        choice = random.randint(0,2)

        if dichDiChuyen > 0:
            dichDiChuyen -= 1

            if dich.angle == 0:
                dich.x += 2
            elif dich.angle == 90:
                dich.y -= 2            
            elif dich.angle == 180:
                dich.x -= 2
            elif dich.angle == 270:
                dich.y += 2

            if dich.x < SIZE_TANK or dich.x > (WIDTH - SIZE_TANK) or dich.y < SIZE_TANK or dich.y > (HEIGHT - SIZE_TANK):
                dich.x = pre_x
                dich.y = pre_y
                dichDiChuyen = 0

            if dich.collidelist(bucTuong) != -1:
                dich.x = pre_x
                dich.y = pre_y
                dichDiChuyen = 0

        elif choice == 0: # Xe tăng địch di chuyển 
            dichDiChuyen = 30
        elif choice == 1: # Xe tăng địch đổi hướng
            dich.angle = random.randint(0,3)*90
        else:             # Xe tăng địch bắn
            if dichNapDan == 0:
                dan = Actor("dan2")
                dan.angle = dich.angle
                dan.pos = dich.pos
                danDich.append(dan)
                dichNapDan = 40
            else:
                dichNapDan -= 1

def enemy_bullet_set(): # CƠ CHẾ KHI BẮN CỦA KẺ ĐỊCH
    global keDich, ketThuc
    for dan in danDich:
        if dan.angle == 0:
            dan.x += 5
        if dan.angle == 180:
            dan.x -= 5
        if dan.angle == 90:
            dan.y -= 5
        if dan.angle == 270:
            dan.y += 5 

# KHI ĐẠN KẺ ĐỊCH PHÁ TƯỜNG, BẮN NGƯỜI CHƠI PLAYER
        for dan in danDich:
            tuong_index = dan.collidelist(bucTuong)
            if tuong_index != -1:
                sounds.guns2.play()
                del bucTuong[tuong_index]
                danDich.remove(dan)

            # Tương tự như người chơi, ta sẽ xóa đạn của kẻ địch khi chúng đi ra khỏi map
            if dan.x < 0 or dan.x > WIDTH or dan.y > HEIGHT:
                danDich.remove(dan)
               
            if dan.colliderect(tank):
                ketThuc = True
                keDich = []

sounds.astro2.set_volume(0.5) # Âm lượng nhạc nền 50 %
sounds.astro2.play()

def update():
    tank_set()
    tank_bullet_set()
    enemy_set()
    enemy_bullet_set()

def draw():
    if ketThuc:
        screen.fill(BLACK)
        screen.draw.text('MISSION FAILED',(130,250), color = RED, fontsize = 100)
        sounds.astro2.stop()
    elif len(keDich) == 0:
        screen.fill(BLACK)
        screen.draw.text('MISSION SUCCESS',(130,250), color = GREEN, fontsize = 100)
        sounds.astro2.stop()
    else:
        background.draw()
        tank.draw()
        for tuong in bucTuong:
            tuong.draw()
        for dan in danPlayer:
            dan.draw()
        for dich in keDich:
            dich.draw()

    for dan in danDich:
        dan.draw()
pgzrun.go()