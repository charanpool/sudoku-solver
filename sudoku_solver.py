from functools import reduce
from collections import defaultdict
import difflib
import pprint
'''
puzzle = [[8, 0, 0, 0, 0, 0, 3, 9, 7],
          [0, 0, 0, 0, 0, 7, 6, 0, 0],
          [0, 7, 0, 8, 0, 0, 0, 0, 4],
          [0, 0, 0, 6, 5, 2, 1, 0, 0],
          [0, 2, 6, 0, 3, 1, 0, 0, 8],
          [0, 1, 5, 9, 0, 0, 0, 2, 0],
          [1, 9, 7, 2, 8, 0, 4, 6, 0],
          [0, 0, 0, 4, 0, 0, 9, 7, 0],
          [2, 0, 0, 3, 0, 0, 8, 1, 0]
          ]

puzzle = [[5, 9, 7, 0, 4, 0, 0, 3, 0],
          [3, 4, 8, 0, 0, 0, 0, 6, 0],
          [6, 1, 2, 0, 9, 0, 0, 8, 4],
          [7, 5, 0, 0, 0, 0, 4, 9, 0],
          [8, 0, 9, 0, 0, 0, 0, 7, 0],
          [4, 0, 0, 6, 0, 0, 0, 5, 0],
          [1, 7, 0, 0, 2, 0, 6, 4, 0],
          [9, 6, 0, 0, 8, 3, 0, 2, 0],
          [2, 8, 0, 0, 0, 0, 0, 1, 0]
         ]

'''
puzzle = [[0,0,3,0,0,0,0,0,1],
          [0,9,0,0,3,5,2,6,8],
          [0,0,0,0,0,0,0,0,0],
          [0,7,0,0,0,0,1,8,6],
          [1,3,0,8,6,0,7,2,5],
          [2,8,6,0,0,0,9,4,3],
          [0,4,1,0,8,0,3,0,0],
          [0,5,0,2,0,6,0,1,0],
          [0,0,0,0,0,3,0,7,0]
         ]

#markUpDict = defaultdict(list)

def checkInRow(row, value):
    if value in row:
        return True

    return False

def checkInCol(col, value):
    if value in col:
        return True
    return False

def checkInBox(box, value):
    box = reduce(lambda x, y :x+y, box)

    if value in box:
        return True

    return False

def getCol(ipList, col):
    return list(map(lambda x : x[col], ipList))

def getBox(ip, i, j):
    box = []
    row = i % 3
    row = i - row
    col = j % 3
    col = j - col

    for k in range(3):
        box.append(ip[row + k][col:col + 3])
    return box

def findMarkupCells():
    markupDict = defaultdict(list)
    ret = [False, False, False]
    for row in range(9):
        for col in range(9):
            print("-----------------------",row, col, puzzle[row][col])
            if puzzle[row][col] == 0:
                currentCol = getCol(puzzle, col)
                box = getBox(puzzle, row, col)
                for i in range(1, 10):
                    ret[0] = checkInRow(puzzle[row], i)
                    ret[1] = checkInCol(currentCol, i)
                    ret[2] = checkInBox(box, i)

                    if True in ret:
                        pass
                    else:
                        markupDict[(row, col)].append(i)
    return markupDict

def rangeOfPrimitiveSets(index):
    #print(index)
    possibleList = []
    for k in range(0, 9):
        t = (index[0], k)
        possibleList.append(t)

    for k in range(0, 9):
        t = (k, index[1])
        if k != index[0]:
            possibleList.append(t)

    i = index[0] - (index[0] % 3)
    j = index[1] - (index[1] % 3)

    for l in range(0, 3):
        for k in range(0, 3):
            t = (i + l, j + k)
            if t not in possibleList:
                possibleList.append(t)
    return possibleList

def hidden_single(markUpDict):
    #traversing for rows only
    count = [0] * 9
    for i in range(9):      #for row wise traversing
        for j in range(9):  #for column wise traversing
            if puzzle[i][j] == 0:
                for val in markUpDict[(i, j)]:
                    count[val-1] += 1  #incrementing respective position in markUpDict
        #count indicates no of times that (index + 1) number is present in that row by count[index]
        #after traversing that row:
        for countIndex in range(9):
            if count[countIndex] == 1:
                #countIndex is the number that is hidden_single
                for k in range(9):  #traversing through entire row again and finding presence of hidden_single
                    if countIndex in markUpDict[(i, k)]:
                        puzzle[i][k] = countIndex
                        break
        count = [0] * 9

    #travesing for columns only
    count = [0] * 9
    for i in range(9):  #column
        for j in range(9):  #row
            if puzzle[j][i] == 0:
                for val in markUpDict[(j, i)]:
                    count[val-1] += 1
        for countIndex in range(9):
            if count[countIndex] == 1:
                #countIndex is that hidden_single
                for k in range(9):
                    if countIndex in markUpDict[(k, i)]:
                        puzzle[k][i] = countIndex
                        break
        count = [0] * 9

    #traversing through each box seperately
    count = [0] * 9
    for i in range(3):
        for j in range(3):
            tempBoxList = boxList((i*3, j*3))
            for position in tempBoxList:    #position is a tuple representing a position
                if puzzle[position[0]][position[1]] == 0:
                    for val in markUpDict[(position[0], position[1])]:
                        count[val-1] += 1
            for countIndex in range(9):
                if count[countIndex] == 1:
                    #traversing through that particual 3x3 block
                    for tempRow in range(3):
                        for tempCol in range(3):
                            if countIndex in markUpDict[(tempRow, tempCol)]:
                                puzzle[tempRow][tempCol] = countIndex
                                break;
        count = [0] * 9

    #calling update_markUp after finding all the hidden_singles
    update_puzzle_from_markup(markUpDict)




def findNakedPair(markUpDict):
    nakedPair = defaultdict(list)
    for key in markUpDict:
        if len(markUpDict[key]) == 3:
            #print(key)
            possibleList = rangeOfPrimitiveSets(key)
            #print(possibleList)
            #exit(0)
            for pos in possibleList:
                if pos in markUpDict.keys():
                    if pos != key:
                    #if 1:
                        if set(markUpDict[pos]) <= set(markUpDict[key]):
                            #print("-------------------",markUpDict[pos], markUpDict[key], pos, key)
                            nakedPair[tuple(markUpDict[key])].append(pos)
                            nakedPair[tuple(markUpDict[key])].append(key)
                            occupancy_update(markUpDict, nakedPair)
                            markUpDict = update_puzzle_from_markup(markUpDict)
                            nakedPair.clear()
                            break
    print(markUpDict)
    #print(puzzle)
    '''
    for i in range(0, 9):
        for j in range(0, 9):
            print(puzzle[i][j], end = " ")
        print()
    exit(0)
    for key in list(nakedPair):
        if len(key) != len(nakedPair[key]):
            #print("-----", key ,nakedPair[key])
            nakedPair.pop(key, None)
            #del nakedSingle[key]
    #print(nakedPair)
    '''
    #return markUpDict
'''
def occupancyTheorem(markupDict, nakedPair):
    #Remove naked pair elements from row, column and box
    print(nakedPair)
    for key in nakedPair.keys():
        posList = nakedPair[key]
        if posList[0][0] == posList[1][0]:
            row = posList[0][0]
            for i in markUpDict.keys():
                if (i[0] == row):
                    if set(markUpDict[i]) <= set(key ):
                        for value in key:
                            markUpDict[i].remove(value)
                            #del markUpDict[i][]
'''

def boxList(pos):
    print(pos)
    print(type(pos))
    rowSet = int(pos[0] / 3)
    columnSet = int(pos[1] / 3)
    tempList = []
    for i in range(3):
        for j in range(3):
            tempList.append((((rowSet * 3) + i), ((columnSet * 3) + j)))
    return tempList

def occupancy_update(markUpDict, preemptiveDict):
    boxSelect = 0
    rowSelect = 0
    columnSelect = 0
    if len(preemptiveDict) == 0:
        print("no new preemptive set found")
        #call for assumption
    else:
        #print(preemptiveDict)
        preemptiveMarkUpList = list(preemptiveDict.keys())
        #print(type(preemptiveMarkUpList))
        #print("--------------",preemptiveMarkUpList)
        preemptivePositionsTuplesList = preemptiveDict[preemptiveMarkUpList[0]]
        row = preemptivePositionsTuplesList[0][0]
        column = preemptivePositionsTuplesList[0][1]
        for i in preemptivePositionsTuplesList:
            if i[0] != row:
                column = -1
            if i[1] != column:
                row = -1
            if row == -1 and column == -1:
                break
        if row == -1 and column == -1:
            #select particular 3x3 block
            boxSelect = 1
        elif row == -1:
            #select that particular column
            rowSelect = 1
        elif column == -1:
            #select that particular row
            columnSelect = 1
        #generating a list of all the positional markUps that are to be updated
        genMarkUpList = []    #list of positions whose values are to be updated eliminating preemption
        if rowSelect == 1:
            row = preemptivePositionsTuplesList[0][0]
            print("row :",row)
            for i in range(0, 9):
                if puzzle[row][i] == 0 and (row,i) not in preemptivePositionsTuplesList:
                    genMarkUpList.append((row, i))
        elif columnSelect == 1:
            column = preemptivePositionsTuplesList[0][1]
            for i in range(0, 9):
                if puzzle[i][column] == 0 and (i,column) not in preemptivePositionsTuplesList:
                    genMarkUpList.append((i, column))
        elif boxSelect == 1:
            #print(preemptiveDict[preemptiveMarkUpList[0]][0])
            tempList = boxList(preemptiveDict[preemptiveMarkUpList[0]][0])
            for i in tempList:
                if puzzle[i[0]][i[1]] == 0 and i not in preemptivePositionsTuplesList:
                    genMarkUpList.append(i)

        #if preemptive sets are in same box and satisfying row or column condition then updating that box

        #when preemptive pair :
        if len(preemptiveDict[preemptiveMarkUpList[0]]) == 2:
            tempList1 = boxList(preemptiveDict[preemptiveMarkUpList[0]][0])
            tempList2 = boxList(preemptiveDict[preemptiveMarkUpList[0]][1])
            if tempList1 == tempList2:
                print("box satisfying ", tempList1)
                for i in tempList1:
                    if (i[0],i[1]) in list(markUpDict.keys()) and i not in preemptivePositionsTuplesList and i not in genMarkUpList:
                        print("tuple extra added since it is present in box :", (i[0], i[1]))
                        genMarkUpList.append(i)
        #when peemptive triplet :
        elif len(preemptiveDict[preemptiveMarkUpList[0]]) == 3:
            tempList1 = boxList(preemptiveDict[preemptiveMarkUpList[0]][0])
            tempList2 = boxList(preemptiveDict[preemptiveMarkUpList[0]][1])
            tempList3 = boxList(preemptiveDict[preemptiveMarkUpList[0]][2])
            if tempList1 == tempList2 and tempList1 == tempList3:
                print("box satisfying ", tempList1)
                for i in tempList1:
                    if (i[0],i[1]) in list(markUpDict.keys()) and i not in preemptivePositionsTuplesList and i not in genMarkUpList:
                        print("tuple extra added since it is present in box :", (i[0], i[1]))
                        genMarkUpList.append(i)
        #when preemptive quad :
        elif len(preemptiveDict[preemptiveMarkUpList[0]]) == 4:
            tempList1 = boxList(preemptiveDict[preemptiveMarkUpList[0]][0])
            tempList2 = boxList(preemptiveDict[preemptiveMarkUpList[0]][1])
            tempList3 = boxList(preemptiveDict[preemptiveMarkUpList[0]][2])
            tempList4 = boxList(preemptiveDict[preemptiveMarkUpList[0]][3])
            if tempList1 == tempList2 and tempList1 == tempList3 and tempList3 == tempList4:
                print("box satisfying ", tempList1)
                for i in tempList1:
                    if (i[0],i[1]) in list(markUpDict.keys()) and i not in preemptivePositionsTuplesList and i not in genMarkUpList:
                        print("tuple extra added since it is present in box :", (i[0], i[1]))
                        genMarkUpList.append(i)

        #updating the markups
        for i in genMarkUpList:    #'i' will hold a tuple or position
            for j in list(preemptiveDict.keys())[0]:    #'j' will hold the value of a list(mark up list), that is obtained from marUpDict{} dictonary
                if j in markUpDict[(i[0], i[1])]:
                    markUpDict[(i[0], i[1])].remove(j)
        #print(markUpDict)
    #update_puzzle_from_markup(markUpDict)
    #markUpDict = update_puzzle_from_markup(markUpDict)
    #return markUpDict

def update_puzzle_from_markup(markUpDict):
    for i in list(markUpDict.keys()):
        if len(markUpDict[i]) == 1:
            puzzle[i[0]][i[1]] = markUpDict[i][0]
            #del markUpDict[i]
            #markUpDict.clear()
            tempmarkUpDict = findMarkupCells()
            markUpDict = tempmarkUpDict.copy()
    return markUpDict
def compare_dicts(d1, d2):
    print("here111111111")
    return ('\n' + '\n'.join(difflib.ndiff(
                   pprint.pformat(d1).splitlines(),
                   pprint.pformat(d2).splitlines())))
if __name__ == "__main__":
    #Finding markup cells
    markUpDict = findMarkupCells()
    #Update the markup cell which contain single value
    for key in markUpDict:
        if len(markUpDict[key]) == 1:
            i, j = key[0], key[1]
            puzzle[i][j] = markUpDict[key][0]
            markUpDict = findMarkupCells()

    #print("Markup Dict :",markUpDict)
    ##nakedPairDict = findNakedPair(markUpDict)
    #print("Naked Pair : ",nakedPairDict)
    print(markUpDict)
    dupMarkupDict = defaultdict(list)
    dupMarkupDict = markUpDict.copy()
    count = 0
    findNakedPair(markUpDict)
    findNakedPair(markUpDict)
    findNakedPair(markUpDict)
    findNakedPair(markUpDict)
    findNakedPair(markUpDict)
    '''
    while True:
        returnBoolList = [False] * 9
        for i in range(9):
            if 0 in puzzle[i]:
                returnBoolList[0] = True
        for i in range(0, 9):
            for j in range(0, 9):
                print(puzzle[i][j], end = " ")
            print()
        if True in returnBoolList:
            findNakedPair(markUpDict)
        else:
            break
    '''
    #findNakedPair(markUpDict)

    #print(puzzle)
    for i in range(0, 9):
        for j in range(0, 9):
            print(puzzle[i][j], end = " ")
        print()
    print(markUpDict)
    exit(0)
    while True:
        findNakedPair(markUpDict)
        print("markupDict:    ",markUpDict)
        print("dupMarkupDict :", dupMarkupDict)
        compare_dicts(markUpDict, dupMarkupDict)
        if markUpDict == dupMarkupDict:
            break
        dupMarkupDict = markUpDict.copy()
        count += 1


    '''
        print("1st time naked pair : ", tempNakedPairDict)
        print("1st time passnaked ::", passNakedPairDict)
        if passNakedPairDict == tempNakedPairDict:
            break
        passNakedPairDict = tempNakedPairDict.copy()
        #print("hello", passNakedPairDict)
        for i in tempNakedPairDict.keys():
            tempDict = {}
            tempDict[i] = tempNakedPairDict[i]
            print(tempDict)
            occupancy_update(markUpDict, tempDict)
        count += 1
        #code to update puzzle
        update_puzzle_from_markup(markUpDict)
        '''
    print("count ::",count)


    #print(puzzle)
    for i in range(0, 9):
        for j in range(0, 9):
            print(puzzle[i][j], end = " ")
        print()
    print(markUpDict)







