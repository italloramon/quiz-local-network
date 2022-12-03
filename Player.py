class Player:
    def __init__(self, conn, name):
        self.conn = conn
        self.name = name
        self.score = 0
        self.life = 3

    def __str__(self) -> str:
        return f"{self.name} have a score: {self.score}"

    def score_up(self):
        self.score += 1

    def isLife(self):
        if self.life > 0:
            return True
        else:
            return False
    
    def life_down(self):
        self.life -= 1