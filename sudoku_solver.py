from functools import reduce
from collections import defaultdict
import argparse
import json
import os

# Default puzzle (used when no input is provided)
DEFAULT_PUZZLE = [
    [0, 0, 3, 0, 0, 0, 0, 0, 1],
    [0, 9, 0, 0, 3, 5, 2, 6, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 0, 0, 1, 8, 6],
    [1, 3, 0, 8, 6, 0, 7, 2, 5],
    [2, 8, 6, 0, 0, 0, 9, 4, 3],
    [0, 4, 1, 0, 8, 0, 3, 0, 0],
    [0, 5, 0, 2, 0, 6, 0, 1, 0],
    [0, 0, 0, 0, 0, 3, 0, 7, 0]
]

puzzle = [row[:] for row in DEFAULT_PUZZLE]


# ============================================================================
# INPUT METHODS
# ============================================================================

def load_from_file(filepath):
    """
    Load a puzzle from a text or JSON file.
    
    Text format (9 lines, 9 digits each, 0 = empty):
        003000001
        090035268
        ...
    
    JSON format:
        {"puzzle": [[0,0,3,...], ...]}
        or just: [[0,0,3,...], ...]
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, 'r') as f:
        content = f.read().strip()
    
    # Try JSON first
    if filepath.endswith('.json'):
        data = json.loads(content)
        if isinstance(data, dict) and 'puzzle' in data:
            return data['puzzle']
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("Invalid JSON format. Expected a 2D array or {'puzzle': [...]}")
    
    # Parse as text file
    lines = content.split('\n')
    grid = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Handle space-separated or continuous digits
        if ' ' in line or ',' in line:
            row = [int(x) for x in line.replace(',', ' ').split()]
        else:
            row = [int(c) for c in line if c.isdigit()]
        if len(row) == 9:
            grid.append(row)
    
    if len(grid) != 9:
        raise ValueError(f"Invalid puzzle format. Expected 9 rows, got {len(grid)}")
    
    return grid


def interactive_input():
    """
    Interactively prompt the user to enter a puzzle row by row.
    """
    print("\n🧩 Enter your Sudoku puzzle")
    print("   Use 0 for empty cells")
    print("   Enter 9 digits per row (spaces optional)\n")
    
    grid = []
    for i in range(9):
        while True:
            try:
                line = input(f"   Row {i + 1}: ").strip()
                # Handle space-separated or continuous digits
                if ' ' in line or ',' in line:
                    row = [int(x) for x in line.replace(',', ' ').split()]
                else:
                    row = [int(c) for c in line if c.isdigit()]
                
                if len(row) != 9:
                    print(f"   ⚠️  Please enter exactly 9 digits (got {len(row)})")
                    continue
                if not all(0 <= x <= 9 for x in row):
                    print("   ⚠️  Digits must be between 0-9")
                    continue
                grid.append(row)
                break
            except ValueError:
                print("   ⚠️  Invalid input. Use digits 0-9 only.")
    
    print("\n   ✅ Puzzle loaded successfully!\n")
    return grid


def print_puzzle(grid, title="Puzzle"):
    """Pretty print the puzzle grid."""
    print(f"\n   {title}:")
    print("   ┌───────┬───────┬───────┐")
    for i, row in enumerate(grid):
        if i > 0 and i % 3 == 0:
            print("   ├───────┼───────┼───────┤")
        row_str = "   │"
        for j, val in enumerate(row):
            if j > 0 and j % 3 == 0:
                row_str += " │"
            display = str(val) if val != 0 else "·"
            row_str += f" {display}"
        row_str += " │"
        print(row_str)
    print("   └───────┴───────┴───────┘\n")

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
    """Find all possible candidates for each empty cell."""
    markupDict = defaultdict(list)
    ret = [False, False, False]
    for row in range(9):
        for col in range(9):
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
    """Get all positions in the 3x3 box containing the given position."""
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
        # No new preemptive set found
        pass
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
                for i in tempList1:
                    if (i[0],i[1]) in list(markUpDict.keys()) and i not in preemptivePositionsTuplesList and i not in genMarkUpList:
                        genMarkUpList.append(i)
        #when peemptive triplet :
        elif len(preemptiveDict[preemptiveMarkUpList[0]]) == 3:
            tempList1 = boxList(preemptiveDict[preemptiveMarkUpList[0]][0])
            tempList2 = boxList(preemptiveDict[preemptiveMarkUpList[0]][1])
            tempList3 = boxList(preemptiveDict[preemptiveMarkUpList[0]][2])
            if tempList1 == tempList2 and tempList1 == tempList3:
                for i in tempList1:
                    if (i[0],i[1]) in list(markUpDict.keys()) and i not in preemptivePositionsTuplesList and i not in genMarkUpList:
                        genMarkUpList.append(i)
        #when preemptive quad :
        elif len(preemptiveDict[preemptiveMarkUpList[0]]) == 4:
            tempList1 = boxList(preemptiveDict[preemptiveMarkUpList[0]][0])
            tempList2 = boxList(preemptiveDict[preemptiveMarkUpList[0]][1])
            tempList3 = boxList(preemptiveDict[preemptiveMarkUpList[0]][2])
            tempList4 = boxList(preemptiveDict[preemptiveMarkUpList[0]][3])
            if tempList1 == tempList2 and tempList1 == tempList3 and tempList3 == tempList4:
                for i in tempList1:
                    if (i[0],i[1]) in list(markUpDict.keys()) and i not in preemptivePositionsTuplesList and i not in genMarkUpList:
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
def solve_puzzle(verbose=False):
    """
    Main solving function that applies all techniques.
    Returns True if puzzle is solved, False otherwise.
    """
    global puzzle
    
    # Finding markup cells
    markUpDict = findMarkupCells()
    
    # Update cells with single candidates (naked singles)
    for key in markUpDict:
        if len(markUpDict[key]) == 1:
            i, j = key[0], key[1]
            puzzle[i][j] = markUpDict[key][0]
            markUpDict = findMarkupCells()
    
    # Apply naked pair technique multiple times
    for _ in range(5):
        findNakedPair(markUpDict)
    
    # Check if solved
    solved = all(puzzle[i][j] != 0 for i in range(9) for j in range(9))
    return solved


def main():
    """Main entry point with CLI argument parsing."""
    global puzzle
    
    parser = argparse.ArgumentParser(
        description="🧩 Sudoku Solver - Solve puzzles using human-like techniques",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sudoku_solver.py                      # Use default puzzle
  python sudoku_solver.py -i                   # Interactive input
  python sudoku_solver.py puzzle.txt           # Load from text file
  python sudoku_solver.py puzzle.json          # Load from JSON file

File formats:
  Text file (9 lines, 9 digits each, 0 = empty):
    003000001
    090035268
    ...

  JSON file:
    {"puzzle": [[0,0,3,...], ...]}
    or: [[0,0,3,...], ...]
        """
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='Path to puzzle file (text or JSON format)'
    )
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Enter puzzle interactively'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed solving steps'
    )
    
    args = parser.parse_args()
    
    # Determine input method
    try:
        if args.interactive:
            puzzle = interactive_input()
        elif args.file:
            print(f"\n   📂 Loading puzzle from: {args.file}")
            puzzle = load_from_file(args.file)
            print("   ✅ Puzzle loaded successfully!\n")
        else:
            print("\n   ℹ️  No input provided. Using default puzzle.")
            print("   💡 Tip: Use -i for interactive mode or provide a file path.\n")
            puzzle = [row[:] for row in DEFAULT_PUZZLE]
    except FileNotFoundError as e:
        print(f"\n   ❌ Error: {e}")
        return 1
    except (ValueError, json.JSONDecodeError) as e:
        print(f"\n   ❌ Error parsing puzzle: {e}")
        return 1
    
    # Show input puzzle
    print_puzzle(puzzle, "Input Puzzle")
    
    # Solve
    print("   🔄 Solving...\n")
    solved = solve_puzzle(verbose=args.verbose)
    
    # Show result
    if solved:
        print_puzzle(puzzle, "✅ Solved Puzzle")
    else:
        print_puzzle(puzzle, "⏳ Partial Solution")
        print("   ⚠️  Could not fully solve with current techniques.")
        print("   💡 This puzzle may require backtracking (not yet implemented).\n")
    
    return 0


if __name__ == "__main__":
    exit(main())







