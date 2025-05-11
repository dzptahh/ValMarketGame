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
        # Basic score based on number of purchases
        score = self.total_purchases * 10
        
        # Add points based on total money spent
        if self.total_spent >= 5000:
            score += 50
        elif self.total_spent >= 3000:
            score += 25

        # Bonus for purchasing higher rarity skins (more expensive)
        rarity_bonus = 0
        for skin in self.inventory:
            if skin.rarity == "Legendary":
                rarity_bonus += 15  # Legendary skins give the highest bonus
            elif skin.rarity == "Epic":
                rarity_bonus += 10  # Epic skins give a moderate bonus
            elif skin.rarity == "Rare":
                rarity_bonus += 5   # Rare skins give a smaller bonus

        score += rarity_bonus

        # Reward for keeping balance - If player has a high balance, they get bonus points
        if self.balance > 7000:
            score += 30  # High balance bonus
        elif self.balance > 5000:
            score += 15  # Moderate balance bonus

        # Add extra points for consistent purchasing behavior (e.g., purchasing every round)
        if self.total_purchases > 10:
            score += 20  # Frequent buyer bonus
        
        # Calculate penalty for excessive spending (if they spent too much too quickly)
        if self.total_spent > 15000:
            score -= 20  # Penalty for overspending

        # Score should never be negative
        score = max(score, 0)

        return score
