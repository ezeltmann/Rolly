from Dice.Die import Die

from panda3d.core import Vec3



class D4(Die):
    def __init__(self, path):
        self.file_path = path
        self.face_dict = {
            1:Vec3(0.0,0.0,1.0),
            2:Vec3(-0.4714045524597168,0.8164966106414795,-0.3333333134651184),
            3:Vec3(-0.4714045524597168,-0.8164966106414795,-0.3333333432674408),
            4:Vec3(0.942808985710144,0.0,-0.3333333134651184),
        }


    def setup_model(self, loader):
        return super().setup_model(loader)
    
    def die_setup(self, render, loader):
        return super().die_setup(render, loader)

    def get_face_value(self, world_np):
        return super().get_face_value(world_np)
