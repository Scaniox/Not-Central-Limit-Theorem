import pygame as pg
from pathlib import Path

vec2 = pg.math.Vector2

k2c_numeric = [(f"{i}") for i in range(10)]
k2c_alpha_lower = [chr(i) for i in range(ord("a"), ord("z")+1)]
k2c_alpha_upper = [chr(i) for i in range(ord("A"), ord("Z")+1)]
k2c_all = ["all"]

class Text(pg.sprite.Sprite):
    def __init__(self, game, start_rect, text):
        super().__init__()
        # store text to attribute
        self.game = game
        self.text = text

        # get font name
        font_name = self.game.config.text_font_name
        font_path = Path(self.game.config.img_pathX) / font_name

        # load font
        self.font = pg.font.SysFont("Arial", 30)
        self.text_colour = self.game.config.text_colour

        # rescale to generate image
        self.rect = start_rect
        self.rescale()

    
    def update(self, dt, events):
        # empty function to ensure functionality
        pass

    def rescale(self):
        # render text to image
        text_img = self.font.render(self.text, True, self.text_colour)
        scale_factor = self.rect.height / text_img.get_height()
        text_size = [text_img.get_width() * scale_factor, self.rect.height]
        text_img = pg.transform.scale(text_img, text_size)
        text_img_rect = text_img.get_rect()

        # scale image to width and height of rect
        self.image = pg.surface.Surface(self.rect.size, flags=pg.SRCALPHA)
        text_img_rect.center = vec2(self.rect.size) / 2
        self.image.blit(text_img, text_img_rect.topleft)


class Input_Box(pg.sprite.Sprite):
    def __init__(self, game, start_rect, default_text, allowed_keys ):
        super().__init__()
        # store attributes
        self.game = game
        self.default_text = default_text
        self.text = ""
        self.allowed_keys = allowed_keys
        self.selected = False

        # get font name
        font_name = self.game.config.text_font_name
        font_path = Path(self.game.config.img_pathX) / font_name

        # load font
        self.font = pg.font.Font(font_path.as_posix(), 20)
        self.text_colour = self.game.config.text_colour

        # rescale to generate image
        self.rect = pg.rect.Rect(start_rect)
        self.rescale()

    def update(self, dt, events):
        for event in events:
            # set selected to true if cursor in rect 
            # and left mouse button clicked, otherwise false
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos):
                    self.selected = True
                else:
                    self.selected = False
                self.rescale()

            # register key presses
            if event.type == pg.KEYDOWN and self.selected:
                # if key is backspace, remove last char from text
                if event.unicode == '\x08':
                        self.text = self.text[:-1]
                # if key is in keys to chars, append to keys
                elif event.unicode in self.allowed_keys or \
                   "all" in self.allowed_keys:
                    self.text += event.unicode
                self.rescale()
    
    def rescale(self):
        # if self.text isn't empty, render text
        if len(self.text) > 0:
            render_text = self.text
            # if self.selected, append _ to the end of the text to show this
            if self.selected:
                render_text += "_"
        # if self.text is empty, render default text
        else:
            render_text = self.default_text

        # render text to image
        text_img = self.font.render(render_text, False, self.text_colour)
        scale_factor = self.rect.height / text_img.get_height()
        text_size = [text_img.get_width() * scale_factor, self.rect.height]
        text_img = pg.transform.scale(text_img, text_size)
        text_img_rect = text_img.get_rect()

        # scale image to width and height of rect
        self.image = pg.surface.Surface(self.rect.size, flags=pg.SRCALPHA)
        self.image.fill((32,32,32))
        if self.selected:
            pg.draw.rect(self.image, (128,128,128), [0,0,*self.rect.size], 1)
        text_img_rect.center = vec2(self.rect.size) / 2
        self.image.blit(text_img, text_img_rect.topleft)


class Toggle(pg.sprite.Sprite):
    def __init__(self, game, start_rect):
        super().__init__()
        self.game = game

        # initialise ticked to false
        self.ticked = False

        self.ticked_img = self.game.img_loader.get("toggle ticked")
        self.unticked_img = self.game.img_loader.get("toggle unticked")
        self.click_snd = self.game.snd_loader.get("click.mp3")

        # init rect and render
        self.rect = pg.rect.Rect(start_rect)
        self.rescale()

    def update(self, dt, events):
        for event in events:
            if self.rect.collidepoint(pg.mouse.get_pos()):
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.ticked = not self.ticked
                    self.click_snd.play()
                    self.rescale()

    def rescale(self):
        # if ticked, render the ticked image
        if self.ticked:
            self.image = pg.transform.scale(self.ticked_img, self.rect.size)
        # if not ticked, render unticked image
        else:
            self.image = pg.transform.scale(self.unticked_img, self.rect.size)


class Slider(pg.sprite.Sprite):
    def __init__(self, game, start_rect):
        super().__init__()
        self.game = game

        # initialise val to 0
        self.val = 1
        self.grabbed = False

        # load assets
        self.slider_img = self.game.img_loader.get("slider.png")
        self.thumb_img = self.game.img_loader.get("slider thumb.png")

        self.grab_snd = self.game.snd_loader.get("click.mp3")

        # initalise rect and render
        self.rect = pg.rect.Rect(start_rect)
        self.rescale()

    def update(self, dt, events):
        mouse_pos = vec2(pg.mouse.get_pos())
        
        for event in events:
            # if mouse is clicked and hovering over thumb rect, grab
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.scrn_thumb_rect.collidepoint(mouse_pos):
                    self.grabbed = True
            # if mouse is unclicked, release 
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if self.grabbed:
                    self.grab_snd.play()
                self.grabbed = False

        # update val based of it is grabbed and mouse movement
        if self.grabbed:
            mouse_disp = pg.mouse.get_pos()[0] - self.rect.left
            self.val = (mouse_disp - (self.thumb_width/2)) /        \
                        (self.rect.width - self.thumb_width)
            self.val = min(max(0, self.val), 1)
            self.rescale()

    def rescale(self):
        # blit slider image
        self.image = pg.surface.Surface(self.rect.size, flags = pg.SRCALPHA)
        self.image.blit(pg.transform.scale(self.slider_img, self.rect.size),
                        (0,0))

        thumb_img = pg.transform.scale(self.thumb_img, [self.rect.height] * 2)
        self.thumb_width = thumb_img.get_width()

        # how many pixels over is the thum displaced:
        thumb_disp = self.val * (self.rect.width - self.thumb_width) 
        thumb_disp += self.thumb_width/2

        # find thumb collide rect
        self.scrn_thumb_rect = thumb_img.get_rect()
        self.scrn_thumb_rect.center = (self.rect.left + thumb_disp,
                                 self.rect.centery)

        # blit thumb to image
        thumb_rect = thumb_img.get_rect()
        thumb_rect.center = (thumb_disp, self.rect.height / 2)
        self.image.blit(thumb_img, thumb_rect)


class Spinner(pg.sprite.Sprite):
    def __init__(self, game, start_rect, options):
        super().__init__()
        self.game = game
        self.options = options
        self.index = 0

        # get font name
        font_name = self.game.config.text_font_name
        font_path = Path(self.game.config.img_pathX) / font_name

        # load font
        self.font = pg.font.Font(font_path.as_posix(), 20)
        self.text_colour = self.game.config.text_colour

        # load images and sounds
        self.arrows_img = self.game.img_loader.get("spinner arrows")
        self.end_hit_sound = self.game.snd_loader.get("spinner end.mp3")
        self.click_snd = self.game.snd_loader.get("click.mp3")

        self.rect = start_rect
        self.rescale()

    def update(self, dt, events):
        mouse_pos = pg.mouse.get_pos()
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                # if mouse is clicked over left button, decrease index
                if self.left_button_rect.collidepoint(mouse_pos):
                    if (self.index == 0):
                        self.end_hit_sound.play()
                    else:
                        self.index -= 1
                        self.click_snd.play()
                        self.rescale()
                # if mouse is clicked over right button, increase index
                elif self.right_button_rect.collidepoint(mouse_pos):
                    if (self.index == len(self.options)-1):
                        self.end_hit_sound.play()
                    else:
                        self.index += 1
                        self.click_snd.play()
                        self.rescale()

    def rescale(self):
        # blit image
        self.image = pg.transform.scale(self.arrows_img, self.rect.size)

        text_img = self.font.render(self.options[self.index], 
                                        False, self.text_colour)
        # rescale text to fit screen
        scale_factor = self.rect.height / text_img.get_height()
        text_size = [text_img.get_width() * scale_factor, self.rect.height]
        text_img = pg.transform.scale(text_img, text_size)
        text_img_rect = text_img.get_rect()

        # button rects
        self.left_button_rect = pg.rect.Rect(
                                        self.rect.left, 
                                        self.rect.top, 
                                        self.rect.width * 1/6, 
                                        self.rect.height    )
        self.right_button_rect = pg.rect.Rect(
                                        self.rect.left+self.rect.width * 5/6,
                                        self.rect.top,
                                        self.rect.width * 1/6, 
                                        self.rect.height    )

        # blit text
        text_img_rect.center = vec2(self.rect.size) / 2
        self.image.blit(text_img, text_img_rect)
        

class Button(pg.sprite.Sprite):
    def __init__(self, game, start_rect, text):
        super().__init__()
        self.game = game
        self.text = text

        # get font name
        font_name = self.game.config.text_font_name
        font_path = Path(self.game.config.img_pathX) / font_name

        # load font
        self.font = pg.font.Font(font_path.as_posix(), 20)
        self.text_colour = self.game.config.text_colour

        self.click_snd = self.game.snd_loader.get("click.mp3")

        self.pressed = [False] * 3
        self.rising_edges = [False] * 3
        self.falling_edges = [False] * 3

        self.rect = start_rect
        self.rescale()

    def update(self, dt, events):
        self.rising_edges = [False] * 3
        self.falling_edges = [False] * 3

        for event in events:
            # detect rising edges
            if self.rect.collidepoint(pg.mouse.get_pos()):
                if event.type == pg.MOUSEBUTTONDOWN and event.button <= 3:
                    self.rising_edges[event.button-1] = True
                    self.pressed[event.button-1] = True

                    self.click_snd.play()

                    self.rescale()
            
            # detect falling edges
            if event.type == pg.MOUSEBUTTONUP and event.button <= 3:
                if self.rect.collidepoint(pg.mouse.get_pos()) and \
                    self.pressed[event.button-1]:
                    self.falling_edges[event.button-1] = True
                self.pressed[event.button-1] = False

                self.rescale()

    def rescale(self):
        # rescale image to rect
        self.image = pg.surface.Surface(self.rect.size)
        self.image.fill((32,32,32))
        if not max(self.pressed):
            pg.draw.rect(self.image, (255,255,255), (0,0,self.rect.width-3,
                                                      self.rect.height-3), 3)
        else:
            pg.draw.rect(self.image, (255,255,255), (3,3,self.rect.width-3,
                                            self.rect.height-3), 3)

        # render text
        text_img = self.font.render(self.text, False, self.text_colour)
        # rescale text to fit screen
        scale_factor = self.rect.height / text_img.get_height()
        text_size = [text_img.get_width() * scale_factor, self.rect.height]
        text_img = pg.transform.scale(text_img, text_size)
        text_img_rect = text_img.get_rect()

        # blit text
        text_img_rect.center = vec2(self.rect.size) / 2
        self.image.blit(text_img, text_img_rect)