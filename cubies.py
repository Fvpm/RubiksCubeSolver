from vpython import *
from cubeRepr import *

        

class Cube3D(object):
    #This object represents the Cube object in the VPython scene and controls it. the destroy() method should be called before a new Cube3D is created.
    faceEdgesDict = {'u':[0,1,2,3], 'l':[1,4,5,9], 'f':[0,4,7,8], 'd':[8,9,10,11], 'r':[3,6,7,11], 'b':[2,5,6,10]}
    faceCornersDict = { 'u':[0,1,2,3], 'l':[0,1,4,5], 'f':[0,2,4,6], 'd':[4,5,6,7],'r':[2,3,6,7], 'b':[1,3,5,7]}
    faceCentersDict = { 'u':[0], 'f':[1], 'l':[2], 'b':[3], 'r':[4], 'd':[5] }
    axisDict = { 'u':vector(0,-1,0), 'l':vector(1,0,0), 'f': vector(0,0,-1), 'd':vector(0,1,0), 'r':vector(-1,0,0), 'b':vector(0,0,1) }

    
    def __init__(self, colors = None):
        if colors:
            self.colors = colors
        else:
            self.colors = [color.white, color.red, color.green, color.orange, color.blue, color.yellow]
        self.centers = []
        self.edges = []
        self.corners = []
        
        self.rotateTime = .33

        for i in range(0,6):
            self.centers.append(Center3D(i,self.colors))
        for i in range(0,12):
            self.edges.append(Edge3D(i,self.colors))
        for i in range(0,8):
            self.corners.append(Corner3D(i,self.colors))

    def mouseMove(self, vobject, movement):
        for corner in self.corners:
            if vobject in corner.stickers:
                upVectors = [0]*6
                moves = ['u','f','l','b','r','d']
                for center in self.centers:
                    upVectors[center.position] = center.stickers[0].up
                print(upVectors)
                print(corner.stickers)
                sideGetters = []
                for sticker in corner.stickers:
                    if sticker != vobject:
                        sideGetters.append(sticker)
                potentialMoves = []
                print(sideGetters)
                for i in range(6):
                    for sticker in sideGetters:
                        if sticker.up.norm().equals(upVectors[i].norm()):
                            potentialMoves.append(i)
                print("potential moves " + str(potentialMoves))
                firstStrength = movement.proj(upVectors[potentialMoves[0]])
                secondStrength = movement.proj(upVectors[potentialMoves[1]])
                firstMag = mag(firstStrength)
                if firstStrength.norm().equals(upVectors[potentialMoves[0]].norm()) == False:
                    firstMag *= -1
                secondMag = mag(secondStrength)
                if secondStrength.norm().equals(upVectors[potentialMoves[1]].norm()) == False:
                    secondMag *= -1
                if abs(firstMag) > abs(secondMag):
                    if firstMag > 0: 
                        if corner.faces.index(potentialMoves[0]) +1 %3 == corner.faces.index(potentialMoves[1]):
                            #its the clockwise turn
                            self.rotate(moves[potentialMoves[1]])
                            return moves[potentialMoves[1]]
                        else: #counterclockwise
                            self.rotate(moves[potentialMoves[1]].upper())
                            return moves[potentialMoves[1]].upper()
                    else:
                        if corner.faces.index(potentialMoves[0]) +1 %3 == corner.faces.index(potentialMoves[1]):
                            self.rotate(moves[potentialMoves[1]].upper())
                            return moves[potentialMoves[1]].upper()
                        else: 
                            self.rotate(moves[potentialMoves[1]])
                            return moves[potentialMoves[1]]
                else:
                    if secondMag > 0: 
                        if corner.faces.index(potentialMoves[1]) +1 %3 == corner.faces.index(potentialMoves[0]):
                            #its the clockwise turn
                            self.rotate(moves[potentialMoves[0]])
                            return moves[potentialMoves[0]]
                        else: #counterclockwise
                            self.rotate(moves[potentialMoves[0]].upper())
                            return moves[potentialMoves[0]].upper()
                    else:
                        if corner.faces.index(potentialMoves[1]) +1 %3 == corner.faces.index(potentialMoves[0]):
                            #its the clockwise turn
                            self.rotate(moves[potentialMoves[0]].upper())
                            return moves[potentialMoves[0]].upper()
                        else: #counterclockwise
                            self.rotate(moves[potentialMoves[0]])
                            return moves[potentialMoves[0]]
                raise Exception("Mouse click move error")
                    

                        

                    
                return
        for edge in self.edges:
            if vobject in edge.stickers:
                
                return
        return None

    def updateColors(self, newColors):
        for cubie in self.centers + self.edges + self.corners:
            cubie.updateColors(newColors)


    def updateRotateTime(self, newTime):
        self.rotateTime = newTime

    def updateStickerColor(self, vbox, newFace):
        theCubie = None
        for cubie in self.centers + self.edges + self.corners:
            if vbox in cubie.stickers:
                theCubie = cubie
                break
        theCubie.updateStickerColor(vbox, newFace[0])


    def rotate(self, face):
    #Takes one of 18 move values [u,d,l,r,f,b,U,u2,d,D2,l.. etc] and rotates the appropriate vpython objects, and updates position and orienation values of cubies.
    #This function takes time, and can lead to errors if interrupted by an event
        angle = pi/2
        if face.isupper():
            angle = -angle
        moveTwice = False
        if len(face) == 2:
            angle *= 2
            face = face[0]
            moveTwice = True
        
        rotatePieces = []
        edgePositions = self.faceEdgesDict[face.lower()]
        cornerPositions = self.faceCornersDict[face.lower()]
        centerPositions = self.faceCentersDict[face.lower()]
        axis = self.axisDict[face.lower()]
        for center in self.centers:
            if center.getPosition() in centerPositions:
                rotatePieces.append(center)
        for edge in self.edges:
            if edge.getPosition() in edgePositions:
                rotatePieces.append(edge)
        for corner in self.corners:
            if corner.getPosition() in cornerPositions:
                rotatePieces.append(corner)

        fps = 24
        time = 1.0/self.rotateTime
        for cubie in rotatePieces:
            cubie.updatePosition(face)
            if moveTwice:
                cubie.updatePosition(face)
        for i in range(0, fps):
            rate(fps * time)
            for cubie in rotatePieces:
                cubie.rotate(axis, angle/fps)

    def toCube(self):
        #creates and returns an instance of Cube class with sticker positions equal to the Cube3D's stickers.

        #generate stickers
        #mapping positions of cubies to indeces of their 3 stickers, starting with orientation 0
        cornerIMap = { 0 : [6,32,18], 1 : [0,16,42], 2: [4,24,34], 3: [2,40,26],
                       4 : [8,20,38], 5 : [14,44,22],6: [10,36,30],7: [12,28,46]}
        #elsewhere in this program I tend to put these "maps" in class code, but toCube() is basically only used when the user is entering solve mode, and even then i's only once. I don't want to clutter class variables if I don't have to.
        #27, 34
        edgeIMap = { 0: [5,33], 1:[7,17], 2:[1,41], 3:[3,25],
                     4: [39,19], 5:[43,23],6:[47,27], 7:[35,31],
                     8: [9,37], 9:[15,21], 10:[13,45], 11:[11,29]}
        faceMap = {0:'u', 1:'f', 2:'l', 3:'b', 4:'r', 5:'d'}
        stickers = [0] * 48
        for corner in self.corners:
            pos = corner.getPosition()
            ori = corner.getOrientation()
            indexes = cornerIMap[pos]
            colorsInt = corner.getFaces()
            colorsStr = [faceMap[x] for x in colorsInt]
            for i in range(3):
                stickers[indexes[i]] = colorsStr[(i + ori) % 3]
        
        for edge in self.edges:
            pos = edge.getPosition()
            ori = edge.getOrientation()
            indexes = edgeIMap[pos]
            colorsInt = edge.getFaces()
            colorsStr = [faceMap[x] for x in colorsInt]
            for i in range(2):
                stickers[indexes[i]] = colorsStr[(i + ori) % 2]

        newCube = Cube(stickers)
        return newCube

    def destroy(self):
        #Makes all the vpython pieces invisible and deletes them.
        for piece in self.edges + self.corners + self.centers: #I need to figure out if this is like dangerously inefficient.
            piece.destroy()


class Cubie3D(object):
    #Parent class of Edge3D, Corner3D, and Center3D housing functions that are generic for any of them.
    def __init__(self, _position):
        self.base = box()
        self.stickers = []
        self.position = _position
        self.orientation = 0
        self.colorVals = []

    def rotate(self, _axis, _angle):
        #rotates the piece around _axis by _angle. This is done instantaneously, so should be called many times for a smooth animation
        for x in self.stickers:
            x.rotate(angle = _angle, axis = _axis, origin = vector(0,0,0))
        self.base.rotate(angle = _angle, axis = _axis, origin = vector(0,0,0))

    def destroy(self):
        #Deletes pieces within the capacity of VPython.
        self.base.visible = False
        for piece in self.stickers:
            piece.visible = False
            del piece
        del self.base

    def updateColors(self, newColors):
        for sticker in self.stickers:
            for color in self.colorVals:
                if sticker.color == color:
                    sticker.color = newColors[self.colorVals.index(color)]
        self.colorVals = newColors
        

    def getPosition(self):
        return self.position

    def getOrientation(self):
        return self.orientation



class Center3D(Cubie3D):
    #This is the class controlling one of the 6 center cubies

    positionDict = { 0 : vector(0,1,0), 1 : vector(0,0,1), 2 : vector(-1,0,0), 3 : vector(0,0,-1), 4: vector(1,0,0), 5: vector(0,-1,0) }

    def __init__(self, position, colors):
        #Position is a value 0 to 5 and colors is an array of VPython colors corresponding to those side's colors.
        #0U 1F 2L 3B 4R 5D
        super().__init__(position)
        basePos = self.positionDict[position]
        self.colorVals = colors
        self.colors = [position]
        self.base = box(pos = basePos, size = vector(0.95,0.95,0.95),  color = color.black)
        sticker = box(pos = basePos * 1.5, size = vector(0.9, 0.05, 0.9), color = colors[position], up = basePos)
        self.stickers.append(sticker)

    def updateStickerColor(self, vbox, face):
        #input vbox, "f"
        return
        sideIndex = {'u':0,'f':1,'l':2,'b':3,'r':4,'d':5}[face]
        index = 0
        while True:
            if self.stickers[index] == vbox:
                break
            index += 1
        vbox.color = self.colorVals[sideIndex]
        self.colors[index] = sideIndex


    def updatePosition(self, move):
        #Updates the cubie based off the move applied to it
        if move in ['f','u','d','b','l','r']:
            return
        #TODO add full cube rotations




class Edge3D(Cubie3D):

    #Useful variables: stickerInfoDict, vectorDict, edgeUpdateMap
    #useless variables: clockwiseUpdates, counterUpdates
    stickerInfoDict = { 0 : [0,1], 1 : [0,2], 2 : [0,3], 3: [0,4],
                        4 : [1,2], 5 : [3,2], 6 : [3,4], 7: [1,4],
                        8 : [5,1], 9 : [5,2], 10: [5,3],11: [5,4]}

    vectorDict = { 0 : vector(0,1,0), 1 : vector(0,0,1), 2 : vector(-1,0,0), 3 : vector(0,0,-1), 4: vector(1,0,0), 5: vector(0,-1,0) }
    clockwiseUpdates = { 'u' : {0:1,1:2,2:3,3:0},
                        'd' : {8:11,11:10,10:9,9:8},
                        'l' : {1:4,4:9,9:5,5:1},
                        'r' : {3:6,6:11,11:7,7:3},
                        'f' : {0:7,7:8,8:4,4:0},
                        'b' : {2:5,5:10,10:6,6:2}}
    counterUpdates = dict()
    for (k1,v1) in clockwiseUpdates.items():
        counterUpdates[k1.upper()] = dict((v2,k2) for k2, v2 in v1.items())
    edgeUpdateMap = dict(counterUpdates)
    edgeUpdateMap.update(clockwiseUpdates)


    def __init__(self, position, colors):
        #0UF 1UL 2UB 3 UR 4FL 5BL 6BR 7FR 8DF 9DF 10DB 11DR
        super().__init__(position)
        self.orientation = 0

        faces = self.stickerInfoDict[position]
        basePos = self.vectorDict[faces[0]] + self.vectorDict[faces[1]] 

        self.colorVals = colors
        self.colors = faces.copy()
        self.base = box(pos = basePos, size = vector(0.95,0.95,0.95), color = color.black)

        for faceNum in faces:
            facePos = self.vectorDict[faceNum] * 0.5 + basePos
            newSticker = box(pos = facePos, up = self.vectorDict[faceNum], size = vector(0.9, 0.05, 0.9), color = colors[faceNum])
            self.stickers.append(newSticker)


    def updateStickerColor(self, vbox, face):
        #input vbox, "f"
        sideIndex = {'u':0,'f':1,'l':2,'b':3,'r':4,'d':5}[face]
        index = 0
        while True:
            if self.stickers[index] == vbox:
                break
            index += 1
        vbox.color = self.colorVals[sideIndex]
        self.colors[index] = sideIndex



    def updatePosition(self,face):
        #Updates the cubie based off the move applied to it
        self.position = self.edgeUpdateMap[face][self.position]
        if face[0].lower() in ['f','b']:
            self.orientation = (self.orientation + 1) % 2

    def getFaces(self):
        return self.colors
            

    

class Corner3D(Cubie3D):
    stickerInfoDict = { 0 : [0,1,2], 1 : [0,3,2], 2: [0,1,4], 3: [0,3,4],
                        4 : [5,1,2], 5 : [5,3,2], 6: [5,1,4], 7: [5,3,4]}
    faceInfoDict = { 0: [0,1,2], 1: [0,2,3], 2: [0,4,1], 3: [0,3,4],
                     4: [5,2,1], 5:[5,3,2], 6:[5,1,4], 7: [5,4,3]}
    vectorDict = { 0 : vector(0,1,0), 1 : vector(0,0,1), 2 : vector(-1,0,0), 3 : vector(0,0,-1), 4: vector(1,0,0), 5: vector(0,-1,0) }
    #Tohelp make cornerUpdateMap
    clockwiseUpdates = { 'u' : {0:1,1:3,3:2,2:0},
                          'd' : {4:6,6:7,7:5,5:4},
                          'l' : {1:0,0:4,4:5,5:1},
                          'r' : {2:3,3:7,7:6,6:2},
                          'f' : {0:2,2:6,6:4,4:0},
                          'b' : {3:1,1:5,5:7,7:3}}
    
    orientationAdditions = { 'l' : {1:2,0:1,4:2,5:1},
                             'r' : {2:2,3:1,7:2,6:1},
                             'f' : {0:2,2:1,6:2,4:1},
                             'b' : {3:2,1:1,5:2,7:1}}

    counterUpdates = dict()
    for (k1,v1) in clockwiseUpdates.items():
        counterUpdates[k1.upper()] = dict((v2,k2) for k2, v2 in v1.items())
    cornerUpdateMap = dict(counterUpdates)
    cornerUpdateMap.update(clockwiseUpdates)

    def __init__(self, position, colors):
        #0UFL 1UBL 2UFR 3UBR 4FL 5DBL 6DFR 7DBR
        super().__init__(position)
        self.orientation = 0

        faces = self.faceInfoDict[position]
        self.faces = faces.copy()
        basePos = self.vectorDict[faces[0]] + self.vectorDict[faces[1]] + self.vectorDict[faces[2]]

        self.colorVals = colors
        self.colors = faces.copy()
        self.base = box(pos = basePos, size = vector(0.95,0.95,0.95), color = color.black)

        for faceNum in faces:
            facePos = self.vectorDict[faceNum] * 0.5 + basePos
            newSticker = box(pos = facePos, up = self.vectorDict[faceNum], size = vector(0.9, 0.05, 0.9), color = colors[faceNum])
            self.stickers.append(newSticker)

    def updateStickerColor(self, vbox, face):
        #input vbox, "f"
        sideIndex = {'u':0,'f':1,'l':2,'b':3,'r':4,'d':5}[face]
        index = 0
        while True:
            if self.stickers[index] == vbox:
                break
            index += 1
        vbox.color = self.colorVals[sideIndex]
        self.colors[index] = sideIndex
            
    def updatePosition(self,face):
        if len(face) == 1 and face.lower() in ['l','r','f','b']:
            self.orientation += self.orientationAdditions[face.lower()][self.position] % 3
        self.position = self.cornerUpdateMap[face][self.position]

    def getFaces(self):
        return self.colors
        
