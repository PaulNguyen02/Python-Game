import pgzrun, random
from random import randint

WIDTH, HEIGHT = 800, 600
WHITE, VIOLET = (255,255,255), (255,0,255)

# Khai báo biến
diem = 0
ket_thuc = False

# Định dạng hình nền
background = Actor("bg3")

# Định dạng xe tăng
tank = Actor('tank3')
tank.x, tank.y = 370, 550

# Định dạng vật phẩm
item = Actor('item3')
item.x, item.y = 200, 0

# Định dạng chướng ngại vật
rock = Actor('rock3')
rock.x, rock.y = 400, 0

# Cơ chế điều khiển xe tăng bằng chuột
def on_mouse_move(pos,rel,buttons):
    tank.x = pos[0]
    tank.y = pos[1]

sounds.astro3.play()
sounds.astro3.set_volume(0.5)

# Xử lí các vật thể và tính điểm
def update():
    global diem, ket_thuc
    # Tăng tốc độ dựa vào điểm
    item.y = item.y + 4 + diem / 4
    rock.y = rock.y + 4 + diem / 4
    # Xử lí giới hạn của màn hình
    if item.y > 600:
        item.y = 0
    if rock.y > 600:
        rock.y = 0
    # Xe tăng nhặt vật phẩm
    if item.colliderect(tank):
        item.x = random.randint(20,780)
        item.y = 0
        diem += 1
        sounds.bruh3.play()
    # Xe tăng tông trúng cục đá
    if rock.colliderect(tank):
        ket_thuc = True
        sounds.bumm3.play()
        sounds.astro3.stop()

# Đưa các đối tượng và thông báo ra màn hình
def draw():
    background.draw()
    if ket_thuc:
        screen.draw.text('Tro choi ket thuc',(360,300), color = WHITE, fontsize=60)
        screen.draw.text('Tong diem: '+ str(diem),(360,350), color = VIOLET, fontsize=80)
    else:
      screen.draw.text('Diem: '+ str(diem),(10,15), color = WHITE, fontsize=60)
      tank.draw()
      item.draw()
      rock.draw()
pgzrun.go()