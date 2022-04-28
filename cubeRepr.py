
class Cube(object):
    #This class represents a rubik's cube as a simple 48-long list of 6 possible values. The class has the ability to make moves, mapping these values to different positions according to how a rubik's cube would move. The efficient moves make this class idea for implementation of a solving algorithm, which is it's purpose in the program. Because the Cube3D class cannot make moves quickly do to it's connection to vpython objects,

    wideDict = {'l':['X','r'], 'L':['x','R'], 'r':['x','l'], 'R':['X','L'],
                'd':['Y','u'], 'D':['y','U'], 'u':['y','d'], 'U':['Y','D'],
                'b':['Z','f'], 'B':['z','F'], 'f':['z','b'], 'F':['Z','B']}

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

    reductionDict = {"xxx":["X"], "yyy":["Y"], "Yxy":["z"], "dd":["d2"], "xYX":["Z"], "Zz":[], "YZy":["x"], "yY":[], "Yy":[], "YZY":["x","y2"], "ZYZ":["x","y2"],
                     "y2xy2":["X"], "xX":[],"Xx":[],"xy2x":["x"], "xy2Z":["X","z"], "yy":["y2"], "Yxy2":["X","z"], "zYx":["Y",'x2'], "Yx2Y":['x2'],'xx2':['X'],
                     "Xx2":['x'],"XzX":['y','x2'],'ZXz':['y'],'Xzy2':['z','Y'],"XYx2":['x','y'],"YZy2":['x','y'],'Xzy':['z','y2'],'y2y':['Y'], 'uuu':['U'],
                     'xy2X':['z2'], 'z2Yx':['Y','X'], 'YXY':['z','x2'], 'x2x':['X'], 'XX':['x2'], 'YXy':['Z'], 'ZZ':['z2'],'YXz':['X'],'YxY':['Z','x2'],
                     'YXy2':['Z','y'],'Yx2z':['Z','X'], 'x2X':['x'], 'xzX':['Y'], 'YY':["y2"], 'ZxZ':['y','x2'], 'Zxz':['Y'], 'XZx2':['z','Y'], 'Zxy':['x'],
                     'Zxy2':['x','y'], 'ZxY':['X','z2'],'Xz2X':['z2'], 'y2Xy':['Z','x'], 'YzY':['z2','X'], 'b2b':['B'], 'bbb':['B'], 'd2d':['D'], 'uu':['u2'],
                     'Ll':[],'uU':[],'UU':['u2'], 'uu':['u2'], 'fF':[], 'Uu2':['u'], 'DD':['d2'], 'Ff':[], 'u2U':['u'], 'l2l2':[], 'Uu':[], 'lL':[], 'l2L':['l'],
                     'r2R':['r'], 'ff':['f2'], 'BB':'b2', 'dD':[], 'uu2':['U'], 'rR':[]}

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
    
    def isSolved(self):
        faces = ['u','d','l','r','f','b']
        for i in range(48):
            if self.stickers[i] != faces[i//8]:
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
        if len(face) == 2 and face[1] == 'w':
            moves = self.wideDict[face[0]]
            self.moves(moves)
            return
        moveMap = self.turnMaps[face]
        newStickers = self.stickers.copy()
        for t in moveMap:
            newStickers[t[1]] = self.stickers[t[0]]
        self.stickers = newStickers
        self.solution.append(face)
        if self.verifyCube() == False:
            return False

    def wholeTurn(self, axis):
        #axis should be in [x, X, y, Y, z, Z]
        if axis == None:
            return
        if len(axis) == 2:
            self.wholeTurn(axis[0])
            self.wholeTurn(axis[0])
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
            return False
            print(axis)
            raise Exception("Cube is broken/unsolvable (axis rotation)")


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
        while(i < len(moveList)-2):
            a = moveList[i]
            b = moveList[i+1]
            c = moveList[i+2]
            str3 = a + b + c
            str2 = a + b
            if str3 in self.reductionDict.keys():
                newSolution.extend(self.reductionDict[str3])
                i += 3
                continue
            elif str2 in self.reductionDict.keys():
                newSolution.extend(self.reductionDict[str2])
                i += 2
                continue
            else:
                newSolution.append(a)
                i += 1
        if i == len(moveList) - 2:
            a = moveList[i]
            b = moveList[i+1]
            str2 = a + b
            if str2 in self.reductionDict.keys():
                newSolution.extend(self.reductionDict[str2])
            else:
                newSolution.append(a)
                newSolution.append(b)
        elif i == len(moveList) - 1:
            newSolution.append(moveList[i])
        return newSolution

 #  def oCheck(self, orientations) -> bool:
 #      #returns true if top orientations match input array
 #      #input array should be of length 8 where the first 4 values are 0 or 1 and the second 4 are 0 1 or 2. Iterate clockwise starting with UF and then UFL
 #      ori = orientations
 #      s = self.stickers
 #      edgeTops = [5,7,1,3]
 #      for i in range(4):
 #          if ori[i] == 0 and s[edgeTops[i]] != 'u':
 #              return False
 #          elif ori[i] == 1 and s[edgeTops[i]] == 'u':
 #              return False
 #      cornerOris = [[6,0,2,4],[32,16,40,24],[18,42,26,34]]
 #      for i in range(4,8):
 #          if s[cornerOris[ori[i]][i-4]] != 'u':
 #              return False
 #      return True
    
    def getOList(self):
        edgeTops = [5,7,1,3]
        cornerOris = [[6,0,2,4],[32,16,40,24],[18,42,26,34]]
        outList = [4] * 8
        s = self.stickers
        for i in range(4):
            outList[i] = 0 if s[edgeTops[i]] == 'u' else 1
        for i in range(4,8):
            for j in range(3):
                if s[cornerOris[j][i-4]] == 'u':
                    outList[i] = j
                    break
        if 4 in outList:
            self.prettyPrint()
            print(outList)
            raise Exception("getOList failure")
            exit()
        return outList
    
    def getPString(self):
        outStr = ""
        for i in [34,33,32,18,17,16,42,41,40,26,25,24]:
            outStr = outStr  + self.stickers[i]
        return outStr
            

    def isOLLSolved(self):
        s = self.stickers
        for i in range(8):
            if s[i] != 'u':
                return False
        return True
            
            

    def isFRFaceMatch(self):
        #Checks if FR is in either UF or UR WITH THE COLOR MATCH
        if self.stickers[33] == 'f' and self.stickers[5] =='r':
            return True
        if self.stickers[25] == 'r' and self.stickers[3] == 'f':
            return True
        return False

            

    def isDFRInUFR(self):
        cornerVals = [self.stickers[x] for x in [4,34,24]]
        cornerVals.sort()
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
        
    def prettyPrint(self):
        print("    ", end = '')
        self.printSpots([0,1,2])
        print("    ", end = '')
        self.printSpots([7,'u',3])
        print("    ", end = '')
        self.printSpots([6,5,4])
        self.printSpots([16,17,18,' ',32,33,34,' ',24,25,26,' ',40,41,42])
        self.printSpots([23,'l',19,' ',39,'f',35,' ',31,'r',27,' ',47,'b',43])
        self.printSpots([22,21,20,' ',38,37,36,' ',30,29,28,' ',46,45,44])
        print("    ", end ='')
        self.printSpots([8,9,10])
        print("    ", end ='')
        self.printSpots([15,'d',11])
        print("    ", end ='')
        self.printSpots([14,13,12])
        print("")

    def printSpots(self, spots):
        #Helper function for pretty print
        s = self.stickers
        for pos in spots:
            if type(pos) is str:
                print(pos, end = '')
            else:
                print(f'{s[pos]}',end = '')
        print("")
