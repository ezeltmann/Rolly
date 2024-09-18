# Filename: fileloader.py

import random
import sys
import direct.directbase.DirectStart

from direct.showbase.ShowBase import ShowBase

from panda3d.core import WindowProperties
from panda3d.core import load_prc_file
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Material
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import BitMask32

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletHelper


import simplepbr

load_prc_file('myConfig.prc')

class DiceTest(ShowBase):
    """Class Representing The Dice Checker"""
    def __init__(self):
        #ShowBase.__init__(self)
        base.cam.setPos(0, -40, 30)
        base.cam.lookAt(0,0,3)
        base.setFrameRateMeter(True)
        simplepbr.init()

        #World Setup
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.worldNP = render.attachNewNode('World')

        #Plane Setup
        shape = BulletPlaneShape(Vec3(0,0,1), 1)
        self.ground_node = BulletRigidBodyNode('Ground')
        self.ground_node.addShape(shape)
        self.ground_np = render.attachNewNode(self.ground_node)
        self.ground_np.setPos(0,0,-2)
        self.world.attach(self.ground_node)

        #Die Setup
        visNP = loader.loadModel("models/cube/die.gltf")
        
        mesh = BulletTriangleMesh()

        for node_path in visNP.find_all_matches('**/+GeomNode'):
            for i in range(node_path.node().get_num_geoms()):
                geom = node_path.node().get_geom(i)
                mesh.add_geom(geom)

        shape = BulletTriangleMeshShape(mesh, True)

        visNP.clearModelNodes()
        self.die_node = BulletRigidBodyNode('Die')
        self.die_node.addShape(shape)
        #self.die.reparentTo(render)
        self.die_node.setMass(1.0)
        self.die_np = render.attachNewNode(self.die_node)
        self.die_node.setDeactivationEnabled(False)
        self.die_node.set_collision_response(True)
        visNP.reparentTo(self.die_np)
        

        #Input
        self.accept('escape', self.exitGame)
        self.accept('f1', self.startRun)
        self.accept('f2', self.stopRun)

        #Startup 
        self.startRun()

    def checkRigidBody(self, name):
        body_list = self.world.getRigidBodies()
        result = False
        for body in body_list:
            if (body.name == name):
                result = True
                break
        return result

    def stopRun(self):
        self.world.remove(self.die_node)
        taskMgr.remove('updateRun')

    def startRun(self):
        if (self.checkRigidBody('Die')):
            self.world.remove(self.die_node)
        
        self.die_np.setPos(0, 0, 15)
        self.die_node.setMass(1.0)
        rand_x = random.randrange(-10,10)
        rand_y = random.randrange(-10,10)

        rand_ax = random.randrange(-10,10)
        rand_ay = random.randrange(-10,10)
        rand_az = random.randrange(-10,10)
        self.die_node.setLinearVelocity(Vec3(rand_x,rand_y,0))
        self.die_node.setAngularVelocity(Vec3(rand_ax, rand_ay, rand_az))
        self.world.attach(self.die_node)
        if (taskMgr.hasTaskNamed('updateRun')):
            taskMgr.remove('updateRun')
        taskMgr.add(self.updateRun, 'updateRun')

    def updateRun(self, task):
        dt = globalClock.getDt()
        self.world.do_physics(dt)
        return task.cont

    def exitGame(self):
        self.stopRun()
        sys.exit()


app = DiceTest()
run()