from cubeSolver import *
from cubies import *
import random

        
class Controller(object):
    def __init__(self): 
        self.scene = canvas(background = color.gray(0.97))
        self.scene.ambient=color.gray(0.7)
        self.cube3d = Cube3D()
        self.scene.bind('keydown',self.onKey)
        self.scene.bind('click',self.onClick)
        self.scene.bind('mousedown',self.onMouseDown)
        self.scene.bind('mouseup',self.onMouseUp)
        self.scene.bind('mousemove',self.onMouseMove)
        self.turnTime = 0.5
        self.cubeRepr = Cube()
        self.keyQueue = []
        self.activeWidgets = []
        self.mode = 0
        self.setWidgetMode(self.mode)
        self.brushColor = 'u'
        self.colorNames = ["White", "Red", "Green", "Orange", "Blue", "Yellow"]
        self.colorCodes = ["FFFFFF","FF0000", "00FF00", "FFAA00", "0000FF", "FFFF00"]

    def setWidgetMode(self, mode):
        #Takes an integer specifying what widgets to display 0 = default toy widget
        self.mode = mode
        for widget in self.activeWidgets:
            widget.delete()
        self.scene.caption = ""
        self.activeWidgets = []
        if mode == 0: #regular
            self.activeWidgets.append(button(bind=self.reset, text="New cube"))
            self.activeWidgets.append(button(bind=self.scramble, text = "Scramble"))
            self.activeWidgets.append(button(bind=self.solve, text = "Solve")) 
            self.activeWidgets.append(button(bind=self.paintMode, text = "Paint"))
            self.activeWidgets.append(button(bind=self.openSettings, text = "Settings"))
        if mode == 1: #paint
            self.activeWidgets.append(button(bind=self.normalMode, text = "Back"))
            self.activeWidgets.append(menu(choices = self.colorNames, bind = self.changeBrushColor))
        if mode == 2: #settings
            self.activeWidgets.append(button(bind=self.normalMode, text = "Back"))
            self.activeWidgets.append(wtext(text = "\n"))
            self.activeWidgets.append(button(bind=self.colorSettings, text = "Change color scheme"))
            self.activeWidgets.append(wtext(text = "\nTurn time: "))
            self.activeWidgets.append(slider(min = 0.2, max = 2.0, step = 0.01, value = 0.5, bind = self.updateTurnSpeed))
        if mode == 3: #color settings
            self.activeWidgets.append(button(bind=self.openSettings, text = "Back"))
            self.activeWidgets.append(wtext(text = "\n Side | Color Name | Color Hex Code"))
            self.activeWidgets.append(wtext(text = "\n Up: "))
            self.activeWidgets.append(winput(text = self.colorNames[0], bind = self.updateColor))
            self.activeWidgets.append(winput(text = self.colorCodes[0], bind = self.updateColor))
            self.activeWidgets.append(wtext(text = "\n Down: "))
            self.activeWidgets.append(winput(text = self.colorNames[5], bind = self.updateColor))
            self.activeWidgets.append(winput(text = self.colorCodes[5], bind = self.updateColor))
            self.activeWidgets.append(wtext(text = "\n Front: "))
            self.activeWidgets.append(winput(text = self.colorNames[1], bind = self.updateColor))
            self.activeWidgets.append(winput(text = self.colorCodes[1], bind = self.updateColor))
            self.activeWidgets.append(wtext(text = "\n Back: "))
            self.activeWidgets.append(winput(text = self.colorNames[3], bind = self.updateColor))
            self.activeWidgets.append(winput(text = self.colorCodes[3], bind = self.updateColor))
            self.activeWidgets.append(wtext(text = "\n Left: "))
            self.activeWidgets.append(winput(text = self.colorNames[2], bind = self.updateColor))
            self.activeWidgets.append(winput(text = self.colorCodes[2], bind = self.updateColor))
            self.activeWidgets.append(wtext(text = "\n Right: "))
            self.activeWidgets.append(winput(text = self.colorNames[4], bind = self.updateColor))
            self.activeWidgets.append(winput(text = self.colorCodes[4], bind = self.updateColor))
            



    def updateColor(self, i):
        count = 0
        for widget in self.activeWidgets:
            if type(widget) == type(self.activeWidgets[3]):
                count += 1
            if widget == i:
                break
        colorMap = {0:0,1:5,2:1,3:3,4:2,5:4} #some intrefacing between UD FB LR that makes sense for settings vs UFL BRD that applies to Cube3D colors input
        if count %2 == 1: #name
            self.colorNames[colorMap[(count-1)//2]] = i.text
        else:#code
            if self.verifyCode(i.text):
                self.colorCodes[colorMap[(count-1)//2]] = i.text
                self.updateCubeColor()
        print(self.colorNames,self.colorCodes)

    def verifyCode(self, text):
        print(text + " " + str(len(text)))
        if len(text) != 6:
            return False
        for char in text.lower():
            if char not in ['a','b','c','d','e','f','1','2','3','4','5','6','7','8','9','0']:
                return False
        return True


    def updateCubeColor():
        #actually take the actual colors on the actual cube.
        #TODO
        pass

    def updateTurnSpeed(self, s):
        self.cube3d.updateRotateTime(s.value)
        self.turnTime = s.value

    def changeBrushColor(self, m):
        index = self.colorNames.index(m.selected)
        self.brushColor = {0:'u', 1:'d', 2:'f', 3:'b', 4:'l', 5:'r'}[index]

    def colorSettings(self, b):
        self.setWidgetMode(3)

    def normalMode(self, b):
        self.setWidgetMode(0)

    def openSettings(self, b):
        self.setWidgetMode(2)

    def paintMode(self, b):
        self.setWidgetMode(1)

    def generateScramble(self, length = 30):
        #Generates a scramble of max length length and returns a list of appropriate moves. Capitalized moves are counterclockwise turns.
        vocab = ['f','F','f2', 'b', 'B', 'b2', 'u', 'U', 'u2', 'd', 'D', 'd2', 'l', 'L', 'l2', 'r', 'R', 'r2']
        scrambleList = []
        for i in range(length):
            scrambleList.append(vocab[random.randint(0,17)])
        removeList = []
        for i in range(length-1):
            if scrambleList[i][0].lower() == scrambleList[i+1][0].lower():
                removeList.append(i)
        removeList = removeList[::-1]
        for i in removeList:
            scrambleList.pop(i)
        return scrambleList

    def scramble(self):
        #Generates a scramble list and scrambles the current 3d cube.
        scrambleList = self.generateScramble()
        print(scrambleList)
        for move in scrambleList:
            self.cube3d.rotate(move)

    def reset(self):
        #Destroys the current cube and creates a new one
        self.cube3d.destroy()
        self.cube3d = Cube3D()
        self.cube3d.updateTurnTime(self.turnTime)
        self.cubeRepr = Cube()

    def solve(self):
            cubeRepr = self.cube3d.toCube()
            solution = CubeSolver.solve(cubeRepr)
            for move in solution:
                self.cube3d.rotate(move)
            #generate and print solution
            pass

    def onKey(self, evt):
        #Called by keypress event listener
        #print(evt.__dict__)
        self.keyQueue.append(evt)
        if len(self.keyQueue) > 1:
            return
        #self.scene.unbind('keydown',self.onKey)
        while len(self.keyQueue) > 0:
            key = self.keyQueue[0].key
            if key.lower() in ['f','b','l','r','u','d']:
                self.cube3d.rotate(key)
            elif key.lower() == "s":
                self.scramble()
            elif key.lower() == "g":
                self.solve()
            elif key.lower() == "n":
                self.reset()
            self.keyQueue.pop(0)
        #self.scene.bind('keydown',self.onKey)

    def onClick(self, evt):
        obj = self.scene.mouse.pick
        if self.mode == 1:
            self.cube3d.updateStickerColor(obj, self.brushColor)


    def onMouseDown(self, evt):
        pass

    def onMouseUp(self, evt):
        #print(evt.__dict__)
        pass

    def onMouseMove(self, evt):
        #print(evt.__dict__)
        pass
        
controller = Controller()
