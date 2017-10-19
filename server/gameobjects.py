

from placable import GameObject
import playerent
import random
import entity


# todo: composition

class Wall(GameObject):
    
    char = 'wall'
    size = 2
    attributes = {
        "solid",
        }


class Rock(GameObject):
    
    char = 'rock'
    size = 10
    attributes = {
        "solid",
        }
    


class Tree(GameObject):
    
    char = 'tree'# 🌳♣♠𐇲𐂷
    size = 3
    attributes = {
        "solid",
        }


class Stone(GameObject):
    
    char = 'stone' # •
    size = 0.2
    attributes = {
        "takable",
        }


class Pebble(GameObject):
    
    char = 'pebble'
    size = 0.2
    attributes = {
        "takable",
        }


class Grass(GameObject):
    
    size = 0.15
    
    def __init__(self, *args):
        self.char = random.choice(["ground", "grass1", "grass2", "grass3"])

class Floor(GameObject):
    
    char = "floor"
    size = 0.1

class Ground(GameObject):
    
    char = "ground"
    size = 0.1

class Water(GameObject):
    
    char = "water"
    size = 0.1
    attributes = {
        "solid"
        }

class Anything(GameObject):
    
    # test object to see if arguments work
    
    size = 1
    
    def __init__(self, room, pos, char):
        self.char = char

class RoomExit(GameObject):
    
    def __init__(self, room, destRoom, destPos=None, char="exit", size=1):
        self.destRoom = destRoom
        self.destPos = destPos
        self.char = char
        self.size = size
    
    def onEnter(self, obj):
        observable = obj.getComponent("observable")
        if observable:
            observable.trigger("changeroom", self.destRoom, self.destPos)


objectdict = {
    "wall": Wall,
    "tree": Tree,
    "player": playerent.Player,
    "stone": Stone,
    "pebble": Pebble,
    "rock": Rock,
    #"rabbit": Rabbit,
    "grass": Grass,
    "water": Water,
    "floor": Floor,
    "ground": Ground,
    "anything": Anything,
    "roomexit": RoomExit,
    "entity": entity.Entity
    }


def makeObject(objtype, *args, **kwargs):
    return objectdict[objtype](*args, **kwargs)
