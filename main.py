# Filename: main.py

"""
TODO:
1. Add d10
2. Add d4
3. Add d100
4. Add d12
5. Rolling Interface
6. Label the sliders for what type of dice
7. Check Dice Numbers to be sure


"""

import random
import sys
from math import floor
from Dice.D6 import D6
from Dice.D8 import D8
from Dice.D20 import D20

from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectSlider
from direct.gui.DirectGui import DirectLabel
from direct.gui.DirectGui import DirectButton

from panda3d.core import load_prc_file
#from panda3d.core import Vec3
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
        self.base.camera.setPos(0, -10, 80)
        self.base.camera.lookAt(0, 0, 3)
        self.base.setFrameRateMeter(True)
        self.sliders = []
        self.labels = []
        self.slider = DirectSlider(range=(0,20), value=10, 
                pageSize=1, command=self.showValue, 
                pos = (-1.4, 0, 0.4), scale=0.25,
                frameColor=(255,255,255,255))
        self.label = DirectLabel(text="10", 
                pos = (-1.7, 0, 0.4), scale=0.25,
                text_scale=0.25)
        self.slider2 = DirectSlider(range=(0,20), value=10, 
                pageSize=1, command=self.showValue2, 
                pos = (-1.4, 0, 0.2), scale=0.25,
                frameColor=(255,255,255,255))
        self.label2 = DirectLabel(text="10", 
                pos = (-1.7, 0, 0.2), scale=0.25,
                text_scale=0.25)
        self.slider3 = DirectSlider(range=(0,20), value=10, 
                pageSize=1, command=self.showValue3, 
                pos = (-1.4, 0, 0), scale=0.25,
                frameColor=(255,255,255,255))
        self.label3 = DirectLabel(text="10", 
                pos = (-1.7, 0, 0), scale=0.25,
                text_scale=0.25)
        self.button = DirectButton(text="Roll!", command=self.roll_dice,
                pos = (-1.5, 0, -0.2), scale=0.25,
                text_scale=0.25)
        self.text = None
        self.dice = []
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


        # Input
        self.base.accept("escape", self.exitGame)
        self.base.accept("f1", self.startRun)
        self.base.accept("f2", self.display_face_up)
        self.base.accept("f3", self.clear_text)

        # Startup
        #self.startRun()

    def roll_dice(self):
        if (len(self.dice) > 0):
            for die in self.dice:
                self.world.remove(die.node)
                die.np.removeNode()
        self.clear_text()
        self.dice = []
        for _i in range(int(floor(self.slider['value']))):
            die = D6("models/dice/d6_num.gltf")
            die.die_setup(self.base.render, self.base.loader)
            self.dice.append(die)
        for _i in range(int(floor(self.slider2['value']))):
            die = D20("models/dice/d20.gltf")
            die.die_setup(self.base.render, self.base.loader)
            self.dice.append(die)
        for _i in range(int(floor(self.slider3['value']))):
            die = D8("models/dice/d8.gltf")
            die.die_setup(self.base.render, self.base.loader)
            self.dice.append(die)
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

    def randomize_die_location(self):
        for die in self.dice:
            rand_x = random.randrange(-10, 10)
            rand_y = random.randrange(-10, 10)
            rand_z = random.randrange(10,20)
            die.np.setPos(rand_x, rand_y, rand_z)
    
    def randomize_die_movement(self):    
        for die in self.dice:
            die.node.setMass(1.0)
            rand_x = random.randrange(-10, 10)
            rand_y = random.randrange(-10, 10)
            rand_ax = random.randrange(-10, 10)
            rand_ay = random.randrange(-10, 10)
            rand_az = random.randrange(-10, 10)
            die.node.setLinearVelocity(Vec3(rand_x, rand_y, 0))
            die.node.setAngularVelocity(Vec3(rand_ax, rand_ay, rand_az))


    def startRun(self):
        self.randomize_die_location()
        self.randomize_die_movement()

        for die in self.dice:
            self.world.attach(die.node)

        if self.base.taskMgr.hasTaskNamed("updateRun"):
            self.base.taskMgr.remove("updateRun")
        self.base.taskMgr.add(self.updateRun, "updateRun")

    def updateRun(self, task):
        dt = globalClock.getDt()
        self.world.do_physics(dt)
        #Check if the die has gone still       
        dice_still = True
        for die in self.dice:
            dice_still = self.still_dice(die.node) and dice_still
        if (dice_still):
            self.base.taskMgr.remove("updateRun")
            self.display_face_up()
        return task.cont

    def display_face_up(self):
        face_value = sum(self.get_face(die) for die in self.dice)
        self.text = OnscreenText(text=f"Total Value: {face_value}", pos=(-0.5,0.02),scale=0.07)

    def still_dice(self, die_node):
        ang = die_node.getAngularVelocity()
        lin = die_node.getLinearVelocity()
        comp_1 = ang.compareTo(Vec3(0,0,0),0.5) #0.05 for d6
        comp_2 = lin.compareTo(Vec3(0,0,0),0.5) #0.05 for d6
        if comp_1 != 0 or comp_2 != 0:
            return False
        die_node.setAngularVelocity(Vec3(0,0,0))
        die_node.setLinearVelocity(Vec3(0,0,0))
        return True

    def clear_text(self):
        if self.text is not None:
            self.text.destroy()
        
    def get_face(self, die):
        return die.get_face_value(self.worldNP)

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

    def showValue(self):
        self.label['text'] = str(int(floor(self.slider['value'])))

    def showValue2(self):
        self.label2['text'] = str(int(floor(self.slider2['value'])))

    def showValue3(self):
        self.label3['text'] = str(int(floor(self.slider3['value'])))



load_prc_file("myConfig.prc")


app = DiceTest()
app.base.run()
