from vpython import *
import random



class Cube(object):
    turnMaps = {'u':[(0,2),(2,4),(4,6),(6,0),(1,3),(3,5),(5,7),(7,1),
                          (32,16),(16,40),(40,24),(24,32),(33,17),(34,18),(17,41),(18,42),(41,25),(42,26),(25,33),(26,34)],
                     'd':[(8,10),(10,12),(12,14),(14,8),(9,11),(11,13),(13,15),(15,9),
                          (38,30),(30,46),(46,22),(22,38),(37,29),(29,45),(45,21),(21,37),(36,28),(28,44),(44,20),(20,36)],
                     'l':[(16,18),(18,20),(20,22),(22,16),(17,19),(19,21),(21,23),(23,17),
                          (0,32),(32,8),(8,44),(44,0),(7,39),(39,15),(15,43),(43,7),(6,38),(38,14),(14,42),(42,6)],
                     'r':[(24,26),(26,28),(28,30),(30,24),(25,27),(27,29),(29,31),(31,25),
                          (4,40),(40,12),(12,36),(36,4),(3,47),(47,11),(11,35),(35,3),(2,46),(46,10),(10,34),(34,2)],
                     'f':[(32,34),(34,36),(36,38),(38,32),(33,35),(35,37),(37,39),(39,33),
                          (18,4),(4,30),(30,8),(8,18),(19,5),(5,31),(31,9),(9,18),(20,6),(6,24),(24,10),(10,20)],
                     'b':[(40,42),(42,44),(44,46),(46,40),(41,43),(43,45),(45,47),(47,41),
                          (2,16),(16,14),(14,28),(28,2),(1,23),(23,13),(13,27),(27,1),(0,22),(22,12),(12,26),(26,0)]}
    reverseMaps = dict()
    for k,v in turnMaps.items():
        reverseMaps[k.upper()] = [(i[1],i[0]) for i in v]

    doubleTurns = dict()
    for k,v in turnMaps.items():
        tempDict = dict()
        for item in v:
            tempDict[item[0]] = item[1]
        oldtempDict = dict(tempDict)
        for k2,v2 in tempDict.items():
            tempDict[k2] = oldtempDict[v2]
        doubleTurns[k + "2"] = [(k,v) for k,v in tempDict.items()]
    turnMaps.update(doubleTurns)
    turnMaps.update(reverseMaps)

    def __init__(self):
        #up down left right front back
        self.stickers = []
        for face in ['u','d','l','r','f','b']:
            for i in range(8):
                self.stickers.append(face)
                
    def move(self,face):
        moveMap = self.turnMaps[face]
        newStickers = self.stickers.copy()
        for t in moveMap:
            newStickers[t[1]] = self.stickers[t[0]]
        self.stickers = newStickers

    def setStickers(self, newStickers):
        if len(newStickers) != 48:
            print("ERROR newStickers wrong length 49")
        self.stickers = newStickers

class Cube3D(object):
    faceEdgesDict = {'u':[0,1,2,3], 'l':[1,4,5,9], 'f':[0,4,7,8], 'd':[8,9,10,11], 'r':[3,6,7,11], 'b':[2,5,6,10]}
    faceCornersDict = { 'u':[0,1,2,3], 'l':[0,1,4,5], 'f':[0,2,4,6], 'd':[4,5,6,7],'r':[2,3,6,7], 'b':[1,3,5,7]}
    faceCentersDict = { 'u':[0], 'f':[1], 'l':[2], 'b':[3], 'r':[4], 'd':[5] }
    axisDict = { 'u':vector(0,-1,0), 'l':vector(1,0,0), 'f': vector(0,0,-1), 'd':vector(0,1,0), 'r':vector(-1,0,0), 'b':vector(0,0,1) }

    def __init__(self):
        self.colors = [color.white, color.red, color.green, color.orange, color.blue, color.yellow]
        self.centers = []
        self.edges = []
        self.corners = []

        for i in range(0,6):
            self.centers.append(Center3D(i,self.colors))
        for i in range(0,12):
            self.edges.append(Edge3D(i,self.colors))
        for i in range(0,8):
            self.corners.append(Corner3D(i,self.colors))


    def rotate(self, face):
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
        for cubie in rotatePieces:
            cubie.updatePosition(face)
            if moveTwice:
                cubie.updatePosition(face)
        for i in range(0, fps):
            rate(fps*2)
            for cubie in rotatePieces:
                cubie.rotate(axis, angle/fps)

    def toCube(self):
        #generate stickers
        #mapping positions of cubies to indeces of their 3 stickers, starting with orientation 0
        cornerIMap = { 0 : [6,32,18], 1 : [0,16,42], 2: [4,24,32], 3: [2,40,26],
                       4 : [8,20,38], 5 : [14,44,22],6: [10,36,30],7: [12,28,46]}
        edgeIMap = { 0: [5,33], 1:[7,17], 2:[1,41], 3:[3,25],
                     4: [39,19], 5:[43,23],6:[47,23], 7:[35,31],
                     8: [9,37], 9:[15,21], 10:[13,45], 11:[11,29]}
        faceMap = {0:'u', 1:'d', 2:'l', 3:'r', 4:'f', 5:'b'}
        stickers = [0] * 48
        for corner in corners:
            pos = corner.getPosition()
            ori = corner.getOrientation()
            indexes = cornerIMap[pos]
            colorsInt = corner.getFaces()
            colorsStr = [faceMap[x] for x in colorsInt]
            for i in range(3):
                stickers[indexes[i]] = colorsStr[(i + ori) % 3]
        
        for edge in edges:
            pos = edge.getPosition()
            ori = edge.getOrientation()
            indexes = edgeIMap[pos]
            colorsInt = edge.getFaces()
            colorsStr = [faceMap[x] for x in colorsInt]
            for i in range(2):
                stickers[indexes[i]] = colorsStr[(i + ori) % 2]

        newCube = Cube()
        newCube.setStickers(stickers)
        return newCube


class Cubie3D(object):
    def __init__(self, _position):
        self.base = box()
        self.stickers = []
        self.position = _position
        self.orientation = 0

    def rotate(self, _axis, _angle):
        for x in self.stickers:
            x.rotate(angle = _angle, axis = _axis, origin = vector(0,0,0))
        self.base.rotate(angle = _angle, axis = _axis, origin = vector(0,0,0))


    def getPosition(self):
        return self.position

    def getOrientation(self):
        return self.orientation



class Center3D(Cubie3D):
    positionDict = { 0 : vector(0,1,0), 1 : vector(0,0,1), 2 : vector(-1,0,0), 3 : vector(0,0,-1), 4: vector(1,0,0), 5: vector(0,-1,0) }
    def __init__(self, position, colors):
        #0U 1F 2L 3B 4R 5D
        super().__init__(position)
        basePos = self.positionDict[position]
        self.colors = [position]
        self.base = box(pos = basePos, size = vector(0.95,0.95,0.95),  color = color.black)
        sticker = box(pos = basePos * 1.5, size = vector(0.9, 0.05, 0.9), color = colors[position], up = basePos)
        self.stickers.append(sticker)

    def updatePosition(self, move):
        if move in ['f','u','d','b','l','r']:
            return

class Edge3D(Cubie3D):
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

        self.colors = faces
        self.base = box(pos = basePos, size = vector(0.95,0.95,0.95), color = color.black)

        for faceNum in faces:
            facePos = self.vectorDict[faceNum] * 0.5 + basePos
            newSticker = box(pos = facePos, up = self.vectorDict[faceNum], size = vector(0.9, 0.05, 0.9), color = colors[faceNum])
            self.stickers.append(newSticker)



    def updatePosition(self,face):
        self.position = self.edgeUpdateMap[face][self.position]
        if face[0].lower() in ['f','b']:
            self.orientation = (self.orientation + 1) % 2
            

    

class Corner3D(Cubie3D):
    stickerInfoDict = { 0 : [0,1,2], 1 : [0,3,2], 2: [0,1,4], 3: [0,3,4],
                        4 : [5,1,2], 5 : [5,3,2], 6: [5,1,4], 7: [5,3,4]}
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

        faces = self.stickerInfoDict[position]
        basePos = self.vectorDict[faces[0]] + self.vectorDict[faces[1]] + self.vectorDict[faces[2]]

        self.colors = faces
        self.base = box(pos = basePos, size = vector(0.95,0.95,0.95), color = color.black)

        for faceNum in faces:
            facePos = self.vectorDict[faceNum] * 0.5 + basePos
            newSticker = box(pos = facePos, up = self.vectorDict[faceNum], size = vector(0.9, 0.05, 0.9), color = colors[faceNum])
            self.stickers.append(newSticker)

    def updatePosition(self,face):
        if len(face) == 1 and face.lower() in ['l','r','f','b']:
            self.orientation += self.orientationAdditions[face.lower()][self.position] % 3
        self.position = self.cornerUpdateMap[face][self.position]
        
        
class Controller(object):
    def __init__(self): 
        scene = canvas(background = color.white)
        self.cube3d = Cube3D()
        scene.bind('keydown',self.onKey)
        scene.bind('click',self.onClick)
        scene.bind('mousedown',self.onMouseDown)
        scene.bind('mouseup',self.onMouseUp)
        scene.bind('mousemove',self.onMouseMove)
        self.cubeRepr = Cube()

    def generateScramble(self, length = 30):
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
        scrambleList = self.generateScramble()
        print(scrambleList)
        for move in scrambleList:
            self.cube3d.rotate(move)

    def onKey(self, evt):
        #print(evt.__dict__)
        key = evt.key
        if key.lower() in ['f','b','l','r','u','d']:
            self.cube3d.rotate(key)
        elif key.lower() == "s":
            self.scramble()
        elif key.lower() == "g":
            cubeRepr = self.cube3d.toCube()
            cubeRepr.solve()
            #generate and print solution
            pass

    def onClick(self, evt):
        #print(evt.__dict__)
        pass

    def onMouseDown(self, evt):
        #print(evt.__dict__)
        pass

    def onMouseUp(self, evt):
        #print(evt.__dict__)
        pass

    def onMouseMove(self, evt):
        #print(evt.__dict__)
        pass
        
controller = Controller()
