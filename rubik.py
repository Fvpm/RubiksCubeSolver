from cubeSolver import *
from cubies import *
import random
import pickle

        
class Controller(object):
    def __init__(self): 
        #Scene settings
        self.scene = canvas(background = color.gray(0.97))
        self.scene.ambient=color.gray(0.7)
        #self.scene.userzoom = False
        self.scene.autoscale = False
        self.scene.forward = vector(-1,-1,-1)
        self.scene.camera.range = .5

        #Cube objects
        self.cube3d = Cube3D()
        self.cubeRepr = Cube()

        #Event binds
        self.scene.bind('keydown',self.onKey)
        self.scene.bind('click',self.onClick)
        #self.scene.bind('mousedown',self.onMouseDown)
        #self.scene.bind('mouseup',self.onMouseUp)
        #self.scene.bind('mousemove',self.onMouseMove)

        #Program Variables.
        self.moveCount = 0
        self.startPosition = None
        self.undoList = []
        self.redoList = []
        self.keyQueue = []
        self.moveQueue = 0
        self.activeWidgets = []
        self.mode = 0
        self.brushColor = 'u'
        self.solution = [] #For solution mode
        self.solutionIndex = 0
        self.autoPlaying = False
        self.loadSettings()

        #Load colors and widgets.
        self.setWidgetMode(self.mode)
        self.updateCubeColor()

    def loadSettings(self):
        #Updates variables with settings from 'settings' file as saved in saveSetings. Takes no input and returns None
        self.colors = [color.white, color.red, color.green, color.orange, color.blue, color.yellow] #I pretty much immdiately overwrite this
        try:
            f = open("settings", 'rb')
        except FileNotFoundError:
            self.colorNames = ["White", "Red", "Green", "Orange", "Blue", "Yellow"]
            self.colorCodes = ["FFFFFF","FF0000", "00FF00", "FFAA00", "0000FF", "FFFF00"]
            self.manualTurnTime = 0.5
            self.solutionTurnTime = 1.0
            self.turnTime = 0.5
            self.saveSettings()
            return
        settingsList = pickle.load(f)
        self.colorNames = settingsList[0]
        self.colorCodes = settingsList[1]
        self.manualTurnTime = settingsList[2]
        self.solutionTurnTime = settingsList[3]
        self.turnTime = self.manualTurnTime


    def saveSettings(self):
        #updates 'settings' file with current variable values that should be saved between sessions
        settingsList = [self.colorNames, self.colorCodes, self.manualTurnTime, self.solutionTurnTime]
        f = open('settings','wb')
        pickle.dump(settingsList,f)

    def changeBrushButton(self, b):
        #Event bind for buttons on paint screen. Takes a button object and searches saved colors to update the currently selected color value.
        i = 0
        while b.background != self.colors[i]:
            i += 1
            if i == 6:
                raise Exception("color logic error")
                exit()
        self.activeWidgets[1].selected = self.colorNames[i]
        self.changeBrushColor(self.activeWidgets[1])

    def setWidgetMode(self, mode):
        #Takes an integer specifying what widgets to display below the primary view
        #0 : Regular
        #1: Paint
        #2: Settings
        #3: Color Settings
        #4: Solution Mode
        #5: Loading solution...
        #6: Solution Error
        if mode == 3 or mode == 4:
            self.scene.unbind('keydown',self.onKey)
        if mode == 2 and self.mode == 3:
            self.scene.bind('keydown',self.onKey)
        if mode == 0 and self.mode == 4:
            self.scene.bind('keydown',self.onKey)
        self.mode = mode
        for widget in self.activeWidgets:
            widget.delete()
        self.scene.caption = ""
        self.activeWidgets = []
        if mode == 0: #regular
            self.turnTime = self.manualTurnTime
            self.updateRotateTime()
            self.activeWidgets.append(button(bind=self.reset, text="New cube"))
            self.activeWidgets.append(button(bind=self.scramble, text = "Scramble"))
            self.activeWidgets.append(button(bind=self.solve, text = "Solve")) 
            self.activeWidgets.append(button(bind=self.paintMode, text = "Paint"))
            self.activeWidgets.append(button(bind=self.openSettings, text = "Settings"))
            
            self.activeWidgets.append(wtext(text='\n'))
            self.activeWidgets.append(button(bind=self.undo, text = "Undo"))
            self.activeWidgets.append(button(bind=self.redo, text = "Redo"))
            self.activeWidgets.append(wtext(text='\n Controls:\n(U)p      (D)own\n(L)eft    (R)ight\n(F)ront   (B)ack\nHold Shift to rotate counter-clockwise'))

        if mode == 1: #paint
            self.activeWidgets.append(button(bind=self.normalMode, text = "Back"))
            self.activeWidgets.append(menu(choices = self.colorNames, bind = self.changeBrushColor))
            self.activeWidgets.append(wtext(text='\n'))
            self.activeWidgets.append(button(text='       \n ', background = self.colors[0], bind = self.changeBrushButton))
            self.activeWidgets.append(button(text='       \n ', background = self.colors[1], bind = self.changeBrushButton))
            self.activeWidgets.append(button(text='       \n ', background = self.colors[2], bind = self.changeBrushButton))
            self.activeWidgets.append(wtext(text='\n'))
            self.activeWidgets.append(button(text='       \n ', background = self.colors[5], bind = self.changeBrushButton))
            self.activeWidgets.append(button(text='       \n ', background = self.colors[3], bind = self.changeBrushButton))
            self.activeWidgets.append(button(text='       \n ', background = self.colors[4], bind = self.changeBrushButton))
            self.activeWidgets.append(wtext(text='\nOnly edges and corners can be painted. Make sure to color in respect to center pieces.'))
        if mode == 2: #settings
            self.activeWidgets.append(button(bind=self.normalMode, text = "Back"))
            self.activeWidgets.append(wtext(text = "\n"))
            self.activeWidgets.append(button(bind=self.colorSettings, text = "Change color scheme"))
            self.activeWidgets.append(wtext(text = "\nManual turn time: "))
            self.activeWidgets.append(slider(min = 0.2, max = 2.0, step = 0.01, value = self.manualTurnTime, bind = self.updateManualTime))
            self.activeWidgets.append(wtext(text = "\nAutomatic turn time: "))
            self.activeWidgets.append(slider(min = 0.2, max = 2.0, step = 0.01, value = self.solutionTurnTime, bind = self.updateSolutionTime))
            self.activeWidgets.append(wtext(text = '\n                                <--Faster--                             --Slower-->'))
        if mode == 3: #color settings
            self.activeWidgets.append(button(bind=self.openSettings, text = "Back"))
            self.activeWidgets.append(wtext(text = "\n Side | Color Name | Color Hex Code"))
            self.activeWidgets.append(wtext(text = "\n Up: "))
            self.activeWidgets.append(winput(text = self.colorNames[0], bind = self.updateColor, type = "string"))
            self.activeWidgets.append(winput(text = self.colorCodes[0], bind = self.updateColor, type = "string"))
            self.activeWidgets.append(wtext(text = "\n Down: "))
            self.activeWidgets.append(winput(text = self.colorNames[5], bind = self.updateColor, type = "string"))
            self.activeWidgets.append(winput(text = self.colorCodes[5], bind = self.updateColor, type = "string"))
            self.activeWidgets.append(wtext(text = "\n Front: "))
            self.activeWidgets.append(winput(text = self.colorNames[1], bind = self.updateColor, type = "string"))
            self.activeWidgets.append(winput(text = self.colorCodes[1], bind = self.updateColor, type = "string"))
            self.activeWidgets.append(wtext(text = "\n Back: "))
            self.activeWidgets.append(winput(text = self.colorNames[3], bind = self.updateColor, type = "string"))
            self.activeWidgets.append(winput(text = self.colorCodes[3], bind = self.updateColor, type = "string"))
            self.activeWidgets.append(wtext(text = "\n Left: "))
            self.activeWidgets.append(winput(text = self.colorNames[2], bind = self.updateColor, type = "string"))
            self.activeWidgets.append(winput(text = self.colorCodes[2], bind = self.updateColor, type = "string"))
            self.activeWidgets.append(wtext(text = "\n Right: "))
            self.activeWidgets.append(winput(text = self.colorNames[4], bind = self.updateColor, type = "string"))
            self.activeWidgets.append(winput(text = self.colorCodes[4], bind = self.updateColor, type = "string"))
            self.activeWidgets.append(wtext(text = '\n'))
            self.activeWidgets.append(button(text = "Reset to Default", bind = self.defaultColors))
        if mode == 4: #Solution mode
            self.turnTime = self.solutionTurnTime
            self.updateRotateTime()
            self.activeWidgets.append(button(bind=self.normalMode, text = "Back"))
            self.activeWidgets.append(wtext(text = self.generateSolutionString()))
            self.activeWidgets.append(button(text="<--", bind=self.moveLeft))
            self.activeWidgets.append(button(text="-->", bind=self.moveRight))
            self.activeWidgets.append(wtext(text = "\n"))
            self.activeWidgets.append(button(text="???", bind = self.autoIncrement))
            self.activeWidgets.append(wtext(text = '\n'))
            self.activeWidgets.append(slider(min = 0.2, max = 2.0, step = 0.01, value = self.turnTime, bind = self.updateSolutionTime))
            self.activeWidgets.append(wtext(text = '\n   <--Faster--                                --Slower-->'))
        if mode == 5: #loading
            self.activeWidgets.append(wtext(text = 'Generating solution...'))
        if mode == 6: #solve error
            self.activeWidgets.append(wtext(text = 'The inputted cube is considered unsolvable. Please fix any errors in paint mode before solving.\n'))
            self.activeWidgets.append(button(text = 'Back', bind = self.normalMode))
            self.activeWidgets.append(button(text = 'Paint', bind = self.paintMode))

    def undo(self, b):
        #Undoes the last manual move
        if len(self.undoList) == 0:
            return
        moveToUndo = self.undoList.pop()
        self.redoList.append(moveToUndo)
        if moveToUndo.islower():
            backMove = moveToUndo.upper()
        else:
            backMove = moveToUndo.lower()
        self.cube3d.rotate(backMove)

    def redo(self, b):
        #Redoes the last manual move
        if len(self.redoList) == 0:
            return
        moveToRedo = self.redoList.pop()
        self.undoList.append(moveToRedo)
        self.cube3d.rotate(moveToRedo)

    def updateSolutionTime(self, s):
        #Updates solution mode rotate time based off slider value.
        self.solutionTurnTime = s.value
        if self.mode == 4:
            self.turnTime = self.solutionTurnTime
            self.updateRotateTime()
    
    def updateManualTime(self, s):
        #Updates manual mode rotate time based off slider value
        self.manualTurnTime = s.value

    def updateRotateTime(self):
        #Sends rotate time update to cube.
        self.cube3d.updateRotateTime(self.turnTime)
    
    def defaultColors(self, b):
        #Sets colors to default and saves settings.
        self.colorNames = ["White", "Red", "Green", "Orange", "Blue", "Yellow"]
        self.colorCodes = ["FFFFFF","FF0000", "00FF00", "FFAA00", "0000FF", "FFFF00"]
        self.saveSettings()
        self.updateCubeColor()
        self.setWidgetMode(2) #Reload color settings to update values
        self.setWidgetMode(3)
    
    def generateSolutionString(self):
        #Takes the current solution, which is a list of moves as well as the current index and outputs a string for use in VPython widget. No input, returns string
        outStr = "\n"
        s = ['>>'] + self.solution
        index = self.solutionIndex
        for i in range(len(s)):
            if i == index:
                outStr += "<b>"
            move = s[i]
            if s[i].islower() or s[i] == ">>":
                outStr += s[i].upper()
            else:
                outStr += s[i] + "'"
            if i == index:
                outStr += "</b>"
            outStr += " "
        outStr += "\n"
        return outStr


    def moveLeft(self, b):
        #Iterates the current solution left one in solution mode, no input or output
        if self.solutionIndex > 0:
            self.moveQueue += 1
            if self.moveQueue > 1:
                return
            self.activeWidgets[0].disabled = True
            self.activeWidgets[3].disabled = True
            self.activeWidgets[5].disabled = True
            while self.moveQueue > 0:
                move = self.solution[self.solutionIndex-1]
                if len(move) == 2:
                    backmove = move
                elif move.isupper():
                    backmove = move.lower()
                else:
                    backmove = move.upper()
                self.solutionIndex -= 1
                self.activeWidgets[1].text = self.generateSolutionString()
                self.cube3d.rotate(backmove)
                self.moveQueue -= 1
            self.activeWidgets[0].disabled = False
            self.activeWidgets[3].disabled = False
            self.activeWidgets[5].disabled = False

    def moveRight(self, b):
        #Iterates the current solution right one in solution mode, no input or output
        if self.solutionIndex + self.moveQueue < len(self.solution):
            self.moveQueue += 1
            if self.moveQueue > 1:
                return
            self.activeWidgets[0].disabled = True
            self.activeWidgets[2].disabled = True
            while self.moveQueue > 0:
                self.solutionIndex += 1
                self.activeWidgets[1].text = self.generateSolutionString()
                self.cube3d.rotate(self.solution[self.solutionIndex-1])
                self.moveQueue -= 1
            self.activeWidgets[0].disabled = False
            self.activeWidgets[2].disabled = False

    def autoIncrement(self, b):
        #Automatically increments solution mode to the right.
        if b.text == "||":
            b.text = '???'
            self.autoPlaying = False
            return
        self.activeWidgets[0].disabled = True
        b.text = "||"
        self.autoPlaying = True
        while(self.autoPlaying):
            self.moveRight(None)
            if self.solutionIndex == len(self.solution):
                b.text = '???'
                self.autoPlaying = False
        self.activeWidgets[0].disabled = False


    def updateColor(self, i):
        #Bound function that takes widget i (a widget in color settings), determines which cube face and setting the widget belongs to, and updates settings accordingly
        count = 0
        for widget in self.activeWidgets:
            if type(widget) == type(self.activeWidgets[3]):
                count += 1
            if widget == i:
                break
        colorMap = {0:0,1:5,2:1,3:3,4:2,5:4} #some interfacing between UD FB LR that makes sense for settings vs UFL BRD that applies to Cube3D colors input
        if count %2 == 1: #name
            self.colorNames[colorMap[(count-1)//2]] = i.text
        else:#code
            if self.verifyCode(i.text):
                self.colorCodes[colorMap[(count-1)//2]] = i.text
                self.updateCubeColor()
        self.saveSettings()

    def verifyCode(self, text):
        #Checks if its a valid RGB hexcode (6 digit hex)
        if len(text) != 6:
            return False
        for char in text.lower():
            if char not in ['a','b','c','d','e','f','1','2','3','4','5','6','7','8','9','0']:
                return False
        return True


    def updateCubeColor(self):
        #Sends updated colors to 3dCube object, updating display to match settings. No input or direct output.
        colorList = []
        for code in self.colorCodes:
            v = []
            for i in range(3):  
                subStr = code[i*2 : i*2+2].lower()
                hexInt = int(subStr,16)
                hexFloat = float(hexInt)/255
                v.append(hexFloat)
            colorList.append(vector(v[0], v[1], v[2]))

        self.colors = colorList
        self.cube3d.updateColors(self.colors)


    #def updateTurnSpeed(self, s):
    #    self.cube3d.updateRotateTime(s.value)
    #    self.turnTime = s.value

    def changeBrushColor(self, m):
        #Bound function to menu widget in color settings. Changes the brush color from the drop-down menu in settings.
        index = self.colorNames.index(m.selected)
        self.brushColor = {0:'u', 1:'f', 2:'l', 3:'b', 4:'r', 5:'d'}[index]

    def colorSettings(self, b):
        #Bound function to button. Chnages display to color settings.
        self.setWidgetMode(3)

    def normalMode(self, b):
        #Bound function to button. Chnages display to normal mode.
        self.setWidgetMode(0)

    def openSettings(self, b):
        #Bound function to button. Chnages display to Settings.
        self.setWidgetMode(2)

    def paintMode(self, b):
        #Bound function to button. Chnages display to paint mode
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

    def scramble(self, b):
        #Generates a scramble list and scrambles the current 3d cube.
        scrambleList = self.generateScramble()
        print(scrambleList)
        self.turnTime = 0.2
        self.updateRotateTime()
        b.enabled = False
        self.scene.unbind('keydown', self.onKey)
        for move in scrambleList:
            self.cube3d.rotate(move)
        self.turnTime = self.manualTurnTime
        self.updateRotateTime()
        b.enabled = True
        self.scene.bind('keydown', self.onKey)

    def reset(self):
        #Destroys the current cube and creates a new one
        self.cube3d.destroy()
        self.cube3d = Cube3D(self.colors)
        self.cube3d.updateRotateTime(self.turnTime)
        self.cubeRepr = Cube()
        self.undoList = []
        self.redoList = []

    def solve(self):
        #Bound function to button. Updates widget display and activates cube solver.
            self.setWidgetMode(5)
            self.solutionIndex = 0
            cubeRepr = self.cube3d.toCube()
            self.solution = CubeSolver.solve(cubeRepr) #This line should take several seconds
            if self.solution == False:
                self.setWidgetMode(6)
                return
            self.setWidgetMode(4)

    def onKey(self, evt):
        #Called by keypress event listener to determine keyboard input
        #print(evt.__dict__)
        self.keyQueue.append(evt)
        if len(self.keyQueue) > 1:
            return
        #self.scene.unbind('keydown',self.onKey)
        while len(self.keyQueue) > 0:
            key = self.keyQueue[0].key
            if key.lower() in ['f','b','l','r','u','d']:
                self.redoList = []
                self.undoList.append(key)
                self.cube3d.rotate(key)
            self.keyQueue.pop(0)
        #self.scene.bind('keydown',self.onKey)

    def onClick(self, evt):
        obj = self.scene.mouse.pick
        if self.mode == 1:
            self.cube3d.updateStickerColor(obj, self.brushColor)


    def onMouseDown(self, evt):
        #Unused function for mouse down event
        return
        if self.mode == 0:
            self.item = self.scene.mouse.pick
            if self.item != None:
                #TODO check if its a sticker
                self.moveCount = 0
                self.startPosition = evt.pos

    def onMouseUp(self, evt):
        #print(evt.__dict__)
        pass

    def onMouseMove(self, evt):
        #unused function for mouse move event
        return
        if self.mode == 0:
            self.moveCount += 1
            if self.moveCount == 5:
                endPosition = evt.pos
                movement = endPosition - self.startPosition
                move = self.cube3d.mouseMove(self.item, movement)
                if move != None:
                    self.undoList.append(move)
        #print(evt.__dict__)
        pass
        
controller = Controller()
