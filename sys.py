import os
from PIL import Image

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


def is_in_rect(pos, rect):
    x, y = pos
    rx, ry, rw, rh = rect
    if (rx <= x <= rx + rw) and (ry <= y <= ry + rh):
        return True
    return False


class MovableObj(object):
    def __init__(self, x, y, w, h, img, visible: bool):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.img=img
        self.visible=visible
        self.is_move=None
        self.img.set_colorkey((255, 255, 255))

    def drag(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                w, h = self.img.get_size()
                if is_in_rect(event.pos, (self.x, self.y, w, h)):
                    self.is_move = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.is_move = False
            if event.type == pygame.MOUSEMOTION:
                if self.is_move:
                    x, y = event.pos
                    image_w, image_h = self.img.get_size()
                    # 保证鼠标在图片的中心
                    self.x=x-image_w/2
                    self.y=y-image_h/2
                    display.blit(self.img, (self.x, self.y))
        pygame.display.update()
        display.blit(self.img, (self.x, self.y))


def take_font(size):
    font=pygame.font.Font(os.path.join("disk/sys/fonts/arialbd.ttf"), size)
    return font


display=pygame.display.set_mode((width, height))


class Window(MovableObj):
    def __init__(self):
        super().__init__(width / 2, height / 2, 100, 100, img=pygame.image.load("disk/sys/images/window.jpg"),
                         visible=True)

    def update(self):
        super().drag()


class Table(object):
    def __init__(self):
        self.img=pygame.image.load("disk/sys/images/R-C (1).jpg")

    def update(self):
        display.blit(self.img, (0, 0))


class BottomContainer(object):
    def __init__(self):
        self.img=pygame.image.load("disk/sys/images/bottom.png")
        self.img.set_colorkey((255, 255, 255))

    def update(self):
        display.blit(self.img, (0, height-self.img.get_height()))


def update_system():
    Table().update()
    BottomContainer().update()


win=Window()
if __name__ == '__main__':
    while True:
        update_system()
        win.update()
        pygame.display.update()
