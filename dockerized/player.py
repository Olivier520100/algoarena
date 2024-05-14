
class Player():

    def __init__(self):

        self.myUnits = []
        self.myBuildings = []
        self.trees = []
        self.enemyUnits = []
        self.enemyBuildings = []
        self.wood = 0
        self.stone = 0
        self.summoncoords = []

    def reset(self):
        
        self.myUnits = []
        self.myBuildings = []
        self.trees = []
        self.enemyUnits = []
        self.enemyBuildings = []
        self.wood = 0
        self.stone = 0
        self.summoncoords = []