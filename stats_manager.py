import csv
import os

class StatsManager:
    def __init__(self, filename="data/purchases.csv"):
        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        self.purchase_history = []

    def record_purchase(self, skin):
        # Record skin purchase with relevant data
        self.purchase_history.append({
            "Skin Name": skin.name,
            "Rarity": skin.rarity,
            "Base Price": skin.base_price,
            "Discounted Price": skin.discounted_price
        })

    def save_data(self, player):
        # Save purchase history and player stats to CSV
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Skin Name", "Rarity", "Base Price", "Discounted Price"])
            writer.writeheader()
            writer.writerows(self.purchase_history)

        # Print out summary info
        print("📁 Purchase history saved to CSV.")
        print(f"💸 Total spent: {player.total_spent} VP")
        print(f"🧮 Skins bought: {player.total_purchases}")
        print(f"🏆 Highest score: {player.calculate_score()}")

    def load_data(self):
        # Optionally load previously saved data from the CSV file
        if os.path.exists(self.filename):
            with open(self.filename, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    print(row)
        else:
            print("No saved data found.")
