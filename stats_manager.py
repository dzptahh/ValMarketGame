# stats_manager.py
import csv
import os

class StatsManager:
    def __init__(self, filename="data/purchases.csv"):
        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        self.purchase_history = []

    def record_purchase(self, skin):
        self.purchase_history.append({
            "Skin Name": skin.name,
            "Rarity": skin.rarity,
            "Base Price": skin.base_price,
            "Discounted Price": skin.discounted_price
        })

    def save_data(self, player):
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Skin Name", "Rarity", "Base Price", "Discounted Price"])
            writer.writeheader()
            writer.writerows(self.purchase_history)

        print("📁 Purchase history saved to CSV.")
        print(f"💸 Total spent: {player.total_spent}")
        print(f"🧮 Skins bought: {player.total_purchases}")
