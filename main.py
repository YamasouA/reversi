import tkinter

BLACK = 1
WHITE = 2

board = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 1, 0, 0, 0],
    [0, 0, 0, 1, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

def click(e):
    mx = int(e.x/80)
    my = int(e.y/80)
    if mx > 7: mx = 7
    if my > 7: my = 7
    if board[my][mx] == 0:
        ishi_utsu(mx, my, BLACK)
    banmen()


def banmen():
    cvs.delete("all")
    for y in range(8):
        for x in range(8):
            X = x*80
            Y = y*80
            cvs.create_rectangle(X, Y, X+80, Y+80, outline="black")
            if board[y][x] == BLACK:
                cvs.create_oval(X+10, Y+10, X+70, Y+70, fill="black", width=0)
            elif board[y][x] == WHITE:
                cvs.create_oval(X+10, Y+10, X+70, Y+70, fill="white", width=0)
            if kaeseru(x, y, BLACK) > 0:
                cvs.create_oval(X+5, Y+5, X+75, Y+75, outline="cyan", width=2)
    cvs.update()

#石を打って相手の石を返す
def ishi_utsu(x, y, iro):
    board[y][x] = iro
    #8方向を探索する
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            k = 0
            sx = x
            sy = y
            while True:
                sx += dx
                sy += dy
                #盤の外
                if sx<0 or sx>7 or sy<0 or sy>7:
                    break
                #石が置いてない
                if board[sy][sx] == 0:
                    break
                #違う色の石がある
                if board[sy][sx] == 3-iro:
                    k += 1
                #同じ色の石があったら間の石を返す
                if board[sy][sx] == iro:
                    for i in range(k):
                        sx -= dx
                        sy -= dy
                        board[sy][sx] = iro
                    break

#そのマスに打てるかを調べる
def kaeseru(x, y, iro):
    if board[y][x] > 0:
        return -1
    total = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            k = 0
            sx = x
            sy = y
            while True:
                sx += dx
                sy += dy
                if sx<0 or sx>7 or sy<0 or sy>7:
                    break
                if board[sy][sx] == 0:
                    break
                if board[sy][sx] == 3-iro:
                    k += 1
                if board[sy][sx] == iro:
                    total += k
                    break
    return total

root = tkinter.Tk()
root.title("リバーシ")
root.resizable(False, False)
root.bind("<Button>", click)
cvs = tkinter.Canvas(width=640, height=700, bg="green")
cvs.pack()
banmen()
root.mainloop()