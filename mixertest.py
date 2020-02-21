import pygame
import time

gameDisplay = pygame.display.set_mode((1000, 600))
pygame.joystick.init()
print("number: ",pygame.joystick.get_count())
#generate chars
sticks=[]
for i in range(pygame.joystick.get_count()):
    sticks.append(pygame.joystick.Joystick(i))
    sticks[-1].init()

jump_out =False
while jump_out == False:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jump_out = True
    
    print("a", sticks[0].get_axis(2))
    print("b", sticks[0].get_axis(3))
    print("c", sticks[0].get_axis(4))
    time.sleep(0.1)
    
    pygame.draw.rect(gameDisplay, (50, 50, 50), (0, 0, 1000, 600), 0)
    pygame.draw.rect(gameDisplay, (100, 200, 255), (100, 0, 800, 500), 0)
        
    pygame.display.update()
    
pygame.quit()
quit()

"""

pressed = {a:1, b:0} = pygame.get_pressed()

pressed = stick[x].get_axis()>0.5
stick[x].get_button()
"""