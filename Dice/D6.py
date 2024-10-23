from Dice.Die import Die

from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.core import BitMask32
from panda3d.core import Vec3



class D6(Die):
    def __init__(self, path):
        self.file_path = path
        self.face_dict = {
                1:Vec3(0.0,-0.0,1.0),
                3:Vec3(-1.0,-0.0,0.0),
                4:Vec3(0.0,1.0,0.0),
                5:Vec3(1.0,-0.0,0.0),
                2:Vec3(0.0,-1.0,0.0),
                6:Vec3(0.0,0.0,-1.0),
        }

    def die_setup(self, render, loader):
        (shape, visNP) = self.setup_model(loader)
        self._node = BulletRigidBodyNode("Die")
        self._node.addShape(shape)
        self._node.setMass(1.0)
        self._np = render.attachNewNode(self._node)
        self._np.setCollideMask(BitMask32.bit(0))
        self._node.setDeactivationEnabled(False)
        self._node.setCollisionResponse(True)
        visNP.reparentTo(self._np)


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
                face = x
        return face
