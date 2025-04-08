import random

class Skin:
    def __init__(self, name, base_price, rarity):
        self.name = name
        self.base_price = base_price  # The original price of the skin, directly from CSV
        self.rarity = rarity
        self.discounted_price = base_price

    def calculate_discount_price(self):
        discount_rate = random.uniform(0.2, 0.5)
        return round(self.base_price * (1 - discount_rate))