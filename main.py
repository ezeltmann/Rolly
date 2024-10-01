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
from Dice.D6 import D6
from Dice.D20 import D20

from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.gui.OnscreenText import OnscreenText

from panda3d.core import load_prc_file
from panda3d.core import Vec3
from panda3d.core import BitMask32

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
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
        self.text = None
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
        self.die_nodes = []
        self.die_nps = []
        for _i in range(20):
            die = D6("models/dice/d6.gltf")
            (die_node, die_np) = die.die_setup(self.base.render, self.base.loader)
            self.die_nodes.append(die_node)
            self.die_nps.append(die_np)

        # Input
        self.base.accept("escape", self.exitGame)
        self.base.accept("f1", self.startRun)
        self.base.accept("f2", self.display_face_up)
        self.base.accept("f3", self.clear_text)

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
        for node in self.die_nodes:
            self.world.remove(node)
        self.base.taskMgr.remove("updateRun")

    def randomize_die(self):
        for die_np in self.die_nps:
            rand_x = random.randrange(-10, 10)
            rand_y = random.randrange(-10, 10)
            rand_z = random.randrange(10,20)
            die_np.setPos(rand_x, rand_y, rand_z)
        
        for die_node in self.die_nodes:
            die_node.setMass(1.0)
            rand_x = random.randrange(-10, 10)
            rand_y = random.randrange(-10, 10)
            rand_ax = random.randrange(-10, 10)
            rand_ay = random.randrange(-10, 10)
            rand_az = random.randrange(-10, 10)
            die_node.setLinearVelocity(Vec3(rand_x, rand_y, 0))
            die_node.setAngularVelocity(Vec3(rand_ax, rand_ay, rand_az))


    def startRun(self):
        for die_node in self.die_nodes:
            #if self.checkRigidBody(die_node.Name):
            self.clear_text()
            self.world.remove(die_node)

        self.randomize_die()

        for die_node in self.die_nodes:
            self.world.attach(die_node)

        if self.base.taskMgr.hasTaskNamed("updateRun"):
            self.base.taskMgr.remove("updateRun")
        self.base.taskMgr.add(self.updateRun, "updateRun")

    def updateRun(self, task):
        dt = globalClock.getDt()
        self.world.do_physics(dt)
        #Check if the die has gone still       
        dice_still = True
        for die_node in self.die_nodes:
            dice_still = self.still_dice(die_node) and dice_still
        if (dice_still):
            self.base.taskMgr.remove("updateRun")
            self.display_face_up()
        return task.cont

    def display_face_up(self):
        face_value = sum(self.up_face(die_np) for die_np in self.die_nps)
        self.text = OnscreenText(text=f"Total Value: {face_value}", pos=(-0.5,0.02),scale=0.07)

    def still_dice(self, die_node):
        ang = die_node.getAngularVelocity()
        lin = die_node.getLinearVelocity()
        comp_1 = ang.compareTo(Vec3(0,0,0),0.05)
        comp_2 = lin.compareTo(Vec3(0,0,0),0.05)
        if comp_1 != 0 or comp_2 != 0:
            return False
        die_node.setAngularVelocity(Vec3(0,0,0))
        die_node.setLinearVelocity(Vec3(0,0,0))
        return True

    def clear_text(self):
        if self.text is not None:
            self.text.destroy()
        

    def up_face(self, die_np):        
        faces = {1:(Vec3(0,0,1),Vec3(0,0,1)), 
                 6:(Vec3(0,0,-1),Vec3(0,0,1)),
                 2:(Vec3(0,0,-1),Vec3(1,0,0)),
                 5:(Vec3(0,0,1),Vec3(1,0,0)),
                 3:(Vec3(0,0,-1),Vec3(0,1,0)),
                 4:(Vec3(0,0,1),Vec3(0,1,0)),
                 }       
        high = 0
        face = 0
        for x, y in faces.items():
            face_vector = self.worldNP.get_relative_vector(die_np, y[1])
            value = y[0].dot(face_vector)
            if (value > high):
                high = value
                face = x
        return face


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
