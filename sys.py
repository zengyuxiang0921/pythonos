import os
import time

import pygame
import tkinter
tk = tkinter.Tk()
width = tk.winfo_screenwidth()
height = tk.winfo_screenheight()
tk.quit()
pygame.init()
mouse=pygame.image.load("disk/sys/R-C.jpg")
mouse.set_colorkey((255, 255, 255))
pygame.display.set_caption("sys")


def take_font(size):
    font=pygame.font.Font(os.path.join("disk/sys/fonts/arialbd.ttf"), size)
    return font


display=pygame.display.set_mode((width, height))


class Window(object):
    def __init__(self, x, y, w, h, visible=True):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.visible=visible
        self.img=pygame.image.load("disk/sys/images/window.jpg").convert()
        display.fill((255, 255, 255))
        display.blit(self.img, (self.x, self.y))
        pygame.display.flip()
        self.is_move = False
        self.img.set_colorkey((255, 255, 255))
        pygame.transform.scale(display, (w, h))

    def is_in_rect(self, pos, rect):
        x, y = pos
        rx, ry, rw, rh = rect
        if (rx <= x <= rx + rw) and (ry <= y <= ry + rh):
            return True
        return False

    def drag(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                w, h = self.img.get_size()
                if self.is_in_rect(event.pos, (self.x, self.y, w, h)):
                    self.is_move = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.is_move = False
            if event.type == pygame.MOUSEMOTION:
                if self.is_move:
                    display.fill((255, 255, 255))
                    x, y = event.pos
                    image_w, image_h = self.img.get_size()
                    # 保证鼠标在图片的中心
                    self.x=x-image_w/2
                    self.y=y-image_h/2
                    display.blit(self.img, (self.x, self.y))
        pygame.display.update()


class Table(object):
    def __init__(self):
        self.img=pygame.image.load("disk/sys/images/R-C (1).jpg")
        display.blit(self.img, (0, 0))
        pygame.display.flip()


win=Window(width/2, height/2, 200, 200)
while True:
    win.drag()
    Table()

