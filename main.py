# Filename: main.py

"""
TODO:
1. Split up methods into smaller calls
    A. __init__
    B.startrun()

2. Start adding multiple dice
3. Start adding a board for rolling
4. Start adding an inverface for calling methods
5. Split classes into multiple files
"""

import random
import sys

from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock

from panda3d.core import load_prc_file
from panda3d.core import Vec3
from panda3d.core import BitMask32

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletDebugNode


import simplepbr


class DiceTest:
    """Class Representing The Dice Checker"""

    def __init__(self):
        self.base = ShowBase()
        self.base.disable_mouse()
        self.base.camera.setPos(0, -50, 40)
        self.base.camera.lookAt(0, 0, 3)
        self.base.setFrameRateMeter(True)
        simplepbr.init()

        self.setup_debug(False)

        # World Setup
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.setDebugNode(self.debug_np.node())
        self.worldNP = self.base.render.attachNewNode("World")

        # Plane Setup
        self.wall_setup()
        

        # Die Setup
        visNP = self.base.loader.loadModel("models/dice/d6.gltf")

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

        # Input
        self.base.accept("escape", self.exitGame)
        self.base.accept("f1", self.startRun)
        self.base.accept("f2", self.stopRun)

        # Startup
        self.startRun()

    def setup_debug(self, debug_level: bool):
        self.debug_node = BulletDebugNode('Debug')
        self.debug_node.showWireframe(debug_level)
        self.debug_node.showConstraints(debug_level)
        self.debug_node.showBoundingBoxes(debug_level)
        self.debug_node.showNormals(debug_level)
        self.debug_np = self.base.render.attachNewNode(self.debug_node)
        self.debug_np.show()

    def checkRigidBody(self, name):
        body_list = self.world.getRigidBodies()
        return any((body.name == name) for body in body_list)

    def stopRun(self):
        self.world.remove(self.die_node)
        self.base.taskMgr.remove("updateRun")

    def startRun(self):
        if self.checkRigidBody("Die"):
            self.world.remove(self.die_node)
        self.die_np.setPos(0, 0, 15)
        self.die_node.setMass(1.0)
        rand_x = random.randrange(-10, 10)
        rand_y = random.randrange(-10, 10)

        rand_ax = random.randrange(-10, 10)
        rand_ay = random.randrange(-10, 10)
        rand_az = random.randrange(-10, 10)
        self.die_node.setLinearVelocity(Vec3(rand_x, rand_y, 0))
        self.die_node.setAngularVelocity(Vec3(rand_ax, rand_ay, rand_az))
        self.world.attach(self.die_node)
        if self.base.taskMgr.hasTaskNamed("updateRun"):
            self.base.taskMgr.remove("updateRun")
        self.base.taskMgr.add(self.updateRun, "updateRun")

    def updateRun(self, task):
        dt = globalClock.getDt()
        self.world.do_physics(dt)
        return task.cont

    def make_wall(self, shape_vector : Vec3, name, x, y, z):
        shape = BulletPlaneShape(shape_vector, 1)
        node = BulletRigidBodyNode(name)
        node.addShape(shape)
        node.setCollisionResponse(True)
        node_path = self.base.render.attachNewNode(node)
        node_path.setCollideMask(BitMask32.allOn())
        node_path.setPos(x, y, z)
        return node

    def wall_setup(self):
        self.world.attach(self.make_wall(Vec3(0,0,1),"Ground",0,0,-2))
        self.world.attach(self.make_wall(Vec3(-25,0,0),"Right Wall", 20, 0, -2))
        self.world.attach(self.make_wall(Vec3(25,0,0),"Left Wall", -20, 0, -2))
        self.world.attach(self.make_wall(Vec3(0,-25,0),"Up Wall", 0, 20, -2))
        self.world.attach(self.make_wall(Vec3(0,25,0),"Down Wall", 0, -20, -2))

    def exitGame(self):
        self.stopRun()
        sys.exit()


load_prc_file("myConfig.prc")
app = DiceTest()
app.base.run()
