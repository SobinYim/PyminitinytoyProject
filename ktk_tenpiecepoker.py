from random import shuffle,randint,choices
from itertools import product, accumulate, zip_longest
from functools import cmp_to_key


class Game:
    def __init__(self):
        self.symbol="♠ ◇ ♡ ♣".split()
        self.number=list(map(str,range(2,11)))+"J Q K A".split()
        self.number.reverse()
        self.deck=list(map(lambda x: "".join(x),product(self.symbol,self.number)))
        self.card=["RoyalStraightFlush","StraightFlush","FourCard","FullHouse","Flush","Straight","Triple","TwoPair","OnePair","HighCard"]

    # 게임 셋
    def set_game_tpp(self):
        self.p1 = 100
        self.p2 = 100
        print('''
10장 포커에 오신 것을 환영합니다.
10장 포커는 10장의 카드로 진행하는 포커입니다.
카드는 모두 공개되며 왼쪽에서 3장이 상대의 손패이고 오른쪽에서 3장이 당신의 손패입니다.
가운데 4장은 공용 카드로, 패 배분이 끝나면 뒤집어 섞습니다. 공용패는 각자 2장씩 선택해 자신의 손패로 가져올 수 있습니다.

각 플레이어에게는 100 포인트씩 지급되며 이 포인트로 게임의 엔트리와 만약 상대와 같은 카드를 원할 경우 경매를 진행할 수 있습니다.
엔트리로는 기본적으로 10포인트부터 베팅할 수 있으며 만약 상대보다 많은 엔트리를 지불하였다면 카드 경매에서 1회에 한하여 우선권을 가져갈 수 있습니다.

승자는 엔트리 포인트를 가져갈 수 있으며 경매에 사용한 포인트는 양 참가자 모두 돌려받을 수 없습니다.
한 플레이어가 엔트리를 더이상 지불할 수 없다면 게임은 종료됩니다.

            ''')
        while self.p1 > 9 and self.p2 > 9:
            self.set_round_tpp()
        print(f"{'상대방' if self.p1>self.p2 else '당신'}의 포인트가 부족하여 더이상 게임을 진행할 수 없습니다.\n{'당신' if self.p1>self.p2 else '상대방'}의 승리입니다!")

    # 라운드 진행
    def set_round_tpp(self):
        self.entry()
        shuffle(self.deck)
        hand = self.deck[:10]
        hand1 = hand[:3]
        hand2 = hand[-3:]
        community = hand[3:-3]
        print("이번 라운드의 카드는 다음과 같습니다.")
        print(*hand)

        def check_hand(start=False):
            print(f"\n당신의 손패: {' '.join(hand1)}\n상대의 손패: {' '.join(hand2)}")
            if start == True:
                print(f"공용 패: {' '.join(community)}")
            elif community:
                print(
                    f"공용 패: {' '.join(sorted(community, key=cmp_to_key(lambda x, y: g.symbol.index(x[0]) - g.symbol.index(y[0]))))}")

        check_hand(True)
        community, order = self.shuffle_hand(community)
        print(f"\n카드를 섞습니다.\n\n{order}")
        while community:
            choice1 = self.select_card(community)
            choice2 = randint(0, len(community) - 1)
            if choice1 == choice2:
                if self.priority == 1:
                    while True:
                        use = input("우선권을 사용하시겠습니까?(y/n) ").lower().rstrip()
                        if use == "y":
                            self.priority = 0
                            winner = "당신"
                            break
                        elif use == "n":
                            winner = self.auction()
                            break
                elif self.priority == 2:
                    self.priority = 0
                    print("상대방이 우선권을 사용하였습니다.\n카드를 상대가 가져갑니다.")
                    winner = "상대"
                else:
                    winner = self.auction()
                if winner == "X":
                    continue
                elif winner == "당신":
                    hand1.append(community.pop(choice1))
                    hand2.append(community.pop(randint(0, len(community) - 1)))
                    self.check_point()
                else:
                    hand2.append(community.pop(choice1))
                    self.check_point()
                    hand1.append(community.pop(self.select_card(community)))
            else:
                hand1.append(community.pop(choice1))
                hand2.append(community.pop(choice2 if choice1 > choice2 else choice2 - 1))
            check_hand()
        judge1, out1=self.check_outs(hand1)
        judge2, out2=self.check_outs(hand2)
        print(f"\n당신은 {out1.pop(0)} {self.card[judge1]} 상대는 {out2.pop(0)} {self.card[judge2]}")
        self.cal_point(self.summarize(out1,out2,[judge1,judge2]))
        self.check_point()

    # high 카드 비교
    def compare_high(self,li_n_cnt):
        li=list(zip_longest(*li_n_cnt, fillvalue=0)) #앞쪽부터 채우나 n_cnt 입력이므로 괜찮음
        p=list(range(len(li_n_cnt)))
        for i in li:
            if sum(i)==0:
                continue
            for j in p:
                if i[j]==0:
                    p.remove(j)
            if len(p)==1:
                return p[0]
        return -1

    # 수 비교
    def compare_num(self,li):
        p1,p2=li
        if p1>p2:
            return 0
        elif p1<p2:
            return 1
        else:
            return -1

    # 문양 비교
    def compare_symbol(self,li):
        p1,p2=li
        if p1<p2:
            return 0
        elif p1>p2:
            return 1
        else:
            return -1

    # 카드 비교
    def compare_card(self,li):
        p1,p2=li
        target=list(zip(p1.pop(0),p2.pop(0)))
        method=target[1][0]
        if method==1:
            res=self.compare_high(target[0])
        elif method==2:
            res=self.compare_num(target[0])
        else:
            res=self.compare_symbol(target[0])
        if res==-1:
            res=self.compare_card([p1,p2])
        return res

    # 가능한 조합 계산
    def check_outs(self,hand):
        RoyalStraightFlush, StraightFlush, FourCard, FullHouse, Flush, Straight, Triple, TwoPair, OnePair, HighCard = [], [], [], [], [], [], [], [], [], []
        hand.sort(key=cmp_to_key(lambda x, y: self.symbol.index(x[0]) - self.symbol.index(y[0])))
        s, n = [], []
        for i in hand:
            s += i[0]  #hand symbol 리스트
            n += [i[1:]]  #hand number 리스트
        def count_n(numberlist):  #hand number counter
            return list(map(lambda x: numberlist.count(x), self.number))
        def check_straight(n_cnt): #return high
            n_cnt = n_cnt[::-1]
            for i in range(8,-2,-1):
                temp = n_cnt[i:i + 5]
                if not temp:
                    temp=[n_cnt[-1]] + n_cnt[:4]
                if 0 not in temp:
                    return i + 5
            return -1
        # 플러쉬
        s_cnt = list(map(lambda x: s.count(x), self.symbol))
        if max(s_cnt) > 4:
            flush_s = [_ for _ in range(4) if s_cnt[_] > 4]
            flush_n = [[]] * 4
            stf=[0]
            acc_card = list(accumulate([0] + s_cnt))
            for i in flush_s:
                n_li = count_n(n[acc_card[i]:acc_card[i + 1]])
                flush_n[i] = n_li
                t=check_straight(n_li)
                if t>stf[0]:
                    stf=[t,i]
                if stf[0] == 13:
                    RoyalStraightFlush = [self.symbol[i],(i,3)]
                    break
            StraightFlush = [self.number[13-stf[0]]]+list(zip(stf,[1,3])) if stf[0]!=0 else []
            flush_id = self.compare_high(flush_n)
            Flush = [self.symbol[flush_id]]+list(zip([flush_n[flush_id], flush_id],[1,3]))
        n_cnt = count_n(n)
        #스트레이트
        t=check_straight(n_cnt)
        if t>0:
            Straight=[self.number[13-t],(t,2),(self.symbol.index(s[[idx for idx, item in enumerate(n) if item == self.number[13 - check_straight(n_cnt)]][0]]), 3)]
        #페어
        pair = []
        triple = []
        for i, j in enumerate(n_cnt):
            if not FourCard and j == 4:
                FourCard = [self.number[i],(13-i,2)]
                break
            if j == 3:
                triple+=[i]
            if j == 2:
                pair+=[i]
        Triple = [self.number[min(triple)]]+[(13-min(triple),2)] if triple else []
        TwoPair = [self.number[min(pair)]]+list(map(lambda x: (13-x,2),pair[:2]))+[(13-n_cnt.index(1),2)] if len(pair) > 1 else []
        OnePair = [self.number[min(pair)],(13-pair[0],2),(self.symbol.index(s[[idx for idx, item in enumerate(n) if item == self.number[pair[0]]][0]]), 3)] if pair else []
        high=[idx for idx, item in enumerate(n) if item==self.number[[i for i,j in enumerate(n_cnt) if j!=0][0]]][0]
        HighCard = [hand[high],(n_cnt,1),(self.symbol.index(s[high]),3)]
        if triple and len(triple) + len(pair) > 1:
            FullHouse = Triple.copy()
        for i, j in enumerate(self.card):
            if eval(j):
                return [i, eval(self.card[i])]

    # 라운드 요약
    def summarize(self,player1,player2,j):
        p1,p2=j
        if p1==p2:
            res=self.compare_card([player1,player2])
        else:
            res=int(p1>p2)
        print(f"{['당신','상대'][res]}의 승리!\n이번 판의 승리 포인트: {self.entrypoint}\n포인트를 정산합니다.")
        return res

    # 셔플
    def shuffle_hand(self,hand):
        hand=hand[::-1]
        def perfect_shuffle(hand):
            n = len(hand)//2
            d1 = hand[:-n]
            d2 = hand[-n:]
            res = []
            for i in range(len(d2)):
                res.extend([d1[i], d2[i]])
            if len(hand) % 2 == 1:
                res += [d1[-1]]
            return res
        def hindu_shuffle(hand):
            n=int(len(hand)*.25)
            res=hand[:n]+hand[-n:]+hand[n:-n]
            return res
        order=["착"]*randint(2,5)+[" 차작 "]*randint(0,3)
        shuffle(order)
        for i in order:
            if i=="착":
                hand=hindu_shuffle(hand)
            else:
                hand=perfect_shuffle(hand)
        return hand,"".join(order).lstrip().replace("  "," ")

    # 카드 선택
    def select_card(self,community):
        n=len(community)
        print(("┌───┐ "*n + "\n" + "│ {} │ "*n + "\n" + "└───┘ "*n + "").format(*range(1, n+1)))
        select=0
        while not select:
            try:
                select=int(input("카드를 선택: "))
            except:
                pass
            if 0<select<=len(community):
                return select-1
            else: select=0

    # 카드 경매
    def auction(self):
        bid1,bid2=0,0
        curbid=0
        pinput,cinput=0,0
        print("입찰을 하려면 현재 입찰가보다 높은 포인트를, 입찰을 그만두려면 0을 입력하세요.")
        while True:
            curbid=max(bid1,bid2)
            print("현재 입찰가:",curbid)
            try:
                pinput=int(input("입찰 포인트 입력: "))
            except: continue
            if pinput<=curbid and pinput!=0:
                print("0(포기) 혹은 현재 입찰가보다 높은 가격을 입력해야 합니다.")
                continue
            if pinput>self.p1:
                print("현재 가지고 있는 포인트를 초과하는 포인트로 입찰할 수 없습니다.")
                continue
            bid1=max(pinput,bid1)
            cinput=choices((0,1),[.75,.25])
            curbid=max(bid1,bid2)
            bid2=bid2 if (cinput==[0] or (curbid!=0 and pinput==0)) else randint(curbid+1,curbid+3)
            curbid=max(bid1,bid2)
            if cinput==[0]:
                print(f"\n상대방이 입찰하지 않았습니다.")
            else:
                print(f"\n상대방이 {bid2} 포인트 입찰하였습니다.")
            print(f"현재 당신의 입찰 포인트: {bid1}\n현재 상대의 입찰 포인트: {bid2}")
            if pinput==0==curbid and cinput==[0]:
                print(f"경매 참가자 모두가 입찰을 포기하였습니다. \n카드 선택 단계로 돌아갑니다.")
                return "X"
            if pinput==0 or cinput==[0]:
                winner="당신" if bid1>bid2 else "상대방"
                print(f"경매 참가자 한쪽이 입찰 의사를 표하지 않았으므로 {winner}에게 카드가 돌아갑니다.")
                self.p1-=bid1
                self.p2-=bid2
                return winner
            if self.p2<=curbid-1 or self.p1<=curbid-1:
                print("올인! 더이상 입찰할 수 없으므로 상대방의 입찰 의사 확인 후, 경매를 마무리합니다.")
                if choices((0, 1), [.25, .75])==[1] and self.p2-curbid+1>0:
                    bid2+=1
                winner = "당신" if bid1 > bid2 else "상대방"
                self.p1-=bid1
                self.p2-=bid2
                return winner

    # 게임 엔트리
    def entry(self):
        entryp1=0
        while not entryp1:
            try:
                entryp1=int(input("이번 라운드에 지불할 엔트리 포인트를 입력하세요: "))
            except:
                print("잘못된 입력!")
                continue
            if not 9<entryp1<=self.p1:
                print(f"유효한 숫자가 아닙니다.\n10과 {self.p1} 사이의 숫자를 입력해주세요.\n")
                entryp1=0
        entryp2=choices([10,11,12,13,15,20],[.7,.2,.05,.04,.009,.001])[0]
        self.p2-=entryp2
        self.p1-=entryp1
        self.entrypoint=entryp2+entryp1
        self.priority=0 if entryp2==entryp1 else 1 if entryp1>entryp2 else 2
        input(f"당신이 지불한 엔트리 포인트: {entryp1}\n상대가 지불한 엔트리 포인트: {entryp2}\n이번 라운드의 승리 포인트: {self.entrypoint}")
        self.check_point()
        input()

    # 포인트 정산
    def cal_point(self,winner):
        if winner == 0:
            self.p1 += self.entrypoint
        elif winner == 1:
            self.p2 += self.entrypoint

    # 포인트 조회
    def check_point(self):
        print(f"\n당신의 현재 포인트: {self.p1}\n상대의 현재 포인트: {self.p2}\n")


if __name__=="__main__":
    g=Game()
    g.set_game_tpp()

#게임이 살짝 루즈한 감이 없잖아 있다.. 추가 베팅 시의 메리트를 만들어주면 좋을 듯
#특별 룰? > 이번 라운드에서 '카드 패'가 나오면 승리 시 엔트리의 정해진 배율만큼 곱하여 돌려주고, 없다면 추가로 베팅 된 엔트리의 절반만 돌려줌
#Ex_20, 30 베팅, 카드 패 존재 시 *1.2라면 승자에게 60을 돌려주고 카드 패가 존재하지 않으면 20(기본)+15(추가 베팅)=35 돌려주기
