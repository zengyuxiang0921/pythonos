import pygame
import threading
from pygame.locals import MOUSEBUTTONDOWN


class BFControlId(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.id = 1

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(BFControlId, "_instance"):
            BFControlId._instance = BFControlId(*args, **kwargs)
        return BFControlId._instance

    def get_new_id(self):
        self.id += 1
        return self.id


CLICK_EFFECT_TIME = 100


class BFButton(object):
    def __init__(self, parent, rect, text='Button', click=None):
        self.x, self.y, self.width, self.height = rect
        self.bg_color = (225, 225, 225)
        self.parent = parent
        self.surface = parent.subsurface(rect)
        self.is_hover = False
        self.in_click = False
        self.click_loss_time = 0
        self.click_event_id = -1
        self.ctl_id = BFControlId().instance().get_new_id()
        self._text = text
        self._click = click
        self._visible = True
        self.init_font()

    def init_font(self):
        font = pygame.font.SysFont('arial', 28)
        white = 100, 100, 100
        self.textImage = font.render(self._text, True, white)
        w, h = self.textImage.get_size()
        self._tx = (self.width - w) / 2
        self._ty = (self.height - h) / 2

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.init_font()

    @property
    def click(self):
        return self._click

    @click.setter
    def click(self, value):
        self._click = value

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    def update(self, event):
        if self.in_click and event.type == self.click_event_id:
            if self._click: self._click(self)
            self.click_event_id = -1
            return

        x, y = pygame.mouse.get_pos()
        if x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height:
            self.is_hover = True
            if event.type == MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                if pressed_array[0]:
                    self.in_click = True
                    self.click_loss_time = pygame.time.get_ticks() + CLICK_EFFECT_TIME
                    self.click_event_id = pygame.USEREVENT+self.ctl_id
                    pygame.time.set_timer(self.click_event_id,CLICK_EFFECT_TIME-10)
        else:
            self.is_hover = False

    def draw(self):
        if self.in_click:
            if self.click_loss_time < pygame.time.get_ticks():
                self.in_click = False
        if not self._visible:
            return
        if self.in_click:
            r,g,b = self.bg_color
            k = 0.95
            self.surface.fill((r*k, g*k, b*k))
        else:
            self.surface.fill(self.bg_color)
        if self.is_hover:
            pygame.draw.rect(self.surface, (0,0,0), (0,0,self.width,self.height), 1)
            pygame.draw.rect(self.surface, (100,100,100), (0,0,self.width-1,self.height-1), 1)
            layers = 5
            r_step = (210-170)/layers
            g_step = (225-205)/layers
            for i in range(layers):
                pygame.draw.rect(self.surface, (170+r_step*i, 205+g_step*i, 255), (i, i, self.width - 2 - i*2, self.height - 2 - i*2), 1)
        else:
            self.surface.fill(self.bg_color)
            pygame.draw.rect(self.surface, (0,0,0), (0,0,self.width,self.height), 1)
            pygame.draw.rect(self.surface, (100,100,100), (0,0,self.width-1,self.height-1), 1)
            pygame.draw.rect(self.surface, self.bg_color, (0,0,self.width-2,self.height-2), 1)

        self.surface.blit(self.textImage, (self._tx, self._ty))


class InputBox:
    def __init__(self, rect: pygame.Rect = pygame.Rect(100, 100, 140, 32)) -> None:
        """
        rect，传入矩形实体，传达输入框的位置和大小
        """
        self.boxBody: pygame.Rect = rect
        self.color_inactive = pygame.Color('lightskyblue3')  # 未被选中的颜色
        self.color_active = pygame.Color('dodgerblue2')  # 被选中的颜色
        self.color = self.color_inactive  # 当前颜色，初始为未激活颜色
        self.active = False
        self.text = ''
        self.done = False
        self.font = pygame.font.Font(None, 32)

    def dealEvent(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.boxBody.collidepoint(event.pos):  # 若按下鼠标且位置在文本框
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if(
                self.active) else self.color_inactive
        if event.type == pygame.KEYDOWN:  # 键盘输入响应
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    # self.text=''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen: pygame.surface.Surface):
        txtSurface = self.font.render(
            self.text, True, self.color)  # 文字转换为图片
        width = max(200, txtSurface.get_width()+10)  # 当文字过长时，延长文本框
        self.boxBody.w = width
        screen.blit(txtSurface, (self.boxBody.x+5, self.boxBody.y+5))
        pygame.draw.rect(screen, self.color, self.boxBody, 2)


class ScrollList:
    """
    滚动列表
    """

    def __init__(self, x, y, w, h, surface_bg, surface_item, padding=(10, 5), spacing=10, callback=None):
        """
        构造滚动列表对象
        :param x: 在窗口中的位置
        :param y: 在窗口中的位置
        :param w: 宽度
        :param h: 高度
        :param surface_bg: 列表背景图
        :param surface_item: 列表每行的背景图
        :param padding: (上下内边距，左右内边距)
        :param spacing: 行距，第一个item的底部到下一个item的头部的距离
        :param callback: item被点中后的回调函数
        """

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.surface_bg = surface_bg
        self.surface_item = surface_item
        self.padding = padding
        self.spacing = spacing
        self.item_list = []  # item列表,格式：{"text":"6666","font":font,"data":data}，其中data是附带数据，可有可无
        self.callback = callback  # 鼠标触发的单击事件
        self.item_h = self.surface_item.get_height()
        # 缓冲区
        self.surface_buffer = None
        self.offset_y = 0  # 缓冲区偏移量
        # 当前偏移量
        self.current_offset_y = 0
        # 鼠标是否按下
        self.is_mouse_down = False
        # 鼠标按下时的坐标(相对坐标，以滚动列表左上角为原点)
        self.m_x = 0
        self.m_y = 0

    def set_buffer(self):
        """
        创建缓冲区
        """
        # 宽度
        buffer_width = self.surface_bg.get_width() - self.padding[1] * 2
        # 高度
        buffer_height = len(self.item_list) * (self.surface_item.get_height() + self.spacing)
        # 创建缓冲区
        self.surface_buffer = pygame.Surface((buffer_width, buffer_height), flags=pygame.SRCALPHA)
        pygame.Surface.convert(self.surface_buffer)
        self.surface_buffer.fill(pygame.Color(255, 255, 255, 0))

        # 画列表
        for i in range(len(self.item_list)):
            self.surface_buffer.blit(self.surface_item, (0, i * (self.item_h + self.spacing)))
            pygame.TextView().draw_text(self.surface_buffer, 15, 22 + i * (self.item_h + self.spacing),
                                 self.item_list[i]['text'],
                                 self.item_list[i]['font'], self.item_list[i]['color'])

    def mouse_move(self, x, y):
        if not self.is_mouse_down:
            return
        # 计算偏移量
        _, d_y = self.get_dxy(x, y)
        self.current_offset_y = d_y - self.m_y
        # 限制拖动范围
        if self.current_offset_y + self.offset_y >= 0:
            self.current_offset_y = 0
            self.offset_y = 0
            # self.is_mouse_down = False

        if self.current_offset_y + self.offset_y <= self.surface_bg.get_width() - self.surface_buffer.get_height():
            self.current_offset_y = 0
            self.offset_y = self.surface_bg.get_width() - self.surface_buffer.get_height()

    def mouse_down(self, x, y):
        if not self.mouse_in_panel(x, y):
            return
        self.is_mouse_down = True
        # 获取相对坐标
        self.m_x, self.m_y = self.get_dxy(x, y)

    def mouse_up(self, x, y):
        d_x, d_y = self.get_dxy(x, y)
        if d_x == self.m_x and d_y == self.m_y:
            # 单纯的点击事件，没有拖动
            try:
                if self.callback is not None:
                    index = (-self.offset_y + self.m_y) // (self.item_h + self.spacing)
                    self.callback(self.item_list[index]['data'])
            except:  # 下标越界
                pass
        else:
            # 拖动事件
            self.offset_y += self.current_offset_y
            self.current_offset_y = 0
        self.is_mouse_down = False

    def mouse_in_panel(self, x, y):
        # 计算相对坐标
        dx, dy = self.get_dxy(x, y)

        return 0 < dx < self.w and 0 < dy < self.h

    def get_dxy(self, x, y):
        # 计算相对坐标
        dx = x - self.x
        dy = y - self.y
        return dx, dy

    def add_item(self, font, text="", color=(233, 115, 115), data=None):
        """
        添加行
        :param font: 字体
        :param text: 显示的文字
        :param color: 文字颜色
        :param data: 附带数据
        """
        item = {
            "text": text,
            "font": font,
            "color": color,
            "data": data
        }
        self.item_list.append(item)
        self.set_buffer()

    def clear_item(self):
        """
        清空列表
        """
        self.item_list = []

    def draw(self, dest_suf):
        # 画背景图
        dest_suf.blit(self.surface_bg, (self.x, self.y))
        # 画item
        dest_suf.blit(self.surface_buffer, (self.x + self.padding[1], self.y + self.padding[0]),
                      (0, -(self.current_offset_y + self.offset_y), self.surface_buffer.get_width(),
                       self.surface_bg.get_height() - self.padding[0] * 2))