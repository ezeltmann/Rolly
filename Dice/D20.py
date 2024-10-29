from Dice.Die import Die


from panda3d.core import Vec3



class D20(Die):
    def __init__(self, path):
        self.file_path = path
        self.face_dict = {
            1:Vec3(-0.0,-0.35682210326194763,-0.9341723322868347),
            2:Vec3(0.0,0.35682210326194763,-0.9341723322868347),
            3:Vec3(0.0,-0.35682210326194763,0.9341723322868347),
            4:Vec3(0.0,0.35682210326194763,0.9341723322868347),
            5:Vec3(-0.9341723322868347,-0.0,-0.35682210326194763),
            6:Vec3(-0.9341723322868347,0.0,0.35682210326194763),
            7:Vec3(-0.35682210326194763,0.9341723322868347,0.0),
            8:Vec3(0.35682210326194763,0.9341723322868347,0.0),
            9:Vec3(0.9341723322868347,0.0,-0.35682210326194763),
            10:Vec3(-0.5773502588272095,-0.5773502588272095,-0.5773502588272095),
            11:Vec3(-0.5773502588272095,-0.5773502588272095,0.5773502588272095),
            12:Vec3(0.9341723322868347,0.0,0.35682210326194763),
            13:Vec3(-0.5773502588272095,0.5773502588272095,-0.5773502588272095),
            14:Vec3(0.5773502588272095,-0.5773502588272095,0.5773502588272095),
            15:Vec3(-0.35682210326194763,-0.9341723322868347,-0.0),
            16:Vec3(-0.5773502588272095,0.5773502588272095,0.5773502588272095),
            17:Vec3(0.5773502588272095,0.5773502588272095,-0.5773502588272095),
            18:Vec3(0.35682210326194763,-0.9341723322868347,0.0),
            19:Vec3(0.5773502588272095,-0.5773502588272095,-0.5773502588272095),
            20:Vec3(0.5773502588272095,0.5773502588272095,0.5773502588272095),
        }

    def die_setup(self, render, loader):
        super().die_setup(render, loader)
        self._node.friction = 10.0
        self._np.setScale(1.5)
        self._node.setMass(1.0)

    def setup_model(self, loader):
        return super().setup_model(loader)
    
    def get_face_value(self, world_np):
        return super().get_face_value(world_np)