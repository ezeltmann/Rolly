from Dice.Die import Die

from panda3d.core import Vec3



class D100(Die):
    def __init__(self, path):
        self.file_path = path
        self.face_dict = {
            10:Vec3(0.7281079888343811,-0.236576646566391,-0.6433429718017578),
            20:Vec3(0.4156269133090973,-0.5720614194869995,0.7071067690849304),
            30:Vec3(-0.0,-0.7655780911445618,-0.6433429718017578),
            40:Vec3(0.6724984645843506,0.2185080200433731,0.7071068286895752),
            50:Vec3(-0.7281079888343811,-0.236576646566391,-0.6433429718017578),
            60:Vec3(0.0,0.7071067690849304,0.7071067690849304),
            70:Vec3(-0.4499955177307129,0.6193657517433167,-0.6433429718017578),
            80:Vec3(-0.6724984645843506,0.2185080200433731,0.7071068286895752),
            90:Vec3(0.4499955177307129,0.6193657517433167,-0.6433429718017578),
            0:Vec3(-0.4156269133090973,-0.5720614194869995,0.7071067690849304),
        }


    def setup_model(self, loader):
        return super().setup_model(loader)
    
    def die_setup(self, render, loader):
        return super().die_setup(render, loader)

    def get_face_value(self, world_np):
        return super().get_face_value(world_np)