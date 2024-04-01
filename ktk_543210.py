class Game:
    def __init__(self):
        self.set1, self.set2 = 0, 0
        self.tot1, self.tot2 = 0, 0
        self.p1 = "당신"
        self.p2 = "상대방"

    # 게임 셋
    def game_set(self):
        global point1, point2, hand1, hand2
        self.point1, self.point2 = 0, 0
        self.hand1, self.hand2 = [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]
        self.rsp = [0, 2, 5]

    # 패 제출
    def takeout(self):
        import random
        while True:
            try:
                self.s1 = int(input("패를 제출:"))
                if self.s1 not in self.hand1:
                    raise Exception("out of range")
                break
            except:
                pass
        self.s2 = random.choice(self.hand2)

    # 제출한 패 핸드에서 지우기
    def pop_card(self):
        self.hand1.pop(self.hand1.index(self.s1))
        self.hand2.pop(self.hand2.index(self.s2))

    # 가위바위보
    def rsp_win(self):
        rsp_res = self.s1 - self.s2
        if rsp_res == 5 or -4 < rsp_res < 0:
            return 1
        elif rsp_res == -5 or 0 < rsp_res < 4:
            return 2
        else:
            return 0

    # 패 비교
    def win(self):
        if self.s1 in self.rsp and self.s2 in self.rsp:
            return self.rsp_win()
        elif self.s1 == self.s2:
            return 0
        elif self.s1 > self.s2:
            return 1
        else:
            return 2

    # 포인트 합산
    def get_point(self, round_res):
        self.pt = self.s1 + self.s2
        if round_res == 1:
            self.point1 += self.pt
        elif round_res == 2:
            self.point2 += self.pt
        else:
            pass

    # 라운드 포인트 계산
    def set_winner(self):
        if self.point1 > self.point2:
            self.set1 += 1
            print(f"{self.p1}이 이겼습니다! 세트 스코어 {self.set1}:{self.set2}")
            return 1
        elif self.point1 < self.point2:
            self.set2 += 1
            print(f"{self.p2}이 이겼습니다! 세트 스코어 {self.set1}:{self.set2}")
            return 2
        else:
            return 0

    # reward
    def cal_point(self, winner):
        if winner == 1:
            self.tot1 += self.point1
        elif winner == 2:
            self.tot2 += self.point2

    def round(self, res):
        print(f"\n{self.p1}이 낸 패:", self.s1)
        print(f"{self.p2}이 낸 패:", self.s2)
        if res == 1:
            print(f"{self.p1}이 이겼습니다! 승점 {self.pt}을 획득합니다!")
        elif res == 2:
            print(f"{self.p1}이 졌습니다. {self.p2}이 승점 {self.pt}을 획득합니다.")
        else:
            print("비겼습니다. 점수 변동 없음.")
        print(f"현재 {self.p1}의 승점: {self.point1}")
        print(f"{self.p2}의 승점: {self.point2}")
        print(f"{self.p1}의 남은 패: ", self.hand1, "\n")

    def battle(self):
        self.takeout()
        res = self.win()
        self.get_point(res)
        self.pop_card()
        self.round(res)


if __name__ == "__main__":
    game = Game()
    print(
        "543210 게임에 오신 것을 환영합니다.\n543210 게임은 매 라운드 0에서 5 사이의 숫자를 선택하여 제출합니다. 한 번 제출한 숫자는 다시 제출할 수 없으며, 더 큰 숫자가 이기는 간단한 게임입니다.")
    print("\n특별한 규칙 : 0은 2를 이기고, 2는 5를 이깁니다. 그럼 행운을 빕니다!\n")
    while True:
        game.game_set()
        for _ in range(6):
            game.battle()
        winner = game.set_winner()
        game.cal_point(winner)
        if game.set1 == 2 or game.set2 == 2:
            break