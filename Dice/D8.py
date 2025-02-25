from Dice.Die import Die

from panda3d.core import Vec3



class D8(Die):
    def __init__(self, path):
        self.file_path = path
        self.face_dict = {
            1:Vec3(0.5773502588272095,-0.5773502588272095,-0.5773502588272095),  # + - -
            2:Vec3(-0.5773502588272095,-0.5773502588272095,-0.5773502588272095), # - - -
            3:Vec3(-0.5773502588272095,0.5773502588272095,-0.5773502588272095),  # - + - 
            4:Vec3(-0.5773502588272095,-0.5773502588272095,0.5773502588272095),  # - - +
            5:Vec3(0.5773502588272095,0.5773502588272095,-0.5773502588272095),   # + + -
            6:Vec3(-0.5773502588272095,0.5773502588272095,0.5773502588272095),   # - + +
            7:Vec3(0.5773502588272095,-0.5773502588272095,0.5773502588272095),   # + - +
            8:Vec3(0.5773502588272095,0.5773502588272095,0.5773502588272095),   # + + +
        }


    def setup_model(self, loader):
        return super().setup_model(loader)
    
    def die_setup(self, render, loader):
        return super().die_setup(render, loader)

    def get_face_value(self, world_np):
        return super().get_face_value(world_np)
