
from .component import Component
from .. import gameobjects


class Equipment(Component):
    
    
    def __init__(self, slots=None):
        if slots is None:
            slots = {}
        self.slots = {key: None for key in slots}
        self.owner = None
        for slot, item in slots.items():
            self.equip(slot, item)
    
    def attach(self, obj):
        self.owner = obj
    
    def getBonus(self, skill):
        return sum(item.getComponent("item").getStat(skill) for item in self.slots.values() if item)
    
    def equip(self, slot, item):
        if slot in self.slots:
            oldItem = self.slots[slot]
            if oldItem:
                self.owner.trigger("take", oldItem)
            self.slots[slot] = item
            if self.owner:
                self.owner.trigger("equipmentchange")
        else:
            # todo: better exception
            raise Exception("No such slot")
    
    def unEquip(self, slot):
        if slot in self.slots:
            self.slots[slot] = None
            if self.owner:
                self.owner.trigger("equipmentchange")
    
    def getSlots(self):
        return self.slots.copy()
    
    def canEquip(self, item):
        return item.getSlot() in self.slots
    
    
    def toJSON(self):
        return {
            slotName: item.serialize() if item else None
            for slotName, item in self.slots.items()
        }
    
    @classmethod
    def fromJSON(cls, slots):
        return cls({
            slotname: gameobjects.createEntity(item) if item else None
            for slotname, item in slots.items()
        })
    
    
