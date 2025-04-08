class Player:
    def __init__(self, balance=10000):
        self.balance = balance  # Starting money
        self.inventory = []
        self.total_spent = 0
        self.total_purchases = 0

    def purchase_skin(self, skin):
        if self.balance >= skin.discounted_price:
            self.balance -= skin.discounted_price
            self.inventory.append(skin)
            self.total_spent += skin.discounted_price
            self.total_purchases += 1
            return True
        return False 

    def add_money(self, amount):
        self.balance += amount

    def calculate_score(self):
        # Simple example: score = total skins + money left
        return len(self.inventory) * 100 + self.balance
