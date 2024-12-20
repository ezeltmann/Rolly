from Dice.Die import Die

from panda3d.core import Vec3



class Modifier(Die):
    def __init__(self, path = None):
        self.value = 0



    def setup_model(self, loader):
        return None
    
    def die_setup(self, render, loader):
        return None
    def get_face_value(self, world_np):
        return self.value