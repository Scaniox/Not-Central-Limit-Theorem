import pygame as pg
import config as cfg
import Asset_Loader as AL
import Menu_System as MSYS

class Game():
    def __init__(self):
        self.game_state_stack = []

        # init pygame env
        pg.init()
        pg.mixer.init()

        # init config
        self.config = cfg.Config()

        # init video
        self.set_screen()

        # init loaders
        self.img_loader = AL.Img_Loader(self)
        self.snd_loader = AL.Snd_Loader(self)

        pg.display.set_caption("Normal Sampling Distribution")
        pg.display.set_icon(self.img_loader.get("icon1"))

        # init screens other than level

        self.main_screen = MSYS.Main(self)

        # push main menu onto game state stack
        self.game_state_stack.append(self.main_screen.tick)

        # call run
        self.run()

        # after running terminates, close
        pg.quit()

    def run(self):
        # main loop
        clock = pg.time.Clock()
        while len(self.game_state_stack) > 0:
            # calculate dt
            if self.config.vsync:
                # delay to achieve correct frame rate
                dt = clock.tick(60)
            else:
                dt = clock.tick()

            # event collect events
            event_list = list(pg.event.get())

            # check events
            for event in event_list:
                # close event: close the game
                if event.type == pg.QUIT:
                    return

            # call correct tick function
            self.game_state_stack[-1](event_list, dt)

            pg.display.flip()


    def set_screen(self):
        """sets the display mode based on parameters in config"""           
        self.screen = pg.display.set_mode(self.config.resolution)

    def rescale(self):
        self.set_screen()

        # call rescale method of all screens
        self.main_screen.rescale()

Game()