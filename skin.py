import random

class Skin:
    def __init__(self, name, base_price, rarity):
        self.name = name
        self.base_price = base_price  # The original price of the skin
        self.rarity = rarity
        self.discounted_price = base_price  # Initially, the discounted price is the same as the base price


    def set_base_price(self):
        prices = {
            "Common": 500,
            "Rare": 1000,
            "Epic": 1500,
            "Legendary": 2000
        }
        return prices.get(self.rarity, 1000)

    def calculate_discount_price(self):
        discount_rate = random.uniform(0.2, 0.5)  # 20% to 50% off
        return round(self.base_price * (1 - discount_rate))
