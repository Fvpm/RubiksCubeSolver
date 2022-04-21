from vpython import *
import random

class CubeSolver(object):

    @classmethod
    def solve(cls, cube):
        

class Cube(object):
    #This class represents a rubik's cube as a simple 48-long list of 6 possible values. The class has the ability to make moves, mapping these values to different positions according to how a rubik's cube would move. The efficient moves make this class idea for implementation of a solving algorithm, which is it's purpose in the program. Because the Cube3D class cannot make moves quickly do to it's connection to vpython objects,


    wholeTurnDict = { "x" : {'f':'u','u':'b','b':'d','d':'f','l':'l','r':'r'}, "X": {'f':'d','d':'b','b':'u','u':'f','l':'l','r':'r'}, "x2":{'f':'b','b':'f','u':'d','d':'u','l':'l','r':'r'},
                      "y" : {'f':'l','l':'b','b':'r','r':'f','u':'u','d':'d'}, "Y": {'f':'r','r':'b','b':'l','l':'f','u':'u','d':'d'}, 'y2':{'f':'b','b':'f','u':'u','d':'d','l':'r','r':'l'},
                      "z" : {'u':'r','r':'d','d':'l','l':'u','f':'f','b':'b'}, "Z": {'u':'l','l':'d','d':'r','r':'u','f':'f','b':'b'}, 'z2':{'f':'f','b':'b','u':'d','d':'u','l':'r','r':'l'}}
    wholeTurnMoveDict = { "x" : {0:44, 1:45, 2:46, 3:47,4:40,5:41,6:42,7:43,  8:32,9:33,10:34,11:35,12:36,13:37,14:38,15:39,
                                 16:22, 17:23,18:16,19:17,20:18,21:19,22:20,23:21,  24:26,25:27,26:28,27:29,28:30,29:31,30:24,31:25,
                                 32:0,33:1,34:2,35:3,36:4,37:5,38:6,39:7,  40:12, 41:13, 42:14, 43:15,44:8,45:9,46:10,47:11},
                          "y" : {0:2,1:3,2:4,3:5,4:6,5:7,6:0,7:1,  8:14,9:15,10:8,11:9,12:10,13:11,14:12,15:13,
                                 16:40,17:41,18:42,19:43,20:44,21:45,22:46,23:47, 24:32,25:33,26:34,27:35,28:36,29:37,30:38,31:39,
                                 32:16,33:17,34:18,35:19,36:20,37:21,38:22,39:23, 40:24,41:25,42:26,43:27,44:28,45:29,46:30,47:31},
                          "z" : {0:26,1:27,2:28,3:29,4:30,5:31,6:24,7:25,  8:18,9:19,10:20,11:21,12:22,13:23,14:16,15:17,
                                 16:2, 17:3,18:4,19:5,20:6,21:7,22:0,23:1, 24:10, 25:11,26:12,27:13,28:14,29:15,30:8,31:9,
                                 32:34,33:35,34:36,35:37,36:38,37:39,38:32,39:33,  40:46,41:47,42:40,43:41,44:42,45:43,46:44,47:45}}
    newEntries = dict()
    for k,v in wholeTurnMoveDict.items():
        newKey = k.upper()
        revDict = {}
        for k2,v2 in v.items():
            revDict[v2] = k2
        newEntries[newKey] = revDict
    wholeTurnMoveDict.update(newEntries)
                         

    edgePairs = { 1:41, 3:25, 5:33, 7:17, 9:37, 11:29, 13:45, 15:21, 17: 7, 19:39, 21:15, 23:43, 25:3, 27: 47, 29:11, 31:35, 33:5, 35:31, 37:9, 39:19, 41:1, 43:23, 45:13, 47:27}
    turnMaps = {'u':[(0,2),(2,4),(4,6),(6,0),(1,3),(3,5),(5,7),(7,1),
                          (32,16),(16,40),(40,24),(24,32),(33,17),(34,18),(17,41),(18,42),(41,25),(42,26),(25,33),(26,34)],
                     'd':[(8,10),(10,12),(12,14),(14,8),(9,11),(11,13),(13,15),(15,9),
                          (38,30),(30,46),(46,22),(22,38),(37,29),(29,45),(45,21),(21,37),(36,28),(28,44),(44,20),(20,36)],
                     'l':[(16,18),(18,20),(20,22),(22,16),(17,19),(19,21),(21,23),(23,17),
                          (0,32),(32,8),(8,44),(44,0),(7,39),(39,15),(15,43),(43,7),(6,38),(38,14),(14,42),(42,6)],
                     'r':[(24,26),(26,28),(28,30),(30,24),(25,27),(27,29),(29,31),(31,25),
                          (4,40),(40,12),(12,36),(36,4),(3,47),(47,11),(11,35),(35,3),(2,46),(46,10),(10,34),(34,2)],
                     'f':[(32,34),(34,36),(36,38),(38,32),(33,35),(35,37),(37,39),(39,33),
                          (18,4),(4,30),(30,8),(8,18),(19,5),(5,31),(31,9),(9,19),(20,6),(6,24),(24,10),(10,20)],
                     'b':[(40,42),(42,44),(44,46),(46,40),(41,43),(43,45),(45,47),(47,41),
                          (2,16),(16,14),(14,28),(28,2),(1,23),(23,13),(13,27),(27,1),(0,22),(22,12),(12,26),(26,0)]}

    #In the next 15 lines I create some class variables for the sole purpose of calculating the other 12 maps for turnMaps. turnMaps needs to be a class variable because I don't want to redo this calculation every time I create a new cube class. The downside is that there are some class variables (reverseMaps, doubleTurns) that I do not care about. I need to do some research and see if I can get rid of these
    #The solving algorithm for this will search trees of move options for the most effective, in order to do this, copies of this class are loaded into memory, changed slightly (usually a whole-cube rotation), and solved. I don't want an instance of this class to take up more space than necessary.
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
    


    def __init__(self, _stickers = None, _solution = []):
        #Creates a new cube with position set by creator.
        #_stickers should be an array of length 48 containing 8 instances of each face value
        if _stickers == None: 
            self.stickers = []
            for face in ['u','d','l','r','f','b']:
                for i in range(8):
                    self.stickers.append(face)
            return
        if len(_stickers) != 48:
            print("ERROR stickers wronglength 48")
            return
        #TODO check for correct values
        self.stickers = _stickers
        self.solution = _solution

    def verifyCube(self):
        for face in ['f','b','l','r','u','d']:
            if self.stickers.count(face) != 8:
                return False

        return True

    def copy(self):
        #returns a new cube identical to this one
        newCube = Cube(self.stickers.copy(), self.solution.copy())
        return newCube
    
    def moves(self,faces):
        for move in faces:
            self.move(move)

    def move(self,face):
        #Makes a move on the cube. 
        #Face should be one of 18 strings with base forms f, u, l, b, r, d and variations f, F, f2 for clockwise, counterclockwise, and double
        if face == None:
            return
        if face[0].lower() in ['x','y','z']:
            self.wholeTurn(face)
            return
        moveMap = self.turnMaps[face]
        newStickers = self.stickers.copy()
        for t in moveMap:
            newStickers[t[1]] = self.stickers[t[0]]
        self.stickers = newStickers
        self.solution.append(face)
        if self.verifyCube() == False:
            print(face)
            raise Exception(face + "move fucked up")

    def wholeTurn(self, axis):
        #axis should be in [x, X, y, Y, z, Z]
        if axis == None:
            return
        if axis not in ['x','X','y','Y','z','Z']:
            print("error 71 incorrect wholeTurn() input")
            return
        mapDict = self.wholeTurnDict[axis]
        newStickers = [0] * 48
        for i in range(48):
        
            newStickers[i] = mapDict[self.stickers[i]]
        moveDict = self.wholeTurnMoveDict[axis]
        for i in range(48):
            self.stickers[moveDict[i]] = newStickers[i]

        self.solution.append(axis)
        if self.verifyCube() == False:
            print(axis)
            raise Exception(axis + "move fucked up")

    def solve(self):
        #Return a string with shortest possible solution
        self.solution = []
        cubes = [self.copy()]
        cubesAfterCross = self.bestCross(cubes)
        #cubesAfterF2L = self.bestF2l(cubesAfterCross)
        for cube in cubesAfterCross:
            print(cube.solution)

    def reduceSolution(self):
        thisReduce = self.solution
        nextReduce = self.reduceList(thisReduce)
        while thisReduce != nextReduce:
            thisReduce = nextReduce
            nextReduce = self.reduceList(thisReduce)
        self.solution = thisReduce

    def getCompLength(self):
        count = 0
        for move in self.solution:
            if move[0].lower() not in ['x','y','z']:
                count += 1
        return count

    
    def reduceList(self, moveList): 
        i = 0
        newSolution = []
        reductionDict = {"xxx":["X"], "yyy":["Y"], "Yxy":["z"], "dd":["d2"], "xYX":["Z"], "Zz":[], "YZy":["x"], "yY":[], "Yy":[], "YZY":["x","y2"], "ZYZ":["x","y2"],
                         "y2xy2":["X"], "xX":[],"Xx":[],"xy2x":["x"], "xy2Z":["X","z"], "yy":["y2"], "Yxy2":["X","z"], "zYx":["Y",'x2'], "Yx2Y":['x2'],'xx2':['X'],
                         "Xx2":['x'],"XzX":['y','x2'],'ZXz':['y'],'Xzy2':['z','Y'],"XYx2":['x','y'],"YZy2":['x','y'],'Xzy':['z','y2'],'y2y':['Y'], 'uuu':['U'],
                         'xy2X':['z2'], 'z2Yx':['Y','X'], 'YXY':['z','x2'], 'x2x':['X'], 'XX':['x2'], 'YXy':['Z'], 'ZZ':['z2'],'YXz':['X'],'YxY':['Z','x2'],
                         'YXy2':['Z','y'],'Yx2z':['Z','X'], 'x2X':['x'], 'xzX':['Y'], 'YY':["y2"], 'ZxZ':['y','x2'], 'Zxz':['Y'], 'XZx2':['z','Y'], 'Zxy':['x'],
                         'Zxy2':['x','y'], 'ZxY':['X','z2'],'Xz2X':['z2'], 'y2Xy':['Z','x'], 'YzY':['z2','X'], 'b2b':['B'], 'bbb':['B'], 'd2d':['D'], 'uu':['u2']}
        while(i < len(moveList)-2):
            a = moveList[i]
            b = moveList[i+1]
            c = moveList[i+2]
            str3 = a + b + c
            str2 = a + b
            if str3 in reductionDict.keys():
                newSolution.extend(reductionDict[str3])
                i += 3
                continue
            elif str2 in reductionDict.keys():
                newSolution.extend(reductionDict[str2])
                i += 2
                continue
            else:
                newSolution.append(a)
                i += 1
        if i == len(moveList) - 2:
            a = moveList[i]
            b = moveList[i+1]
            str2 = a + b
            if str2 in reductionDict.keys():
                newSolution.extend(reductionDict[str2])
            else:
                newSolution.append(a)
                newSolution.append(b)
        elif i == len(moveList) - 1:
            newSolution.append(moveList[i])
        return newSolution

    def reduceAxes(self, moveList):
        #ttakes a list of moves and returns the list of moves with no axes rotations (but with the same moves)
        if len(moveList) == 0:
            return moveList
        i = len(moveList) - 1
        while(i > 0):
            if moveList[i][0].lower() in ['x','y','z']:
                break
            i -= 1
        if i == 0 and moveList[0][0].lower() not in ['x','y','z']:
            return moveList
        axis = moveList[i]
        if len(axis) == 2:
            pass
        elif axis.isupper():
            axis = axis.lower()
        else:
            axis = axis.upper()
        newList = []
        for j in range(i):
            newList.append(moveList[j])
        for j in range(i+1,len(moveList)):
            move = moveList[j]
            isCounter = moveList[j][0].isupper()
            isDouble = True if len(moveList[j]) == 2 else False
            moveCore = move[0].lower()
            newMoveCore = self.wholeTurnDict[axis][moveCore]
            if isCounter:
                newList.append(newMoveCore.upper())
            elif isDouble:
                newList.append(newMoveCore + "2")
            else:
                newList.append(newMoveCore)
        return self.reduceAxes(newList)
            
    def bestF2l(self, cubes):
        rotationGenerators = [None,"y","y","y"]
        inCubes = []
        #generate starting position rotations
        for rotation in rotationGenerators:
            for cube in cubes:
                cube.wholeTurn(rotation)
                inCubes.append(cube.copy())
        outCubes = []
        for cube in inCubes:
            #For f2l im basically following a set of algorithms http://www.rubiksplace.com/speedcubing/F2L-algorithms/ here. I tend to favor shorter options with no axis rotations. I would just undo these axis rotations afterwards anyways.
            #For the cases that are not included i am using accompanying pdf to fill in blanks
            #The algorithms assume we are filling the front right edge and that the needed corner piece is in that column. That means the corner piece will either be in the bottom right or can be found by rotating u several tims.
            while not cube.isF2lSolved():
                if cube.downCrossSolved() == False:
                    print("something has gone wrong")
                    raise Exception("destructive moves in f2l")
                print("nothing is happening")
                
                if cube.isFrontRightColSolved():
                    cube.wholeTurn('y')
                else:#look for corner to insert
                    dfrCornerVals = [cube.stickers[10],cube.stickers[30],cube.stickers[36]]
                    dfrCornerVals.sort()
                    if dfrCornerVals == ['d','f','r']: #corner is down. cases
                        self.f2lReleaseEdge(cube)
                        if cube.stickers[36] == 'f': #corner is correct but edge is messing:
                            if cube.stickers[35] == 'r' and cube.stickers[31] == 'f': #Case 41
                                for move in ['r','U','R','u','Y','R','u2','r','u2','R','u','r']:
                                    cube.move(move)
                                continue
                            while not cube.isFRFaceMatch():
                                print("edge should be on top 266")
                                cube.move('u')
                            if cube.stickers[33] == 'f' and cube.stickers[5] == 'r': #case 25
                                for move in ['u','r','U','R','U','y','L','u','L']:
                                    cube.move(move)
                                continue
                            if cube.stickers[25] == 'r' and cube.stickers[3] == 'f': #case 26
                                for move in ['y','U','L','u','l','Y','u','r','U','R']:
                                    cube.move(move)
                                continue
                            print("ERROR weird case 266")
                        elif cube.stickers[36] == 'd': #white is in front
                            if sorted([cube.stickers[x] for x in [35,31]]) == ['f','r']: #edge is in front
                                if cube.stickers[35] == 'f': #case 37
                                    cube.moves(['r','U','R','U','r','u','R','u2','r','U','R'])
                                    continue
                                else: #case 39
                                    cube.moves(['Y','r2','F','U','f','u','r','U','r'])
                                    continue
                            else:#edge is on top
                                while not cube.isFRFaceMatch():
                                    print("edge should be on top 287")
                                    cube.move('u')
                                if cube.stickers[33] == 'f': #case 27
                                    cube.moves(['Y','R','U','r','u','R','U','r'])
                                    continue
                                else: #case 29
                                    cube.moves(['r','U','R','u','r','U','R'])
                                    continue
                        else: #white is on the right
                            if sorted([cube.stickers[x] for x in [35,31]]) == ['f','r']:
                                if cube.stickers[35] == 'f': #case 38
                                    cube.moves(['r','u','R','u2','r','U','R','u','r','u','R'])
                                    continue
                                else: #case 40
                                    cube.moves(['r','u','R','U','r','U','R','u2','Y','R','U','r'])
                                    continue
                                    
                            else: #edge is on to
                                while not cube.isFRFaceMatch():
                                    cube.move('u')
                                if cube.stickers[33] == 'f': #case 30
                                    cube.moves(['Y','R','u','r','U','R','u','r'])
                                    continue
                                else: #case 28
                                    cube.moves(['r','u','R','U','r','u','R'])
                                    continue
                    else: #corner is somewhere else. we have to get it in UFR
                        if self.f2lReleaseCorner(cube):
                            continue
                            #continue should bring us back to the beginning of loop
                        while not cube.isDFRInUFR():
                            print("corner should be on top 318")
                            cube.move('u')
                        self.f2lReleaseEdge(cube)
                        #corner is now in UFR
                        if cube.stickers[34] == 'r': #side colors are switched, white on top
                            #the tuples are in format (index of f, index of r, moves to execute)
                                         #case 23
                            locations = [( 5,33, ['u2','r2','u2','R','U','r','U','r2']),
                                         #case 18
                                         (33, 5, ['Y','R','u2','r','u','R','U','r']),
                                         #case 21
                                         ( 7,17, ['r','U','R','u2','r','u','R']),
                                         #case 20
                                         (17, 7, ['Y','U','R','u2','r','U','R','u','r']),
                                         #case 19
                                         ( 1,41, ['u','r','u2','R','u','r','U','R']),
                                         #case 22
                                         (41, 1, ['Y','R','u','r','u2','R','U','r']),
                                         #case 17
                                         ( 3,25, ['r','u2','R','U','r','u','R']),
                                         #case 24
                                         (25, 3, ['Y','u2','r2','u2','r','u','R','u','r2']),
                                         #case 36
                                         (35,31, ['r','u','R','U','r','u','R','U','r','u','R']),
                                         #case 35
                                         (31,35, ['r','U','R','Y','u','R','u','r'])]
                            for location in locations:
                                frontSpot = location[0]
                                rightSpot = location[1]
                                moves = location[2]
                                if cube.stickers[frontSpot] == 'f' and cube.stickers[rightSpot] == 'r':
                                    cube.moves(moves)
                                    break
                        elif cube.stickers[34] == 'f': #front matches, white on right
                                         #case 14        
                            locations = [( 5,33, ['R','u2','r2','u','r2','u','r']),
                                         #case 2
                                         (33, 5, ['f','R','F','r']),
                                         #case 12
                                         ( 7,17, ['U','r','u','R','u','r','u','R']),
                                         #case 4
                                         (17, 7, ['Y','u','R','U','r','u2','R','u','r']),
                                         #case 10
                                         ( 1,41, ['r','u','R']),
                                         #case 6
                                         (41, 1, ['Y','u','R','u2','r','u2','R','u','r']),
                                         #case 16
                                         ( 3,25, ['U','r','U','R','u','r','u','R']),
                                         #case 8
                                         (25, 3, ['r','U','R','u2','Y','R','U','r']),
                                         #case 32
                                         (35,31, ['U','r','u2','R','u','r','u','R']),
                                         #case 34
                                         (31,35, ['y','u2','L','u','l','u','y','l','u','L',])]
                            for location in locations:
                                frontSpot = location[0]
                                rightSpot = location[1]
                                moves = location[2]
                                if cube.stickers[frontSpot] == 'f' and cube.stickers[rightSpot] == 'r':
                                    cube.moves(moves)
                                    break
                            pass
                            #TODO 2-16 Even, 32,34
                        elif cube.stickers[34] == 'd': #right matches, white on left
                                         #case 7        
                            locations = [( 5,33, ['y','L','u','l','u2','y','r','u','R']),
                                         #case 15
                                         (33, 5, ['Y','u','R','u','r','U','R','U','r']),
                                         #case 5
                                         ( 7,17, ['U','r','u2','R','u2','r','U','R']),
                                         #case 9
                                         (17, 7, ['Y','R','U','r']),
                                         #case 3
                                         ( 1,41, ['U','r','u','R','u2','r','U','R']),
                                         #case 11
                                         (41, 1, ['U','r','U','R','u','Y','R','U','r']),
                                         #case 1
                                         ( 3,25, ['u','r','U','R']),
                                         #case 13
                                         (25, 3, ['U','r','u2','R','Y','u','R','U','r']),
                                         #case 31
                                         (35,31, ['U','r','U','R','u2','r','U','R']),
                                         #case 33
                                         (31,35, ['U','r','u','R','Y','u','R','U','r'])]
                            for location in locations:
                                frontSpot = location[0]
                                rightSpot = location[1]
                                moves = location[2]
                                if cube.stickers[frontSpot] == 'f' and cube.stickers[rightSpot] == 'r':
                                    cube.moves(moves)
                                    break
                        else:
                            print("ERROR i thought i covered all the cases 327")
            cube.reduceSolution()
            outCubes.append(cube)
        return outCubes


    def isFRFaceMatch(self):
        #Checks if FR is in either UF or UR WITH THE COLOR MATCH
        if self.stickers[33] == 'f' and self.stickers[5] =='r':
            return True
        if self.stickers[25] == 'r' and self.stickers[3] == 'f':
            return True
        return False

    def f2lReleaseCorner(self, cube):
        #check if corner is in the bottom layer in the wrong column, and if so move it DFR. If an edge needs to be released as well, we cant accidentally put this corner in a wrong slot again.
        if sorted([cube.stickers[x] for x in [38,8,20]]) == ['d','f','r']:#its in FL
            for move in ['L','r','U','R','l']:
                cube.move(move)
            return True
        if sorted([cube.stickers[x] for x in [22,44,14]]) == ['d','f','r']: #its in BL
            for move in ['l','F','u2','f','L']:
                cube.move(move)
            return True
        if sorted([cube.stickers[x] for x in [28,46,12]]) == ['d','f','r']: #its in BR
            for move in ['b','F','u','f','B']:
                cube.move(move)
            return True
        return False
            
            
    def f2lReleaseEdge(self, cube):
        #release the front right edge if its in one of the other equatorial edges
        #first check if is actually in one of them
        edgePairs = [(19,39),(23,43),(27,47)]
        #if sorted([cube.stickers[19],cube.stickers[39]]) == ['f','r']:
        if sorted([cube.stickers[x] for x in [19,39]]) == ['f','r']: #its in front left
            for move in ['L','U','l','u']:
                cube.move(move)
            return True
        if sorted([cube.stickers[x] for x in [23,43]]) == ['f','r']: #its in back left
            for move in ['l','U','L','u']:
                cube.move(move)
            return True
        if sorted([cube.stickers[x] for x in [27,43]]) == ['f','r']: #back right
            for move in ['b','u','B','U']:
                cube.move(move)
            return True
        return False

    def isDFRInUFR(self):
        cornerVals = [self.stickers[x] for x in [4,34,24]]
        cornerVals.sort
        if cornerVals == ['d','f','r']:
            return True
        else:
            return False

    def isFrontRightColSolved(self):
        #simple one
        if self.stickers[35] != 'f' or self.stickers[36] != 'f':
            return False
        if self.stickers[30] != 'r' or self.stickers[31] != 'r':
            return False
        if self.stickers[10] != 'd':
            return False
        return True


    def isF2lSolved(self):
        ##is bottom face solved
        #if [self.stickers(x) for x in range(8,16)].count('d') != 8:
        #    return False
        ##is front face solved
        #if [self.stickers(x) for x in range(35,40)].count('f') !=5:
        #    return False
        
        checks = [(8,16,'d'),(35,40,'f'),(19,24,'l'),(27,32,'r'),(43,48,'b')]
        for t in checks:
            num = t[1]-t[0]
            if[self.stickers[x] for x in range(t[0],t[1])].count(t[2]) != num:
                return False
        return True

    def bestCross(self, cubes):
        #Cubes is a list of cubes but it should happen to be length 1
        oCube = cubes[0]
        inCubes = []
        startMoves = ["y","y","y","x","y","y","y","X","y","y","y",'X','y','y','y','x','y','y','y','x','y','y','y']
        inCubes.append(oCube.copy())
        for move in startMoves:
            oCube.wholeTurn(move)
            inCubes.append(oCube.copy())
        outCubes = []
        for cube in inCubes:
            while(not cube.downCrossSolved()):#Checking if this is solved
                if cube.dOnDownCross() == 4: #Whites are right and colors are wrong  (otherwise while loop wouldnt activate)
                    while(cube.crossColorsRight() < 2): #if whites are all on bottom, then you can rotate the bottom until 2 or 4 are in correct positions
                        cube.move('d')#
                    if(cube.crossColorsRight() == 4):
                        continue
                    else:#After rotating the bottom, swap the 2 remaining incorrect facs
                        incorrectFaces = []
                        for (x,y) in [(37,'f'),(29,'r'),(45,'b'),(21,'l')]:
                            if cube.stickers[x] != y:
                                incorrectFaces.append(y)
                        cube.move(incorrectFaces[0]+"2")
                        rotation = ["l","b","r","f"]
                        moves = (rotation.index(incorrectFaces[1]) - rotation.index(incorrectFaces[0])) % 4
                        for i in range(moves):
                            cube.move("u")
                        cube.move(incorrectFaces[1]+"2")
                        for i in range((moves-4)%4):
                            cube.move("u")
                        cube.move(incorrectFaces[0]+"2")
                else: #whites are not on bottom
                    edgeMoves = {23:'b',19:'F',39:'l',35:'R',31:'f',27:'B',47:'r',43:'L',
                                 33:'f',37:'f',17:'l',21:'l',41:'b',45:'b',29:'r',25:'r',5:'f2',1:'b2',3:'r2',7:'l2'}
                    edgeWatches = {'b':13,'B':13,'b2':13,'f':9,'F':9,'f2':9,'r':11,'R':11,'r2':11,'l':15,'L':15,'l2':15}
                    for edgeSpot in edgeMoves.keys():
                        if cube.stickers[edgeSpot] == 'd':
                            while cube.stickers[edgeWatches[edgeMoves[edgeSpot]]] == "d":
                                cube.move('d')
                            cube.move(edgeMoves[edgeSpot])
            cube.reduceSolution()
            cube.solution = self.reduceAxes(cube.solution)
            outCubes.append(cube)
        #Add culling here later if desired
        return outCubes
                            

    def dOnDownCross(self) -> int:
        return [self.stickers[x] for x in [9,11,13,15]].count('d')

    def crossColorsRight(self) -> int:
        crossList = [(True if self.stickers[x]==y else False) for (x,y) in [(37,'f'),(29,'r'),(45,'b'),(21,'l')]]
        return crossList.count(True)

    def downCrossSolved(self) ->bool:
        if self.dOnDownCross() < 4:
            return False
        if self.crossColorsRight() < 4:
            return False
        return True
        

class Cube3D(object):
    #This object represents the Cube object in the VPython scene and controls it. the destroy() method should be called before a new Cube3D is created.
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
        for cubie in rotatePieces:
            cubie.updatePosition(face)
            if moveTwice:
                cubie.updatePosition(face)
        for i in range(0, fps):
            rate(fps*2)
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
        self.colors = [position]
        self.base = box(pos = basePos, size = vector(0.95,0.95,0.95),  color = color.black)
        sticker = box(pos = basePos * 1.5, size = vector(0.9, 0.05, 0.9), color = colors[position], up = basePos)
        self.stickers.append(sticker)

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

        self.colors = faces
        self.base = box(pos = basePos, size = vector(0.95,0.95,0.95), color = color.black)

        for faceNum in faces:
            facePos = self.vectorDict[faceNum] * 0.5 + basePos
            newSticker = box(pos = facePos, up = self.vectorDict[faceNum], size = vector(0.9, 0.05, 0.9), color = colors[faceNum])
            self.stickers.append(newSticker)



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

    def getFaces(self):
        return self.colors
        
        
class Controller(object):
    def __init__(self): 
        scene = canvas(background = color.gray(0.97))
        scene.ambient=color.gray(0.7)
        self.cube3d = Cube3D()
        scene.bind('keydown',self.onKey)
        scene.bind('click',self.onClick)
        scene.bind('mousedown',self.onMouseDown)
        scene.bind('mouseup',self.onMouseUp)
        scene.bind('mousemove',self.onMouseMove)
        self.cubeRepr = Cube()

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
        for move in scrambleList:
            self.cube3d.rotate(move)

    def reset(self):
        #Destroys the current cube and creates a new one
        self.cube3d.destroy()
        self.cube3d = Cube3D()
        self.cubeRepr = Cube()

    def onKey(self, evt):
        #Called by keypress event listener
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
        elif key.lower() == "n":
            self.reset()

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
