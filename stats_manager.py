import csv
import os

class StatsManager:
    def __init__(self, leaderboard_path="data/leaderboard.csv", purchases_path="data/purchases.csv"):
        self.leaderboard_path = os.path.abspath(leaderboard_path)
        self.purchases_path = os.path.abspath(purchases_path)

        # Ensure directories exist
        os.makedirs(os.path.dirname(self.leaderboard_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.purchases_path), exist_ok=True)

        self.purchase_history = []
        self.leaderboard = self.load_leaderboard()
        self.additional_money_record = []
        self.total_money_spent = []

    def record_purchase(self, skin):
        """ Record a skin purchase in the purchase history. """
        self.purchase_history.append({
            "Skin Name": skin.name,
            "Rarity": skin.rarity,
            "Base Price": skin.base_price,
            "Discounted Price": skin.discounted_price
        })

    def save_data(self, player):
        """ Save player data and purchase history to CSV files. """
        # Save leaderboard data
        with open(self.leaderboard_path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Player Name", "Score"])
            # Write header only if file is empty
            if file.tell() == 0:
                writer.writeheader()
            # Write player data
            writer.writerow({
                "Player Name": player.name,
                "Score": player.calculate_score()
            })

        # Save purchase history
        with open(self.purchases_path, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Skin Name", "Rarity", "Base Price", "Discounted Price"])
            writer.writeheader()
            writer.writerows(self.purchase_history)

        # Track total money spent for data visualization
        self.total_money_spent.append(player.total_spent)

        # Debugging output
        print(f"📁 Data saved. Leaderboard: {self.leaderboard_path}, Purchases: {self.purchases_path}")
        print(f"💸 Total spent by {player.name}: {player.total_spent} VP")
        print(f"🏆 Score saved: {player.calculate_score()} Points")

    def load_leaderboard(self):
        """ Load leaderboard data from CSV. """
        leaderboard = []
        if os.path.exists(self.leaderboard_path):
            with open(self.leaderboard_path, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        leaderboard.append({
                            "name": row["Player Name"],
                            "score": int(row["Score"])
                        })
                    except ValueError:
                        print(f"Data format error in row: {row}")
        return leaderboard

    def get_top_scores(self):
        """ Get top 10 scores sorted by score. """
        if not self.leaderboard:
            self.leaderboard = self.load_leaderboard()

        # Sort and return top 10
        sorted_leaderboard = sorted(self.leaderboard, key=lambda x: x['score'], reverse=True)
        return sorted_leaderboard[:10]

    def get_purchase_history(self):
        """ Get purchase history data. """
        if os.path.exists(self.purchases_path):
            with open(self.purchases_path, mode="r") as file:
                reader = csv.DictReader(file)
                return list(reader)
        return []

    def test_data_saving(self, player):
        """ Test method for data saving. """
        self.save_data(player)
        print(f"Leaderboard Data: {self.leaderboard}")
        print(f"Purchase History: {self.purchase_history}")

