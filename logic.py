import aiohttp
import random

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer, power=10, hp=100):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.img = None
        self.power = power
        self.hp = hp
        self.max_hp = hp
        self.level = 1
        self.exp = 0
        self.coins = 0
        self.food_inventory = {"basic": 0, "rare": 0, "epic": 0}
        self.types = []
        self.abilities = []

        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            # Reuse existing instance for this trainer
            existing = Pokemon.pokemons[pokemon_trainer]
            self.pokemon_number = existing.pokemon_number
            self.name = existing.name
            self.img = existing.img
            self.power = existing.power
            self.hp = existing.hp
            self.max_hp = existing.max_hp
            self.level = existing.level
            self.exp = existing.exp
            self.coins = existing.coins
            self.food_inventory = existing.food_inventory
            self.types = existing.types
            self.abilities = existing.abilities

    async def get_name(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    self.types = [t["type"]["name"] for t in data["types"]]
                    self.abilities = [a["ability"]["name"] for a in data["abilities"]]
                    return data["forms"][0]["name"]
                else:
                    self.types = ["normal"]
                    self.abilities = ["unknown"]
                    return "Pikachu"

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
        types_str = ", ".join(self.types) if self.types else "Unknown"
        abilities_str = ", ".join(self.abilities) if self.abilities else "Unknown"
        return f"**Pokémon: {self.name}**\nTypes: {types_str}\nAbilities: {abilities_str}\nLevel: {self.level}\nEXP: {self.exp}/100\nHP: {self.hp}\nPower: {self.power}\nCoins: {self.coins}\nFood: {self.food_inventory}"

    async def gain_exp(self, amount):
        self.exp += amount
        leveled_up = False
        while self.exp >= 100:
            self.exp -= 100
            self.level += 1
            self.power += 10
            self.max_hp += 20
            self.hp += 20
            leveled_up = True
        if leveled_up:
            return f"Your {await self.get_name()} leveled up to {self.level}! Power +10, HP +20."
        return ""

    async def feed(self, food_type):
        if food_type not in self.food_inventory:
            return "Invalid food type."
        if self.food_inventory[food_type] <= 0:
            return f"You don't have any {food_type} food."
        self.food_inventory[food_type] -= 1
        exp_gained = {"basic": 10, "rare": 25, "epic": 50}[food_type]
        heal_amount = {"basic": 20, "rare": 50, "epic": 100}[food_type]
        old_hp = self.hp
        self.hp = min(self.hp + heal_amount, self.max_hp)
        healed = self.hp - old_hp
        level_msg = await self.gain_exp(exp_gained)
        return f"Fed your Pokémon {food_type} food! Gained {exp_gained} EXP and healed {healed} HP. {level_msg}"

    def buy_food(self, food_type, quantity=1):
        prices = {"basic": 20, "rare": 50, "epic": 100}
        if food_type not in prices:
            return "Invalid food type."
        cost = prices[food_type] * quantity
        if self.coins < cost:
            return f"Not enough coins. You have {self.coins}, need {cost}."
        self.coins -= cost
        self.food_inventory[food_type] += quantity
        return f"Bought {quantity} {food_type} food for {cost} coins."

    async def reroll_superpower(self):
        if self.coins < 200:
            return "Not enough coins. Rerolling superpower costs 200 coins."
        self.coins -= 200
        old_number = self.pokemon_number
        self.pokemon_number = random.randint(1, 1000)
        self.name = None  # Reset name
        new_name = await self.get_name()
        return f"Rerolled superpower! Your Pokémon changed from #{old_number} to #{self.pokemon_number} ({new_name})."

    async def show_img(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["sprites"]["front_default"]
                else:
                    return None

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = random.randint(1, 5)
            if chance == 1:
                return "Pokemon Penyihir menggunakan perisai dalam battle"

        if enemy.hp > self.power:
            enemy.hp -= self.power
            result = f"Pertarungan @{self.pokemon_trainer} melawan @{enemy.pokemon_trainer}\nHP @{enemy.pokemon_trainer} sekarang {enemy.hp}"
        else:
            enemy.hp = 0
            coins_gained = random.randint(10, 50)
            self.coins += coins_gained
            exp_gained = 20
            level_msg = await self.gain_exp(exp_gained)
            result = f"@{self.pokemon_trainer} menang melawan @{enemy.pokemon_trainer}!\nGained {coins_gained} coins and {exp_gained} EXP.{level_msg}"
        return result


class Wizard(Pokemon):
    pass


class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = random.randint(5, 15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nPetarung menggunakan serangan super dengan kekuatan:{super_power} "
