from Dice.Die import Die

from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.core import BitMask32




class D6(Die):
    def __init__(self, path):
        self.file_path = path

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