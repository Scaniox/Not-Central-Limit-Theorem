import re
from pathlib import Path
import sys

class Config():
    def __init__(self):
        # get file paths
        if getattr(sys, 'frozen', False):
            # is running in exe
            if hasattr(sys, '_MEIPASS'):
                app_path = Path(sys._MEIPASS)
                exe_parent_path = Path(sys.executable).parent
            else:
                print("can't find local path")
                input()
        else:
            # is running in python interpreter
            app_path = Path(__file__).parent
            exe_parent_path = app_path

            
        #print(f"local path: {app_path}, exe parent path: {exe_parent_path}")

        # file paths: they are in reference to the game root foolder
        self.img_pathX = (app_path / 'img').as_posix()
        self.snd_pathX = (app_path / 'snd').as_posix()
        self.scoreboard_pathX = (exe_parent_path / 'scoreboard.csv').as_posix()
        self.xlsx_path = exe_parent_path / 'data.xlsx'

        # graphics config
        self.resolution = [800, 600]
        self.rescaleable = True
        self.fullscreen = False
        self.vsync = True
        self.coloursX = [(0xAC, 0x32, 0x32),
                        (0xDF, 0x71, 0x26),
                        (0x99, 0XE5, 0X50),
                        (0X00, 0X50, 0xEF),
                        (0X76, 0X42, 0X8A),
                        (0X00, 0XCC, 0XCC)]
        self.camera_zoom = 10
        self.key_frame_count = 10
        self.key_displacement = 4

        # sound
        self.game_vol = 1.0
        self.music_vol = 0.46683673469387754
        self.player_step_snd_delay = 300

        # fonts
        self.text_colour = (0, 0, 0)
        self.text_font_name = 'Arial'

        # walking sprites
        self.player_hurt_cooldown = 500
        self.player_max_health = 5
        self.player_max_speed = 0.05
        self.player_acc = 0.3
        self.enemy_speed = 0.02

        # maze generation
        self.maze_blocks_start_proportion = 0.08333333333333333
        self.maze_blocks_distance_proportion = 0.16666666666666666
        self.maze_gateway_jitter = 0
        self.maze_gateway_skip_threshold = 0.2
        self.maze_branch_stop_threshold = 0.05
        self.maze_key_count = 6
        self.maze_checkpoint_count = 5
        self.maze_enemy_count = 6
        self.walls_width_px = 16
        self.walls_height_px = 24

    # self modifying code: save the attributes  by rewriting this file
    def save(self):
        self_file = open(__file__, "r")
        self_file_str = self_file.read()
        self_file.close()

        for identifier, val in self.__dict__.items():
            if identifier[-1] != "X":
                self_file_str = re.sub(f" self.{identifier} = .+\n",
                                    f" self.{identifier} = {repr(val)}\n",
                                    self_file_str)

        self_file = open(__file__, "w")
        self_file.write(self_file_str)
        self_file.close()
