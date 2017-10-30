
from .components.inventory import Inventory
from .components.inputcontroller import InputController
from .components.move import Move
from .components.fighter import Fighter
from .components.healing import Healing
from .components.alignment import Alignment
from .components.target import Target
from . import faction
from . import entity
import queue

class Player:
    
    def __init__(self, name, world):
        
        self.name = name
        self.world = world
        
        self.roomname = None
        
        self.entity = None
        
        self.inventory = Inventory(10)
        self.health = None
        self.maxHealth = 100
        
        self.messages = queue.Queue()
        
        self.resetView = True
        
        self.changes = set()
        
        self.canChangeRoom=False
        
    
    def leaveRoom(self):
        if self.entity:
            self.health = self.getHealth()[0]
            self.entity.remove()
            self.entity = None
        self.world.deactivateRoom(self.roomname)
    
    def joinRoom(self, roomname, place=None):
        self.canChangeRoom = False
        room = self.world.getRoom(roomname)
        if not room:
            raise Exception("Invalid Room")
        
        if self.entity:
            self.leaveRoom()
            
            
        self.world.activateRoom(roomname)
        
        pos = place or room.getEntrance()
        self.entity = entity.Entity(
            sprite = "player",
            height = 2,
            name = '~' + self.name,
            components={
                "inventory": self.inventory,
                "move": Move(slowness=2),
                "controller": InputController(),
                "fighter": Fighter(self.maxHealth, 5, slowness=4, health=self.health or self.maxHealth),
                "alignment": Alignment(faction.GOOD),
                "heal": Healing(interval=50),
                "target": Target()
                })
        self.entity.construct(room.getRoomData())
        self.entity.addListener(self.onPlayerAction)
        room.addObj(pos, self.entity)
        self.roomname = roomname
        self.place = pos
        self.resetView = True
        self.canChangeRoom = True
    
    def getRoom(self):
        return self.roomname
    
    def onPlayerAction(self, o, action, *data):
        if action == "changeroom" and self.canChangeRoom:
            room, pos = data
            self.joinRoom(room, pos)
        
        if action == "attack":
            obj, damage = data
            self.log("{} attacks {} for {} damage".format(self.name, obj.getName(), damage))
        
        if action == "kill":
            obj = data[0]
            self.log("{} kills {}".format(self.name, obj.getName()))
        
        if action == "damage":
            obj, damage = data
            self.log("{} got {} damage from {}".format(self.name, damage, obj.getName()))
            self.changes.add("health")
        
        if action == "heal":
            obj, health = data
            if obj:
                self.log("{} got {} health from {}".format(self.name, health, obj.getName()))
            self.changes.add("health")
        
        if action == "die":
            obj = data[0]
            self.log("{} got killed by {}".format(self.name, obj.getName()))
            self.entity = None
            self.roomname = None
            self.place = None
            self.health = self.maxHealth
        
        if action == "inventorychange":
            self.changes.add("inventory")
        
        if action == "objectenter" or action == "objectleave":
            self.changes.add("ground")
        
        if action == "move":
            self.changes.add("ground")
            self.changes.add("pos")
        
    
    def control(self, action):
        if not self.entity or not (isinstance(action, list) or isinstance(action, tuple)) or len(action) < 1:
            return
        controller = self.entity.getComponent("controller")
        controller.addAction(action)
    
    def getHealth(self):
        if self.entity:
            return self.entity.getComponent("fighter").getHealth()
        else:
            return None
    
    def getInventory(self):
        if self.entity:
            return self.inventory.getItems()
        else:
            return []
    
    def getInteractions(self):
        if not self.entity:
            return []
        controller = self.entity.getComponent("controller")
        return controller.getInteractions()
    
    def getGroundObjs(self):
        if not self.entity:
            return []
        objs = list(self.entity.getGround().getObjs())
        if self.entity in objs:
            objs.remove(self.entity)
        return objs
    
    def getPos(self):
        if not self.entity:
            return None
        return self.entity.getGround().getPos()
    
    def shouldResetView(self):
        return self.resetView
    
    def viewResetDone(self):
        self.resetView = False
    
    def log(self, msg):
        self.messages.put(msg)
        print(msg)
    
    def readMessages(self):
        m = []
        while not self.messages.empty():
            m.append(self.messages.get())
        return m
    
    def getChanges(self):
        return self.changes
    
    def resetChanges(self):
        self.changes = set()
    
    def isActive(self):
        return bool(self.roomname and self.entity)
