import pygame



window = pygame.display.set_mode((1000,1000))
game = True


class RectArea():
    dx, dy = 0, 0 #смещение камеры FOV
    def __init__(self, x, y, width, height, border_width=1, border_color='light green'):
        self.rect = pygame.Rect(x, y, width, height)
        self.border_width = border_width
        self.border_color = border_color
        RectArea.dx = x 
        RectArea.dy = y
        self.fov = pygame.Rect(self.dx,self.dy,width/12,height/12)
    
    #отрисовка миникарты
    def draw(self, win):
        pygame.draw.rect(win, self.border_color, self.rect, self.border_width)
        pygame.draw.rect(win, self.border_color, self.fov, self.border_width)
        print("Изменение dx, dy", RectArea.dx, RectArea.dy)

    #отслеживание клика по миникарте
    def click_handler(self):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] >= self.rect.x + self.fov.width // 2 and mouse_pos[0] <= self.rect.x + self.rect.width- self.fov.width // 2 and mouse_pos[1] >= self.rect.y + self.fov.height // 2 and mouse_pos[1] <= self.rect.y + self.rect.width - self.fov.height // 2:
            if pygame.mouse.get_pressed()[0]:
                RectArea.dx = pygame.mouse.get_pos()[0]-self.fov.width//2
                RectArea.dy = pygame.mouse.get_pos()[1]-self.fov.height//2
                self.fov = pygame.Rect(RectArea.dx,RectArea.dy, self.rect.width//12, self.rect.height//12)

    def draw_object(self,win,objects):
        for obj in objects:
            new_obj = pygame.Rect(0,0,0,0)
            new_obj.x = obj.rect.x // 12 + self.rect.x
            new_obj.y = obj.rect.y // 12 + self.rect.y
            new_obj.width = obj.rect.width // 12
            new_obj.height = obj.rect.height // 12
   
            pygame.draw.rect(win, obj.color, new_obj)
        

class Mob:
    def __init__(self, x,y, w,h):
        self.rect = pygame.Rect(x,y,w,h)
        self.color = (255,0,0)
        self.new_rect = pygame.Rect(x,y,w,h)

    def draw(self, win, mini_map):
        self.new_rect = pygame.Rect(0,0,0,0)
        self.new_rect.x = self.rect.x - (RectArea.dx-mini_map.rect.x) * 12
        self.new_rect.y = self.rect.y - (RectArea.dy-mini_map.rect.y) * 12
        self.new_rect.width = self.rect.width
        self.new_rect.height = self.rect.height
        #print("Позиция нового объекта", new_rect.x, new_rect.y)
        pygame.draw.rect(win, self.color, self.new_rect)
        #print(self.new_rect)

    def collide(self):
        if pygame.mouse.get_pressed()[0] and self.new_rect.collidepoint(pygame.mouse.get_pos()):
            print('КЛИК ПО ОБЪЕКТУ', self)


r = RectArea(0,750,250,250, 5)
mob = Mob(350,350,150,150)
mob2 = Mob(1350,1350,100,100)

objects = [mob, mob2]

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    window.fill((0,0,0))

    mob.draw(window, r)
    mob2.draw(window, r)
    mob.collide()
    mob2.collide()
    r.draw(window)
    r.click_handler()
    r.draw_object(window, objects)

    pygame.display.update()