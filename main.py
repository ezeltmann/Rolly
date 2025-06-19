# Filename: main.py

"""
TODO:
* Simplify the Dice
* Reorginize window
* Advantage
* Disadvantage
* Help Menu
"""

import random
import sys
import json
from Dice.Modifier import Modifier
from Dice.parser import get_dice_list

from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectEntry
from direct.gui.DirectGui import YesNoDialog

from panda3d.core import load_prc_file
from panda3d.core import Vec3
from panda3d.core import BitMask32
from panda3d.core import CardMaker
from panda3d.core import LPoint3f
from panda3d.core import LVecBase3f

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


        self.text_entry = DirectEntry(text = "", scale=0.1, 
                                      initialText="", numLines=4, focus=1,
                                      pos = (-1.45, 0, 0.45),
                                      width = 5)
        self.button = DirectButton(text="Roll!", command=self.roll_dice,
                pos = (-1.2, 0, 0), scale=0.25,
                text_scale=0.25)
        self.name_entry = DirectEntry(text = "", scale=0.1, 
                                      initialText="", numLines=1,
                                      pos = (-1.45, 0, -0.45),
                                      width = 5)
        self.button = DirectButton(text="Save Roll", command=self.save_roll,
                                   pos=(-1.2,0,-0.6), scale=0.25, text_scale=0.25)
        self.rolls = self.load_saved_rolls()
        self.populate_roll_buttons(self.rolls)

        self.text = None
        self.imageObject = None
        self.entry_value = ""
        self.dice = []
        simplepbr.init()
        self.x = 0
        self.y = 0
        self.z = 0
        

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
        self.base.accept("enter",self.roll_dice) 
        # Startup
        #self.startRun()

    def enter_value(self, textEntered):
        self.entry_value = textEntered

    def save_saved_rolls(self, rolls):
        with open("saved_rolls.json", mode="w", encoding="utf-8") as write_file:
            json.dump(rolls, write_file)

    def load_saved_rolls(self):
        rolls = None
        with open("saved_rolls.json", mode="r", encoding="utf-8") as read_file:
            rolls = json.load(read_file)
        
        return rolls

    def populate_roll_buttons(self, button_dict):
        self.save_saved_rolls(self.rolls)
        self.sav_btns = []
        self.del_btns = []
        trash_can = self.base.loader.loadTexture("icon/trash_can_icon.png")
        pos = 0.7
        pos_trash = 0.715
        for btn_name, roll in button_dict.items():
            button = DirectButton(text=btn_name, command=self.roll_saved_dice, 
                                        extraArgs=[roll], pos=LPoint3f(1.1,0,pos),
                                        scale=LVecBase3f(0.085,0.085,0.085))
            del_btn = DirectButton(image=trash_can, command=self.delete_saved_roll,
                                        pos=LPoint3f(1.425,0,pos_trash), image_scale=LVecBase3f(0.5,0.5,0.5), 
                                        scale=LVecBase3f(0.09,0.09,0.09), extraArgs=[btn_name])
            del_btn.setTransparency(True)
            self.sav_btns.append(button)
            self.del_btns.append(del_btn)
            pos -= 0.2
            pos_trash -= 0.2



    def delete_saved_roll(self, btn_name):
        text = f"Are you sure you want to delete\n the roll named {btn_name}"
        self.del_conf_dialog = YesNoDialog(dialogName="YesNoDialog", text=text,
                             command=self.delete_roll, extraArgs=[btn_name])

    def delete_roll(self, answer, btn_name):
        #roll        
        self.del_conf_dialog.cleanup()
        if (answer == 1):
            del self.rolls[btn_name]
            self.clear_saved_roll_buttons()
            self.populate_roll_buttons(self.rolls)

    def save_roll(self):
        roll = self.text_entry.get()
        name = self.name_entry.get()
        self.rolls[name] = roll
        self.clear_saved_roll_buttons()
        self.populate_roll_buttons(self.rolls)

    def clear_saved_roll_buttons(self):
        for btn in self.sav_btns:
                btn.destroy()
        for btn in self.del_btns:
                btn.destroy()
        self.sav_btns = []
        self.del_btns = []

    def roll_saved_dice(self, roll):
        if (len(self.dice) > 0):
            for die in self.dice:
                if (not isinstance(die,Modifier)):
                    self.world.remove(die.node)
                    die.np.removeNode()
        self.clear_text()
        self.dice = []
        self.dice = get_dice_list(roll, self.base)
        self.startRun()

    def roll_dice(self):
        if (len(self.dice) > 0):
            for die in self.dice:
                if (not isinstance(die,Modifier)):
                    self.world.remove(die.node)
                    die.np.removeNode()
        self.clear_text()
        self.dice = []
        self.dice = get_dice_list(self.text_entry.get(), self.base)
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
            if (not isinstance(die,Modifier)):
                rand_x = random.randrange(-10, 10)
                rand_y = random.randrange(-10, 10)
                rand_z = random.randrange(10,20)
                die.np.setPos(rand_x, rand_y, rand_z)
    
    def randomize_die_movement(self):    
        for die in self.dice:
            if (not isinstance(die,Modifier)):
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
            if (not isinstance(die,Modifier)):
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
            if (not isinstance(die,Modifier)):
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
        cm = CardMaker('Background')
        self.card = self.base.render.attachNewNode(cm.generate())
        tex = self.base.loader.loadTexture('models/blender/background.png')
        self.card.setTexture(tex)
        self.card.setScale(40.0)
        self.card.setPosHpr(Vec3(-20,-20,-2),Vec3(270,270,270))

    def exitGame(self):
        self.stopRun()
        sys.exit()

load_prc_file("myConfig.prc")


app = DiceTest()
app.base.run()



