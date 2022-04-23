from vpython import *
from cubeRepr import *
import random

class CubeSolver(object):

    wholeTurnDict = { "x" : {'f':'u','u':'b','b':'d','d':'f','l':'l','r':'r'}, "X": {'f':'d','d':'b','b':'u','u':'f','l':'l','r':'r'}, "x2":{'f':'b','b':'f','u':'d','d':'u','l':'l','r':'r'},
                      "y" : {'f':'l','l':'b','b':'r','r':'f','u':'u','d':'d'}, "Y": {'f':'r','r':'b','b':'l','l':'f','u':'u','d':'d'}, 'y2':{'f':'b','b':'f','u':'u','d':'d','l':'r','r':'l'},
                      "z" : {'u':'r','r':'d','d':'l','l':'u','f':'f','b':'b'}, "Z": {'u':'l','l':'d','d':'r','r':'u','f':'f','b':'b'}, 'z2':{'f':'f','b':'b','u':'d','d':'u','l':'r','r':'l'}}

    @classmethod
    def solve(cls, originalCube):
        #Return a string with shortest possible solution
        originalCube.solution = []
        cubes = [originalCube.copy()]
        cubesAfterCross = cls.bestCross(cubes)
        cubesAfterF2l = cls.bestF2l(cubesAfterCross)
        print("-----")
        shortest = cls.reduceAxes(cubesAfterF2l[0].solution)
        for cube in cubesAfterF2l:
            sol = cls.reduceAxes(cube.solution)
            if len(sol) < len(shortest):
                shortest = sol
            print(sol)
            #cube.prettyPrint()
        print("-----")
        print(f'shortest with len {len(shortest)} is:')
        print(shortest)
        return shortest


    @classmethod
    def bestF2l(cls, cubes):
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
                #print(cube.solution)
                #cube.prettyPrint()
                if cube.downCrossSolved() == False:
                    print("something has gone wrong")
                    raise Exception("destructive moves in f2l")
                
                if cube.isFrontRightColSolved():
                    cube.wholeTurn('y')
                else:#look for corner to insert
                    dfrCornerVals = [cube.stickers[10],cube.stickers[30],cube.stickers[36]]
                    dfrCornerVals.sort()
                    if dfrCornerVals == ['d','f','r']: #corner is down. cases
                        cls.f2lReleaseEdge(cube)
                        if cube.stickers[36] == 'f': #corner is correct but edge is messing:
                            if cube.stickers[35] == 'r' and cube.stickers[31] == 'f': #Case 41
                                for move in ['r','U','R','u','Y','R','u2','r','u2','R','u','r']:
                                    cube.move(move)
                                continue
                            while not cube.isFRFaceMatch():
                                cube.move('u')
                            if cube.stickers[33] == 'f' and cube.stickers[5] == 'r': #case 25
                                for move in ['u','r','U','R','U','y','L','u','l']:
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
                        if cls.f2lReleaseCorner(cube):
                            continue
                            #continue should bring us back to the beginning of loop
                        count = 0
                        while not cube.isDFRInUFR():
                            if(count == 5):
                                print("corner should be on top 318")
                                cube.prettyPrint()
                                raise Exception("Corner should be on top 318")
                                exit()
                            cube.move('u')
                            count += 1
                        cls.f2lReleaseEdge(cube)
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
            #cube.solution = cls.reduceAxes(cube.solution)
            outCubes.append(cube)
        return outCubes


    @classmethod
    def bestCross(cls, cubes):
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
            #cube.solution = cls.reduceAxes(cube.solution)
            outCubes.append(cube)
        #Add culling here later if desired
        return outCubes

    @classmethod
    def reduceAxes(cls, moveList):
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
            newMoveCore = cls.wholeTurnDict[axis][moveCore]
            if isCounter:
                newList.append(newMoveCore.upper())
            elif isDouble:
                newList.append(newMoveCore + "2")
            else:
                newList.append(newMoveCore)
        return cls.reduceAxes(newList)
        
    @classmethod
    def f2lReleaseCorner(cls, cube):
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
            
    @classmethod
    def f2lReleaseEdge(cls, cube):
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
        if sorted([cube.stickers[x] for x in [27,47]]) == ['f','r']: #back right
            for move in ['b','u','B','U']:
                cube.move(move)
            return True
        return False
    

