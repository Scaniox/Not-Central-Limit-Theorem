import pygame as pg
from pathlib import Path
import xml.etree.ElementTree as ET


class Img_Loader():
    def __init__(self, game):
        self.game = game
        self.assets = {}
        self.sprite_sheets = []

        # load sprite sheets
        img_path = Path(self.game.config.img_pathX)
        for file_path in img_path.glob("*"):
            file_name = file_path.as_posix()
            if file_name.endswith(".xml"):
                # create a sprite sheet object for each xml file in img_path
                self.sprite_sheets.append(Sprite_Sheet(game, file_name[:-4]))

    def get(self, img_name):
        image = False
        # check already loaded assets for the image
        if img_name in self.assets.keys():
            return self.assets[img_name]

        # check for the image in the image folder
        elif (loaded_img := self.load(img_name)):
            image = loaded_img

        # try to find sprite in spritesheets
        else:
            for sheet in self.sprite_sheets:
                if loaded_image := sheet.get(img_name):
                    # when we find an image, stop looking
                    image = loaded_image
                    break

        # sprite cant be found
        if not(image):
            image = pg.surface.Surface((10, 10)).convert_alpha()
            image.fill((255, 0, 255))

        # cache and return image
        self.assets[img_name] = image
        return image

    def load(self, img_name):
        # search img_path for images
        img_path = Path(self.game.config.img_pathX)
        # iterate through files in img_path
        for file_path in img_path.glob("*"):
            if file_path.name.startswith(img_name):
                # if the names match, load image and return it
                image = pg.image.load(file_path.as_posix()).convert_alpha()
                return image

        # no image was found
        return False


class Snd_Loader():
    def __init__(self, game):
        self.game = game
        self.assets = {}

    def get(self, snd_name):
        # check in assets
        if snd_name in self.assets.keys():
            return self.assets[snd_name]

        # try to load sound
        if loaded_sound := self.load(snd_name):
            self.assets[snd_name] = loaded_sound
            return loaded_sound

        # failed to load sound, return generic sound
        else:
            no_sound_path = Path(__file__).parent / "snd" / "no_sound.wav"
            return pg.mixer.Sound(no_sound_path.as_posix())

    def load(self, snd_name):
        snd_path = Path(self.game.config.snd_pathX)
        # iterate through all files in snd_path
        for file_path in snd_path.rglob("*"):
            if file_path.name.startswith(snd_name):
                # return the sound if it has the correct name
                return pg.mixer.Sound(file_path.as_posix())


class Sprite_Sheet():
    def __init__(self, game, sheet_path):
        self.game = game
        self.sheet_path = sheet_path
        self.sprite_coords = {}

        # ensure img and xml are loadable
        img_path = Path(sheet_path + ".png")
        xml_path = Path(sheet_path + ".xml")
        if img_path.is_file() and xml_path.is_file():
            # load image
            self.img = pg.image.load(img_path.as_posix()).convert_alpha()

            # load xml
            self.load_xml(xml_path)

    def load_xml(self, xml_path):
        # load xml tree
        xml_tree_root = ET.parse(xml_path.as_posix()).getroot()
        # iterate through entries in the xml file
        for entry in xml_tree_root:
            # extract name and rect 
            attributes = entry.attrib
            name = attributes["name"]
            rect = [int(attributes[i]) for i in ["x", "y", "width", "height"]]
            # store to sprite_coords
            self.sprite_coords[name] = rect


    def get(self, sprite_name):
        # check the this sheet has this sprite
        if sprite_name in self.sprite_coords.keys():
            # find the rect of the requested sprite
            rect = self.sprite_coords[sprite_name]
            # gain the sprite surface
            image = self.img.subsurface(rect)
            image_copy = pg.surface.Surface(image.get_size())
            image_copy.blit(image, (0,0))
            return image
            
        # no sprite found
        return False
