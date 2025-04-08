import csv
import os

class StatsManager:
    def __init__(self, filename="data/leaderboard.csv"):
        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        self.purchase_history = []
        self.leaderboard = self.load_leaderboard()
        self.additional_money_record = [] # Keep track of money added.
        self.total_money_spent = []

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
        with open(self.filename, mode="a", newline="") as file:  # Append mode to add new scores
            writer = csv.DictWriter(file, fieldnames=["Player Name", "Score"])
            if file.tell() == 0:  # Write header only if the file is empty
                writer.writeheader()
            writer.writerow({"Player Name": "Player", "Score": player.calculate_score()})  # Changed Player Name

        # Save purchase history to a different CSV
        with open("data/purchases.csv", mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Skin Name", "Rarity", "Base Price", "Discounted Price"])
            writer.writeheader()
            writer.writerows(self.purchase_history)
        
        self.total_money_spent.append(player.total_spent) #record total money spent

        # Print out summary info.  This will go to the console, not the GUI.
        print("📁 Purchase history saved to CSV.")
        print(f"💸 Total spent: {player.total_spent} VP")
        print(f"🧮 Skins bought: {player.total_purchases}")
        print(f"🏆 Final Score: {player.calculate_score()}")

    def load_leaderboard(self):
        # Load leaderboard data
        leaderboard = []
        if os.path.exists(self.filename):
            with open(self.filename, mode="r") as file:
                reader = csv.DictReader(file)
                leaderboard.extend(
                    {"name": row["Player Name"], "score": int(row["Score"])}
                    for row in reader
                )
        return leaderboard

    def get_top_scores(self):
        # Sort leaderboard by score and return top 10
        self.leaderboard.sort(key=lambda x: x['score'], reverse=True)
        return self.leaderboard[:10]  # Return top 10 scores
    