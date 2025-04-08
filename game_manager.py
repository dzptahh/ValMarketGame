import time

class GameManager:
    def __init__(self, player, market, stats):
        self.player = player
        self.market = market
        self.stats = stats
        self.time_left = 30  # seconds for a round
        self.game_running = False

    def start_game(self):
        """Starts the game and handles the game loop."""
        print("🎉 Welcome to Valorant Night Market!")
        self.market.generate_offers()
        self.game_running = True
        start_time = time.time()

        while self.game_running and time.time() - start_time < self.time_left:
            self.show_offers()
            self.handle_player_input()

        self.end_game()

    def show_offers(self):
        """Displays the available skins to the player."""
        print("\n🛍 Current Offers:")
        for i, skin in enumerate(self.market.available_skins, start=1):
            print(f"{i}. {skin.name} ({skin.rarity}) - {skin.discounted_price} VP")
        print(f"\n💰 Balance: {self.player.balance} VP")

    def handle_player_input(self):
        """Handles player input for buying skins."""
        try:
            choice = int(input("Enter skin number to buy: "))
            if 0 < choice <= len(self.market.available_skins):
                skin = self.market.available_skins[choice - 1]
                self.process_purchase(skin)
            else:
                print("⚠ Invalid skin number.")
        except ValueError:
            print("⚠ Please enter a valid number.")

    def process_purchase(self, skin):
        """Process the purchase and deduct balance if successful."""
        if self.player.balance >= skin.discounted_price:
            self.player.balance -= skin.discounted_price  # Deduct balance on successful purchase
            self.player.total_spent += skin.discounted_price
            self.player.total_purchases += 1
            self.player.inventory.append(skin)
            return True
        return False
        

    def end_game(self):
        """Ends the game and shows final results."""
        self.game_running = False
        print("\n⏱ Time’s up!")
        print(f"🎯 Final Score: {self.player.calculate_score()}")
        print(f"📦 Inventory: {[skin.name for skin in self.player.inventory]}")
        self.stats.save_data(self.player)
