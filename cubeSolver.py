from vpython import *
from cubeRepr import *
import random

class CubeSolver(object):

    wholeTurnDict = { "x" : {'f':'u','u':'b','b':'d','d':'f','l':'l','r':'r'}, "X": {'f':'d','d':'b','b':'u','u':'f','l':'l','r':'r'}, "x2":{'f':'b','b':'f','u':'d','d':'u','l':'l','r':'r'},
                      "y" : {'f':'l','l':'b','b':'r','r':'f','u':'u','d':'d'}, "Y": {'f':'r','r':'b','b':'l','l':'f','u':'u','d':'d'}, 'y2':{'f':'b','b':'f','u':'u','d':'d','l':'r','r':'l'},
                      "z" : {'u':'r','r':'d','d':'l','l':'u','f':'f','b':'b'}, "Z": {'u':'l','l':'d','d':'r','r':'u','f':'f','b':'b'}, 'z2':{'f':'f','b':'b','u':'d','d':'u','l':'r','r':'l'}}
    #oll algorithms should be in standard CFOP orer
    ollMap = [ ([1,1,1,1,2,1,2,1], ['r','u','B','r','b','r2','U','R','f','r','F']),
               ([1,1,1,1,2,1,1,2], ['y','y','f','R','F','r','u','r2','B','R','b','U','R']),
               ([1,1,1,1,2,2,2,0], ['y','Rw','r2','u','R','u','rw','u2','Rw','u','R','rw']),
               ([1,1,1,1,1,1,0,1], ['y','Rw','r','U','rw','u2','Rw','U','r','U','r2','rw']),
               ([0,1,1,0,2,2,2,0], ['Rw','u2','r','u','R','u','rw']), #5
               ([0,0,1,1,0,1,1,1], ['y2','rw','u2','R','U','r','U','Rw']),
               ([1,0,0,1,0,2,2,2], ['rw','u','R','u','r','u2','Rw']),
               ([1,1,0,0,1,1,1,0], ['Lw','U','l','U','L','u2','lw']),
               ([1,1,0,0,0,1,1,1], ['Y','R','U','r','y','rw','U','Rw','u','rw','u','Rw']),
               ([1,0,0,1,2,2,2,0], ['Y','r','u','R','y','R','f','r','U','R','F','r']), #10
               ([0,0,1,1,2,0,2,2], ['y','rw','u','R','u','R','f','r','F','r','u2','Rw']),
               ([0,1,1,0,1,1,0,1], ['y','f','r','u','r2','f','r','Y','r2','u','r','u2','R']),
               ([1,0,1,0,0,2,2,2], ['f','u','r','u2','R','U','r','u','R','F']),
               ([1,0,1,0,1,1,1,0], ['R','f','r','u','R','F','r','f','U','F']),
               ([1,0,1,0,2,2,2,0], ['y2','R','F','r','L','U','l','u','R','f','r']), #15
               ([1,0,1,0,0,1,1,1], ['y2','rw','u','Rw','r','u','R','U','rw','U','Rw']),
               ([1,1,1,1,2,0,1,0], ['F','r','u2','Rw','u','f2','U','rw','u2','R','f']),
               ([1,1,1,1,2,1,0,0], ['y','f','r','u','R','dw','R','u2','R','f','r','F']),
               ([1,1,1,1,2,0,0,1], ['R','u2','f','r','u','R','U','Y','r2','u2','r','b']),
               ([1,1,1,1,0,0,0,0], ['r','b','u','B','R','f2','b','D','L','d','B','f2']), #20
               ([0,0,0,0,2,1,2,1], ['r','u','R','u','r','U','R','u','r','u2','R']),
               ([0,0,0,0,2,1,1,2], ['r','u2','r2','U','r2','U','r2','u2','r']),
               ([0,0,0,0,0,2,1,0], ['r2','D','r','u2','R','d','r','u2','r']),
               ([0,0,0,0,1,2,0,0], ['l','f','R','F','L','f','r','F']),
               ([0,0,0,0,2,0,1,0], ['R','F','L','f','r','F','l','f']), #25
               ([0,0,0,0,1,1,1,0], ['y2','R','U','r','U','R','u2','r']),
               ([0,0,0,0,0,2,2,2], ['r','u','R','u','r','u2','R']),
               ([1,0,0,1,0,0,0,0], ['rw','u','R','U','Rw','r','u','r','U','R']),
               ([0,0,1,1,2,0,0,1], ['X','U','R','u','L','U','r2','U','R','u2','rw']),
               ([0,1,1,0,2,0,0,1], ['y2','F','l','u','l2','u','l2','u2','L','u','f']), #30
               ([0,0,1,1,0,0,1,2], ['y2','R','U','f','u','r','U','R','F','r']),
               ([0,1,1,0,1,2,0,0], ['r','u','B','U','R','u','r','b','R']),
               ([1,0,1,0,1,2,0,0], ['r','u','R','U','R','f','r','F']),
               ([1,0,1,0,0,1,2,0], ['r','u','R','Dw','Lw','U','l','u','Rw','r']),
               ([0,1,1,0,1,0,2,0], ['r','u2','r2','f','r','F','r','u2','R']), #35
               ([0,0,1,1,1,0,2,0], ['r','u','R','U','F','u2','f','u','r','u','R']),
               ([0,0,1,1,0,2,0,1], ['y','R','f','r','F','U','F','u','f']),
               ([0,1,1,0,0,1,0,2], ['y2','r','u','R','u','r','U','R','U','R','f','r','F']), #says optimal 10 this is 12
               ([1,0,1,0,0,2,0,1], ['l','F','L','U','l','u','f','U','L']),
               ([1,0,1,0,2,0,1,0], ['R','f','r','u','R','U','F','u','r']), #40
               ([0,1,1,0,1,0,0,2], ['y2','r2','l','Z','Lw','U','r','dw','l','U','l','Lw']),
               ([0,0,1,1,1,0,0,2], ['y2','l2','R','z','rw','u','L','Dw','R','u','R','rw']),
               ([0,0,1,1,0,0,2,1], ['Fw','L','U','l','u','fw']),
               ([0,1,1,0,2,1,0,0], ['y2','f','u','r','U','R','F']),
               ([1,0,1,0,2,1,0,0], ['f','r','u','R','U','F']), #45
               ([0,1,0,1,0,0,2,1], ['R','U','R','f','r','F','u','r']),
               ([1,1,0,0,1,2,2,1], ['F','L','U','l','u','L','U','l','u','f']),
               ([1,0,0,1,2,1,1,2], ['f','r','u','R','U','r','u','R','U','F']),
               ([0,0,1,1,1,2,2,1], ['r','B','r2','f','r2','b','r2','F','r']),
               ([0,1,1,0,2,1,1,2], ['y2','R','f','r2','B','r2','F','r2','b','R']), #50
               ([1,0,1,0,1,2,2,1], ['f','u','r','U','R','u','r','U','R','F']),
               ([0,1,0,1,1,2,2,1], ['R','U','r','U','R','dw','R','u','r','b']),
               ([1,0,0,1,2,1,2,1], ['Lw','U','l','U','L','u','l','U','L','u2','lw']),
               ([1,1,0,0,2,1,2,1], ['y2','f','R','F','r','u2','f2','l','f','L','f']),
               ([0,1,0,1,2,1,2,1], ['r','u2','r2','U','r','U','R','u2','f','r','F']), #55
               ([1,0,1,0,2,1,2,1], ['f','r','u','R','U','r','F','rw','u','R','U','Rw']),
               ([1,0,1,0,0,0,0,0], ['r','u','R','U','rw','R','u','r','U','Rw']) ]

                #string encoding is 34 33 32 18 17 16 42 41 40 26 25 24
    pllMap = [ ('fbflrlbfbrlr', ['l','r','u2','L','R','F','B','u2','f','b']), #H perm
               ('ffflrlblbrbr', ['y2','f2','U','l','R','f2','L','r','U','f2']), #U Perm
               ('ffflblbrbrlr', ['y2','f2','u','x','R','l','u2','X','r','L','u','f2']), #b
               ('frflblblbrfr', ['x2','r2','l2','u','x2','r2','l2','u','x2','r2','l2','f2','x2','r2','l2','f2','u2']), #z perm
               ('bffllbrbrfrl', ['x','R','u','R','d2','r','U','R','d2','r2']), #A Perm
               ('rfrfllbbflrb', ['x','r','D','r','u2','R','d','r','u2','r2']),
               ('lfrflbrblbrf', ['x','u','R','U','l','u','r','U','rw','rw','U','r','u','l','U','R','u','x']), #E perm
               ('ffflrbrblblr', ['R','u','r','U','r2','F','U','f','u','r','f','R','F','r2','U']), #F perm
               ('lblbfrflbrrf', ['y','r2','uw','R','u','R','U','r','Uw','r2','Y','R','u','r']), #G perm
               ('blrfbflfbrrl', ['y','F','U','f','r2','uw','R','u','r','U','r','Uw','r2']),
               ('rbrfllbrflfb', ['y','r2','Uw','r','U','r','u','R','uw','r2','b','U','B']),
               ('lrbrllbfrfbf', ['y2','r','u','R','Y','r2','Uw','r','U','R','u','R','uw','r2']),
               ('fllbfflbbrrr', ['y2','x','r2','f','r','F','r','u2','Rw','u','rw','u2']), #J perm
               ('rrflllbbrffb', ['y2','f2','r','u','R','f2','l','D','l','d','l2']),
               ('ffbrrlbbfllr', ['r','U','l','u2','R','u','L'] * 2), #N perm
               ('bfflrrfbbrll', ['z'] + ['U','r','D','r2','u','R','d'] * 2 + ['Z']),
               ('lfrfllbrbrbf', ['r','u2','R','u2','r','B','R','U','r','u','r','b','r2','u']), #R Perm
               ('frfllbrblbfr', ['Z','U','l2','u','l2','U','f','u','l','U','L','U','F','u2','z']),
               ('rfflrlbbrflb', ['r','u','R','U','R','f','r2','U','R','U','r','u','R','F']), # T Perm
               ('bffllrfrbrbl', ['R','u','R','U','y','R','F','r2','U','R','u','R','f','r','f']), #V perm
               ('bfflbrflbrrl', ['r2','U','R','u','r','U','x','D','R','u','R','U','R','d','r'])] #y perm



    





    @classmethod
    def solve(cls, originalCube):
        #Return a string with shortest possible solution
        originalCube.solution = []
        cubes = [originalCube.copy()]
        cubesAfterCross = cls.bestCross(cubes)
        print("cross complete" + str(len(cubesAfterCross)))
        cubesAfterF2l = cls.bestF2l(cubesAfterCross)
        print("f2l complete" + str(len(cubesAfterF2l)))
        cubesAfterOLL = cls.bestOLL(cubesAfterF2l)
        print("oll complete" + str(len(cubesAfterOLL)))
        solvedCubes = cls.bestPLL(cubesAfterOLL)
        print("pll complete" + str(len(solvedCubes)))
        shortest = cls.reduceAxes(solvedCubes[0].solution)
        for cube in solvedCubes:
            cube.solution = cls.reduceAxes(cube.solution)
            cube.reduceSolution()
            sol = cube.solution
            if len(sol) < len(shortest):
                shortest = sol
            #print(sol)
            #cube.prettyPrint()
        print("solutions reduced")
        print(f'shortest with len {len(shortest)} is:')
        print(shortest)
        return shortest

    @classmethod
    def bestPLL(cls, cubes):
        outCubes = []
        for cube in cubes:
            count = 0
            while cube.isSolved() == False:
                cube.move('u')
                for i in range(4):
                    pStr = cube.getPString()
                    for combo in cls.pllMap:
                        if pStr == combo[0]:
                            cube.moves(combo[1])
                            break
                    cube.move('y')
                count += 1
                if count == 8:
                    cube.prettyPrint()
                    raise Exception("no PLL case match, cases should be complete.")
                    exit()
            cube.reduceSolution()
            outCubes.append(cube)
        return outCubes
        

    @classmethod
    def bestOLL(cls, cubes):
        outCubes = []
        for cube in cubes:
            count = 0
            while cube.isOLLSolved() == False:
                cube.move('y')
                oList = cube.getOList()
                for combo in cls.ollMap:
                    if oList == combo[0]:
                        for move in combo[1]:
                            cube.move(move)
                        if cube.isOLLSolved() == False:
                            print(combo)
                            cube.prettyPrint()
                            raise Exception("Move error on OLL")
                            exit()
                        break
                count += 1
                if count == 5:
                    print("ERROR no OLL case match. Cases should be complete.")
                    cube.prettyPrint()
                    raise Exception("no OLL case match. cases should be complete.")
                    exit()
            cube.reduceSolution()
            outCubes.append(cube)
        return outCubes


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
            if cube.isSolved():
                print('f2l solution')
                return outCubes
        lengths = [cube.getCompLength() for cube in outCubes]
        print(outCubes)
        print(lengths)
        average = sum(lengths) // len(lengths)
        lengths.sort()
        mean = lengths[len(lengths)//4]
        average = mean if mean < average else average
        newOutCubes = []
        for cube in outCubes:
            if cube.getCompLength() < average:
                newOutCubes.append(cube)
        if len(newOutCubes) == 0:
            for cube in outCubes:
                if cube.getCompLength() == average:
                    newOutCubes.append(cube)
                    break
        return newOutCubes

    @classmethod
    def expandSearch(cls, cubes, depth):
        if depth == 0:
            return cubes
        htms = ['f','F','f2','u','U','u2','l','L','l2','r','R','r2','d','D','d2','b','B','b2']
        outCubes = []
        count = 0
        for cube in cubes:
            if count % 100 == 0:
                print(count)
            for move in htms:
                newCube = cube.copy()
                newCube.move(move)
                outCubes.append(newCube)
        return cls.expandSearch(outCubes, depth-1)
            
        
        

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
        inCubes = cls.expandSearch(inCubes, 1)
        print(len(inCubes))
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
            if cube.isSolved():
                print('cross solution')
                return outCubes
        #Add culling here later if desired
        lengths = [cube.getCompLength() for cube in outCubes]
        print(lengths)
        average = sum(lengths) // len(lengths)
        lengths.sort()
        mean = lengths[len(lengths)//4] #this is the median? lol
        average = mean if mean < average else average
        newOutCubes = []
        for cube in outCubes:
            if cube.getCompLength() < average:
                newOutCubes.append(cube)
        if len(newOutCubes) == 0:
            for cube in outCubes:
                if cube.getCompLength() == average:
                    newOutCubes.append(cube)
                    break
                    
        return newOutCubes

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
    

