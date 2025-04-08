# game_manager.py
import time

class GameManager:
    def __init__(self, player, market, stats):
        self.player = player
        self.market = market
        self.stats = stats
        self.time_left = 60  # seconds for a round

    def start_game(self):
        print("🎉 Welcome to Valorant Night Market!")
        self.market.generate_offers()
        start_time = time.time()

        while time.time() - start_time < self.time_left:
            self.show_offers()
            choice = input("Enter skin number to buy or 'skip': ")

            if choice.lower() == 'skip':
                continue

            try:
                index = int(choice) - 1
                skin = self.market.available_skins[index]
                success = self.player.purchase_skin(skin)
                if success:
                    self.stats.record_purchase(skin)
                    print(f"✅ Bought {skin.name} for {skin.discounted_price} VP")
                else:
                    print("❌ Not enough balance.")
            except (ValueError, IndexError):
                print("⚠ Invalid input.")

        self.end_game()

    def show_offers(self):
        print("\n🛍 Current Offers:")
        for i, skin in enumerate(self.market.available_skins, start=1):
            print(f"{i}. {skin.name} ({skin.rarity}) - {skin.discounted_price} VP")
        print(f"\n💰 Balance: {self.player.balance} VP")

    def end_game(self):
        print("\n⏱ Time’s up!")
        print(f"🎯 Final Score: {self.player.calculate_score()}")
        print(f"📦 Inventory: {[skin.name for skin in self.player.inventory]}")
        self.stats.save_data(self.player)
