from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, AmbientLight, PointLight, CollisionTraverser, CollisionHandlerPusher
from panda3d.core import CollisionCapsule, CollisionNode, CollisionTube, NodePath, Fog, WindowProperties, BitMask32
from panda3d.bullet import BulletWorld, BulletPlaneShape, BulletDebugNode, BulletBoxShape, BulletRigidBodyNode
from panda3d.bullet import BulletGhostNode
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.filter.CommonFilters import CommonFilters
import numpy as np
import random as rm
from math import sin
from direct.actor.Actor import Actor

confVars = """
win-size 1280 760
window-title Estranged
cursor-hidden 1
threading-model /Draw
show-scene-graph-analyzer-meter 0
show-frame-rate-meter 1
client-sleep 0.003
textures-auto-power-2 #t
"""
loadPrcFileData("", confVars)

keyMap = {
    "forward": False,
    "backward": False,
    "left": False,
    "right": False,
    "sprint": False,
    "reachL": False,
    "reachR": False,
    "bend": False,
    "test": False
}

# # Models stored as numbers
# modLib = {
#     1: "my-models/empty",
#     2: "my-models/map-pieces/End2",  # it's whatever :<
#     3: "my-models/end4",
#     5: "my-models/end1",
#     6: "my-models/line1",
#     7: "my-models/end3",
#     10: "my-models/elbow2",
#     14: "my-models/elbow3",
#     15: "my-models/elbow1",
#     21: "my-models/elbow4",
#     30: "my-models/tee1",
#     35: "my-models/line2",
#     42: "my-models/tee3",
#     70: "my-models/tee2",
#     105: "my-models/tee4",
#     210: "my-models/cross"
# }

modLib = {
    1: "my-models/map-pieces/Empty",
    2: "my-models/map-pieces/End2",
    3: "my-models/map-pieces/End4",
    5: "my-models/map-pieces/End1",
    6: "my-models/map-pieces/Line1",
    7: "my-models/map-pieces/End3",
    10: "my-models/map-pieces/Elbow2",
    14: "my-models/map-pieces/Elbow3",
    15: "my-models/map-pieces/Elbow1",
    21: "my-models/map-pieces/Elbow4",
    30: "my-models/map-pieces/Tee1",
    35: "my-models/map-pieces/Line2",
    42: "my-models/map-pieces/Tee3",
    70: "my-models/map-pieces/Tee2",
    105: "my-models/map-pieces/Tee4",
    210: "my-models/map-pieces/Cross"
}

textLib = {
    0: [""],  # For when no text is present
    1: ["[WASD]: Move    [QE]: Reach    [SHIFT]: Sprint    [SPACE]: Kneel    [CLICK]: Grab"],
    2: ["\"Hi, I'm self.char, and I don't know what I'm saying\"", "\"some filler\"", "\"this looks cool\""]
}


# callback function to update the keyMap
def updateKeyMap(key, state):
    keyMap[key] = state


class MyGame(ShowBase):
    def __init__(self):
        super().__init__()

        # Disables default camera control
        self.disableMouse()

        # Initialize chunk nodes
        self.elem2 = NodePath('elem')
        self.elem5 = NodePath('elem')
        self.elem6 = NodePath('elem')
        self.elem7 = NodePath('elem')
        self.elem8 = NodePath('elem')
        self.elem9 = NodePath('elem')
        self.elem10 = NodePath('elem')
        self.elem11 = NodePath('elem')
        self.elem12 = NodePath('elem')
        self.elem13 = NodePath('elem')
        self.elem14 = NodePath('elem')
        self.elem15 = NodePath('elem')
        self.elem16 = NodePath('elem')
        self.elem17 = NodePath('elem')
        self.elem18 = NodePath('elem')
        self.elem19 = NodePath('elem')
        self.elem22 = NodePath('elem')

        # Initialize variables
        def InitializeVars():
            self.angleX = 80
            self.cursorX = 0
            self.cursorY = 0
            self.sensitivity = 42000
            self.initialOffset = 0
            self.animFrame = 0
            self.zMod = 5
            self.count1 = 0
            self.count2 = 0
            self.mapX = 0
            self.mapY = 0
            self.lightX = 0
            self.lightY = -2
            self.lr = 0
            self.ll = 0
            self.lu = 0
            self.ld = 0
            self.lq = 0
            self.rq = 0
            self.uq = 0
            self.dq = 0
            self.batch0 = [0, -2]
            self.CD = 80
            self.slower = 1
            self.hasLeft = []
            self.hasRight = []
            self.vig = 0
            self.txtNum = 1
            self.transBool = 0
            self.dur = 0
            self.placeHolder = 0
            self.ghostNumL = 0
            self.ghostNumR = 0
            self.ghostNumU = 0
            self.ghostNumD = 0
            self.gBoxNum7U = 0
            self.gBoxNum7D = 0
            self.gBoxNum17U = 0
            self.gBoxNum17D = 0
            self.gBoxNum13L = 0
            self.gBoxNum13R = 0
            self.gBoxNum11L = 0
            self.gBoxNum11R = 0
            self.gBoxNum2U = 0
            self.gBoxNum2D = 0
            self.gBoxNum22U = 0
            self.gBoxNum22D = 0
            self.gBoxNum14L = 0
            self.gBoxNum14R = 0
            self.gBoxNum10L = 0
            self.gBoxNum10R = 0
            self.sBXSnum13L = 0
            self.sBXSnum13R = 0
            self.sBXSnum11L = 0
            self.sBXSnum11R = 0
            self.sBXSnum17U = 0
            self.sBXSnum17D = 0
            self.sBXSnum7U = 0
            self.sBXSnum7D = 0
            self.sBXSnum14L = 0
            self.sBXSnum14R = 0
            self.sBXSnum10L = 0
            self.sBXSnum10R = 0
            self.sBXSnum22U = 0
            self.sBXSnum22D = 0
            self.sBXSnum2U = 0
            self.sBXSnum2D = 0
            self.lBXnum14L = 0
            self.lBXnum14R = 0
            self.lBXnum10L = 0
            self.lBXnum10R = 0
            self.lBXnum22U = 0
            self.lBXnum22D = 0
            self.lBXnum2U = 0
            self.lBXnum2D = 0
            self.cULnum = 0
            self.cURnum = 0
            self.cDLnum = 0
            self.cDRnum = 0
            self.b13numL = 0
            self.b13numR = 0
            self.b11numL = 0
            self.b11numR = 0
            self.b7numU = 0
            self.b7numD = 0
            self.b17numU = 0
            self.b17numD = 0
            self.b14numL = 0
            self.b14numR = 0
            self.b10numL = 0
            self.b10numR = 0
            self.b2numU = 0
            self.b2numD = 0
            self.b22numU = 0
            self.b22numD = 0
            self.e13num = 0
            self.e11num = 0
            self.e17num = 0
            self.e7num = 0
            self.e14num = 0
            self.e10num = 0
            self.e22num = 0
            self.e2num = 0
            self.textX = -1.58
            self.X = self.textX
            self.textY = -0.912
            self.yellow = 0.865
            self.blue = 0.82
            self.boxX = 0.0000001
            self.text = ""
            self.whichBatch = False
            self.mapYet = False
            self.bigscreen = False
            self.everyOther = True
            self.bool1 = False
            self.bool2 = True
            self.spkrOn = False
            self.map = np.zeros((4000, 4000))
            self.items = np.zeros((4000, 4000), dtype=object)
            self.wp = WindowProperties()
            self.wp.setFixedSize(True)
            self.win.requestProperties(self.wp)
            self.cTrav = CollisionTraverser()
            self.pusher = CollisionHandlerPusher()
            self.filters = CommonFilters(self.win, self.cam)

        InitializeVars()

        # Seed map
        self.map[0, 0] = 35

        # Load player character
        self.char = Actor("my-models/char1", {"walk": "my-models/char1-walk", "stand": "my-models/char1-stand"})
        self.char.setH(180)
        self.char.setPos(self.CD * 1.5, self.CD * 1.5, 0)
        self.char.loop("stand")
        self.char.reparentTo(render)

        # Get bone control
        self.neckBone = self.char.controlJoint(None, "modelRoot", "spine.005")
        self.angleY = -8
        self.neckBone.setP(self.angleY * -1 - 40)
        self.backBone = self.char.controlJoint(None, "modelRoot", "spine.001")
        self.armLeft = self.char.controlJoint(None, "modelRoot", "shoulder.L")
        self.armLeft.setR(253.54)
        self.armRight = self.char.controlJoint(None, "modelRoot", "shoulder.R")
        self.armRight.setR(106.45)
        self.handLeft = self.char.exposeJoint(None, "modelRoot", "hand.L")
        self.handRight = self.char.exposeJoint(None, "modelRoot", "hand.R")

        # Jack is an empty node makes moving the camera easier when bending over
        self.jack = NodePath("for-bend")
        self.jack.setY(-0.1)
        self.jack.reparentTo(self.char)

        self.ceiling = loader.loadModel("my-models/map-pieces/plane")  # this is a sneaky way of hiding
        self.ceiling.setZ(19)  # the edges of the ceiling
        self.ceiling.reparentTo(render)
        self.ceiling = loader.loadModel("my-models/map-pieces/plane")
        self.ceiling.setPos(self.CD * 3, 0, 19)
        self.ceiling.reparentTo(render)
        self.ceiling = loader.loadModel("my-models/map-pieces/plane")
        self.ceiling.setPos(0, self.CD * 3, 19)
        self.ceiling.reparentTo(render)
        self.ceiling = loader.loadModel("my-models/map-pieces/plane")
        self.ceiling.setPos(self.CD * 3, self.CD * 3, 19)
        self.ceiling.reparentTo(render)

        # self.cam.setPosHpr(10, 7, 5, 135, -20, 0)  # back/side view
        # self.cam.setPosHpr(12, -14, 1.8, 40, 2, 0)  # front/side view
        # self.cam.setPosHpr(0, -22, -1, 0, 3, 0)  # front view
        self.camLens.setFov(50)  # set FOV
        self.cam.reparentTo(render)

        # self.obj = loader.loadModel("models/camera")
        self.cam.setPosHpr(0, -1.5, 1.8, 180, self.angleY, 0)  # ORIGINAL
        # self.obj.setPosHpr(0, -1.5, 1.8, 180, self.angleY, 0)
        # self.obj.hide()
        self.cam.reparentTo(self.jack)
        # self.obj.reparentTo(self.jack)

        # Sounds
        self.testSound = loader.loadSfx("Sleigh-Bells.ogg")

        # Gui
        self.blackStripe = OnscreenImage(
            image="blackStripe.gif",
            pos=(0, 0, -2.58),
            scale=1.78
        )
        self.vignette = OnscreenImage(  # Opacity on this to increase when sprinting
            image="Vignette.png",
            scale=1.78,
            color=(0, 0, 0, 0)
        )
        self.vignette.setTransparency(True)

        # Fonts
        self.mono = loader.loadFont("Courier Prime.ttf")
        self.jacksyn = loader.loadFont("DroidSans.ttf")

        self.textUI = OnscreenText(
            text=self.text,
            pos=(self.textX, self.textY),
            mayChange=True,
            align=0,
            font=self.mono,
            scale=0.052,
            fg=(0.869, 0.858, 0.823, 1)  # Color only shows for a frame, but kept here for reference
        )
        self.speaker = OnscreenText(
            pos=(self.textX, self.textY),
            mayChange=True,
            align=0,
            font=self.mono,
            scale=0.052
        )

        def setupLights():

            self.LC = (1, 1, 0.8, 1)  # Light color
            BC = (0.05, 0.05, 0.1, 1)  # Background color
            LA = (0.5, 0.1, 0)  # Light attenuation
            self.LH = 15  # Light height

            self.setBackgroundColor(0.05, 0, 0)  # Set the color things fade off to in the distance
            ambLight = AmbientLight("ambLight")
            ambLight.setColor(BC)
            render.setLight(render.attachNewNode(ambLight))
            render.setShaderAuto()

            myFog = Fog("Fog")
            myFog.setColor(BC)
            myFog.setExpDensity(0.003)  # TODO: try exponential fog
            render.setFog(myFog)

            self.filters.setBlurSharpen(1.6)  # makes it feel like an eerie creepypasta

            self.plE2L = PointLight("overhead")
            self.plE2L.setAttenuation(LA)
            self.E2L = render.attachNewNode(self.plE2L)
            self.E2L.setPos(self.CD * -0.75, self.CD * 1.5, self.LH)
            render.setLight(self.E2L)
            self.plE2R = PointLight("overhead")
            self.plE2R.setAttenuation(LA)
            self.E2R = render.attachNewNode(self.plE2R)
            self.E2R.setPos(self.CD * -0.25, self.CD * 1.5, self.LH)
            render.setLight(self.E2R)
            self.plE2U = PointLight("overhead")
            self.plE2U.setAttenuation(LA)
            self.E2U = render.attachNewNode(self.plE2U)
            self.E2U.setPos(self.CD * -0.5, self.CD * 1.75, self.LH)
            render.setLight(self.E2U)
            self.plE2D = PointLight("overhead")
            self.plE2D.setAttenuation(LA)
            self.E2D = render.attachNewNode(self.plE2D)
            self.E2D.setPos(self.CD * -0.5, self.CD * 1.25, self.LH)
            render.setLight(self.E2D)

            self.plE5L = PointLight("overhead")
            self.plE5L.setAttenuation(LA)
            self.E5L = render.attachNewNode(self.plE5L)
            self.E5L.setPos(self.CD * -1.75, self.CD * 1.5, self.LH)
            render.setLight(self.E5L)
            self.plE5R = PointLight("overhead")
            self.plE5R.setAttenuation(LA)
            self.E5R = render.attachNewNode(self.plE5R)
            self.E5R.setPos(self.CD * -1.25, self.CD * 1.5, self.LH)
            render.setLight(self.E5R)
            self.plE5U = PointLight("overhead")
            self.plE5U.setAttenuation(LA)
            self.E5U = render.attachNewNode(self.plE5U)
            self.E5U.setPos(self.CD * -1.5, self.CD * 1.75, self.LH)
            render.setLight(self.E5U)
            self.plE5D = PointLight("overhead")
            self.plE5D.setAttenuation(LA)
            self.E5D = render.attachNewNode(self.plE5D)
            self.E5D.setPos(self.CD * -1.5, self.CD * 1.25, self.LH)
            render.setLight(self.E5D)

            self.plE6L = PointLight("overhead")
            self.plE6L.setAttenuation(LA)
            self.E6L = render.attachNewNode(self.plE6L)
            self.E6L.setPos(self.CD * -2.75, self.CD * 1.5, self.LH)
            render.setLight(self.E6L)
            self.plE6R = PointLight("overhead")
            self.plE6R.setAttenuation(LA)
            self.E6R = render.attachNewNode(self.plE6R)
            self.E6R.setPos(self.CD * -2.25, self.CD * 1.5, self.LH)
            render.setLight(self.E6R)
            self.plE6U = PointLight("overhead")
            self.plE6U.setAttenuation(LA)
            self.E6U = render.attachNewNode(self.plE6U)
            self.E6U.setPos(self.CD * -2.5, self.CD * 1.75, self.LH)
            render.setLight(self.E6U)
            self.plE6D = PointLight("overhead")
            self.plE6D.setAttenuation(LA)
            self.E6D = render.attachNewNode(self.plE6D)
            self.E6D.setPos(self.CD * -2.5, self.CD * 1.25, self.LH)
            render.setLight(self.E6D)

            self.plE7L = PointLight("overhead")
            self.plE7L.setAttenuation(LA)
            self.E7L = render.attachNewNode(self.plE7L)
            self.E7L.setPos(self.CD * 0.25, self.CD * 1.5, self.LH)
            render.setLight(self.E7L)
            self.plE7R = PointLight("overhead")
            self.plE7R.setAttenuation(LA)
            self.E7R = render.attachNewNode(self.plE7R)
            self.E7R.setPos(self.CD * 0.75, self.CD * 1.5, self.LH)
            render.setLight(self.E7R)
            self.plE7U = PointLight("overhead")
            self.plE7U.setAttenuation(LA)
            self.E7U = render.attachNewNode(self.plE7U)
            self.E7U.setPos(self.CD * 0.5, self.CD * 1.75, self.LH)
            render.setLight(self.E7U)
            self.plE7D = PointLight("overhead")
            self.plE7D.setAttenuation(LA)
            self.E7D = render.attachNewNode(self.plE7D)
            self.E7D.setPos(self.CD * 0.5, self.CD * 1.25, self.LH)
            render.setLight(self.E7D)

            self.plE8L = PointLight("overhead")
            self.plE8L.setAttenuation(LA)
            self.E8L = render.attachNewNode(self.plE8L)
            self.E8L.setPos(self.CD * 1.25, self.CD * 5.5, self.LH)
            render.setLight(self.E8L)
            self.plE8R = PointLight("overhead")
            self.plE8R.setAttenuation(LA)
            self.E8R = render.attachNewNode(self.plE8R)
            self.E8R.setPos(self.CD * 1.75, self.CD * 5.5, self.LH)
            render.setLight(self.E8R)
            self.plE8U = PointLight("overhead")
            self.plE8U.setAttenuation(LA)
            self.E8U = render.attachNewNode(self.plE8U)
            self.E8U.setPos(self.CD * 1.5, self.CD * 5.75, self.LH)
            render.setLight(self.E8U)
            self.plE8D = PointLight("overhead")
            self.plE8D.setAttenuation(LA)
            self.E8D = render.attachNewNode(self.plE8D)
            self.E8D.setPos(self.CD * 1.5, self.CD * 5.25, self.LH)
            render.setLight(self.E8D)

            self.plE9L = PointLight("overhead")
            self.plE9L.setAttenuation(LA)
            self.E9L = render.attachNewNode(self.plE9L)
            self.E9L.setPos(self.CD * 1.25, self.CD * 4.5, self.LH)
            render.setLight(self.E9L)
            self.plE9R = PointLight("overhead")
            self.plE9R.setAttenuation(LA)
            self.E9R = render.attachNewNode(self.plE9R)
            self.E9R.setPos(self.CD * 1.75, self.CD * 4.5, self.LH)
            render.setLight(self.E9R)
            self.plE9U = PointLight("overhead")
            self.plE9U.setAttenuation(LA)
            self.E9U = render.attachNewNode(self.plE9U)
            self.E9U.setPos(self.CD * 1.5, self.CD * 4.75, self.LH)
            render.setLight(self.E9U)
            self.plE9D = PointLight("overhead")
            self.plE9D.setAttenuation(LA)
            self.E9D = render.attachNewNode(self.plE9D)
            self.E9D.setPos(self.CD * 1.5, self.CD * 4.25, self.LH)
            render.setLight(self.E9D)

            self.plE10L = PointLight("overhead")
            self.plE10L.setAttenuation(LA)
            self.E10L = render.attachNewNode(self.plE10L)
            self.E10L.setPos(self.CD * 1.25, self.CD * -0.5, self.LH)
            render.setLight(self.E10L)
            self.plE10R = PointLight("overhead")
            self.plE10R.setAttenuation(LA)
            self.E10R = render.attachNewNode(self.plE10R)
            self.E10R.setPos(self.CD * 1.75, self.CD * -0.5, self.LH)
            render.setLight(self.E10R)
            self.plE10U = PointLight("overhead")
            self.plE10U.setAttenuation(LA)
            self.E10U = render.attachNewNode(self.plE10U)
            self.E10U.setPos(self.CD * 1.5, self.CD * -0.25, self.LH)
            render.setLight(self.E10U)
            self.plE10D = PointLight("overhead")
            self.plE10D.setAttenuation(LA)
            self.E10D = render.attachNewNode(self.plE10D)
            self.E10D.setPos(self.CD * 1.5, self.CD * -0.75, self.LH)
            render.setLight(self.E10D)

            self.plE11L = PointLight("overhead")
            self.plE11L.setAttenuation(LA)
            self.E11L = render.attachNewNode(self.plE11L)
            self.E11L.setPos(self.CD * 1.25, self.CD * 0.5, self.LH)
            render.setLight(self.E11L)
            self.plE11R = PointLight("overhead")
            self.plE11R.setAttenuation(LA)
            self.E11R = render.attachNewNode(self.plE11R)
            self.E11R.setPos(self.CD * 1.75, self.CD * 0.5, self.LH)
            render.setLight(self.E11R)
            self.plE11U = PointLight("overhead")
            self.plE11U.setAttenuation(LA)
            self.E11U = render.attachNewNode(self.plE11U)
            self.E11U.setPos(self.CD * 1.5, self.CD * 0.75, self.LH)
            render.setLight(self.E11U)
            self.plE11D = PointLight("overhead")
            self.plE11D.setAttenuation(LA)
            self.E11D = render.attachNewNode(self.plE11D)
            self.E11D.setPos(self.CD * 1.5, self.CD * 0.25, self.LH)
            render.setLight(self.E11D)

            self.plE12L = PointLight("overhead")
            self.plE12L.setAttenuation(LA)
            self.E12L = render.attachNewNode(self.plE12L)
            self.E12L.setPos(self.CD * 1.25, self.CD * 1.5, self.LH)
            render.setLight(self.E12L)
            self.plE12R = PointLight("overhead")
            self.plE12R.setAttenuation(LA)
            self.E12R = render.attachNewNode(self.plE12R)
            self.E12R.setPos(self.CD * 1.75, self.CD * 1.5, self.LH)
            render.setLight(self.E12R)
            self.plE12U = PointLight("overhead")
            self.plE12U.setAttenuation(LA)
            self.E12U = render.attachNewNode(self.plE12U)
            self.E12U.setPos(self.CD * 1.5, self.CD * 1.75, self.LH)
            render.setLight(self.E12U)
            self.plE12D = PointLight("overhead")
            self.plE12D.setAttenuation(LA)
            self.E12D = render.attachNewNode(self.plE12D)
            self.E12D.setPos(self.CD * 1.5, self.CD * 1.25, self.LH)
            render.setLight(self.E12D)

            self.plE13L = PointLight("overhead")
            self.plE13L.setAttenuation(LA)
            self.E13L = render.attachNewNode(self.plE13L)
            self.E13L.setPos(self.CD * 1.25, self.CD * 2.5, self.LH)
            render.setLight(self.E13L)
            self.plE13R = PointLight("overhead")
            self.plE13R.setAttenuation(LA)
            self.E13R = render.attachNewNode(self.plE13R)
            self.E13R.setPos(self.CD * 1.75, self.CD * 2.5, self.LH)
            render.setLight(self.E13R)
            self.plE13U = PointLight("overhead")
            self.plE13U.setAttenuation(LA)
            self.E13U = render.attachNewNode(self.plE13U)
            self.E13U.setPos(self.CD * 1.5, self.CD * 2.75, self.LH)
            render.setLight(self.E13U)
            self.plE13D = PointLight("overhead")
            self.plE13D.setAttenuation(LA)
            self.E13D = render.attachNewNode(self.plE13D)
            self.E13D.setPos(self.CD * 1.5, self.CD * 2.25, self.LH)
            render.setLight(self.E13D)

            self.plE14L = PointLight("overhead")
            self.plE14L.setAttenuation(LA)
            self.E14L = render.attachNewNode(self.plE14L)
            self.E14L.setPos(self.CD * 1.25, self.CD * 3.5, self.LH)
            render.setLight(self.E14L)
            self.plE14R = PointLight("overhead")
            self.plE14R.setAttenuation(LA)
            self.E14R = render.attachNewNode(self.plE14R)
            self.E14R.setPos(self.CD * 1.75, self.CD * 3.5, self.LH)
            render.setLight(self.E14R)
            self.plE14U = PointLight("overhead")
            self.plE14U.setAttenuation(LA)
            self.E14U = render.attachNewNode(self.plE14U)
            self.E14U.setPos(self.CD * 1.5, self.CD * 3.75, self.LH)
            render.setLight(self.E14U)
            self.plE14D = PointLight("overhead")
            self.plE14D.setAttenuation(LA)
            self.E14D = render.attachNewNode(self.plE14D)
            self.E14D.setPos(self.CD * 1.5, self.CD * 3.25, self.LH)
            render.setLight(self.E14D)

            self.plE15L = PointLight("overhead")
            self.plE15L.setAttenuation(LA)
            self.E15L = render.attachNewNode(self.plE15L)
            self.E15L.setPos(self.CD * 1.25, self.CD * -1.5, self.LH)
            render.setLight(self.E15L)
            self.plE15R = PointLight("overhead")
            self.plE15R.setAttenuation(LA)
            self.E15R = render.attachNewNode(self.plE15R)
            self.E15R.setPos(self.CD * 1.75, self.CD * -1.5, self.LH)
            render.setLight(self.E15R)
            self.plE15U = PointLight("overhead")
            self.plE15U.setAttenuation(LA)
            self.E15U = render.attachNewNode(self.plE15U)
            self.E15U.setPos(self.CD * 1.5, self.CD * -1.25, self.LH)
            render.setLight(self.E15U)
            self.plE15D = PointLight("overhead")
            self.plE15D.setAttenuation(LA)
            self.E15D = render.attachNewNode(self.plE15D)
            self.E15D.setPos(self.CD * 1.5, self.CD * -1.75, self.LH)
            render.setLight(self.E15D)

            self.plE16L = PointLight("overhead")
            self.plE16L.setAttenuation(LA)
            self.E16L = render.attachNewNode(self.plE16L)
            self.E16L.setPos(self.CD * 1.25, self.CD * -2.5, self.LH)
            render.setLight(self.E16L)
            self.plE16R = PointLight("overhead")
            self.plE16R.setAttenuation(LA)
            self.E16R = render.attachNewNode(self.plE16R)
            self.E16R.setPos(self.CD * 1.75, self.CD * -2.5, self.LH)
            render.setLight(self.E16R)
            self.plE16U = PointLight("overhead")
            self.plE16U.setAttenuation(LA)
            self.E16U = render.attachNewNode(self.plE16U)
            self.E16U.setPos(self.CD * 1.5, self.CD * -2.25, self.LH)
            render.setLight(self.E16U)
            self.plE16D = PointLight("overhead")
            self.plE16D.setAttenuation(LA)
            self.E16D = render.attachNewNode(self.plE16D)
            self.E16D.setPos(self.CD * 1.5, self.CD * -2.75, self.LH)
            render.setLight(self.E16D)

            self.plE17L = PointLight("overhead")
            self.plE17L.setAttenuation(LA)
            self.E17L = render.attachNewNode(self.plE17L)
            self.E17L.setPos(self.CD * 2.25, self.CD * 1.5, self.LH)
            render.setLight(self.E17L)
            self.plE17R = PointLight("overhead")
            self.plE17R.setAttenuation(LA)
            self.E17R = render.attachNewNode(self.plE17R)
            self.E17R.setPos(self.CD * 2.75, self.CD * 1.5, self.LH)
            render.setLight(self.E17R)
            self.plE17U = PointLight("overhead")
            self.plE17U.setAttenuation(LA)
            self.E17U = render.attachNewNode(self.plE17U)
            self.E17U.setPos(self.CD * 2.5, self.CD * 1.75, self.LH)
            render.setLight(self.E17U)
            self.plE17D = PointLight("overhead")
            self.plE17D.setAttenuation(LA)
            self.E17D = render.attachNewNode(self.plE17D)
            self.E17D.setPos(self.CD * 2.5, self.CD * 1.25, self.LH)
            render.setLight(self.E17D)

            self.plE18L = PointLight("overhead")
            self.plE18L.setAttenuation(LA)
            self.E18L = render.attachNewNode(self.plE18L)
            self.E18L.setPos(self.CD * 5.25, self.CD * 1.5, self.LH)
            render.setLight(self.E18L)
            self.plE18R = PointLight("overhead")
            self.plE18R.setAttenuation(LA)
            self.E18R = render.attachNewNode(self.plE18R)
            self.E18R.setPos(self.CD * 5.75, self.CD * 1.5, self.LH)
            render.setLight(self.E18R)
            self.plE18U = PointLight("overhead")
            self.plE18U.setAttenuation(LA)
            self.E18U = render.attachNewNode(self.plE18U)
            self.E18U.setPos(self.CD * 5.5, self.CD * 1.75, self.LH)
            render.setLight(self.E18U)
            self.plE18D = PointLight("overhead")
            self.plE18D.setAttenuation(LA)
            self.E18D = render.attachNewNode(self.plE18D)
            self.E18D.setPos(self.CD * 5.5, self.CD * 1.25, self.LH)
            render.setLight(self.E18D)

            self.plE19L = PointLight("overhead")
            self.plE19L.setAttenuation(LA)
            self.E19L = render.attachNewNode(self.plE19L)
            self.E19L.setPos(self.CD * 4.25, self.CD * 1.5, self.LH)
            render.setLight(self.E19L)
            self.plE19R = PointLight("overhead")
            self.plE19R.setAttenuation(LA)
            self.E19R = render.attachNewNode(self.plE19R)
            self.E19R.setPos(self.CD * 4.75, self.CD * 1.5, self.LH)
            render.setLight(self.E19R)
            self.plE19U = PointLight("overhead")
            self.plE19U.setAttenuation(LA)
            self.E19U = render.attachNewNode(self.plE19U)
            self.E19U.setPos(self.CD * 4.5, self.CD * 1.75, self.LH)
            render.setLight(self.E19U)
            self.plE19D = PointLight("overhead")
            self.plE19D.setAttenuation(LA)
            self.E19D = render.attachNewNode(self.plE19D)
            self.E19D.setPos(self.CD * 4.5, self.CD * 1.25, self.LH)
            render.setLight(self.E19D)

            self.plE22L = PointLight("overhead")
            self.plE22L.setAttenuation(LA)
            self.E22L = render.attachNewNode(self.plE22L)
            self.E22L.setPos(self.CD * 3.25, self.CD * 1.5, self.LH)
            render.setLight(self.E22L)
            self.plE22R = PointLight("overhead")
            self.plE22R.setAttenuation(LA)
            self.E22R = render.attachNewNode(self.plE22R)
            self.E22R.setPos(self.CD * 3.75, self.CD * 1.5, self.LH)
            render.setLight(self.E22R)
            self.plE22U = PointLight("overhead")
            self.plE22U.setAttenuation(LA)
            self.E22U = render.attachNewNode(self.plE22U)
            self.E22U.setPos(self.CD * 3.5, self.CD * 1.75, self.LH)
            render.setLight(self.E22U)
            self.plE22D = PointLight("overhead")
            self.plE22D.setAttenuation(LA)
            self.E22D = render.attachNewNode(self.plE22D)
            self.E22D.setPos(self.CD * 3.5, self.CD * 1.25, self.LH)
            render.setLight(self.E22D)

        setupLights()

        def setupCollision():
            # BULLET PHYSICS ENGINE
            self.world = BulletWorld()
            self.world.setGravity((0, 0, -21))

            # debugNode = BulletDebugNode('Debug')
            # debugNode.showWireframe(True)
            # debugNode.showConstraints(True)
            # debugNode.showBoundingBoxes(False)
            # debugNode.showNormals(True)
            # debugNP = render.attachNewNode(debugNode)
            # debugNP.show()
            # self.world.setDebugNode(debugNP.node())

            shape = BulletPlaneShape((0, 0, 1), 0)
            self.node = BulletRigidBodyNode('Ground')
            self.node.addShape(shape)
            self.node.setFriction(0.7)
            self.ground = render.attachNewNode(self.node)
            self.ground.setCollideMask(BitMask32.bit(0))
            self.world.attachRigidBody(self.node)

            shape = BulletPlaneShape((0, 0, -1), -19)
            self.node = BulletRigidBodyNode('Ceiling')
            self.node.addShape(shape)
            self.ground = render.attachNewNode(self.node)
            self.ground.setCollideMask(BitMask32.bit(0))
            self.world.attachRigidBody(self.node)

            # Setup Mah Ghosties
            # corners
            shape = BulletBoxShape((self.CD * 5 / 6, self.CD * 5 / 6, 9.5))

            self.cUL = BulletGhostNode('Corner')
            self.cUL.addShape(shape)
            self.CornUL = render.attachNewNode(self.cUL)
            self.CornUL.setPos(self.CD / 6, self.CD * 17 / 6, 9.5)
            self.CornUL.setCollideMask(BitMask32.bit(0))
            self.world.attachGhost(self.cUL)

            self.cUR = BulletGhostNode('Corner')
            self.cUR.addShape(shape)
            self.CornUR = render.attachNewNode(self.cUR)
            self.CornUR.setPos(self.CD * 17 / 6, self.CD / 6, 9.5)
            self.CornUR.setCollideMask(BitMask32.bit(0))
            self.world.attachGhost(self.cUR)

            self.cDL = BulletGhostNode('Corner')
            self.cDL.addShape(shape)
            self.CornDL = render.attachNewNode(self.cDL)
            self.CornDL.setPos(self.CD / 6, self.CD / 6, 9.5)
            self.CornDL.setCollideMask(BitMask32.bit(0))
            self.world.attachGhost(self.cDL)

            self.cDR = BulletGhostNode('Corner')
            self.cDR.addShape(shape)
            self.CornDR = render.attachNewNode(self.cDR)
            self.CornDR.setPos(self.CD * 17 / 6, self.CD * 17 / 6, 9.5)
            self.CornDR.setCollideMask(BitMask32.bit(0))
            self.world.attachGhost(self.cDR)


            # 'bouncers'
            shape = BulletBoxShape((self.CD / 6.1, 0, 9.5))

            self.b14L = BulletGhostNode('Bouncer')
            self.b14L.addShape(shape)
            self.bounc14L = render.attachNewNode(self.b14L)
            self.bounc14L.setPos(self.CD * 7 / 6, self.CD * 11 / 3, 9.5)
            self.bounc14L.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.b14L)

            self.b14R = BulletGhostNode('Bouncer')
            self.b14R.addShape(shape)
            self.bounc14R = render.attachNewNode(self.b14R)
            self.bounc14R.setPos(self.CD * 11 / 6, self.CD * 11 / 3, 9.5)
            self.bounc14R.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.b14R)

            self.b10R = BulletGhostNode('Bouncer')
            self.b10R.addShape(shape)
            self.bounc10R = render.attachNewNode(self.b10R)
            self.bounc10R.setPos(self.CD * 11 / 6, self.CD * -2 / 3, 9.5)
            self.bounc10R.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.b10R)

            self.b10L = BulletGhostNode('Bouncer')
            self.b10L.addShape(shape)
            self.bounc10L = render.attachNewNode(self.b10L)
            self.bounc10L.setPos(self.CD * 7 / 6, self.CD * -2 / 3, 9.5)
            self.bounc10L.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.b10L)

            self.b13L = BulletGhostNode('Bouncer')
            self.b13L.addShape(shape)
            self.bounc13L = render.attachNewNode(self.b13L)
            self.bounc13L.setPos(self.CD * 7 / 6, self.CD * 8 / 3, 9.5)
            self.bounc13L.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.b13L)

            self.b13R = BulletGhostNode('Bouncer')
            self.b13R.addShape(shape)
            self.bounc13R = render.attachNewNode(self.b13R)
            self.bounc13R.setPos(self.CD * 11 / 6, self.CD * 8 / 3, 9.5)
            self.bounc13R.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.b13R)

            self.b11R = BulletGhostNode('Bouncer')
            self.b11R.addShape(shape)
            self.bounc11R = render.attachNewNode(self.b11R)
            self.bounc11R.setPos(self.CD * 11 / 6, self.CD / 3, 9.5)
            self.bounc11R.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.b11R)

            self.b11L = BulletGhostNode('Bouncer')
            self.b11L.addShape(shape)
            self.bounc11L = render.attachNewNode(self.b11L)
            self.bounc11L.setPos(self.CD * 7 / 6, self.CD / 3, 9.5)
            self.bounc11L.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.b11L)

            shape = BulletBoxShape((0, self.CD / 6.1, 9.5))

            self.b17D = BulletGhostNode('Bouncer')
            self.b17D.addShape(shape)
            self.bounc17D = render.attachNewNode(self.b17D)
            self.bounc17D.setPos(self.CD * 8 / 3, self.CD * 7 / 6, 9.5)
            self.bounc17D.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.b17D)

            self.b17U = BulletGhostNode('Bouncer')
            self.b17U.addShape(shape)
            self.bounc17U = render.attachNewNode(self.b17U)
            self.bounc17U.setPos(self.CD * 8 / 3, self.CD * 11 / 6, 9.5)
            self.bounc17U.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.b17U)

            self.b22D = BulletGhostNode('Bouncer')
            self.b22D.addShape(shape)
            self.bounc22D = render.attachNewNode(self.b22D)
            self.bounc22D.setPos(self.CD * 11 / 3, self.CD * 7 / 6, 9.5)
            self.bounc22D.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.b22D)

            self.b22U = BulletGhostNode('Bouncer')
            self.b22U.addShape(shape)
            self.bounc22U = render.attachNewNode(self.b22U)
            self.bounc22U.setPos(self.CD * 11 / 3, self.CD * 11 / 6, 9.5)
            self.bounc22U.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.b22U)

            self.b7U = BulletGhostNode('Bouncer')
            self.b7U.addShape(shape)
            self.bounc7U = render.attachNewNode(self.b7U)
            self.bounc7U.setPos(self.CD / 3, self.CD * 11 / 6, 9.5)
            self.bounc7U.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.b7U)

            self.b7D = BulletGhostNode('Bouncer')
            self.b7D.addShape(shape)
            self.bounc7D = render.attachNewNode(self.b7D)
            self.bounc7D.setPos(self.CD / 3, self.CD * 7 / 6, 9.5)
            self.bounc7D.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.b7D)

            self.b2U = BulletGhostNode('Bouncer')
            self.b2U.addShape(shape)
            self.bounc2U = render.attachNewNode(self.b2U)
            self.bounc2U.setPos(self.CD * -2 / 3, self.CD * 11 / 6, 9.5)
            self.bounc2U.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.b2U)

            self.b2D = BulletGhostNode('Bouncer')
            self.b2D.addShape(shape)
            self.bounc2D = render.attachNewNode(self.b2D)
            self.bounc2D.setPos(self.CD * -2 / 3, self.CD * 7 / 6, 9.5)
            self.bounc2D.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.b2D)

            #ends
            shape = BulletBoxShape((self.CD / 2, self.CD / 2, 9.5))

            self.ghostL = BulletGhostNode('Wall')
            self.ghostL.addShape(shape)
            self.ghostWallL = render.attachNewNode(self.ghostL)
            self.ghostWallL.setPos(self.CD * -3 / 2, self.CD * 3 / 2, 9.5)
            self.ghostWallL.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.ghostL)

            self.ghostR = BulletGhostNode('Wall')
            self.ghostR.addShape(shape)
            self.ghostWallR = render.attachNewNode(self.ghostR)
            self.ghostWallR.setPos(self.CD * 9 / 2, self.CD * 3 / 2, 9.5)
            self.ghostWallR.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.ghostR)

            self.ghostD = BulletGhostNode('Wall')
            self.ghostD.addShape(shape)
            self.ghostWallD = render.attachNewNode(self.ghostD)
            self.ghostWallD.setPos(self.CD * 1.5, self.CD * -3 / 2, 9.5)
            self.ghostWallD.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.ghostD)

            self.ghostU = BulletGhostNode('Wall')
            self.ghostU.addShape(shape)
            self.ghostWallU = render.attachNewNode(self.ghostU)
            self.ghostWallU.setPos(self.CD * 1.5, self.CD * 9 / 2, 9.5)
            self.ghostWallU.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.ghostU)

            # static ghost boxes
            shape = BulletBoxShape((0, self.CD / 6, 9.5))

            self.sBxs13L = BulletGhostNode('Boxes')
            self.sBxs13L.addShape(shape)
            self.sBoxes13L = render.attachNewNode(self.sBxs13L)
            self.sBoxes13L.setPos(self.CD * 4 / 3, self.CD * 13 / 6, 9.5)
            self.sBoxes13L.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.sBxs13L)

            self.sBxs14L = BulletGhostNode('Boxes')
            self.sBxs14L.addShape(shape)
            self.sBoxes14L = render.attachNewNode(self.sBxs14L)
            self.sBoxes14L.setPos(self.CD * 4 / 3, self.CD * 23 / 6, 9.5)
            self.sBoxes14L.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.sBxs14L)

            self.sBxs11L = BulletGhostNode('Boxes')
            self.sBxs11L.addShape(shape)
            self.sBoxes11L = render.attachNewNode(self.sBxs11L)
            self.sBoxes11L.setPos((self.CD * 4 / 3, self.CD * 5 / 6, 9.5))
            self.sBoxes11L.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.sBxs11L)

            self.sBxs13R = BulletGhostNode('Boxes')
            self.sBxs13R.addShape(shape)
            self.sBoxes13R = render.attachNewNode(self.sBxs13R)
            self.sBoxes13R.setPos((self.CD * 5 / 3, self.CD * 13 / 6, 9.5))
            self.sBoxes13R.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.sBxs13R)

            self.sBxs14R = BulletGhostNode('Boxes')
            self.sBxs14R.addShape(shape)
            self.sBoxes14R = render.attachNewNode(self.sBxs14R)
            self.sBoxes14R.setPos((self.CD * 5 / 3, self.CD * 23 / 6, 9.5))
            self.sBoxes14R.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.sBxs14R)

            self.sBxs11R = BulletGhostNode('Boxes')
            self.sBxs11R.addShape(shape)
            self.sBoxes11R = render.attachNewNode(self.sBxs11R)
            self.sBoxes11R.setPos((self.CD * 5 / 3, self.CD * 5 / 6, 9.5))
            self.sBoxes11R.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.sBxs11R)

            self.sBxs10R = BulletGhostNode('Boxes')
            self.sBxs10R.addShape(shape)
            self.sBoxes10R = render.attachNewNode(self.sBxs10R)
            self.sBoxes10R.setPos((self.CD * 5 / 3, -self.CD * 5 / 6, 9.5))
            self.sBoxes10R.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.sBxs10R)

            self.sBxs10L = BulletGhostNode('Boxes')
            self.sBxs10L.addShape(shape)
            self.sBoxes10L = render.attachNewNode(self.sBxs10L)
            self.sBoxes10L.setPos((self.CD * 4 / 3, -self.CD * 5 / 6, 9.5))
            self.sBoxes10L.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.sBxs10L)

            shape = BulletBoxShape((self.CD / 6, 0, 9.5))

            self.sBxs7U = BulletGhostNode('Boxes')
            self.sBxs7U.addShape(shape)
            self.sBoxes7U = render.attachNewNode(self.sBxs7U)
            self.sBoxes7U.setPos((self.CD * 5 / 6, self.CD * 5 / 3, 9.5))
            self.sBoxes7U.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.sBxs7U)

            self.sBxs17U = BulletGhostNode('Boxes')
            self.sBxs17U.addShape(shape)
            self.sBoxes17U = render.attachNewNode(self.sBxs17U)
            self.sBoxes17U.setPos((self.CD * 13 / 6, self.CD * 5 / 3, 9.5))
            self.sBoxes17U.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.sBxs17U)

            self.sBxs7D = BulletGhostNode('Boxes')
            self.sBxs7D.addShape(shape)
            self.sBoxes7D = render.attachNewNode(self.sBxs7D)
            self.sBoxes7D.setPos((self.CD * 5 / 6, self.CD * 4 / 3, 9.5))
            self.sBoxes7D.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.sBxs7D)

            self.sBxs2D = BulletGhostNode('Boxes')
            self.sBxs2D.addShape(shape)
            self.sBoxes2D = render.attachNewNode(self.sBxs2D)
            self.sBoxes2D.setPos((-self.CD * 5 / 6, self.CD * 4 / 3, 9.5))
            self.sBoxes2D.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.sBxs2D)

            self.sBxs2U = BulletGhostNode('Boxes')
            self.sBxs2U.addShape(shape)
            self.sBoxes2U = render.attachNewNode(self.sBxs2U)
            self.sBoxes2U.setPos((-self.CD * 5 / 6, self.CD * 5 / 3, 9.5))
            self.sBoxes2U.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.sBxs2U)

            self.sBxs17D = BulletGhostNode('Boxes')
            self.sBxs17D.addShape(shape)
            self.sBoxes17D = render.attachNewNode(self.sBxs17D)
            self.sBoxes17D.setPos((self.CD * 13 / 6, self.CD * 4 / 3, 9.5))
            self.sBoxes17D.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.sBxs17D)

            self.sBxs22U = BulletGhostNode('Boxes')
            self.sBxs22U.addShape(shape)
            self.sBoxes22U = render.attachNewNode(self.sBxs22U)
            self.sBoxes22U.setPos((self.CD * 23 / 6, self.CD * 5 / 3, 9.5))
            self.sBoxes22U.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.sBxs22U)

            self.sBxs22D = BulletGhostNode('Boxes')
            self.sBxs22D.addShape(shape)
            self.sBoxes22D = render.attachNewNode(self.sBxs22D)
            self.sBoxes22D.setPos((self.CD * 23 / 6, self.CD * 4 / 3, 9.5))
            self.sBoxes22D.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.sBxs22D)

            shape = BulletBoxShape((0, self.CD / 3, 9.5))

            self.lBx14L = BulletGhostNode('Boxes')
            self.lBx14L.addShape(shape)
            self.longBx14L = render.attachNewNode(self.lBx14L)
            self.longBx14L.setPos((self.CD * 4 / 3, self.CD * 3, 9.5))
            self.longBx14L.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.lBx14L)

            self.lBx14R = BulletGhostNode('Boxes')
            self.lBx14R.addShape(shape)
            self.longBx14R = render.attachNewNode(self.lBx14R)
            self.longBx14R.setPos((self.CD * 5 / 3, self.CD * 3, 9.5))
            self.longBx14R.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.lBx14R)

            self.lBx10L = BulletGhostNode('Boxes')
            self.lBx10L.addShape(shape)
            self.longBx10L = render.attachNewNode(self.lBx10L)
            self.longBx10L.setPos((self.CD * 4 / 3, 0, 9.5))
            self.longBx10L.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.lBx10L)

            self.lBx10R = BulletGhostNode('Boxes')
            self.lBx10R.addShape(shape)
            self.longBx10R = render.attachNewNode(self.lBx10R)
            self.longBx10R.setPos((self.CD * 5 / 3, 0, 9.5))
            self.longBx10R.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.lBx10R)

            shape = BulletBoxShape((self.CD / 3, 0, 9.5))

            self.lBx2U = BulletGhostNode('Boxes')
            self.lBx2U.addShape(shape)
            self.longBx2U = render.attachNewNode(self.lBx2U)
            self.longBx2U.setPos((0, self.CD * 5 / 3, 9.5))
            self.longBx2U.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.lBx2U)

            self.lBx2D = BulletGhostNode('Boxes')
            self.lBx2D.addShape(shape)
            self.longBx2D = render.attachNewNode(self.lBx2D)
            self.longBx2D.setPos((0, self.CD * 4 / 3, 9.5))
            self.longBx2D.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.lBx2D)

            self.lBx22U = BulletGhostNode('Boxes')
            self.lBx22U.addShape(shape)
            self.longBx22U = render.attachNewNode(self.lBx22U)
            self.longBx22U.setPos((self.CD * 3, self.CD * 5 / 3, 9.5))
            self.longBx22U.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.lBx22U)

            self.lBx22D = BulletGhostNode('Boxes')
            self.lBx22D.addShape(shape)
            self.longBx22D = render.attachNewNode(self.lBx22D)
            self.longBx22D.setPos((self.CD * 3, self.CD * 4 / 3, 9.5))
            self.longBx22D.setCollideMask(BitMask32.bit(2))
            self.world.attachGhost(self.lBx22D)

            # Ghost Box time!!! :S XD
            shape = BulletBoxShape((0, self.CD / 6, 9.5))

            self.g13L = BulletGhostNode('Wallb')
            self.g13L.addShape(shape)
            self.gBox13L = render.attachNewNode(self.g13L)
            self.gBox13L.setPos(self.CD * 4 / 3, self.CD * 2.5, 9.5)
            self.world.attachGhost(self.g13L)

            self.g13R = BulletGhostNode('Wallb')
            self.g13R.addShape(shape)
            self.gBox13R = render.attachNewNode(self.g13R)
            self.gBox13R.setPos(self.CD * 5 / 3, self.CD * 2.5, 9.5)
            self.world.attachGhost(self.g13R)

            self.g14L = BulletGhostNode('Wallb')
            self.g14L.addShape(shape)
            self.gBox14L = render.attachNewNode(self.g14L)
            self.gBox14L.setPos(self.CD * 4 / 3, self.CD * 3.5, 9.5)
            self.world.attachGhost(self.g14L)

            self.g14R = BulletGhostNode('Wallb')
            self.g14R.addShape(shape)
            self.gBox14R = render.attachNewNode(self.g14R)
            self.gBox14R.setPos(self.CD * 5 / 3, self.CD * 3.5, 9.5)
            self.world.attachGhost(self.g14R)

            self.g11L = BulletGhostNode('Wallb')
            self.g11L.addShape(shape)
            self.gBox11L = render.attachNewNode(self.g11L)
            self.gBox11L.setPos(self.CD * 4 / 3, self.CD * 0.5, 9.5)
            self.world.attachGhost(self.g11L)

            self.g11R = BulletGhostNode('Wallb')
            self.g11R.addShape(shape)
            self.gBox11R = render.attachNewNode(self.g11R)
            self.gBox11R.setPos(self.CD * 5 / 3, self.CD * 0.5, 9.5)
            self.world.attachGhost(self.g11R)

            self.g10L = BulletGhostNode('Wallb')
            self.g10L.addShape(shape)
            self.gBox10L = render.attachNewNode(self.g10L)
            self.gBox10L.setPos(self.CD * 4 / 3, -self.CD * 0.5, 9.5)
            self.world.attachGhost(self.g10L)

            self.g10R = BulletGhostNode('Wallb')
            self.g10R.addShape(shape)
            self.gBox10R = render.attachNewNode(self.g10R)
            self.gBox10R.setPos(self.CD * 5 / 3, -self.CD * 0.5, 9.5)
            self.world.attachGhost(self.g10R)

            shape = BulletBoxShape((self.CD / 6, 0, 9.5))

            self.g7U = BulletGhostNode('Wallb')
            self.g7U.addShape(shape)
            self.gBox7U = render.attachNewNode(self.g7U)
            self.gBox7U.setPos(self.CD * 0.5, self.CD * 5 / 3, 9.5)
            self.world.attachGhost(self.g7U)

            self.g7D = BulletGhostNode('Wallb')
            self.g7D.addShape(shape)
            self.gBox7D = render.attachNewNode(self.g7D)
            self.gBox7D.setPos(self.CD * 0.5, self.CD * 4 / 3, 9.5)
            self.world.attachGhost(self.g7D)

            self.g2U = BulletGhostNode('Wallb')
            self.g2U.addShape(shape)
            self.gBox2U = render.attachNewNode(self.g2U)
            self.gBox2U.setPos(-self.CD * 0.5, self.CD * 5 / 3, 9.5)
            self.world.attachGhost(self.g2U)

            self.g2D = BulletGhostNode('Wallb')
            self.g2D.addShape(shape)
            self.gBox2D = render.attachNewNode(self.g2D)
            self.gBox2D.setPos(-self.CD * 0.5, self.CD * 4 / 3, 9.5)
            self.world.attachGhost(self.g2D)

            self.g17U = BulletGhostNode('Wallb')
            self.g17U.addShape(shape)
            self.gBox17U = render.attachNewNode(self.g17U)
            self.gBox17U.setPos(self.CD * 2.5, self.CD * 5 / 3, 9.5)
            self.world.attachGhost(self.g17U)

            self.g17D = BulletGhostNode('Wallb')
            self.g17D.addShape(shape)
            self.gBox17D = render.attachNewNode(self.g17D)
            self.gBox17D.setPos(self.CD * 2.5, self.CD * 4 / 3, 9.5)
            self.world.attachGhost(self.g17D)

            self.g22U = BulletGhostNode('Wallb')
            self.g22U.addShape(shape)
            self.gBox22U = render.attachNewNode(self.g22U)
            self.gBox22U.setPos(self.CD * 3.5, self.CD * 5 / 3, 9.5)
            self.world.attachGhost(self.g22U)

            self.g22D = BulletGhostNode('Wallb')
            self.g22D.addShape(shape)
            self.gBox22D = render.attachNewNode(self.g22D)
            self.gBox22D.setPos(self.CD * 3.5, self.CD * 4 / 3, 9.5)
            self.world.attachGhost(self.g22D)

            # let's make some ends
            self.e13 = BulletGhostNode('EndYo')
            self.e13.addShape(shape)
            self.end13 = render.attachNewNode(self.e13)
            self.end13.setPos(self.CD * 1.5, self.CD * 8 / 3, 9.5)
            self.world.attachGhost(self.e13)

            self.e14 = BulletGhostNode('EndYo')
            self.e14.addShape(shape)
            self.end14 = render.attachNewNode(self.e14)
            self.end14.setPos(self.CD * 1.5, self.CD * 11 / 3, 9.5)
            self.world.attachGhost(self.e14)

            self.e11 = BulletGhostNode('EndYo')
            self.e11.addShape(shape)
            self.end11 = render.attachNewNode(self.e11)
            self.end11.setPos(self.CD * 1.5, self.CD / 3, 9.5)
            self.world.attachGhost(self.e11)

            self.e10 = BulletGhostNode('EndYo')
            self.e10.addShape(shape)
            self.end10 = render.attachNewNode(self.e10)
            self.end10.setPos(self.CD * 1.5, -self.CD * 2 / 3, 9.5)
            self.world.attachGhost(self.e10)

            shape = BulletBoxShape((0, self.CD / 6, 9.5))

            self.e17 = BulletGhostNode('EndYo')
            self.e17.addShape(shape)
            self.end17 = render.attachNewNode(self.e17)
            self.end17.setPos(self.CD * 8 / 3, self.CD * 1.5, 9.5)
            self.world.attachGhost(self.e17)

            self.e22 = BulletGhostNode('EndYo')
            self.e22.addShape(shape)
            self.end22 = render.attachNewNode(self.e22)
            self.end22.setPos(self.CD * 11 / 3, self.CD * 1.5, 9.5)
            self.world.attachGhost(self.e22)

            self.e7 = BulletGhostNode('EndYo')
            self.e7.addShape(shape)
            self.end7 = render.attachNewNode(self.e7)
            self.end7.setPos(self.CD / 3, self.CD * 1.5, 9.5)
            self.world.attachGhost(self.e7)

            self.e2 = BulletGhostNode('EndYo')
            self.e2.addShape(shape)
            self.end2 = render.attachNewNode(self.e2)
            self.end2.setPos(-self.CD * 2 / 3, self.CD * 1.5, 9.5)
            self.world.attachGhost(self.e2)

            # PANDA PHYSICS ENGINE
            self.CH = 7  # Collider height

            colliderNode = CollisionNode("player")
            colliderNode.addSolid(CollisionCapsule(-0.25, -0.16, -0.06, -0.4, -0.8, 0.18, 0.4))
            self.collider = self.handRight.attachNewNode(colliderNode)
            self.collider.setCollideMask(BitMask32.bit(1))
            # self.collider.show()
            self.pusher.addCollider(self.collider, self.char)
            self.cTrav.addCollider(self.collider, self.pusher)
            self.pusher.setHorizontal(True)

            colliderNode = CollisionNode("player")
            colliderNode.addSolid(CollisionCapsule(0.25, -0.16, -0.06, 0.4, -0.8, 0.18, 0.4))
            self.collider = self.handLeft.attachNewNode(colliderNode)
            self.collider.setCollideMask(BitMask32.bit(1))
            # self.collider.show()
            self.pusher.addCollider(self.collider, self.char)
            self.cTrav.addCollider(self.collider, self.pusher)
            self.pusher.setHorizontal(True)

            # Set Collider Walls
            # Vertical
            wallSolid = CollisionTube(self.CD * 4 / 3, self.CD * 0.7, self.CH, self.CD * 4 / 3, self.CD * 4 / 3,
                                      self.CH, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            render.attachNewNode(wallNode)

            wallSolid = CollisionTube(self.CD * 5 / 3, self.CD * 0.7, self.CH, self.CD * 5 / 3, self.CD * 4 / 3,
                                      self.CH, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            render.attachNewNode(wallNode)

            wallSolid = CollisionTube(self.CD * 4 / 3, self.CD * 2.3, self.CH, self.CD * 4 / 3, self.CD * 5 / 3,
                                      self.CH, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            render.attachNewNode(wallNode)

            wallSolid = CollisionTube(self.CD * 5 / 3, self.CD * 2.3, self.CH, self.CD * 5 / 3, self.CD * 5 / 3,
                                      self.CH, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            render.attachNewNode(wallNode)

            # Vertical Unchanging
            wallSolid = CollisionTube(self.CD, self.CD, self.CH, self.CD, self.CD * 4 / 3, self.CH, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            render.attachNewNode(wallNode)

            wallSolid = CollisionTube(self.CD * 2, self.CD, self.CH, self.CD * 2, self.CD * 4 / 3, self.CH, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            render.attachNewNode(wallNode)

            wallSolid = CollisionTube(self.CD, self.CD * 2, self.CH, self.CD, self.CD * 5 / 3, self.CH, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            render.attachNewNode(wallNode)

            wallSolid = CollisionTube(self.CD * 2, self.CD * 2, self.CH, self.CD * 2, self.CD * 5 / 3, self.CH, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            render.attachNewNode(wallNode)

            # Horizontal
            wallSolid = CollisionTube(self.CD * 0.7, self.CD * 4 / 3, self.CH, self.CD * 4 / 3, self.CD * 4 / 3,
                                      self.CH, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            render.attachNewNode(wallNode)

            wallSolid = CollisionTube(self.CD * 5 / 3, self.CD * 4 / 3, self.CH, self.CD * 2.3, self.CD * 4 / 3,
                                      self.CH, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            render.attachNewNode(wallNode)

            wallSolid = CollisionTube(self.CD * 0.7, self.CD * 5 / 3, self.CH, self.CD * 4 / 3, self.CD * 5 / 3,
                                      self.CH, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            render.attachNewNode(wallNode)

            wallSolid = CollisionTube(self.CD * 5 / 3, self.CD * 5 / 3, self.CH, self.CD * 2.3, self.CD * 5 / 3,
                                      self.CH, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            render.attachNewNode(wallNode)

            # Horizontal Unchanging
            wallSolid = CollisionTube(self.CD, self.CD, self.CH, self.CD * 4 / 3, self.CD, self.CH, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            render.attachNewNode(wallNode)

            wallSolid = CollisionTube(self.CD * 5 / 3, self.CD, self.CH, self.CD * 2, self.CD, self.CH, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            render.attachNewNode(wallNode)

            wallSolid = CollisionTube(self.CD, self.CD * 2, self.CH, self.CD * 4 / 3, self.CD * 2, self.CH, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            render.attachNewNode(wallNode)

            wallSolid = CollisionTube(self.CD * 5 / 3, self.CD * 2, self.CH, self.CD * 2, self.CD * 2, self.CH, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            render.attachNewNode(wallNode)

            # Middles
            wallSolid = CollisionTube(self.CD, self.CD * 4 / 3, 0, self.CD, self.CD * 5 / 3, 0, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            self.wallL0 = render.attachNewNode(wallNode)
            wallSolid = CollisionTube(self.CD * 4 / 3, self.CD * 4 / 3, 0, self.CD * 4 / 3, self.CD * 5 / 3, 0, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            self.wallL1 = render.attachNewNode(wallNode)

            wallSolid = CollisionTube(self.CD * 2, self.CD * 4 / 3, 0, self.CD * 2, self.CD * 5 / 3, 0, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            self.wallR0 = render.attachNewNode(wallNode)
            wallSolid = CollisionTube(self.CD * 5 / 3, self.CD * 4 / 3, 0, self.CD * 5 / 3, self.CD * 5 / 3, 0, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            self.wallR1 = render.attachNewNode(wallNode)

            wallSolid = CollisionTube(self.CD * 4 / 3, self.CD * 2, 0, self.CD * 5 / 3, self.CD * 2, 0, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            self.wallU0 = render.attachNewNode(wallNode)
            wallSolid = CollisionTube(self.CD * 4 / 3, self.CD * 5 / 3, 0, self.CD * 5 / 3, self.CD * 5 / 3, 0, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            self.wallU1 = render.attachNewNode(wallNode)

            wallSolid = CollisionTube(self.CD * 4 / 3, self.CD, 0, self.CD * 5 / 3, self.CD, 0, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            self.wallD0 = render.attachNewNode(wallNode)
            wallSolid = CollisionTube(self.CD * 4 / 3, self.CD * 4 / 3, 0, self.CD * 5 / 3, self.CD * 4 / 3, 0, 0.2)
            wallNode = CollisionNode("wall")
            wallNode.addSolid(wallSolid)
            self.wallD1 = render.attachNewNode(wallNode)

        setupCollision()

        # Take Keyboard and Mouse input
        self.accept("w", updateKeyMap, ["forward", True])
        self.accept("w-up", updateKeyMap, ["forward", False])
        self.accept("shift-w", updateKeyMap, ["forward", True])
        self.accept("shift-w-up", updateKeyMap, ["forward", False])
        self.accept("s", updateKeyMap, ["backward", True])
        self.accept("s-up", updateKeyMap, ["backward", False])
        self.accept("shift-s", updateKeyMap, ["backward", True])
        self.accept("shift-s-up", updateKeyMap, ["backward", False])
        self.accept("a", updateKeyMap, ["left", True])
        self.accept("a-up", updateKeyMap, ["left", False])
        self.accept("shift-a", updateKeyMap, ["left", True])
        self.accept("shift-a-up", updateKeyMap, ["left", False])
        self.accept("d", updateKeyMap, ["right", True])
        self.accept("d-up", updateKeyMap, ["right", False])
        self.accept("shift-d", updateKeyMap, ["right", True])
        self.accept("shift-d-up", updateKeyMap, ["right", False])
        self.accept("q", updateKeyMap, ["reachL", True])
        self.accept("q-up", updateKeyMap, ["reachL", False])
        self.accept("shift-q", updateKeyMap, ["reachL", True])
        self.accept("shift-q-up", updateKeyMap, ["reachL", False])
        self.accept("e", updateKeyMap, ["reachR", True])
        self.accept("e-up", updateKeyMap, ["reachR", False])
        self.accept("shift-e", updateKeyMap, ["reachR", True])
        self.accept("shift-e-up", updateKeyMap, ["reachR", False])
        self.accept("shift", updateKeyMap, ["sprint", True])
        self.accept("shift-up", updateKeyMap, ["sprint", False])
        self.accept("space", updateKeyMap, ["bend", True])
        self.accept("space-up", updateKeyMap, ["bend", False])
        self.accept("mouse1", self.grab)
        self.accept("shift-mouse1", self.grab)
        self.accept("f11", self.fullscreen)
        self.accept("0", updateKeyMap, ["test", True])
        self.accept("0-up", updateKeyMap, ["test", False])

        self.taskMgr.add(self.update, "update")

    def grab(self):
        if keyMap["reachR"] and not self.hasRight:  # Right goes first cuz most people are right handed
            for child in self.E12U.getChildren():
                if (self.handRight.getPos(self.E12U) - child.getPos()).length() < 1.3:
                    for j in self.items[self.mapX, self.mapY]:
                        if j[1] == child.getPos():
                            self.hasRight = j
                            self.items[self.mapX, self.mapY].remove(j)
                    child.wrtReparentTo(self.handRight)
                    print("its happening :o")
                    self.move = child.posInterval(0.07, (-0.2, 0.1, 0), child.getPos())
                    self.move.start()
                else:
                    print((self.handRight.getPos(self.E12U) - child.getPos()).length())
            if not self.hasRight:  # checks surrounding squares for items you could be grabbing
                for child in self.E13U.getChildren():
                    if (self.handRight.getPos(self.E13U) - child.getPos()).length() < 1.3:
                        for j in self.items[self.mapX, self.mapY + 1]:
                            if j[1] == child.getPos():
                                self.hasRight = j
                                self.items[self.mapX, self.mapY + 1].remove(j)
                        child.wrtReparentTo(self.handRight)
                        self.move = child.posInterval(0.07, (-0.2, 0.1, 0), child.getPos())
                        self.move.start()
                    else:
                        print((self.handRight.getPos(self.E13U) - child.getPos()).length())
                if not self.hasRight:
                    for child in self.E11U.getChildren():
                        if (self.handRight.getPos(self.E11U) - child.getPos()).length() < 1.3:
                            for j in self.items[self.mapX, self.mapY - 1]:
                                if j[1] == child.getPos():
                                    self.hasRight = j
                                    self.items[self.mapX, self.mapY - 1].remove(j)
                            child.wrtReparentTo(self.handRight)
                            self.move = child.posInterval(0.07, (-0.2, 0.1, 0), child.getPos())
                            self.move.start()
                        else:
                            print((self.handRight.getPos(self.E11U) - child.getPos()).length())
                    if not self.hasRight:
                        for child in self.E7U.getChildren():
                            if (self.handRight.getPos(self.E7U) - child.getPos()).length() < 1.3:
                                for j in self.items[self.mapX - 1, self.mapY]:
                                    if j[1] == child.getPos():
                                        self.hasRight = j
                                        self.items[self.mapX - 1, self.mapY].remove(j)
                                child.wrtReparentTo(self.handRight)
                                self.move = child.posInterval(0.07, (-0.2, 0.1, 0), child.getPos())
                                self.move.start()
                            else:
                                print((self.handRight.getPos(self.E7U) - child.getPos()).length())
                        if not self.hasRight:
                            for child in self.E17U.getChildren():
                                if (self.handRight.getPos(self.E17U) - child.getPos()).length() < 1.3:
                                    for j in self.items[self.mapX + 1, self.mapY]:
                                        if j[1] == child.getPos():
                                            self.hasRight = j
                                            self.items[self.mapX + 1, self.mapY].remove(j)
                                    child.wrtReparentTo(self.handRight)
                                    self.move = child.posInterval(0.07, (-0.2, 0.1, 0), child.getPos())
                                    self.move.start()
                                else:
                                    print((self.handRight.getPos(self.E17U) - child.getPos()).length())
        elif self.hasRight:
            for child in self.handRight.getChildren():
                if child.getPos() != (0, 0, 0):  # so we don't lose our collision capsules ¯\_(ツ)_/¯
                    if len(self.hasRight) > 5:
                        child.node().setKinematic(0)
                    child.wrtReparentTo(self.E12U)
                    self.hasRight[1] = child.getPos()
                    self.hasRight[2] = child.getHpr()
                    if self.items[self.mapX, self.mapY] == 0:
                        self.items[self.mapX, self.mapY] = []
                    self.items[self.mapX, self.mapY].append(self.hasRight)
                    self.hasRight = []
                    print(self.items[self.mapX, self.mapY])
        if len(self.hasRight) > 5:
            for i in self.handRight.getChildren():
                if i.getPos() != (0, 0, 0):
                    i.node().setKinematic(1)  # turn off forces/gravity for held rigid bodies
        if keyMap["reachL"] and not self.hasLeft:
            for child in self.E12U.getChildren():
                if (self.handLeft.getPos(self.E12U) - child.getPos()).length() < 1.3:
                    for i in self.items[self.mapX, self.mapY]:
                        if i[1] == child.getPos():
                            self.hasLeft = i
                            self.items[self.mapX, self.mapY].remove(i)
                    child.wrtReparentTo(self.handLeft)
                    self.move = child.posInterval(0.07, (0.2, 0.1, 0), child.getPos())
                    self.move.start()
                else:
                    print((self.handLeft.getPos(self.E12U) - child.getPos()).length())
            if not self.hasLeft:  # checks surrounding squares for items you could be grabbing
                for child in self.E13U.getChildren():
                    if (self.handLeft.getPos(self.E13U) - child.getPos()).length() < 1.3:
                        for j in self.items[self.mapX, self.mapY + 1]:
                            if j[1] == child.getPos():
                                self.hasLeft = j
                                self.items[self.mapX, self.mapY + 1].remove(j)
                        child.wrtReparentTo(self.handLeft)
                        self.move = child.posInterval(0.07, (0.2, 0.1, 0), child.getPos())
                        self.move.start()
                    else:
                        print((self.handLeft.getPos(self.E13U) - child.getPos()).length())
                if not self.hasLeft:
                    for child in self.E11U.getChildren():
                        if (self.handLeft.getPos(self.E11U) - child.getPos()).length() < 1.3:
                            for j in self.items[self.mapX, self.mapY - 1]:
                                if j[1] == child.getPos():
                                    self.hasLeft = j
                                    self.items[self.mapX, self.mapY - 1].remove(j)
                            child.wrtReparentTo(self.handLeft)
                            self.move = child.posInterval(0.07, (0.2, 0.1, 0), child.getPos())
                            self.move.start()
                        else:
                            print((self.handLeft.getPos(self.E11U) - child.getPos()).length())
                    if not self.hasLeft:
                        for child in self.E7U.getChildren():
                            if (self.handLeft.getPos(self.E7U) - child.getPos()).length() < 1.3:
                                for j in self.items[self.mapX - 1, self.mapY]:
                                    if j[1] == child.getPos():
                                        self.hasLeft = j
                                        self.items[self.mapX - 1, self.mapY].remove(j)
                                child.wrtReparentTo(self.handLeft)
                                self.move = child.posInterval(0.07, (0.2, 0.1, 0), child.getPos())
                                self.move.start()
                            else:
                                print((self.handLeft.getPos(self.E7U) - child.getPos()).length())
                        if not self.hasLeft:
                            for child in self.E17U.getChildren():
                                if (self.handLeft.getPos(self.E17U) - child.getPos()).length() < 1.3:
                                    for j in self.items[self.mapX + 1, self.mapY]:
                                        if j[1] == child.getPos():
                                            self.hasLeft = j
                                            self.items[self.mapX + 1, self.mapY].remove(j)
                                    child.wrtReparentTo(self.handLeft)
                                    self.move = child.posInterval(0.07, (0.2, 0.1, 0), child.getPos())
                                    self.move.start()
                                else:
                                    print((self.handLeft.getPos(self.E17U) - child.getPos()).length())
        elif self.hasLeft:
            for child in self.handLeft.getChildren():
                if child.getPos() != (0, 0, 0):  # so we don't lose our collision shapes ¯\_(ツ)_/¯
                    if len(self.hasLeft) > 5:
                        child.node().setKinematic(0)
                    child.wrtReparentTo(self.E12U)
                    print(child, child.getPos())
                    self.hasLeft[1] = child.getPos()
                    self.hasLeft[2] = child.getHpr()
                    if self.items[self.mapX, self.mapY] == 0:
                        self.items[self.mapX, self.mapY] = []
                    self.items[self.mapX, self.mapY].append(self.hasLeft)
                    self.hasLeft = []
                    print(self.items[self.mapX, self.mapY])
        if len(self.hasLeft) > 5:
            for i in self.handLeft.getChildren():
                if i.getPos() != (0, 0, 0) and child.getY() != 0.06:
                    i.node().setKinematic(1)

    def fullscreen(self):
        self.bigscreen = not self.bigscreen
        if self.bigscreen:
            self.wp.setFullscreen(True)
            self.getWinX = self.win.getProperties().getXOrigin() - 2  # This is to account for the border
            self.getWinY = self.win.getProperties().getYOrigin() - 32
            # Adjust UI
            self.blackStripe.setPos(0, 0, -2.62)
            self.textX = -1.7
            self.textY = -0.94
            if self.X:
                self.X = self.textX
        else:
            self.wp.setFullscreen(False)
            self.wp.setSize(1280, 760)
            self.wp.setOrigin(self.getWinX, self.getWinY)
            self.blackStripe.setPos(0, 0, -2.58)
            self.textX = -1.58
            self.textY = -0.912
            if self.X:
                self.X = self.textX
        self.initialOffset = 0
        self.win.requestProperties(self.wp)

    def update(self, task):
        dt = globalClock.getDt()
        ft = globalClock.getFrameTime()
        self.world.doPhysics(dt)

        def loadMap():
            # Determines where to spawn the lights
            self.dx = self.mapX - self.lightX
            self.dy = self.mapY - self.lightY
            if abs(self.dx) > 1:
                self.lightX = self.mapX + int(self.dx / 2)
                self.lightY = self.mapY
                if self.whichBatch:
                    self.batch0 = [self.lightX, self.lightY]
                else:
                    self.batch1 = [self.lightX, self.lightY]
                self.whichBatch = not self.whichBatch
            if abs(self.dy) > 1:
                self.lightX = self.mapX
                self.lightY = self.mapY + int(self.dy / 2)
                if self.whichBatch:
                    self.batch0 = [self.lightX, self.lightY]
                else:
                    self.batch1 = [self.lightX, self.lightY]
                self.whichBatch = not self.whichBatch
            # Determines which chunks are loaded at any given time
            for i in range(0, 5):
                for j in range(0, 5):
                    newX = self.mapX - 2 + i
                    newY = self.mapY - 2 + j
                    if 5 * i + j not in [0, 1, 3, 4, 20, 21, 23, 24]:
                        mapAssign(newX, newY, 5 * i + j)

        # Reads and writes map for model generation
        def mapAssign(X, Y, elem):
            # Move a few chunks
            if elem == 5:
                X -= 2
                Y += 2
            elif elem == 6:
                X -= 3
                Y += 1
            elif elem == 8:
                X += 1
                Y += 3
            elif elem == 9:
                X += 1
                Y += 1
            elif elem == 15:
                X -= 1
                Y -= 1
            elif elem == 16:
                X -= 1
                Y -= 3
            elif elem == 18:
                X += 3
                Y -= 1
            elif elem == 19:
                X += 2
                Y -= 2

            # Writes the map
            if self.map[X, Y] == 0:
                num = 1
                if self.map[X - 1, Y] == 0:  # CHECK LEFT FOR RIGHT
                    if rm.randint(0, 2) > 0:
                        num = num * 3
                elif self.map[X - 1, Y] % 2 == 0:
                    num = num * 3
                if self.map[X + 1, Y] == 0:  # CHECK RIGHT FOR LEFT
                    if rm.randint(0, 2) > 0:
                        num = num * 2
                elif self.map[X + 1, Y] % 3 == 0:
                    num = num * 2
                if self.map[X, Y - 1] == 0:  # CHECK UP FOR DOWN
                    if rm.randint(0, 2) > 0:
                        num = num * 7
                elif self.map[X, Y - 1] % 5 == 0:
                    num = num * 7
                if self.map[X, Y + 1] == 0:  # CHECK DOWN FOR UP
                    if rm.randint(0, 2) > 0:
                        num = num * 5
                elif self.map[X, Y + 1] % 7 == 0:
                    num = num * 5
                itemFill(num, elem, X, Y)
                self.map[X, Y] = num  # Store the final number

            # Determine which lights to turn on
            if abs(self.batch0[0] - X) < 2 and abs(self.batch0[1] - Y) < 2:
                if self.map[X, Y] % 2 == 0:
                    self.lr = True
                if self.map[X, Y] % 3 == 0:
                    self.ll = True
                if self.map[X, Y] % 5 == 0:
                    self.lu = True
                if self.map[X, Y] % 7 == 0:
                    self.ld = True
            elif abs(self.batch1[0] - X) < 2 and abs(self.batch1[1] - Y) < 2:
                if self.map[X, Y] % 2 == 0:
                    self.lr = True
                if self.map[X, Y] % 3 == 0:
                    self.ll = True
                if self.map[X, Y] % 5 == 0:
                    self.lu = True
                if self.map[X, Y] % 7 == 0:
                    self.ld = True
            else:
                if self.map[X, Y] % 2 == 0:  # if False, turn on respective collider
                    self.qr = True
                else:
                    self.qr = False
                if self.map[X, Y] % 3 == 0:
                    self.ql = True
                else:
                    self.ql = False
                if self.map[X, Y] % 5 == 0:
                    self.qu = True
                else:
                    self.qu = False
                if self.map[X, Y] % 7 == 0:
                    self.qd = True
                else:
                    self.qd = False

            # Refreshes the chunks
            if elem == 2:
                self.elem2.removeNode()
                self.elem2 = loader.loadModel(modLib[self.map[X, Y]])
                self.elem2.setPos(self.CD * -0.5, self.CD * 1.5, 0)
                self.elem2.reparentTo(render)
                if self.lr:
                    self.plE2R.setColor(self.LC)
                    if self.ll:
                        self.plE2L.setColor(self.LC)
                        self.end2.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE2L.setColor(0)
                        self.end2.setCollideMask(BitMask32.bit(2))
                    if self.lu:
                        self.plE2U.setColor(self.LC)
                        self.gBox2U.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE2U.setColor(0)
                        self.gBox2U.setCollideMask(BitMask32.bit(2))
                    if self.ld:
                        self.plE2D.setColor(self.LC)
                        self.gBox2D.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE2D.setColor(0)
                        self.gBox2D.setCollideMask(BitMask32.bit(2))
                else:
                    self.plE2L.setColor(0)
                    self.plE2R.setColor(0)
                    self.plE2U.setColor(0)
                    self.plE2D.setColor(0)
                    if self.ql:
                        self.end2.setCollideMask(BitMask32.bit(9))
                    else:
                        self.end2.setCollideMask(BitMask32.bit(2))
                    if self.qu:
                        self.gBox2U.setCollideMask(BitMask32.bit(9))
                    else:
                        self.gBox2U.setCollideMask(BitMask32.bit(2))
                    if self.qd:
                        self.gBox2D.setCollideMask(BitMask32.bit(9))
                    else:
                        self.gBox2D.setCollideMask(BitMask32.bit(2))
            elif elem == 5:
                self.elem5.removeNode()
                self.elem5 = loader.loadModel(modLib[self.map[X, Y]])
                self.elem5.setPos(self.CD * -1.5, self.CD * 1.5, 0)
                self.elem5.reparentTo(render)
                if self.lr:
                    self.plE5R.setColor(self.LC)
                    if self.ll:
                        self.plE5L.setColor(self.LC)
                    else:
                        self.plE5L.setColor(0)
                    if self.lu:
                        self.plE5U.setColor(self.LC)
                    else:
                        self.plE5U.setColor(0)
                    if self.ld:
                        self.plE5D.setColor(self.LC)
                    else:
                        self.plE5D.setColor(0)
                else:
                    self.plE5L.setColor(0)
                    self.plE5R.setColor(0)
                    self.plE5U.setColor(0)
                    self.plE5D.setColor(0)
            elif elem == 6:
                self.elem6.removeNode()
                self.elem6 = loader.loadModel(modLib[self.map[X, Y]])
                self.elem6.setPos(self.CD * -2.5, self.CD * 1.5, 0)
                self.elem6.reparentTo(render)
                if self.lr:
                    self.plE6R.setColor(self.LC)
                    if self.ll:
                        self.plE6L.setColor(self.LC)
                    else:
                        self.plE6L.setColor(0)
                    if self.lu:
                        self.plE6U.setColor(self.LC)
                    else:
                        self.plE6U.setColor(0)
                    if self.ld:
                        self.plE6D.setColor(self.LC)
                    else:
                        self.plE6D.setColor(0)
                else:
                    self.plE6L.setColor(0)
                    self.plE6R.setColor(0)
                    self.plE6U.setColor(0)
                    self.plE6D.setColor(0)
            elif elem == 7:
                self.elem7.removeNode()
                self.elem7 = loader.loadModel(modLib[self.map[X, Y]])
                self.elem7.setPos(self.CD * 0.5, self.CD * 1.5, 0)
                self.elem7.reparentTo(render)
                if self.lr:
                    self.plE7R.setColor(self.LC)
                    if self.ll:
                        self.plE7L.setColor(self.LC)
                        self.end7.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE7L.setColor(0)
                        self.end7.setCollideMask(BitMask32.bit(2))
                    if self.lu:
                        self.plE7U.setColor(self.LC)
                        self.gBox7U.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE7U.setColor(0)
                        self.gBox7U.setCollideMask(BitMask32.bit(2))
                    if self.ld:
                        self.plE7D.setColor(self.LC)
                        self.gBox7D.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE7D.setColor(0)
                        self.gBox7D.setCollideMask(BitMask32.bit(2))
                else:
                    self.plE7L.setColor(0)
                    self.plE7R.setColor(0)
                    self.plE7U.setColor(0)
                    self.plE7D.setColor(0)
                    if self.ql:
                        self.end7.setCollideMask(BitMask32.bit(9))
                    else:
                        self.end7.setCollideMask(BitMask32.bit(2))
                    if self.qu:
                        self.gBox7U.setCollideMask(BitMask32.bit(9))
                    else:
                        self.gBox7U.setCollideMask(BitMask32.bit(2))
                    if self.qd:
                        self.gBox7D.setCollideMask(BitMask32.bit(9))
                    else:
                        self.gBox7D.setCollideMask(BitMask32.bit(2))
            elif elem == 8:
                self.elem8.removeNode()
                self.elem8 = loader.loadModel(modLib[self.map[X, Y]])
                self.elem8.setPos(self.CD * 1.5, self.CD * 5.5, 0)
                self.elem8.reparentTo(render)
                if self.ld:
                    self.plE8D.setColor(self.LC)
                    if self.ll:
                        self.plE8L.setColor(self.LC)
                    else:
                        self.plE8L.setColor(0)
                    if self.lr:
                        self.plE8R.setColor(self.LC)
                    else:
                        self.plE8R.setColor(0)
                    if self.lu:
                        self.plE8U.setColor(self.LC)
                    else:
                        self.plE8U.setColor(0)
                else:
                    self.plE8L.setColor(0)
                    self.plE8R.setColor(0)
                    self.plE8U.setColor(0)
                    self.plE8D.setColor(0)
            elif elem == 9:
                self.elem9.removeNode()
                self.elem9 = loader.loadModel(modLib[self.map[X, Y]])
                self.elem9.setPos(self.CD * 1.5, self.CD * 4.5, 0)
                self.elem9.reparentTo(render)
                if self.ld:
                    self.plE9D.setColor(self.LC)
                    if self.ll:
                        self.plE9L.setColor(self.LC)
                    else:
                        self.plE9L.setColor(0)
                    if self.lr:
                        self.plE9R.setColor(self.LC)
                    else:
                        self.plE9R.setColor(0)
                    if self.lu:
                        self.plE9U.setColor(self.LC)
                    else:
                        self.plE9U.setColor(0)
                else:
                    self.plE9L.setColor(0)
                    self.plE9R.setColor(0)
                    self.plE9U.setColor(0)
                    self.plE9D.setColor(0)
            elif elem == 10:
                self.elem10.removeNode()
                self.elem10 = loader.loadModel(modLib[self.map[X, Y]])
                self.elem10.setPos(self.CD * 1.5, self.CD * -0.5, 0)
                self.elem10.reparentTo(render)
                if self.lu:
                    self.plE10U.setColor(self.LC)
                    if self.ll:
                        self.plE10L.setColor(self.LC)
                        self.gBox10L.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE10L.setColor(0)
                        self.gBox10L.setCollideMask(BitMask32.bit(2))
                    if self.lr:
                        self.plE10R.setColor(self.LC)
                        self.gBox10R.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE10R.setColor(0)
                        self.gBox10R.setCollideMask(BitMask32.bit(2))
                    if self.ld:
                        self.plE10D.setColor(self.LC)
                        self.end10.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE10D.setColor(0)
                        self.end10.setCollideMask(BitMask32.bit(2))
                else:
                    self.plE10L.setColor(0)
                    self.plE10R.setColor(0)
                    self.plE10U.setColor(0)
                    self.plE10D.setColor(0)
                    if self.ql:
                        self.gBox10L.setCollideMask(BitMask32.bit(9))
                    else:
                        self.gBox10L.setCollideMask(BitMask32.bit(2))
                    if self.qr:
                        self.gBox10R.setCollideMask(BitMask32.bit(9))
                    else:
                        self.gBox10R.setCollideMask(BitMask32.bit(2))
                    if self.qd:
                        self.end10.setCollideMask(BitMask32.bit(9))
                    else:
                        self.end10.setCollideMask(BitMask32.bit(2))
            elif elem == 11:
                self.elem11.removeNode()
                self.elem11 = loader.loadModel(modLib[self.map[X, Y]])
                self.elem11.setPos(self.CD * 1.5, self.CD * 0.5, 0)
                self.elem11.reparentTo(render)
                if self.lu:
                    self.plE11U.setColor(self.LC)
                    if self.ll:
                        self.plE11L.setColor(self.LC)
                        self.gBox11L.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE11L.setColor(0)
                        self.gBox11L.setCollideMask(BitMask32.bit(2))
                    if self.lr:
                        self.plE11R.setColor(self.LC)
                        self.gBox11R.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE11R.setColor(0)
                        self.gBox11R.setCollideMask(BitMask32.bit(2))
                    if self.ld:
                        self.plE11D.setColor(self.LC)
                        self.end11.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE11D.setColor(0)
                        self.end11.setCollideMask(BitMask32.bit(2))
                else:
                    self.plE11L.setColor(0)
                    self.plE11R.setColor(0)
                    self.plE11U.setColor(0)
                    self.plE11D.setColor(0)
                    if self.ql:
                        self.gBox11L.setCollideMask(BitMask32.bit(9))
                    else:
                        self.gBox11L.setCollideMask(BitMask32.bit(2))
                    if self.qr:
                        self.gBox11R.setCollideMask(BitMask32.bit(9))
                    else:
                        self.gBox11R.setCollideMask(BitMask32.bit(2))
                    if self.qd:
                        self.end11.setCollideMask(BitMask32.bit(9))
                    else:
                        self.end11.setCollideMask(BitMask32.bit(2))
            elif elem == 12:
                self.elem12.removeNode()
                self.elem12 = loader.loadModel(modLib[self.map[X, Y]])
                self.elem12.setPos(self.CD * 1.5, self.CD * 1.5, 0)
                self.elem12.reparentTo(render)
                if self.lr:
                    self.plE12R.setColor(self.LC)
                    self.wallR0.setZ(0)
                    self.wallR1.setZ(0)
                else:
                    self.plE12R.setColor(0)
                    self.wallR0.setZ(self.CH)
                    self.wallR1.setZ(self.CH)
                if self.ll:
                    self.plE12L.setColor(self.LC)
                    self.wallL0.setZ(0)
                    self.wallL1.setZ(0)
                else:
                    self.plE12L.setColor(0)
                    self.wallL0.setZ(self.CH)
                    self.wallL1.setZ(self.CH)
                if self.lu:
                    self.plE12U.setColor(self.LC)
                    self.wallU0.setZ(0)
                    self.wallU1.setZ(0)
                else:
                    self.plE12U.setColor(0)
                    self.wallU0.setZ(self.CH)
                    self.wallU1.setZ(self.CH)
                if self.ld:
                    self.plE12D.setColor(self.LC)
                    self.wallD0.setZ(0)
                    self.wallD1.setZ(0)
                else:
                    self.plE12D.setColor(0)
                    self.wallD0.setZ(self.CH)
                    self.wallD1.setZ(self.CH)
            elif elem == 13:
                self.elem13.removeNode()
                self.elem13 = loader.loadModel(modLib[self.map[X, Y]])
                self.elem13.setPos(self.CD * 1.5, self.CD * 2.5, 0)
                self.elem13.reparentTo(render)
                if self.ld:
                    self.plE13D.setColor(self.LC)
                    if self.ll:
                        self.plE13L.setColor(self.LC)
                        self.gBox13L.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE13L.setColor(0)
                        self.gBox13L.setCollideMask(BitMask32.bit(2))
                    if self.lr:
                        self.plE13R.setColor(self.LC)
                        self.gBox13R.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE13R.setColor(0)
                        self.gBox13R.setCollideMask(BitMask32.bit(2))
                    if self.lu:
                        self.plE13U.setColor(self.LC)
                        self.end13.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE13U.setColor(0)
                        self.end13.setCollideMask(BitMask32.bit(2))
                else:
                    self.plE13L.setColor(0)
                    self.plE13R.setColor(0)
                    self.plE13U.setColor(0)
                    self.plE13D.setColor(0)
                    if self.ql:
                        self.gBox13L.setCollideMask(BitMask32.bit(9))
                    else:
                        self.gBox13L.setCollideMask(BitMask32.bit(2))
                    if self.qr:
                        self.gBox13R.setCollideMask(BitMask32.bit(9))
                    else:
                        self.gBox13R.setCollideMask(BitMask32.bit(2))
                    if self.qu:
                        self.end13.setCollideMask(BitMask32.bit(9))
                    else:
                        self.end13.setCollideMask(BitMask32.bit(2))
            elif elem == 14:
                self.elem14.removeNode()
                self.elem14 = loader.loadModel(modLib[self.map[X, Y]])
                self.elem14.setPos(self.CD * 1.5, self.CD * 3.5, 0)
                self.elem14.reparentTo(render)
                if self.ld:
                    self.plE14D.setColor(self.LC)
                    if self.ll:
                        self.plE14L.setColor(self.LC)
                        self.gBox14L.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE14L.setColor(0)
                        self.gBox14L.setCollideMask(BitMask32.bit(2))
                    if self.lr:
                        self.plE14R.setColor(self.LC)
                        self.gBox14R.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE14R.setColor(0)
                        self.gBox14R.setCollideMask(BitMask32.bit(2))
                    if self.lu:
                        self.plE14U.setColor(self.LC)
                        self.end14.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE14U.setColor(0)
                        self.end14.setCollideMask(BitMask32.bit(2))
                else:
                    self.plE14L.setColor(0)
                    self.plE14R.setColor(0)
                    self.plE14U.setColor(0)
                    self.plE14D.setColor(0)
                    if self.ql:
                        self.gBox14L.setCollideMask(BitMask32.bit(9))
                    else:
                        self.gBox14L.setCollideMask(BitMask32.bit(2))
                    if self.qr:
                        self.gBox14R.setCollideMask(BitMask32.bit(9))
                    else:
                        self.gBox14R.setCollideMask(BitMask32.bit(2))
                    if self.qu:
                        self.end14.setCollideMask(BitMask32.bit(9))
                    else:
                        self.end14.setCollideMask(BitMask32.bit(2))
            elif elem == 15:
                self.elem15.removeNode()
                self.elem15 = loader.loadModel(modLib[self.map[X, Y]])
                self.elem15.setPos(self.CD * 1.5, self.CD * -1.5, 0)
                self.elem15.reparentTo(render)
                if self.lu:
                    self.plE15U.setColor(self.LC)
                    if self.ll:
                        self.plE15L.setColor(self.LC)
                    else:
                        self.plE15L.setColor(0)
                    if self.lr:
                        self.plE15R.setColor(self.LC)
                    else:
                        self.plE15R.setColor(0)
                    if self.ld:
                        self.plE15D.setColor(self.LC)
                    else:
                        self.plE15D.setColor(0)
                else:
                    self.plE15L.setColor(0)
                    self.plE15R.setColor(0)
                    self.plE15U.setColor(0)
                    self.plE15D.setColor(0)
            elif elem == 16:
                self.elem16.removeNode()
                self.elem16 = loader.loadModel(modLib[self.map[X, Y]])
                self.elem16.setPos(self.CD * 1.5, self.CD * -2.5, 0)
                self.elem16.reparentTo(render)
                if self.lu:
                    self.plE16U.setColor(self.LC)
                    if self.ll:
                        self.plE16L.setColor(self.LC)
                    else:
                        self.plE16L.setColor(0)
                    if self.lr:
                        self.plE16R.setColor(self.LC)
                    else:
                        self.plE16R.setColor(0)
                    if self.ld:
                        self.plE16D.setColor(self.LC)
                    else:
                        self.plE16D.setColor(0)
                else:
                    self.plE16L.setColor(0)
                    self.plE16R.setColor(0)
                    self.plE16U.setColor(0)
                    self.plE16D.setColor(0)
            elif elem == 17:
                self.elem17.removeNode()
                self.elem17 = loader.loadModel(modLib[self.map[X, Y]])
                self.elem17.setPos(self.CD * 2.5, self.CD * 1.5, 0)
                self.elem17.reparentTo(render)
                if self.ll:
                    self.plE17L.setColor(self.LC)
                    if self.lr:
                        self.plE17R.setColor(self.LC)
                        self.end17.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE17R.setColor(0)
                        self.end17.setCollideMask(BitMask32.bit(2))
                    if self.lu:
                        self.plE17U.setColor(self.LC)
                        self.gBox17U.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE17U.setColor(0)
                        self.gBox17U.setCollideMask(BitMask32.bit(2))
                    if self.ld:
                        self.plE17D.setColor(self.LC)
                        self.gBox17D.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE17D.setColor(0)
                        self.gBox17D.setCollideMask(BitMask32.bit(2))
                else:
                    self.plE17L.setColor(0)
                    self.plE17R.setColor(0)
                    self.plE17U.setColor(0)
                    self.plE17D.setColor(0)
                    if self.qr:
                        self.end17.setCollideMask(BitMask32.bit(9))
                    else:
                        self.end17.setCollideMask(BitMask32.bit(2))
                    if self.qu:
                        self.gBox17U.setCollideMask(BitMask32.bit(9))
                    else:
                        self.gBox17U.setCollideMask(BitMask32.bit(2))
                    if self.qd:
                        self.gBox17D.setCollideMask(BitMask32.bit(9))
                    else:
                        self.gBox17D.setCollideMask(BitMask32.bit(2))
            elif elem == 18:
                self.elem18.removeNode()
                self.elem18 = loader.loadModel(modLib[self.map[X, Y]])
                self.elem18.setPos(self.CD * 5.5, self.CD * 1.5, 0)
                self.elem18.reparentTo(render)
                if self.ll:
                    self.plE18L.setColor(self.LC)
                    if self.lr:
                        self.plE18R.setColor(self.LC)
                    else:
                        self.plE18R.setColor(0)
                    if self.lu:
                        self.plE18U.setColor(self.LC)
                    else:
                        self.plE18U.setColor(0)
                    if self.ld:
                        self.plE18D.setColor(self.LC)
                    else:
                        self.plE18D.setColor(0)
                else:
                    self.plE18L.setColor(0)
                    self.plE18R.setColor(0)
                    self.plE18U.setColor(0)
                    self.plE18D.setColor(0)
            elif elem == 19:
                self.elem19.removeNode()
                self.elem19 = loader.loadModel(modLib[self.map[X, Y]])
                self.elem19.setPos(self.CD * 4.5, self.CD * 1.5, 0)
                self.elem19.reparentTo(render)
                if self.ll:
                    self.plE19L.setColor(self.LC)
                    if self.lr:
                        self.plE19R.setColor(self.LC)
                    else:
                        self.plE19R.setColor(0)
                    if self.lu:
                        self.plE19U.setColor(self.LC)
                    else:
                        self.plE19U.setColor(0)
                    if self.ld:
                        self.plE19D.setColor(self.LC)
                    else:
                        self.plE19D.setColor(0)
                else:
                    self.plE19L.setColor(0)
                    self.plE19R.setColor(0)
                    self.plE19U.setColor(0)
                    self.plE19D.setColor(0)
            else:  # doesn't have to check the num cuz this is the last statement
                self.elem22.removeNode()
                self.elem22 = loader.loadModel(modLib[self.map[X, Y]])
                self.elem22.setPos(self.CD * 3.5, self.CD * 1.5, 0)
                self.elem22.reparentTo(render)
                if self.ll:
                    self.plE22L.setColor(self.LC)
                    if self.lr:
                        self.plE22R.setColor(self.LC)
                        self.end22.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE22R.setColor(0)
                        self.end22.setCollideMask(BitMask32.bit(2))
                    if self.lu:
                        self.plE22U.setColor(self.LC)
                        self.gBox22U.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE22U.setColor(0)
                        self.gBox22U.setCollideMask(BitMask32.bit(2))
                    if self.ld:
                        self.plE22D.setColor(self.LC)
                        self.gBox22D.setCollideMask(BitMask32.bit(9))
                    else:
                        self.plE22D.setColor(0)
                        self.gBox22D.setCollideMask(BitMask32.bit(2))
                else:
                    self.plE22L.setColor(0)
                    self.plE22R.setColor(0)
                    self.plE22U.setColor(0)
                    self.plE22D.setColor(0)
                    if self.qr:
                        self.end22.setCollideMask(BitMask32.bit(9))
                    else:
                        self.end22.setCollideMask(BitMask32.bit(2))
                    if self.qu:
                        self.gBox22U.setCollideMask(BitMask32.bit(9))
                    else:
                        self.gBox22U.setCollideMask(BitMask32.bit(2))
                    if self.qd:
                        self.gBox22D.setCollideMask(BitMask32.bit(9))
                    else:
                        self.gBox22D.setCollideMask(BitMask32.bit(2))
            # Reset lights for next run
            self.lr = 0
            self.ll = 0
            self.lu = 0
            self.ld = 0

        # The following functions move stuff when the map's redrawn
        def itemMoveL():
            # Remove far away stuff
            for child in self.E8U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E9U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E14U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E13U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E6U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E11U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E10U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E15U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E16U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            # Move items
            for child in self.E5U.getChildren():
                child.reparentTo(self.E6U)
            for child in self.E2U.getChildren():
                child.reparentTo(self.E5U)
            for child in self.E7U.getChildren():
                child.reparentTo(self.E2U)
            for child in self.E12U.getChildren():
                child.reparentTo(self.E7U)
            for child in self.E17U.getChildren():
                child.reparentTo(self.E12U)
            for child in self.E22U.getChildren():
                child.reparentTo(self.E17U)
            for child in self.E19U.getChildren():
                child.reparentTo(self.E22U)
            for child in self.E18U.getChildren():
                child.reparentTo(self.E19U)
            # Spawn new items
            if self.items[self.mapX, self.mapY + 4]:
                for i in self.items[self.mapX, self.mapY + 4]:
                    newItem(i, self.E8U, self.mapX, self.mapY + 4)
            if self.items[self.mapX, self.mapY + 3]:
                for i in self.items[self.mapX, self.mapY + 3]:
                    newItem(i, self.E9U, self.mapX, self.mapY + 3)
            if self.items[self.mapX, self.mapY + 2]:
                for i in self.items[self.mapX, self.mapY + 2]:
                    newItem(i, self.E14U, self.mapX, self.mapY + 2)
            if self.items[self.mapX, self.mapY + 1]:
                for i in self.items[self.mapX, self.mapY + 1]:
                    newItem(i, self.E13U, self.mapX, self.mapY + 1)
            if self.items[self.mapX + 4, self.mapY]:
                for i in self.items[self.mapX + 4, self.mapY]:
                    newItem(i, self.E18U, self.mapX + 4, self.mapY)
            if self.items[self.mapX, self.mapY - 1]:
                for i in self.items[self.mapX, self.mapY - 1]:
                    newItem(i, self.E11U, self.mapX, self.mapY - 1)
            if self.items[self.mapX, self.mapY - 2]:
                for i in self.items[self.mapX, self.mapY - 2]:
                    newItem(i, self.E10U, self.mapX, self.mapY - 2)
            if self.items[self.mapX, self.mapY - 3]:
                for i in self.items[self.mapX, self.mapY - 3]:
                    newItem(i, self.E15U, self.mapX, self.mapY - 3)
            if self.items[self.mapX, self.mapY - 4]:
                for i in self.items[self.mapX, self.mapY - 4]:
                    newItem(i, self.E16U, self.mapX, self.mapY - 4)

        def itemMoveR():
            # Remove far away stuff
            for child in self.E8U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E9U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E14U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E13U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E18U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E11U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E10U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E15U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E16U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            # Move items
            for child in self.E19U.getChildren():
                child.reparentTo(self.E18U)
            for child in self.E22U.getChildren():
                child.reparentTo(self.E19U)
            for child in self.E17U.getChildren():
                child.reparentTo(self.E22U)
            for child in self.E12U.getChildren():
                child.reparentTo(self.E17U)
            for child in self.E7U.getChildren():
                child.reparentTo(self.E12U)
            for child in self.E2U.getChildren():
                child.reparentTo(self.E7U)
            for child in self.E5U.getChildren():
                child.reparentTo(self.E2U)
            for child in self.E6U.getChildren():
                child.reparentTo(self.E5U)
            # Spawn new items
            if self.items[self.mapX, self.mapY + 4]:
                for i in self.items[self.mapX, self.mapY + 4]:
                    newItem(i, self.E8U, self.mapX, self.mapY + 4)
            if self.items[self.mapX, self.mapY + 3]:
                for i in self.items[self.mapX, self.mapY + 3]:
                    newItem(i, self.E9U, self.mapX, self.mapY + 3)
            if self.items[self.mapX, self.mapY + 2]:
                for i in self.items[self.mapX, self.mapY + 2]:
                    newItem(i, self.E14U, self.mapX, self.mapY + 2)
            if self.items[self.mapX, self.mapY + 1]:
                for i in self.items[self.mapX, self.mapY + 1]:
                    newItem(i, self.E13U, self.mapX, self.mapY + 1)
            if self.items[self.mapX - 4, self.mapY]:
                for i in self.items[self.mapX - 4, self.mapY]:
                    newItem(i, self.E6U, self.mapX - 4, self.mapY)
            if self.items[self.mapX, self.mapY - 1]:
                for i in self.items[self.mapX, self.mapY - 1]:
                    newItem(i, self.E11U, self.mapX, self.mapY - 1)
            if self.items[self.mapX, self.mapY - 2]:
                for i in self.items[self.mapX, self.mapY - 2]:
                    newItem(i, self.E10U, self.mapX, self.mapY - 2)
            if self.items[self.mapX, self.mapY - 3]:
                for i in self.items[self.mapX, self.mapY - 3]:
                    newItem(i, self.E15U, self.mapX, self.mapY - 3)
            if self.items[self.mapX, self.mapY - 4]:
                for i in self.items[self.mapX, self.mapY - 4]:
                    newItem(i, self.E16U, self.mapX, self.mapY - 4)

        def itemMoveU():
            # Remove far away stuff
            for child in self.E6U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E5U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E2U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E7U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E8U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E17U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E22U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E19U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E18U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            # Move items
            for child in self.E9U.getChildren():
                child.reparentTo(self.E8U)
            for child in self.E14U.getChildren():
                child.reparentTo(self.E9U)
            for child in self.E13U.getChildren():
                child.reparentTo(self.E14U)
            for child in self.E12U.getChildren():
                child.reparentTo(self.E13U)
            for child in self.E11U.getChildren():
                child.reparentTo(self.E12U)
            for child in self.E10U.getChildren():
                child.reparentTo(self.E11U)
            for child in self.E15U.getChildren():
                child.reparentTo(self.E10U)
            for child in self.E16U.getChildren():
                child.reparentTo(self.E15U)
            # Spawn new items
            if self.items[self.mapX - 4, self.mapY]:
                for i in self.items[self.mapX - 4, self.mapY]:
                    newItem(i, self.E6U, self.mapX - 4, self.mapY)
            if self.items[self.mapX - 3, self.mapY]:
                for i in self.items[self.mapX - 3, self.mapY]:
                    newItem(i, self.E5U, self.mapX - 3, self.mapY)
            if self.items[self.mapX - 2, self.mapY]:
                for i in self.items[self.mapX - 2, self.mapY]:
                    newItem(i, self.E2U, self.mapX - 2, self.mapY)
            if self.items[self.mapX - 1, self.mapY]:
                for i in self.items[self.mapX - 1, self.mapY]:
                    newItem(i, self.E7U, self.mapX - 1, self.mapY)
            if self.items[self.mapX, self.mapY - 4]:
                for i in self.items[self.mapX, self.mapY - 4]:
                    newItem(i, self.E16U, self.mapX, self.mapY - 4)
            if self.items[self.mapX + 1, self.mapY]:
                for i in self.items[self.mapX + 1, self.mapY]:
                    newItem(i, self.E17U, self.mapX + 1, self.mapY)
            if self.items[self.mapX + 2, self.mapY]:
                for i in self.items[self.mapX + 2, self.mapY]:
                    newItem(i, self.E22U, self.mapX + 2, self.mapY)
            if self.items[self.mapX + 3, self.mapY]:
                for i in self.items[self.mapX + 3, self.mapY]:
                    newItem(i, self.E19U, self.mapX + 3, self.mapY)
            if self.items[self.mapX + 4, self.mapY]:
                for i in self.items[self.mapX + 4, self.mapY]:
                    newItem(i, self.E18U, self.mapX + 4, self.mapY)

        def itemMoveD():
            # Remove far away stuff
            for child in self.E6U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E5U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E2U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E7U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E16U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E17U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E22U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E19U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            for child in self.E18U.getChildren():
                for j in child.getChildren():
                    if j.getX():
                        j.removeNode()
                        self.world.removeRigidBody(child.node())
                else:
                    child.removeNode()
            # Move items
            for child in self.E15U.getChildren():
                child.reparentTo(self.E16U)
            for child in self.E10U.getChildren():
                child.reparentTo(self.E15U)
            for child in self.E11U.getChildren():
                child.reparentTo(self.E10U)
            for child in self.E12U.getChildren():
                child.reparentTo(self.E11U)
            for child in self.E13U.getChildren():
                child.reparentTo(self.E12U)
            for child in self.E14U.getChildren():
                child.reparentTo(self.E13U)
            for child in self.E9U.getChildren():
                child.reparentTo(self.E14U)
            for child in self.E8U.getChildren():
                child.reparentTo(self.E9U)
            # Spawn new items
            if self.items[self.mapX - 4, self.mapY]:
                for i in self.items[self.mapX - 4, self.mapY]:
                    newItem(i, self.E6U, self.mapX - 4, self.mapY)
            if self.items[self.mapX - 3, self.mapY]:
                for i in self.items[self.mapX - 3, self.mapY]:
                    newItem(i, self.E5U, self.mapX - 3, self.mapY)
            if self.items[self.mapX - 2, self.mapY]:
                for i in self.items[self.mapX - 2, self.mapY]:
                    newItem(i, self.E2U, self.mapX - 2, self.mapY)
            if self.items[self.mapX - 1, self.mapY]:
                for i in self.items[self.mapX - 1, self.mapY]:
                    newItem(i, self.E7U, self.mapX - 1, self.mapY)
            if self.items[self.mapX, self.mapY + 4]:
                for i in self.items[self.mapX, self.mapY + 4]:
                    newItem(i, self.E8U, self.mapX, self.mapY + 4)
            if self.items[self.mapX + 1, self.mapY]:
                for i in self.items[self.mapX + 1, self.mapY]:
                    newItem(i, self.E17U, self.mapX + 1, self.mapY)
            if self.items[self.mapX + 2, self.mapY]:
                for i in self.items[self.mapX + 2, self.mapY]:
                    newItem(i, self.E22U, self.mapX + 2, self.mapY)
            if self.items[self.mapX + 3, self.mapY]:
                for i in self.items[self.mapX + 3, self.mapY]:
                    newItem(i, self.E19U, self.mapX + 3, self.mapY)
            if self.items[self.mapX + 4, self.mapY]:
                for i in self.items[self.mapX + 4, self.mapY]:
                    newItem(i, self.E18U, self.mapX + 4, self.mapY)

        def newItem(modelStr, parent, X, Y):
            if self.items[X, Y] == 0:
                self.items[X, Y] = []
            if modelStr not in self.items[X, Y]:
                self.items[X, Y].append(modelStr)

            if "box" in modelStr:
                shape = BulletBoxShape(modelStr[4])
                self.node = BulletRigidBodyNode('box')
                self.node.setMass(200)
                self.node.addShape(shape)
                self.path = parent.attachNewNode(self.node)
                self.path.setPosHpr(modelStr[1], modelStr[2])
                self.world.attachRigidBody(self.node)
                self.path.setCollideMask(BitMask32.bit(0) | BitMask32.bit(2))
                self.model = loader.loadModel(modelStr[0])
                self.model.setPos(modelStr[5])
                self.model.reparentTo(self.path)
            else:
                spawner = loader.loadModel(modelStr[0])
                spawner.setPosHpr(modelStr[1], modelStr[2])
                spawner.reparentTo(parent)

        def itemFill(piece, elem, X, Y):
            # convert the elem number to something newItem can work with
            if elem == 2:
                elem = self.E2U
            elif elem == 5:
                elem = self.E5U
            elif elem == 6:
                elem = self.E6U
            elif elem == 7:
                elem = self.E7U
            elif elem == 8:
                elem = self.E8U
            elif elem == 9:
                elem = self.E9U
            elif elem == 10:
                elem = self.E10U
            elif elem == 11:
                elem = self.E11U
            elif elem == 12:
                elem = self.E12U
            elif elem == 13:
                elem = self.E13U
            elif elem == 14:
                elem = self.E14U
            elif elem == 15:
                elem = self.E15U
            elif elem == 16:
                elem = self.E16U
            elif elem == 17:
                elem = self.E17U
            elif elem == 18:
                elem = self.E18U
            elif elem == 19:
                elem = self.E19U
            else:
                elem = self.E22U

            if rm.randint(0, 3) > 2:
                regions = [[0, -self.CD / 4]]
                # This finds a random spot in the hallway to spawn items (eventually carts)
                if piece % 2 == 0:
                    regions.append([self.CD / 3, -self.CD / 4])
                if piece % 3 == 0:
                    regions.append([-self.CD / 3, -self.CD / 4])
                if piece % 5 == 0:
                    regions.append([0, self.CD / 12])
                if piece % 7 == 0:
                    regions.append([0, -self.CD * 7 / 12])
                xy = regions[rm.randint(0, len(regions) - 1)]
                xy[0] += rm.randint(-6, 6) * self.CD / 46
                xy[1] += rm.randint(-6, 6) * self.CD / 46
                newItem(["models/teapot", (xy[0], xy[1], -self.LH), (rm.randint(0, 360), 0, 0)], elem, X, Y)

            if piece in [2, 3, 5, 7, 10, 14, 15, 21, 210]:
                foo = 1
                for i in ["my-models/decor/outlet", "my-models/decor/panel"]:
                    if not rm.randint(0, foo):
                        if piece == 210:
                            pick = rm.randint(1, 3)
                        else:
                            pick = 0
                        if piece == 2:
                            xy = (-self.CD / 6, rm.randint(-19, -5) * self.CD / 50, 0)
                            h = 270
                        elif piece == 3:
                            xy = (self.CD / 6, rm.randint(-19, -5) * self.CD / 50, 0)
                            h = 90
                        elif piece == 5:
                            xy = (rm.randint(-7, 7) * self.CD / 50, -self.CD * 5 / 12, 0)
                            h = 0
                        elif piece == 7:
                            xy = (rm.randint(-7, 7) * self.CD / 50, -self.CD / 12, 0)
                            h = 180
                        elif piece == 10 or pick == 1:
                            if rm.randint(0, 1):
                                xy = (self.CD / 6, rm.randint(-3, 11) * self.CD / 49, 0)
                                h = 90
                            else:
                                xy = (rm.randint(9, 22) * self.CD / 47, -self.CD / 12, 0)
                                h = 180
                        elif piece == 14 or pick == 2:
                            if rm.randint(0, 1):
                                xy = (self.CD / 6, rm.randint(-35, -22) * self.CD / 49, 0)
                                h = 90
                            else:
                                xy = (rm.randint(9, 22) * self.CD / 47, -self.CD * 5 / 12, 0)
                                h = 0
                        elif piece == 15 or pick == 3:
                            if rm.randint(0, 1):
                                xy = (-self.CD / 6, rm.randint(-3, 11) * self.CD / 49, 0)
                                h = 270
                            else:
                                xy = (rm.randint(-23, -9) * self.CD / 48, -self.CD / 12, 0)
                                h = 180
                        else:
                            if rm.randint(0, 1):
                                xy = (-self.CD / 6, rm.randint(-35, -22) * self.CD / 49, 0)
                                h = 270
                            else:
                                xy = (rm.randint(-23, -9) * self.CD / 48, -self.CD * 5 / 12, 0)
                                h = 0
                        newItem([i, xy, (h, 0, 0)], elem, X, Y)
                    foo += 2

            if piece in [6, 30, 35, 42, 70, 105] and rm.randint(0, 2):
                xy = [0, 0]
                # make sure the vents don't cover the lights
                while xy in [[0, 0], [1, 0], [0, -5], [1, -5], [-2, -2], [-2, -3], [3, -2], [3, -3]]:
                    xy[0] = rm.randint(-4, 5)
                    xy[1] = rm.randint(-7, 2)
                xy = ((xy[0] - 0.5) * self.CD / 10, xy[1] * self.CD / 10, 0)
                newItem(["my-models/decor/vent", xy, (0, 0, 0)], elem, X, Y)

        # MOVE CHAR + CAMERA + SET ANIMATION
        currentAnim = self.char.getCurrentAnim()
        self.animFrame = self.char.getAnimControl("walk").getFrame()
        self.jack.setZ(5.5 - sin(self.char.getAnimControl("walk").getFrame() * 0.5236) / 7)
        self.cam.setP(self.backBone.getP() + self.angleY)

        # BACKWARD
        if keyMap["backward"]:
            self.char.setFluidY(self.char, +self.speed * self.slower * 0.8 * dt)
            if currentAnim != "walk":
                self.char.loop("walk")
            self.char.setPlayRate(-self.playRate, "walk")
        # FORWARD
        if keyMap["forward"]:
            self.char.setFluidY(self.char, -self.speed * self.slower * dt)
            if currentAnim != "walk":
                self.char.loop("walk")
            self.char.setPlayRate(self.playRate, "walk")
        # LEFT / RIGHT
        if (keyMap["left"] or keyMap["right"]) and (keyMap["forward"] or keyMap["backward"]):
            self.slower = 0.71  # Slows speed for two directions at once
        else:
            self.slower = 1
        if keyMap["right"]:
            self.char.setFluidX(self.char, -self.speed * self.slower * dt)
            if currentAnim != "walk":
                self.char.loop("walk")
        if keyMap["left"]:
            self.char.setFluidX(self.char, +self.speed * self.slower * dt)
            if currentAnim != "walk":
                self.char.loop("walk")
        # BEN DOVER
        if keyMap["bend"]:
            self.backBone.setP(self.backBone, -(self.backBone.getP() + self.angleY + 13.36) * dt * 13)
            self.neckBone.setP(-(self.backBone.getP() + self.angleY + 53.36))
            self.speed = 6
            self.sensMod = 0.4
            self.playRate = 0.4
            # for reaching arms
            self.angleL = 175 + bool(self.hasLeft) * 13
            self.angleR = 185 - bool(self.hasRight) * 13
        else:
            self.backBone.setH(0)
            self.backBone.setP(self.backBone, -(self.backBone.getP() + 13.36) * dt * 12)
            self.backBone.setR(0)
            self.jack.setHpr(0, 346.64, 0)
            # for reaching arms
            self.angleL = -self.angleY * 0.85 + 175 + bool(self.hasLeft) * 13
            self.angleR = self.angleY * 0.85 + 185 - bool(self.hasRight) * 13
            # SPRINT MODIFIER
            if keyMap["sprint"]:
                if (keyMap["left"] or keyMap["right"] or keyMap["forward"] or keyMap["backward"]) and (self.vig < 1):
                    if not ((keyMap["left"] and keyMap["right"]) or (keyMap["forward"] and keyMap["backward"])):
                        self.vig += dt / 5
                        self.vignette.setColor(0, 0, 0, self.vig)
                    # Cooldown
                    elif self.vig > 0:
                        self.vig -= dt / 5  # This is in here a few times cuz of various conditions
                        self.vignette.setColor(0, 0, 0, self.vig)  # that it should run for
                # Cooldown
                elif self.vig > 0:
                    self.vig -= dt / 5  # and cuz i need to find a better way to write code
                    self.vignette.setColor(0, 0, 0, self.vig)
                self.speed = 50
                self.playRate = 2
                self.zMod = 4
            elif keyMap["forward"] and keyMap["backward"]:
                self.speed = 23
                self.playRate = 0.5
                self.zMod = 10
            else:
                self.speed = 20
                self.playRate = 1
                self.zMod = 5
            self.sensMod = 1
        self.jack.setP(self.backBone.getP())
        # Cooldown
        if not keyMap["sprint"] and (self.vig > 0):
            self.vig -= dt / 5  # See?  here it is again (:
            self.vignette.setColor(0, 0, 0, self.vig)
        # STAND
        if currentAnim != "stand":
            self.armWaver = sin(self.animFrame * 0.2618) * 20
            if not bool(keyMap["forward"] + keyMap["backward"] + keyMap["left"] + keyMap["right"]):
                self.char.loop("stand")
        else:
            self.armWaver = 0
        # REACH ARMS
        if keyMap["reachL"]:
            self.armLeft.setP(7)
            self.count1 = 0
        else:
            if self.count1 > 0.2:
                self.armLeft.setP(-7.37)
            else:
                self.count1 += dt
            self.angleL = self.angleY * keyMap["bend"] / 1.8 + 253.54 + self.armWaver
        self.armLeft.setR(self.armLeft, -(self.armLeft.getR() % 360 - self.angleL) * dt * 9)
        if keyMap["reachR"]:
            self.armRight.setP(7)
            self.count2 = 0
        else:
            if self.count2 > 0.2:
                self.armRight.setP(-7.37)
            else:
                self.count2 += dt
            self.angleR = -self.angleY * keyMap["bend"] / 1.8 + 106.45 + self.armWaver
        self.armRight.setR(self.armRight, -(self.armRight.getR() % 360 - self.angleR) * dt * 9)

        # SET THE ORIENTATION
        if self.mouseWatcherNode.hasMouse():
            if self.initialOffset > 0.1:  # Makes dragging cursor to window more comfortable
                # X-axis
                self.angleX -= self.cursorX * dt * self.sensitivity * self.sensMod
                self.char.setH(self.angleX + 100)
                self.cursorX = self.mouseWatcherNode.getMouseX()
                # Y-axis
                self.angleY += self.cursorY * dt * self.sensitivity * self.sensMod / 4
                if self.angleY < -85:
                    self.angleY = -85
                if self.angleY > 90 - 15 * keyMap["bend"]:
                    self.angleY = 90 - 15 * keyMap["bend"]
                elif not keyMap["bend"]:
                    self.neckBone.setP(self.angleY * -1 - 40)
                self.cursorY = self.mouseWatcherNode.getMouseY()
            elif self.win.getProperties().getForeground():
                self.initialOffset += dt
            self.win.movePointer(0, int(self.win.getXSize() / 2), int(self.win.getYSize() / 2))
        else:
            self.cursorX = 0
            self.initialOffset = 0

        # Find and report player map coords
        if int(self.char.getX() / self.CD) > 1:
            self.char.setX(self.char.getX() - self.CD)  # teleport char so you never actually move :)
            self.mapX += 1
            itemMoveL()
            loadMap()
            print(self.mapX, self.mapY)
        elif int(self.char.getX() / self.CD) < 1:
            self.char.setX(self.char.getX() + self.CD)
            self.mapX -= 1
            itemMoveR()
            loadMap()
            print(self.mapX, self.mapY)
        elif int(self.char.getY() / self.CD) > 1:
            self.char.setY(self.char.getY() - self.CD)
            self.mapY += 1
            itemMoveD()
            loadMap()
            print(self.mapX, self.mapY)
        elif int(self.char.getY() / self.CD) < 1:
            self.char.setY(self.char.getY() + self.CD)
            self.mapY -= 1
            itemMoveU()
            loadMap()
            print(self.mapX, self.mapY)
        elif not self.mapYet:
            loadMap()
            newItem(["models/jack", (0, 2, 1 - self.LH), (0, 0, 0)], self.E12U, 0, 0)
            newItem(["models/camera", (2, 2, 1 - self.LH), (0, 0, 0)], self.E12U, 0, 0)
            newItem(["my-models/sunflower", (-4, 2, 1 - self.LH), (0, 0, 0)], self.E12U, 0, 0)
            print(self.mapX, self.mapY)
            self.mapYet = True

        def textManager(txtNum, transBool, dur):
            if dur > 0:
                self.dur = ft + dur
            if self.dur and (ft >= self.dur):
                self.dur = 0
                txtNum = self.placeHolder
                transBool = 1  # not sure how to treat this
            if not self.dur and (self.txtNum != txtNum):
                del textLib[self.txtNum][0]  # get rid of dialogue once it's been used
            self.transBool = transBool
            self.txtNum = txtNum
            if not self.dur:  # store messages that are intended to show for a long period of time
                self.placeHolder = self.txtNum

            # TODO: figure out how multiple messages happening at the same time is dealt with
            # TODO: make it not change text when the specified list is empty

            #  transBool asks if we're transitioning to or not
            #
            #  dur is duration.  if none is specified, the text
            #  just stays the same until another text gets sent,
            #  then reverts back after that messages duration
            #
            #  if there's a duration on something, we're gonna
            #  remove it from the list after using it, cuz it's
            #  probably not something worth saying twice
            #
            #  textLib stores all the stuff that gets said.  That's
            #  the plan atm.

            if textLib[self.txtNum][0] != self.text:
                if self.transBool:
                    self.textUI.setFg((self.yellow, self.yellow, self.blue, 1))
                    self.speaker.setFg((self.yellow, self.yellow, self.blue, self.spkrOn * 0.94))
                    if self.yellow > 0:
                        self.yellow -= dt * 4
                        self.blue -= dt / 2
                    elif self.blue > 0:
                        self.blue -= dt * 10
                    else:  # Once the transition is complete
                        self.transBool = 0
                        self.yellow = 0.865
                        self.blue = 0.82
                        self.textUI.setText(self.text)
                else:
                    self.text = textLib[txtNum][0]
                    self.textUI.setText(self.text)
                    print("im running bitch")
                    if txtNum in [2]:  # change font based on who's talking
                        self.X = 0
                        self.textUI.setFont(self.jacksyn)
                        self.textUI.setScale(0.065, 0.057)
                        self.textUI.setAlign(2)
                        self.speaker.setText("Char:")
                        self.spkrOn = True
                    else:
                        self.X = self.textX
                        self.textUI.setFont(self.mono)
                        self.textUI.setScale(0.052)
                        self.textUI.setAlign(0)
                        self.spkrOn = False

            elif self.text:  # This makes sense because it won't be called if that ^^ gets called
                r = rm.randint(-1, 1)
                g = rm.randint(-1, 1)  # This block of code changes
                b = rm.randint(-1, 1)  # the hue of the text while
                offset = (r + g + b) / 3  # retaining its brightness
                r = 0.869 + (r - offset) / 8
                g = 0.858 + (g - offset) / 8
                b = 0.823 + (b - offset) / 8
                self.textUI.setFg((r, g, b, 1))
                self.speaker.setFg((r, g, b, self.spkrOn))
            self.textUI.setPos(self.X, self.textY)  # This has to run all the time in case the screen size gets changed
            self.speaker.setPos(self.textX, self.textY)

        # GHOST WALLS: Do yo thang!
        # pay attention to noop conditions when adding more
        def ghostUpdate():
            ghostL = self.ghostWallL.node()
            if self.ghostNumL != ghostL.getOverlappingNodes():
                for node in ghostL.getOverlappingNodes():
                    if node.getChildren():
                        node.setAngularVelocity((0, 0, 0))
                        if node.getLinearVelocity()[0] < -0.2:
                            node.setLinearVelocity((2, 0, 0))
            self.ghostNumL = ghostL.getNumOverlappingNodes()

            ghostR = self.ghostWallR.node()
            if self.ghostNumR != ghostR.getOverlappingNodes():
                for node in ghostR.getOverlappingNodes():
                    if node.getChildren():
                        node.setAngularVelocity((0, 0, 0))
                        if node.getLinearVelocity()[0] > 0.2:
                            node.setLinearVelocity((-2, 0, 0))
            self.ghostNumR = ghostR.getNumOverlappingNodes()

            ghostD = self.ghostWallD.node()
            if self.ghostNumD != ghostD.getOverlappingNodes():
                for node in ghostD.getOverlappingNodes():
                    if node.getChildren():
                        node.setAngularVelocity((0, 0, 0))
                        if node.getLinearVelocity()[1] < -0.2:
                            node.setLinearVelocity((0, 2, 0))
            self.ghostNumD = ghostD.getNumOverlappingNodes()

            ghostU = self.ghostWallU.node()
            if self.ghostNumD != ghostU.getOverlappingNodes():
                for node in ghostU.getOverlappingNodes():
                    if node.getChildren():
                        node.setAngularVelocity((0, 0, 0))
                        if node.getLinearVelocity()[1] > 0.2:
                            node.setLinearVelocity((0, -2, 0))
            self.ghostNumU = ghostU.getNumOverlappingNodes()

            g13L = self.gBox13L.node()
            if self.gBoxNum13L != g13L.getNumOverlappingNodes():
                for node in g13L.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] < -0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 2, poon[0] / 2, poon[0] / 2))
                            node.setLinearVelocity((-noop[0] / 5, noop[1] / 2, noop[2]))
            self.gBoxNum13L = g13L.getNumOverlappingNodes()

            g13R = self.gBox13R.node()
            if self.gBoxNum13R != g13R.getNumOverlappingNodes():
                for node in g13R.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] > 0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 2, poon[0] / 2, poon[0] / 2))
                            node.setLinearVelocity((-noop[0] / 5, noop[1] / 2, noop[2]))
            self.gBoxNum13R = g13R.getNumOverlappingNodes()

            g11L = self.gBox11L.node()
            if self.gBoxNum11L != g11L.getNumOverlappingNodes():
                for node in g11L.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] < -0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 2, poon[0] / 2, poon[0] / 2))
                            node.setLinearVelocity((noop[0] / 5, noop[1] / 2, noop[2]))
            self.gBoxNum11L = g11L.getNumOverlappingNodes()

            g11R = self.gBox11R.node()
            if self.gBoxNum11R != g11R.getNumOverlappingNodes():
                for node in g11R.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] > 0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 2, poon[0] / 2, poon[0] / 2))
                            node.setLinearVelocity((-noop[0] / 5, noop[1] / 2, noop[2]))
            self.gBoxNum11R = g11R.getNumOverlappingNodes()

            g7U = self.gBox7U.node()
            if self.gBoxNum7U != g7U.getNumOverlappingNodes():
                for node in g7U.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] > 0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 2, poon[0] / 2, poon[0] / 2))
                            node.setLinearVelocity((noop[0] / 2, -noop[1] / 5, noop[2]))
            self.gBoxNum7U = g7U.getNumOverlappingNodes()

            g7D = self.gBox7D.node()
            if self.gBoxNum7D != g7D.getNumOverlappingNodes():
                for node in g7D.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] < -0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 2, poon[0] / 2, poon[0] / 2))
                            node.setLinearVelocity((noop[0] / 2, noop[1] / 5, noop[2]))
            self.gBoxNum7D = g7D.getNumOverlappingNodes()

            g17U = self.gBox17U.node()
            if self.gBoxNum17U != g17U.getNumOverlappingNodes():
                for node in g17U.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] > 0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 2, poon[0] / 2, poon[0] / 2))
                            node.setLinearVelocity((noop[0] / 2, -noop[1] / 5, noop[2]))
            self.gBoxNum17U = g17U.getNumOverlappingNodes()

            g17D = self.gBox17D.node()
            if self.gBoxNum17D != g17D.getNumOverlappingNodes():
                for node in g17D.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] < -0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 2, poon[0] / 2, poon[0] / 2))
                            node.setLinearVelocity((noop[0] / 2, noop[1] / 5, noop[2]))
            self.gBoxNum17D = g17D.getNumOverlappingNodes()

            g14L = self.gBox14L.node()
            if self.gBoxNum14L != g14L.getNumOverlappingNodes():
                for node in g14L.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] < -0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 2, poon[0] / 2, poon[0] / 2))
                            node.setLinearVelocity((-noop[0] / 5, noop[1] / 2, noop[2]))
            self.gBoxNum14L = g14L.getNumOverlappingNodes()

            g14R = self.gBox14R.node()
            if self.gBoxNum14R != g14R.getNumOverlappingNodes():
                for node in g14R.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] > 0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 2, poon[0] / 2, poon[0] / 2))
                            node.setLinearVelocity((-noop[0] / 5, noop[1] / 2, noop[2]))
            self.gBoxNum14R = g14R.getNumOverlappingNodes()

            g10L = self.gBox10L.node()
            if self.gBoxNum10L != g10L.getNumOverlappingNodes():
                for node in g10L.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] < -0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 2, poon[0] / 2, poon[0] / 2))
                            node.setLinearVelocity((noop[0] / 5, noop[1] / 2, noop[2]))
            self.gBoxNum10L = g10L.getNumOverlappingNodes()

            g10R = self.gBox10R.node()
            if self.gBoxNum10R != g10R.getNumOverlappingNodes():
                for node in g10R.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] > 0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 2, poon[0] / 2, poon[0] / 2))
                            node.setLinearVelocity((-noop[0] / 5, noop[1] / 2, noop[2]))
            self.gBoxNum10R = g10R.getNumOverlappingNodes()

            g2U = self.gBox2U.node()
            if self.gBoxNum2U != g2U.getNumOverlappingNodes():
                for node in g2U.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] > 0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 2, poon[0] / 2, poon[0] / 2))
                            node.setLinearVelocity((noop[0] / 2, -noop[1] / 5, noop[2]))
            self.gBoxNum2U = g2U.getNumOverlappingNodes()

            g2D = self.gBox2D.node()
            if self.gBoxNum2D != g2D.getNumOverlappingNodes():
                for node in g2D.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] < -0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 2, poon[0] / 2, poon[0] / 2))
                            node.setLinearVelocity((noop[0] / 2, noop[1] / 5, noop[2]))
            self.gBoxNum2D = g2D.getNumOverlappingNodes()

            g22U = self.gBox22U.node()
            if self.gBoxNum22U != g22U.getNumOverlappingNodes():
                for node in g22U.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] > 0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 2, poon[0] / 2, poon[0] / 2))
                            node.setLinearVelocity((noop[0] / 2, -noop[1] / 5, noop[2]))
            self.gBoxNum22U = g22U.getNumOverlappingNodes()

            g22D = self.gBox22D.node()
            if self.gBoxNum22D != g22D.getNumOverlappingNodes():
                for node in g22D.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] < -0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 2, poon[0] / 2, poon[0] / 2))
                            node.setLinearVelocity((noop[0] / 2, noop[1] / 5, noop[2]))
            self.gBoxNum22D = g22D.getNumOverlappingNodes()

            cUL = self.CornUL.node()
            if self.cULnum != cUL.getNumOverlappingNodes():
                for node in cUL.getOverlappingNodes():
                    if node.getChildren():
                        node.setAngularVelocity((0, 0, 0))
                        node.setLinearVelocity((0, 0, 0))
            self.cULnum = cUL.getNumOverlappingNodes()

            cUR = self.CornUR.node()
            if self.cURnum != cUR.getNumOverlappingNodes():
                for node in cUR.getOverlappingNodes():
                    if node.getChildren():
                        node.setAngularVelocity((0, 0, 0))
                        node.setLinearVelocity((0, 0, 0))
            self.cURnum = cUR.getNumOverlappingNodes()

            cDL = self.CornDL.node()
            if self.cDLnum != cDL.getNumOverlappingNodes():
                for node in cDL.getOverlappingNodes():
                    if node.getChildren():
                        node.setAngularVelocity((0, 0, 0))
                        node.setLinearVelocity((0, 0, 0))
            self.cDLnum = cDL.getNumOverlappingNodes()

            cDR = self.CornDR.node()
            if self.cDRnum != cDR.getNumOverlappingNodes():
                for node in cDR.getOverlappingNodes():
                    if node.getChildren():
                        node.setAngularVelocity((0, 0, 0))
                        node.setLinearVelocity((0, 0, 0))
            self.cDRnum = cDR.getNumOverlappingNodes()

            sBxs13L = self.sBoxes13L.node()
            if self.sBXSnum13L != sBxs13L.getNumOverlappingNodes():
                for node in sBxs13L.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] < -0.2:
                            node.setLinearVelocity((-noop[0] / 2, noop[1] / 1.4, noop[2]))
            self.sBXSnum13L = sBxs13L.getNumOverlappingNodes()

            sBxs11L = self.sBoxes11L.node()
            if self.sBXSnum11L != sBxs11L.getNumOverlappingNodes():
                for node in sBxs11L.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] < -0.2:
                            node.setLinearVelocity((-noop[0] / 2, noop[1] / 1.4, noop[2]))
            self.sBXSnum11L = sBxs11L.getNumOverlappingNodes()

            sBxs13R = self.sBoxes13R.node()
            if self.sBXSnum13R != sBxs13R.getNumOverlappingNodes():
                for node in sBxs13R.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] > 0.2:
                            node.setLinearVelocity((-noop[0] / 2, noop[1] / 1.4, noop[2]))
            self.sBXSnum13R = sBxs13R.getNumOverlappingNodes()

            sBxs11R = self.sBoxes11R.node()
            if self.sBXSnum11R != sBxs11R.getNumOverlappingNodes():
                for node in sBxs11R.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] > 0.2:
                            node.setLinearVelocity((-noop[0] / 2, noop[1] / 1.4, noop[2]))
            self.sBXSnum11R = sBxs11R.getNumOverlappingNodes()

            sBxs7U = self.sBoxes7U.node()
            if self.sBXSnum7U != sBxs7U.getNumOverlappingNodes():
                for node in sBxs7U.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] > 0.2:
                            node.setLinearVelocity((noop[0] / 1.4, -noop[1] / 2, noop[2]))
            self.sBXSnum7U = sBxs7U.getNumOverlappingNodes()

            sBxs17U = self.sBoxes17U.node()
            if self.sBXSnum17U != sBxs17U.getNumOverlappingNodes():
                for node in sBxs17U.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] > 0.2:
                            node.setLinearVelocity((noop[0] / 1.4, -noop[1] / 2, noop[2]))
            self.sBXSnum17U = sBxs17U.getNumOverlappingNodes()

            sBxs7D = self.sBoxes7D.node()
            if self.sBXSnum7D != sBxs7D.getNumOverlappingNodes():
                for node in sBxs7D.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] < -0.2:
                            node.setLinearVelocity((noop[0] / 1.4, -noop[1] / 2, noop[2]))
            self.sBXSnum7D = sBxs7D.getNumOverlappingNodes()

            sBxs17D = self.sBoxes17D.node()
            if self.sBXSnum17D != sBxs17D.getNumOverlappingNodes():
                for node in sBxs17D.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] < -0.2:
                            node.setLinearVelocity((noop[0] / 1.4, -noop[1] / 2, noop[2]))
            self.sBXSnum17D = sBxs17D.getNumOverlappingNodes()

            sBxs14L = self.sBoxes14L.node()
            if self.sBXSnum14L != sBxs14L.getNumOverlappingNodes():
                for node in sBxs14L.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] < -0.2:
                            node.setLinearVelocity((-noop[0] / 2, noop[1] / 1.4, noop[2]))
            self.sBXSnum14L = sBxs14L.getNumOverlappingNodes()

            sBxs10L = self.sBoxes10L.node()
            if self.sBXSnum10L != sBxs10L.getNumOverlappingNodes():
                for node in sBxs10L.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] < -0.2:
                            node.setLinearVelocity((-noop[0] / 2, noop[1] / 1.4, noop[2]))
            self.sBXSnum10L = sBxs10L.getNumOverlappingNodes()

            sBxs14R = self.sBoxes14R.node()
            if self.sBXSnum14R != sBxs14R.getNumOverlappingNodes():
                for node in sBxs14R.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] > 0.2:
                            node.setLinearVelocity((-noop[0] / 2, noop[1] / 1.4, noop[2]))
            self.sBXSnum14R = sBxs14R.getNumOverlappingNodes()

            sBxs10R = self.sBoxes10R.node()
            if self.sBXSnum10R != sBxs10R.getNumOverlappingNodes():
                for node in sBxs10R.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] > 0.2:
                            node.setLinearVelocity((-noop[0] / 2, noop[1] / 1.4, noop[2]))
            self.sBXSnum10R = sBxs10R.getNumOverlappingNodes()

            sBxs2U = self.sBoxes2U.node()
            if self.sBXSnum2U != sBxs2U.getNumOverlappingNodes():
                for node in sBxs2U.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] > 0.2:
                            node.setLinearVelocity((noop[0] / 1.4, -noop[1] / 2, noop[2]))
            self.sBXSnum2U = sBxs2U.getNumOverlappingNodes()

            sBxs22U = self.sBoxes22U.node()
            if self.sBXSnum22U != sBxs22U.getNumOverlappingNodes():
                for node in sBxs22U.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] > 0.2:
                            node.setLinearVelocity((noop[0] / 1.4, -noop[1] / 2, noop[2]))
            self.sBXSnum22U = sBxs22U.getNumOverlappingNodes()

            sBxs2D = self.sBoxes2D.node()
            if self.sBXSnum2D != sBxs2D.getNumOverlappingNodes():
                for node in sBxs2D.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] < -0.2:
                            node.setLinearVelocity((noop[0] / 1.4, -noop[1] / 2, noop[2]))
            self.sBXSnum2D = sBxs2D.getNumOverlappingNodes()

            sBxs22D = self.sBoxes22D.node()
            if self.sBXSnum22D != sBxs22D.getNumOverlappingNodes():
                for node in sBxs22D.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] < -0.2:
                            node.setLinearVelocity((noop[0] / 1.4, -noop[1] / 2, noop[2]))
            self.sBXSnum22D = sBxs22D.getNumOverlappingNodes()

            lBx14L = self.longBx14L.node()
            if self.lBXnum14L != lBx14L.getNumOverlappingNodes():
                for node in lBx14L.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] < -0.2:
                            node.setLinearVelocity((-noop[0] / 2, noop[1] / 1.7, noop[2]))
            self.lBXnum14L = lBx14L.getNumOverlappingNodes()

            lBx10L = self.longBx10L.node()
            if self.lBXnum10L != lBx10L.getNumOverlappingNodes():
                for node in lBx10L.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] < -0.2:
                            print(noop)
                            node.setLinearVelocity((-noop[0] / 2, noop[1] / 1.7, noop[2]))
            self.lBXnum10L = lBx10L.getNumOverlappingNodes()

            lBx14R = self.longBx14R.node()
            if self.lBXnum14R != lBx14R.getNumOverlappingNodes():
                for node in lBx14R.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] > 0.2:
                            node.setLinearVelocity((-noop[0] / 2, noop[1] / 1.7, noop[2]))
            self.lBXnum14R = lBx14R.getNumOverlappingNodes()

            lBx10R = self.longBx10R.node()
            if self.lBXnum10R != lBx10R.getNumOverlappingNodes():
                for node in lBx10R.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] > 0.2:
                            node.setLinearVelocity((-noop[0] / 2, noop[1] / 1.7, noop[2]))
            self.lBXnum10R = lBx10R.getNumOverlappingNodes()

            lBx2U = self.longBx2U.node()
            if self.lBXnum2U != lBx2U.getNumOverlappingNodes():
                for node in lBx2U.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] > 0.2:
                            node.setLinearVelocity((noop[0] / 1.7, -noop[1] / 2, noop[2]))
            self.lBXnum2U = lBx2U.getNumOverlappingNodes()

            lBx22U = self.longBx22U.node()
            if self.lBXnum22U != lBx22U.getNumOverlappingNodes():
                for node in lBx22U.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] > 0.2:
                            node.setLinearVelocity((noop[0] / 1.7, -noop[1] / 2, noop[2]))
            self.lBXnum22U = lBx22U.getNumOverlappingNodes()

            lBx2D = self.longBx2D.node()
            if self.lBXnum2D != lBx2D.getNumOverlappingNodes():
                for node in lBx2D.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] < -0.2:
                            node.setLinearVelocity((noop[0] / 1.7, -noop[1] / 2, noop[2]))
            self.lBXnum2D = lBx2D.getNumOverlappingNodes()

            lBx22D = self.longBx22D.node()
            if self.lBXnum22D != lBx22D.getNumOverlappingNodes():
                for node in lBx22D.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] < -0.2:
                            node.setLinearVelocity((noop[0] / 1.7, -noop[1] / 2, noop[2]))
            self.lBXnum22D = lBx22D.getNumOverlappingNodes()

            b13L = self.bounc13L.node()
            if self.b13numL != b13L.getNumOverlappingNodes():
                for node in b13L.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] > 0.2:
                            node.setLinearVelocity((noop[0] / 1.2, -2, noop[2]))
            self.b13numL = b13L.getNumOverlappingNodes()
            b13R = self.bounc13R.node()
            if self.b13numR != b13R.getNumOverlappingNodes():
                for node in b13R.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] > 0.2:
                            node.setLinearVelocity((noop[0] / 1.2, -2, noop[2]))
            self.b13numR = b13R.getNumOverlappingNodes()

            b11L = self.bounc11L.node()
            if self.b11numL != b11L.getNumOverlappingNodes():
                for node in b11L.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] < -0.2:
                            node.setLinearVelocity((noop[0] / 1.2, 2, noop[2]))
            self.b11numL = b11L.getNumOverlappingNodes()
            b11R = self.bounc11R.node()
            if self.b11numR != b11R.getNumOverlappingNodes():
                for node in b11R.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] < -0.2:
                            node.setLinearVelocity((noop[0] / 1.2, 2, noop[2]))
            self.b11numR != b11R.getNumOverlappingNodes()

            b17D = self.bounc17D.node()
            if self.b17numD != b17D.getNumOverlappingNodes():
                for node in b17D.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] > 0.2:
                            node.setLinearVelocity((-2, noop[1] / 1.2, noop[2]))
            self.b17numD = b17D.getNumOverlappingNodes()
            b17U = self.bounc17U.node()
            if self.b17numU != b17U.getNumOverlappingNodes():
                for node in b17U.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] > 0.2:
                            node.setLinearVelocity((-2, noop[1] / 1.2, noop[2]))
            self.b17numU = b17U.getNumOverlappingNodes()

            b7D = self.bounc7D.node()
            if self.b7numD != b7D.getNumOverlappingNodes():
                for node in b7D.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] < -0.2:
                            node.setLinearVelocity((2, noop[1] / 1.2, noop[2]))
            self.b7numD = b7D.getNumOverlappingNodes()
            b7U = self.bounc7U.node()
            if self.b7numU != b7U.getNumOverlappingNodes():
                for node in b7U.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] < -0.2:
                            node.setLinearVelocity((2, noop[1] / 1.2, noop[2]))
            self.b7numU = b7U.getNumOverlappingNodes()

            b22D = self.bounc22D.node()
            if self.b22numD != b22D.getNumOverlappingNodes():
                for node in b22D.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] > 0.2:
                            node.setLinearVelocity((-3, noop[1] / 1.2, noop[2]))
            self.b22numD = b22D.getNumOverlappingNodes()
            b22U = self.bounc22U.node()
            if self.b22numU != b22U.getNumOverlappingNodes():
                for node in b22U.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] > 0.2:
                            node.setLinearVelocity((-3, noop[1] / 1.2, noop[2]))
            self.b22numU = b22U.getNumOverlappingNodes()

            b2D = self.bounc2D.node()
            if self.b2numD != b2D.getNumOverlappingNodes():
                for node in b2D.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] < -0.2:
                            node.setLinearVelocity((3, noop[1] / 1.2, noop[2]))
            self.b2numD = b2D.getNumOverlappingNodes()
            b2U = self.bounc2U.node()
            if self.b2numU != b2U.getNumOverlappingNodes():
                for node in b2U.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] < -0.2:
                            node.setLinearVelocity((3, noop[1] / 1.2, noop[2]))
            self.b2numU = b2U.getNumOverlappingNodes()

            b10L = self.bounc10L.node()
            if self.b10numL != b10L.getNumOverlappingNodes():
                for node in b10L.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] < -0.2:
                            node.setLinearVelocity((noop[0] / 1.2, 3, noop[2]))
            self.b10numL = b10L.getNumOverlappingNodes()
            b10R = self.bounc10R.node()
            if self.b10numR != b10R.getNumOverlappingNodes():
                for node in b10R.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] < -0.2:
                            node.setLinearVelocity((noop[0] / 1.2, 3, noop[2]))
            self.b10numR = b10R.getNumOverlappingNodes()

            b14L = self.bounc14L.node()
            if self.b14numL != b14L.getNumOverlappingNodes():
                for node in b14L.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] > 0.2:
                            node.setLinearVelocity((noop[0] / 1.2, -3, noop[2]))
            self.b14numL = b14L.getNumOverlappingNodes()
            b14R = self.bounc14R.node()
            if self.b14numR != b14R.getNumOverlappingNodes():
                for node in b14R.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] > 0.2:
                            node.setLinearVelocity((noop[0] / 1.2, -3, noop[2]))
            self.b14numR = b14R.getNumOverlappingNodes()

            e7 = self.end7.node()
            if self.e7num != e7.getNumOverlappingNodes():
                for node in e7.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] < -0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 3, poon[0] / 3, poon[0] / 3))
                            node.setLinearVelocity((-noop[0] / 10, noop[1], noop[2]))
            self.e7num = e7.getNumOverlappingNodes()

            e17 = self.end17.node()
            if self.e17num != e17.getNumOverlappingNodes():
                for node in e17.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] > 0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 3, poon[0] / 3, poon[0] / 3))
                            node.setLinearVelocity((-noop[0] / 10, noop[1], noop[2]))
            self.e17num = e17.getNumOverlappingNodes()

            e13 = self.end13.node()
            if self.e13num != e13.getNumOverlappingNodes():
                for node in e13.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] > 0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 3, poon[0] / 3, poon[0] / 3))
                            node.setLinearVelocity((noop[0], -noop[1] / 10, noop[2]))
            self.e13num = e13.getNumOverlappingNodes()

            e11 = self.end11.node()
            if self.e11num != e11.getNumOverlappingNodes():
                for node in e11.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] < -0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 3, poon[0] / 3, poon[0] / 3))
                            node.setLinearVelocity((noop[0], -noop[1] / 10, noop[2]))
            self.e11num = e11.getNumOverlappingNodes()

            e2 = self.end2.node()
            if self.e2num != e2.getNumOverlappingNodes():
                for node in e2.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] < -0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 3, poon[0] / 3, poon[0] / 3))
                            node.setLinearVelocity((-noop[0] / 10, noop[1], noop[2]))
            self.e2num = e2.getNumOverlappingNodes()

            e22 = self.end22.node()
            if self.e22num != e22.getNumOverlappingNodes():
                for node in e22.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[0] > 0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 3, poon[0] / 3, poon[0] / 3))
                            node.setLinearVelocity((-noop[0] / 10, noop[1], noop[2]))
            self.e22num = e22.getNumOverlappingNodes()

            e14 = self.end14.node()
            if self.e14num != e14.getNumOverlappingNodes():
                for node in e14.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] > 0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 3, poon[0] / 3, poon[0] / 3))
                            node.setLinearVelocity((noop[0], -noop[1] / 10, noop[2]))
            self.e14num = e14.getNumOverlappingNodes()

            e10 = self.end10.node()
            if self.e10num != e10.getNumOverlappingNodes():
                for node in e10.getOverlappingNodes():
                    if node.getChildren():
                        noop = node.getLinearVelocity()
                        if noop[1] < -0.2:
                            poon = node.getAngularVelocity()
                            node.setAngularVelocity((poon[0] / 3, poon[0] / 3, poon[0] / 3))
                            node.setLinearVelocity((noop[0], -noop[1] / 10, noop[2]))
            self.e10num = e10.getNumOverlappingNodes()

        ghostUpdate()

        def bulletUpdate():
            # UPDATE POSITION DATA OF BULLET OBJECTS
            for i in self.E12U.getChildren():
                for j in i.getChildren():
                    if j.getX():
                        for k in self.items[self.mapX, self.mapY]:
                            if len(k) > 5:  # Determines whether catalogued item is a bullet body
                                if round(j.getX(), 7) == round(k[5][0], 7):
                                    k[1] = i.getPos()
                                    k[2] = i.getHpr()
                                    if int(i.getX() / self.CD + 1.5) == 0:  # these lines move objects to other
                                        i.wrtReparentTo(self.E7U)           # squares when they cross the border
                                        k[1] = i.getPos()
                                        if self.items[self.mapX - 1, self.mapY] == 0:
                                            self.items[self.mapX - 1, self.mapY] = []
                                        self.items[self.mapX - 1, self.mapY].append(k)
                                        self.items[self.mapX, self.mapY].remove(k)
                                    if int(i.getX() / self.CD + 1.5) == 2:
                                        i.wrtReparentTo(self.E17U)
                                        k[1] = i.getPos()
                                        if self.items[self.mapX + 1, self.mapY] == 0:
                                            self.items[self.mapX + 1, self.mapY] = []
                                        self.items[self.mapX + 1, self.mapY].append(k)
                                        self.items[self.mapX, self.mapY].remove(k)
                                    if int(i.getY() / self.CD + 1.75) == 2:
                                        i.wrtReparentTo(self.E13U)
                                        k[1] = i.getPos()
                                        if self.items[self.mapX, self.mapY + 1] == 0:
                                            self.items[self.mapX, self.mapY + 1] = []
                                        self.items[self.mapX, self.mapY + 1].append(k)
                                        self.items[self.mapX, self.mapY].remove(k)
                                    if int(i.getY() / self.CD + 1.75) == 0:
                                        i.wrtReparentTo(self.E11U)
                                        k[1] = i.getPos()
                                        if self.items[self.mapX, self.mapY - 1] == 0:
                                            self.items[self.mapX, self.mapY - 1] = []
                                        self.items[self.mapX, self.mapY - 1].append(k)
                                        self.items[self.mapX, self.mapY].remove(k)
            for i in self.E13U.getChildren():
                for j in i.getChildren():
                    if j.getX():
                        for k in self.items[self.mapX, self.mapY + 1]:
                            if len(k) > 5:
                                if round(j.getX(), 7) == round(k[5][0], 7):
                                    k[1] = i.getPos()
                                    k[2] = i.getHpr()
                                    if int(i.getY() / self.CD + 2.5) == 0:
                                        i.wrtReparentTo(self.E12U)
                                        k[1] = i.getPos()
                                        if self.items[self.mapX, self.mapY] == 0:
                                            self.items[self.mapX, self.mapY] = []
                                        self.items[self.mapX, self.mapY].append(k)
                                        self.items[self.mapX, self.mapY + 1].remove(k)
                                    if int(i.getY() / self.CD + 2.5) == 2:
                                        i.wrtReparentTo(self.E14U)
                                        k[1] = i.getPos()
                                        if self.items[self.mapX, self.mapY + 2] == 0:
                                            self.items[self.mapX, self.mapY + 2] = []
                                        self.items[self.mapX, self.mapY + 2].append(k)
                                        self.items[self.mapX, self.mapY + 1].remove(k)
                                        print("in 14")
            for i in self.E14U.getChildren():
                for j in i.getChildren():
                    if j.getX():
                        for k in self.items[self.mapX, self.mapY + 2]:
                            if len(k) > 5:
                                if round(j.getX(), 7) == round(k[5][0], 7):
                                    k[1] = i.getPos()
                                    k[2] = i.getHpr()
                                    if int(i.getY() / self.CD + 2.5) == 0:
                                        i.wrtReparentTo(self.E13U)
                                        k[1] = i.getPos()
                                        if self.items[self.mapX, self.mapY + 2] == 0:
                                            self.items[self.mapX, self.mapY + 2] = []
                                        self.items[self.mapX, self.mapY + 1].append(k)
                                        self.items[self.mapX, self.mapY + 2].remove(k)
            for i in self.E11U.getChildren():
                for j in i.getChildren():
                    if j.getX():
                        for k in self.items[self.mapX, self.mapY - 1]:
                            if len(k) > 5:
                                if round(j.getX(), 7) == round(k[5][0], 7):
                                    k[1] = i.getPos()
                                    k[2] = i.getHpr()
                                    if int(i.getY() / self.CD + 1.5) == 0:
                                        i.wrtReparentTo(self.E10U)
                                        k[1] = i.getPos()
                                        if self.items[self.mapX, self.mapY - 2] == 0:
                                            self.items[self.mapX, self.mapY - 2] = []
                                        self.items[self.mapX, self.mapY - 2].append(k)
                                        self.items[self.mapX, self.mapY - 1].remove(k)
                                        print("in 10")
                                    if int(i.getY() / self.CD + 1.5) == 2:
                                        i.wrtReparentTo(self.E12U)
                                        k[1] = i.getPos()
                                        if self.items[self.mapX, self.mapY] == 0:
                                            self.items[self.mapX, self.mapY] = []
                                        self.items[self.mapX, self.mapY].append(k)
                                        self.items[self.mapX, self.mapY - 1].remove(k)
            for i in self.E10U.getChildren():
                for j in i.getChildren():
                    if j.getX():
                        for k in self.items[self.mapX, self.mapY - 2]:
                            if len(k) > 5:
                                if round(j.getX(), 7) == round(k[5][0], 7):
                                    k[1] = i.getPos()
                                    k[2] = i.getHpr()
                                    if int(i.getX() / self.CD + 1.5) == 2:
                                        i.wrtReparentTo(self.E11U)
                                        k[1] = i.getPos()
                                        if self.items[self.mapX, self.mapY - 1] == 0:
                                            self.items[self.mapX, self.mapY - 1] = []
                                        self.items[self.mapX, self.mapY - 1].append(k)
                                        self.items[self.mapX, self.mapY - 2].remove(k)
            for i in self.E7U.getChildren():
                for j in i.getChildren():
                    if j.getX():
                        for k in self.items[self.mapX - 1, self.mapY]:
                            if len(k) > 5:
                                if round(j.getX(), 7) == round(k[5][0], 7):
                                    k[1] = i.getPos()
                                    k[2] = i.getHpr()
                                    if int(i.getX() / self.CD + 1.5) == 0:
                                        i.wrtReparentTo(self.E2U)
                                        k[1] = i.getPos()
                                        if self.items[self.mapX - 2, self.mapY] == 0:
                                            self.items[self.mapX - 2, self.mapY] = []
                                        self.items[self.mapX - 2, self.mapY].append(k)
                                        self.items[self.mapX - 1, self.mapY].remove(k)
                                        print("in 2")
                                    if int(i.getX() / self.CD + 1.5) == 2:
                                        i.wrtReparentTo(self.E12U)
                                        k[1] = i.getPos()
                                        if self.items[self.mapX, self.mapY] == 0:
                                            self.items[self.mapX, self.mapY] = []
                                        self.items[self.mapX, self.mapY].append(k)
                                        self.items[self.mapX - 1, self.mapY].remove(k)
            for i in self.E2U.getChildren():
                for j in i.getChildren():
                    if j.getX():
                        for k in self.items[self.mapX - 2, self.mapY]:
                            if len(k) > 5:
                                if round(j.getX(), 7) == round(k[5][0], 7):
                                    k[1] = i.getPos()
                                    k[2] = i.getHpr()
                                    if int(i.getX() / self.CD + 1.5) == 2:
                                        i.wrtReparentTo(self.E7U)
                                        k[1] = i.getPos()
                                        if self.items[self.mapX - 1, self.mapY] == 0:
                                            self.items[self.mapX - 1, self.mapY] = []
                                        self.items[self.mapX - 1, self.mapY].append(k)
                                        self.items[self.mapX - 2, self.mapY].remove(k)
            for i in self.E17U.getChildren():
                for j in i.getChildren():
                    if j.getX():
                        for k in self.items[self.mapX + 1, self.mapY]:
                            if len(k) > 5:
                                if round(j.getX(), 7) == round(k[5][0], 7):
                                    k[1] = i.getPos()
                                    k[2] = i.getHpr()
                                    if int(i.getX() / self.CD + 1.5) == 0:
                                        i.wrtReparentTo(self.E12U)
                                        k[1] = i.getPos()
                                        if self.items[self.mapX, self.mapY] == 0:
                                            self.items[self.mapX, self.mapY] = []
                                        self.items[self.mapX, self.mapY].append(k)
                                        self.items[self.mapX + 1, self.mapY].remove(k)
                                    if int(i.getX() / self.CD + 1.5) == 2:
                                        i.wrtReparentTo(self.E22U)
                                        k[1] = i.getPos()
                                        if self.items[self.mapX + 2, self.mapY] == 0:
                                            self.items[self.mapX + 2, self.mapY] = []
                                        self.items[self.mapX + 2, self.mapY].append(k)
                                        self.items[self.mapX + 1, self.mapY].remove(k)
                                        print("in 22")
            for i in self.E22U.getChildren():
                for j in i.getChildren():
                    if j.getX():
                        for k in self.items[self.mapX + 2, self.mapY]:
                            if len(k) > 5:
                                if round(j.getX(), 7) == round(k[5][0], 7):
                                    k[1] = i.getPos()
                                    k[2] = i.getHpr()
                                    if int(i.getX() / self.CD + 1.5) == 0:
                                        i.wrtReparentTo(self.E17U)
                                        k[1] = i.getPos()
                                        if self.items[self.mapX + 1, self.mapY] == 0:
                                            self.items[self.mapX + 1, self.mapY] = []
                                        self.items[self.mapX + 1, self.mapY].append(k)
                                        self.items[self.mapX + 2, self.mapY].remove(k)

        #  The goal here is to run code every other frame that needs
        #  to get updated, but is not as critical
        if self.everyOther:
            textManager(self.txtNum, self.transBool, 0)  # This will keep the dialogue/UI up to date
        else:
            bulletUpdate()
        #  Will add fatigue manager to the else of this
        self.everyOther = not self.everyOther

        #  Using the zero key to test different parts of the code
        if keyMap["test"]:
            if self.bool1:  # bool1 is used to make sure pressing 0 only calls code once

                textManager(2, 1, 4)

                newItem(["my-models/cube", (0, 0, 0), (0, 0, 0), "box", (1, 1, 1), (self.boxX, 0, 0)],
                        self.E12U, self.mapX, self.mapY)
                # Modifying this boxX to the smallest possible interval let's know which
                # self.items string to update for to keep track of it's respective object
                self.boxX += 0.0000001

                self.bool1 = False
        else:
            self.bool1 = True

        return task.cont


game = MyGame()
game.run()
