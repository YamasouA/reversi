import tkinter
import random
import tkinter.messagebox

#フォントの定義
FS = ("Times New Roman", 30)
FL = ("Times New Roman", 80)

BLACK = 1
WHITE = 2

#クリックした増野列と行の値
mx, my = 0, 0
#クリックしたときに1を代入する変数
mc = 0
#ゲーム進行を管理
proc = -1
#どちらの順番かを管理
turn = 0
#メッセージ表示用の変数
msg = ""

#空いてるマスの数
space = 0
#プレーヤーとコンピュータの石の色
color = [0, 0]
who = ["あなた", "コンピュータ"]
lv = 0

board = []
# 局面を保存する
back = []
for y in range(8):
    board.append([0, 0, 0, 0, 0, 0, 0, 0])
    back.append([0, 0, 0, 0, 0, 0, 0, 0])


priority = [
	[6, 2, 5, 4, 4, 5, 2, 6],
	[2, 1, 3, 3, 3, 3, 1, 2],
	[5, 3, 3, 3, 3, 3, 3, 5],
	[4, 3, 3, 0, 0, 3, 3, 4],
	[4, 3, 3, 0, 0, 3, 3, 4],
	[5, 3, 3, 3, 3, 3, 3, 5],
	[2, 1, 3, 3, 3, 3, 1, 2],
	[6, 2, 5, 4, 4, 5, 2, 6]
]

def computer_1(iro):
	sx = 0
	sy = 0
	p = 0
	for y in range(len(priority[0])):
		for x in range(len(priority[1])):
			if kaeseru(x, y, iro) > 0 and priority[y][x] > p:
				p = priority[y][x]
				sx = x
				sy = y
	return sx, sy


#盤面をクリックしたときに動く関数
def click(e):
    global mx, my, mc
    mc = 1
    mx = int(e.x/80)
    my = int(e.y/80)
    if mx > 7: mx = 7
    if my > 7: my = 7


def banmen():
    cvs.delete("all")
    cvs.create_text(320, 670, text=msg, fill="silver", font=FS)
    for y in range(8):
        for x in range(8):
            X = x*80
            Y = y*80
            cvs.create_rectangle(X, Y, X+80, Y+80, outline="black")
            if board[y][x] == BLACK:
                cvs.create_oval(X+10, Y+10, X+70, Y+70, fill="black", width=0)
            elif board[y][x] == WHITE:
                cvs.create_oval(X+10, Y+10, X+70, Y+70, fill="white", width=0)
    cvs.update()

#盤面の初期化
def ban_syokika():
    global space
    space = 60
    for y in range(8):
        for x in range(8):
            board[y][x] = 0
    board[3][4] = BLACK
    board[4][3] = BLACK
    board[3][3] = WHITE
    board[4][4] = WHITE

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
    #print(iro)
    print(x, y, iro)
    if board[y][x] > 0:
        print(board[y][x])
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
                    #print('wow')
                    break
                if board[sy][sx] == 3-iro:
                    #print('Hello')
                    k += 1
                if board[sy][sx] == iro:
                    #print('total', total, 'k', k)
                    total += k
                    break
    print(total)           
    return total

#打てるマスがあるかを調べる
def uteru_masu(iro):
    for y in range(8):
        for x in range(8):
            if kaeseru(x, y, iro) > 0:
                return True
    return False

#黒と白の石の数を数える
def ishino_kazu():
    b = 0
    w = 0
    for y in range(8):
        for x in range(8):
            if board[y][x] == BLACK: b += 1
            if board[y][x] == WHITE: w += 1
    return b, w

# モンテカルロ法による思考ルーチン
def save():
	for y in range(len(board[0])):
		for x in range(len(board[1])):
			back[y][x] = board[y][x]

def load():
	for y in range(len(board[0])):
		for x in range(len(board[1])):
			board[y][x] = back[y][x]

def uchiau(iro):
	while True:
		print("uchiau now")
		if uteru_masu(BLACK) == False and uteru_masu(WHITE) == False:
			break
		iro = 3 - iro
		if uteru_masu(iro) == True:
			while True:
				x = random.randint(0, 7)
				y = random.randint(0, 7)
				if kaeseru(x, y, iro) > 0:
					ishi_utsu(x, y, iro)
					break
def computer_2(iro, loops):
	global msg
	win = [0] * 64
	save()

	for y in range(len(board[0])):
		for x in range(len(board[1])):
			if kaeseru(x, y, iro) > 0:
				msg += "."
				banmen()
				win[x+y*8] = 1
				for i in range(loops):
					ishi_utsu(x, y, iro)
					uchiau(iro)
					b, w = ishino_kazu()
					if iro == BLACK and b > w:
						win[x+y*8] += 1
					if iro == WHITE and w > b:
						win[x+y*8] += 1
					load()
	m = 0
	n = 0
	for i in range(64):
		if win[i] > m:
			m = win[i]
			n = i
	x = n % 8
	y = int(n / 8)
	return x, y


#コンピュータの思考ルーチン
def computer_0(iro): 
    #ランダムに打つ
    while True:
        rx = random.randint(0, 7)
        ry = random.randint(0, 7)
        if kaeseru(rx, ry, iro) > 0:
            return rx, ry

def main():
    global mc, proc, turn, msg, space, color, lv
    banmen()
    if proc == -1:
        cvs.create_text(320, 200, text="Reversi", fill="gold", font=FL)
        msg = "レベルを選択"
        cvs.create_text(80, 440, text="Lv. 1", fill="lime", font=FS)
        cvs.create_text(320, 440, text="Lv. 2", fill="lime", font=FS)
        cvs.create_text(560, 440, text="Lv. 3", fill="lime", font=FS)
        if mc == 1: #ウィンドウをクリック
            mc = 0
            #先手の文字をクリックしたら
            if (mx== 0 or mx== 1) and my == 5:
                lv = 1
            if (mx== 3 or mx== 4) and my == 5:
                lv = 2
            if (mx== 6 or mx== 7) and my == 5:
                lv = 3
            print("lv: ", lv)
            proc = 0

    if proc == 0: #タイトル画面
        msg = "先手、後手を選択"
        cvs.create_text(160, 440, text="先手(黒)", fill="lime", font=FS)
        cvs.create_text(480, 440, text="後手(白)", fill="lime", font=FS)
        if mc == 1: #ウィンドウをクリック
            mc = 0
            #先手の文字をクリックしたら
            if (mx==1 or mx==2) and my == 5:
                ban_syokika()
                color[0] = BLACK
                color[1] = WHITE
                turn = 0
                proc = 1
            if (mx==5 or mx==6) and my == 5:
                ban_syokika()
                color[0] = WHITE
                color[1] = BLACK
                turn = 1
                proc = 1
        
    elif proc == 1: #順番を表示
        msg = "あなたの番です"
        if turn==1:
            msg = "コンピュータ考え中"
        proc = 2
    elif proc == 2: #石を打つマスを決める
        if turn == 0: #プレーヤー
            #print('a')
            #print(proc, turn, mc)
            if mc == 1:
                mc = 0
                #print('b', kaeseru(mx, my, color[turn]))
                #print(mx, my, color[turn])
                if kaeseru(mx, my, color[turn]) > 0:
                    ishi_utsu(mx, my, color[turn])
                    proc = 3
                    space -= 1
                    #print('c')
            #print('play')
        else: #コンピュータ
            if lv == 1:
                cx, cy = computer_0(color[turn])
            elif lv == 2:
                cx, cy = computer_1(color[turn])
            elif lv == 3:
                MONTE = [300, 300, 240, 180, 120, 60, 1]
                # 空いているますの数に応じてモンテカルロで計算する回数を減らす
                cx, cy = computer_2(color[turn], MONTE[int(space/10)])
            ishi_utsu(cx, cy, color[turn])
            proc = 3
            space -= 1
    elif proc == 3:#打つ番を交代
        msg = ""
        turn = 1-turn
        proc = 4
        
    elif proc == 4:#打てるマスがあるか
        
        if space == 0:
            proc = 5
        elif uteru_masu(BLACK)==False and uteru_masu(WHITE)==False:
            tkinter.messagebox.showinfo("", "終局")
            proc = 5
        elif uteru_masu(color[turn]) == False:
            tkinter.messagebox.showinfo("", who[turn]+"は打てないのでパス")
            proc = 3
        else:
            proc = 1
        
    elif proc == 5:#勝敗判定
        b, w = ishino_kazu()
        tkinter.messagebox.showinfo("終局", "黒={}、白={}".format(b, w))
        if (color[0]==BLACK and b>w) or (color[0]==WHITE and w>b):
            tkinter.messagebox.showinfo("", "あなたの勝利")
        elif(color[1]==BLACJ and b>w) or (color[1]==WHITE and w>b):
            tkinter.messagebox.showinfo("", "コンピュータの勝利")
        else:
            tkinter.messagebox.showinfo("", "引き分け")
        proc = -1 
    root.after(100, main)

root = tkinter.Tk()
root.title("リバーシ")
root.resizable(False, False)
root.bind("<Button>", click)
#cvs = tkinter.Canvas(width=640, height=700, bg="green")
cvs = tkinter.Canvas(width=1000, height=1000, bg="green")
cvs.pack()
root.after(100, main)
root.mainloop()
