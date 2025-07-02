class ChargeCalculator:
    def __init__(self, project_repository):
        self.charge = 0
        self.project_repository = project_repository

    def add(self, cost):
        # 요금을 계산해서 += charge
        self.charge += cost
    
    def execute(self):
        # repository를 통해 db에 사용자의 charge정보를 업데이트
        print(f"최종 비용 : {self.charge}")
        self.project_repository.add_charge(self.charge)