import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
warnings.filterwarnings("ignore", message='No handlers could be found for logger "chess.engine"')

from sys import stdout
import random

import chess
import chess.uci
import chess.pgn
 
pieces = ["p","p","k","q","r","b","n",
          "P","P","P","K","R","B","Q","N"]

piecesCopy = list(pieces)

f = open("positions.txt", "a")
 
def check_king(brd, c, r):
    for j in range(-1, 1):
        for i in range(-1, 1):
            cc = c + i
            rr = r + j
            if -1 < cc < 8 and -1 < rr < 8:
                pc = brd[cc + rr * 8]
                if pc == "k" or pc == "K":
                    return 1
    return 0
 
 
def generate_board():
    for i in range(10):
        n = len(pieces) - 1
        while n > 0:
            pt = random.randrange(n)
            tp = pieces[n]
            pieces[n] = pieces[pt]
            pieces[pt] = tp
            n -= 1
 
    board = [0 for i in range(64)]
    while len(pieces) > 1:
        pc = pieces[0]
        pieces.pop(0)
        while 1:
            c = random.randrange(8)
            r = random.randrange(8)
            if ((r == 0 or r == 7) and (pc == "P" or pc == "p")) or ((pc == "k" or pc == "K") and 1 == check_king( board, c, r)):
                continue
            if board[c + r * 8] == 0:
                break
        board[c + r * 8] = pc
 
    return board
 
 
def start():
    global pieces, piecesCopy
    validBoard = False
    while validBoard == False:
        try:
            brd = generate_board()
            e = 0
            x = ""
            for j in range(8):
                for i in range(8):
                    if brd[i + j * 8] == 0:
                        e += 1
                    else:
                        if e > 0:
                            x+= str(e)
                            e = 0
                        x+=brd[i + j * 8]
                if e > 0:
                    x+= str(e)
                    e = 0
                if j < 7:
                    x+= "/"
            if random.random() > 0.5:
                x+=" w - - 0 1"
                #1 = White to move
                move = "1"
            else:
                x+=" b - - 0 1"
                move = "0"
            board = chess.Board(x)
            #Now we have our board ready, load your engine:
            handler = chess.uci.InfoHandler()
            engine = chess.uci.popen_engine('Stockfish/src/stockfish') #give correct address of your engine here
            engine.info_handlers.append(handler)
            #give your position to the engine:
            engine.position(board)
            #Set your evaluation time, in ms:
            evaltime = 2000 #so 2 seconds
            evaluation = engine.go(movetime=evaltime)
            score = handler.info["score"][1].cp/100.0
            validBoard = True
        except:
            validBoard = False
        finally:
            pieces = list(piecesCopy)

    print x,
    x = ""
    for j in range (8):
        for i in range (8):
            letter = brd[i + j * 8]
            if letter == 0:
                x += "0, "
            else:
                if letter == "P":
                    x += "10, "
                elif letter == "p":
                    x += "-10, "
                elif letter == "N":
                    x += "30, "
                elif letter == "n":
                    x += "-30, "
                elif letter == "B":
                    x += "35, "
                elif letter == "b":
                    x += "-35, "
                elif letter == "R":
                    x += "50, "
                elif letter == "r":
                    x += "-50, "
                elif letter == "Q":
                    x += "100, "
                elif letter == "q":
                    x += "-100, "
                elif letter == "K":
                    x += "1000, "
                elif letter == "k":
                    x += "-1000, "
    x+= str(move)+", "
    x+= str(score)
    #print best move, evaluation and mainline:
    print score
    f.write(x + "\n")
                
 
# entry point
start()
f.close()

