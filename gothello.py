from random import shuffle,choice
from itertools import product

class Game:
    def __init__(self):
        self.board=[["_"]*8 for _ in range(8)]
        self.white=[]
        self.black=[]
        self.stone=["X","O"]

    #게임 세팅
    def game_set(self):
        self.white={(3,3),(4,4)}
        self.black={(3,4),(4,3)}
        self.empty=list(product(*[list(range(8))]*2,repeat=True))
        for i in self.white|self.black:
            self.empty.remove(i)
        for v,h in self.white:
            self.board[v][h]="O"
        for v, h in self.black:
            self.board[v][h]="X"

    #게임 판 확인
    def show_board(self):
        print(" ",*range(1,9))
        for i,j in enumerate(self.board):
            print(chr(65+i),*j)

    #차례 선택
    def select_stone(self):
        shuffle(self.stone)
        while True:
            user=input("선택(1/2): ")
            if user in ["1","2"]:
                self.player=self.stone.pop(int(user)-1)
                self.computer=self.stone[0]
                break
        print(f"당신은 {'흑(X)' if self.player=='X' else '백(O)'}돌 입니다.")
        print("흑돌이 선(先)입니다")

    #돌 뒤집기
    def flip(self,coord,dir_tuple,stone):
        direction,n=dir_tuple
        x,y=coord
        tmp=[]
        if direction==0:#우좌상하↘↙↗↖
            self.board[x][y:y+n+1]=list(stone*(n+1))
            tmp=[(x,i) for i in range(y,y+n+1)]
        elif direction==1:
            self.board[x][y-n:y+1]=list(stone*(n+1))
            tmp=[(x,i) for i in range(y-n,y+1)]
        elif direction==2:
            for i in range(x-n,x+1):
                self.board[i][y]=stone
                tmp += [(i, y)]
        elif direction==3:
            for i in range(x,x+n+1):
                self.board[i][y]=stone
                tmp += [(i, y)]
        elif direction==4:
            for i in range(n+1):
                self.board[x+i][y+i]=stone
                tmp += [(x+i, y+i)]
        elif direction==5:
            for i in range(n+1):
                self.board[x+i][y-i]=stone
                tmp += [(x+i, y-i)]
        elif direction==6:
            for i in range(n+1):
                self.board[x-i][y+i]=stone
                tmp += [(x-i, y+i)]
        else:
            for i in range(n+1):
                self.board[x-i][y-i]=stone
                tmp += [(x-i, y-i)]
        tmp=set(tmp)
        if stone=="O":
            self.white.update(tmp)
            self.black-=tmp
        else:
            self.black.update(tmp)
            self.white-=tmp

    #착수 가능한 위치인지 검사
    def validation(self,coord, stone):
        x, y = coord
        if coord in self.white|self.black:
            return False
        # horizontal[right,left]
        value_list=[self.board[x][y + 1:],[] if y==0 else self.board[x][y - 1::-1]]
        # vertical[up/down]
        tmp=[i[y] for i in self.board]
        value_list+=[[] if x==0 else tmp[x-1::-1], tmp[x+1::]]
        # diagonal
        rd,ld=[],[]
        for i, j in enumerate(range(x, 8)):
            if i == 0:
                continue
            if y+i < 8:
                rd += [self.board[j][y+i]]
            if y-i >= 0:
                ld += [self.board[j][y-i]]
        value_list+=[rd,ld]
        ru,lu=[],[]
        for i, j in enumerate(range(x, -1, -1)):
            if i == 0:
                continue
            if y+i < 8:
                ru += [self.board[j][y + i]]
            if y-i >= 0:
                lu += [self.board[j][y - i]]
        value_list+=[ru,lu]
        res=[]
        for idx, i in enumerate(value_list): #→←↑↓↘↙↗↖
            # if not i:
            #     continue
            tg = "".join(i).split(stone)
            if len(tg)==1:
                continue
            tg=tg[0]
            if tg and "_" not in tg:
                res += [(idx, len(tg))] #dir, stones
        if sum([i[1] for i in res]):
            return res
        return False

    #빙고 체크
    def check_bingo(self):
        def check(board):
            for i in board:
                if "_" in i:
                    continue
                else:
                    tg=set(i)
                    if len(tg)==1:
                        return tg
        res=check(self.board)
        if not res:
            res=check(map(list,zip(*self.board)))
        if not res:
            tg=set([self.board[i][i] for i in range(8)])
            if len(tg)==1 and "_" not in tg:
                res=tg
        if not res:
            tg = set([self.board[i][7-i] for i in range(8)])
            if len(tg) == 1 and "_" not in tg:
                res = tg
        return res if res else False

    #착수
    def put(self,coord,stone):
        dir_li=self.validation(coord,stone)
        if dir_li:
            for dir_tup in dir_li:
                self.flip(coord,dir_tup,stone)
            return True

    #수 탐색
    def explore_moves(self,stone):
        valid_moves=[]
        for i in self.empty:
            tmp=self.validation(i,stone)
            if tmp:
                valid_moves+=[i]
        return valid_moves

    #턴: 플레이어
    def player_turn(self):
        while True:
            coord=sorted(input("돌을 놓을 위치: ").upper())
            try:
                coord=(ord(coord[1])-65,int(coord[0])-1)
            except:
                pass
            if len(coord)>1 and sum(map(lambda x:0<=x<8,coord))==2:
                flag=self.put(coord,self.player)
                if flag:
                    self.show_board()
                    self.empty.remove(coord)
                    break

    #턴: 컴퓨터
    def computer_turn(self,valid_moves):
        coord=choice(valid_moves)
        self.put(coord,self.computer)
        self.show_board()
        self.empty.remove(coord)

if __name__=="__main__":
    g=Game()
    g.game_set()
    g.show_board()
    g.select_stone()
    if g.player=="O":
        valid_moves=g.explore_moves(g.computer)
        if valid_moves:
            g.computer_turn(valid_moves)
        else:
            print("착수 가능한 공간이 없습니다. 턴을 넘깁니다.")
    while True:
        if g.explore_moves(g.player):
            g.player_turn()
        else:
            print("착수 가능한 공간이 없습니다. 턴을 넘깁니다.")
        input("상대의 입력을 기다리는 중...(press any key)")
        valid_moves=g.explore_moves(g.computer)
        if valid_moves:
            g.computer_turn(valid_moves)
        if not all([len(g.empty),len(g.white),len(g.black)]):
            if g.black==g.white:
                print("돌의 개수가 같아 무승부 입니다!")
                break
            winner="X" if g.black>g.white else "O"
            winner="당신" if g.player==winner else "상대"
            print(f"BINGO!\n{winner}의 승리입니다!!")
            break
        bingo=g.check_bingo()
        if bingo:
            print(bingo)
            winner="당신" if bingo=={g.player} else "상대"
            print(f"BINGO!\n{winner}의 승리입니다!!")
            break

#사람끼리 두면 좀 더 재밌을 것 같은데 컴퓨터가 상대라 너무 싱겁게 끝나버린다,,
#그래서 생각해 본 대안: 빙고 나는 순간 돌 개수 세서 승부 판단하기?