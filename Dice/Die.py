from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.core import BitMask32
from panda3d.core import Vec3
from math import floor


class Die():
    def __init__ (self, path = None, node = None, np = None, face_dict = None):
        self._path = path
        self._node = node
        self._np = np
        self._face_dict = face_dict

    @property
    def file_path(self):
        return self._path
    
    @file_path.setter
    def file_path(self, new_path):
        self._path = new_path
    
    @property
    def node(self):
        return self._node
    
    @node.setter
    def node(self, new_node):
        self._node = new_node

    @property
    def np(self):
        return self._np
    
    @np.setter
    def np(self, new_np):
        self._np = new_np

    @property
    def face_dict(self):
        return self._face_dict
    
    @face_dict.setter
    def face_dict(self, new_face_dict):
        self._face_dict = new_face_dict

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