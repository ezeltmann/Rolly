
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.core import BitMask32

import die

class D20(die):
    def __init__(self, path):
        self.set_file(path)

    def die_setup(self):
        visNP = self.base.loader.loadModel(self.get_file())
        mesh = BulletTriangleMesh()

        for node_path in visNP.find_all_matches("**/+GeomNode"):
            for i in range(node_path.node().get_num_geoms()):
                geom = node_path.node().get_geom(i)
                mesh.add_geom(geom)

        shape = BulletTriangleMeshShape(mesh, True)

        visNP.clearModelNodes()
        self.die_node = BulletRigidBodyNode("Die")
        self.die_node.addShape(shape)
        # self.die.reparentTo(render)
        self.die_node.setMass(1.0)
        self.die_np = self.base.render.attachNewNode(self.die_node)
        self.die_np.setCollideMask(BitMask32.bit(0))
        self.die_node.setDeactivationEnabled(False)
        self.die_node.setCollisionResponse(True)
        visNP.reparentTo(self.die_np)