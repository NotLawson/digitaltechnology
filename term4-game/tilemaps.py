import importlib as imlib

class Map:
    def __init__(self, map):
        map = imlib.import_module(f"maps.{map}.map")
        self.textures = map.textures
        self.map = map.map
        self.tilesize = map.tilesize
        self.height = map.height
        self.width = map.width
        self.types = map.tile_types
        self.tile_types = map.tile_types
        self.bg_colour = map.bg_colour

class TileTypes:
    solid = "1"
    air = "0"
    platform = "2"
    spawn = "3"
    hidingspot = "4"
    itemspawner = "5"

