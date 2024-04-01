from time import time,asctime
from random import randint

class Game:
    def __init__(self):
        self.rep=True
        self.ranking=[]
        self.clear_record=0
        self.name=input("Player의 이름을 입력해주세요:: ")
        print(f"환영합니다 {self.name}님")

    #메뉴 선택
    def menu(self):
        select=input("메뉴를 선택하세요::\n1. 게임 설명\n2. 게임 시작\n3. 무한 모드 랭킹\n4. exit\n")
        if select=="1":
            self.rule()
        elif select=="2":
            game_mode=self.mode_select()
            if game_mode=="1":
                if self.clear_record!=0:
                    m_select=self.mode_select(1)
                    if m_select=="1":
                        self.start_normal()
                    elif m_select=="2":
                        self.start_normal(limit=3)
                    else:
                        print("잘못된 입력, 초기 화면으로 돌아갑니다.")
                else:
                    self.start_normal()
            elif game_mode=="2":
                self.start_infinite()
            else:
                print("잘못된 입력, 초기 화면으로 돌아갑니다.")
        elif select=="3":
            self.show_rank()
        elif select=="4":
            self.rep=False
        else:
            print("잘못된 입력, 다시 선택해주세요.")

    #게임 룰
    def rule(self):
        print("******************RULE******************")
        print("랜덤한 숫자 X가 게임 시작 시에 주어집니다.")
        print("이 숫자를 마지막에 말하는 사람의 패배!")
        print("한 번에 연달아 입력할 수 있는 수는 최대 3개입니다.")
        print("5초 안에 입력하지 못하면 패배!")
        print("숫자 3,6,9 대신에 -(하이픈)을 입력해야 합니다.")
        print("입력 예) 28-- => 28, 29, 30을 입력한 것과 같음!")
        print("\n무한 모드에서는 숫자 X의 제한 없이 패배할 때까지 게임이 계속됩니다.")
        print("하드 모드와 무한 모드의 시간 제한은 3초입니다.")
        print("****************************************\n")

    #모드 선택
    def mode_select(self,hard=0):
        mode=["무한","하드"]
        select=input(f"모드를 선택하세요::\n1. 일반 모드\n2. {mode[hard]} 모드\n")
        return select

    #노말 모드
    def start_normal(self,limit=5):
        self.X=randint(20,100)
        self.lastnum=0
        self.time_limit=limit
        self.con=1
        self.win=0
        print(f"이번 게임의 X는!!! >>> {self.X} <<< 입니다!")
        input("enter를 누르면 시작합니다")
        while self.con:
            self.turn()
        if self.win==1:
            print("당신의 승리! ｡₍ᐢ.ˬ.ᐢ₎* ")
            self.clear_record=1

    #무한 모드
    def start_infinite(self,limit=3):
        self.X=10**15
        self.lastnum=0
        self.time_limit=limit
        self.con=1
        input("enter를 누르면 시작합니다")
        while self.con:
            self.turn()
        if len(self.ranking)<11 or self.ranking[-1][0]<self.lastnum:
            self.ranking.append((self.lastnum,asctime()))
        self.ranking.sort(reverse=True)

    #기록 조회
    def show_rank(self):
        print(f"{self.name} 님의 무한 모드 기록")
        if self.ranking:
            print("랭크 기록\t일시")
            for i,j in enumerate(self.ranking):
                print(f"{i+1}.   \t{j[0]}\t{j[1]}")
        else:
            print("\n* 기록이 없습니다. *\n")

    #턴: 플레이어
    def player_turn(self):
        start_turn=time()
        self.entry=input()
        end_turn=time()
        if end_turn-start_turn>self.time_limit:
            return False
        return True

    #턴
    def turn(self):
        case=list(map(lambda x:str(x) if sum([str(x).count(i) for i in ["3","6","9"]])==0 else "-",
                      range(self.lastnum+1,self.lastnum+4)))
        ex=list("".join(case[:i]) for i in range(1,4))
        ###게임 종료
        pt=self.player_turn()
        if pt==False:
            print(f"시간 초과로 {self.name} 님의 패배입니다!")
            self.con=0
        if self.entry not in ex:
            print(f"잘못된 입력으로 {self.name} 님의 패배입니다!")
            self.con=0
        try:
            self.lastnum+=1+ex.index(self.entry)
        except:
            pass
        if self.lastnum>=self.X:
            print(f"이번 게임의 X를 외치셨으므로 {self.name} 님의 패배입니다!")
            self.con=0
        ###컴퓨터의 턴
        if self.con!=0:
            case=list(map(lambda x: str(x) if sum([str(x).count(i) for i in ["3", "6", "9"]]) == 0 else "-",
                            range(self.lastnum + 1, self.lastnum + 4)))
            if 1<self.X-self.lastnum<5:
                cn=self.X-self.lastnum-1
            elif self.X-self.lastnum==1:
                cn=1
            else:
                cn=randint(1,3)
            print(*case[:cn],"\n", sep="")
            self.lastnum+=cn
            if self.lastnum>=self.X:
                self.win=1
                self.con=0

if __name__ == "__main__":
    g=Game()
    while g.rep:
        g.menu()