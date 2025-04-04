from Dice.Die import Die

from panda3d.core import Vec3



class D2(Die):
    def __init__(self, path):
        self.file_path = path
        self.face_dict = {
            1:Vec3(0.0,-0.0,1.0),
            1.1:Vec3(0.0,1.0,0.0),
            1.2:Vec3(0.0,0.0,-1.0),
            2:Vec3(1.0,-0.0,0.0),
            2.1:Vec3(0.0,-1.0,0.0),
            2.2:Vec3(-1.0,-0.0,0.0),
        }


    def setup_model(self, loader):
        return super().setup_model(loader)
    
    def die_setup(self, render, loader):
        return super().die_setup(render, loader)

    def get_face_value(self, world_np):
        return super().get_face_value(world_np)
