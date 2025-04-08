import random
from skin import Skin  # Assuming the Skin class is defined

class Market:
    def __init__(self):
        self.available_skins = []
        self.rarity_pool = ["Common", "Rare", "Epic", "Legendary"]
        self.skin_names = [
            "Prime Vandal", "Elderflame Operator", "Reaver Sheriff",
            "Ion Phantom", "Glitchpop Judge", "RGX Vandal"
        ]
        self.discounts = [0.1, 0.2, 0.3, 0.4, 0.5]  # Discount options from 10% to 50%

    def generate_offers(self, count=6):
        self.available_skins = []
        for _ in range(count):
            name = random.choice(self.skin_names)
            rarity = random.choice(self.rarity_pool)
            base_price = random.randint(1000, 3000)  # Random price between 1000 and 3000
            skin = Skin(name, base_price, rarity)
            self.apply_discount(skin)
            self.available_skins.append(skin)

    def apply_discount(self, skin):
        discount = random.choice(self.discounts)  # Randomly choose a discount
        skin.discounted_price = round(skin.base_price * (1 - discount))  # Round to nearest integer


    def refresh_skins(self):
        self.generate_offers()
