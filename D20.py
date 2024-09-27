
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.core import BitMask32

import Die

class D20(Die):
    def __init__(self, path):
        self.set_file(path)

    def die_setup(self, render, loader):
        (shape, visNP) = self.setup_model(loader)
        die_node = BulletRigidBodyNode("Die")
        die_node.addShape(shape)
        die_node.setMass(1.0)
        die_np = render.attachNewNode(die_node)
        die_np.setCollideMask(BitMask32.bit(0))
        die_node.setDeactivationEnabled(False)
        die_node.setCollisionResponse(True)
        visNP.reparentTo(die_np)
        return (die_node, die_np)


    def setup_model(self, loader):
        visNP = loader.loadModel(self.get_file())
        mesh = BulletTriangleMesh()

        for node_path in visNP.find_all_matches("**/+GeomNode"):
            for i in range(node_path.node().get_num_geoms()):
                geom = node_path.node().get_geom(i)
                mesh.add_geom(geom)

        shape = BulletTriangleMeshShape(mesh, True)
        visNP.clearModelNodes()

        return (shape, visNP)