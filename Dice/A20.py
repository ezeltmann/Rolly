from Dice.Die import Die
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.core import BitMask32
from math import floor

from panda3d.core import Vec3



class A20(Die):
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
        visNP = loader.loadModel(self.file_path)
        mesh = BulletTriangleMesh()

        for node_path in visNP.find_all_matches("**/+GeomNode"):
            for i in range(node_path.node().get_num_geoms()):
                geom = node_path.node().get_geom(i)
                mesh.add_geom(geom)

        shape = BulletTriangleMeshShape(mesh, True)
        visNP.clearModelNodes()

        return (shape, visNP) 
    
    def get_face_value(self, world_np):
        faces = self.face_dict
        high = 0
        face = 0
        for x, y in faces.items():
            face_vector = world_np.get_relative_vector(self.np, y)
            value = Vec3(0,0,1).dot(face_vector)
            if (value > high):
                high = value
                face = floor(x)
        return face
        