class Player:
    def __init__(self, name="Unknown", balance=10000):
        self.name = name
        self.balance = balance
        self.inventory = []
        self.total_spent = 0
        self.total_purchases = 0

    def purchase_skin(self, skin):
        if self.balance >= skin.discounted_price:
            self.balance -= skin.discounted_price  # Deduct balance on successful purchase
            self.total_spent += skin.discounted_price
            self.total_purchases += 1
            self.inventory.append(skin)
            return True
        return False

    def calculate_score(self):
        score = self.total_purchases * 10
        if self.total_spent >= 5000:
            score += 50
        elif self.total_spent >= 3000:
            score += 25
        return score