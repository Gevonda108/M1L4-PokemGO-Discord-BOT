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

    async def get_name(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["forms"][0]["name"]
                else:
                    return "Pikachu"

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
        return f"The name of your Pokémon: {self.name}"

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
            return (
                f"Pertarungan @{self.pokemon_trainer} melawan @{enemy.pokemon_trainer}\n"
                f"HP @{enemy.pokemon_trainer} sekarang {enemy.hp}"
            )
        else:
            enemy.hp = 0
            return f"@{self.pokemon_trainer} menang melawan @{enemy.pokemon_trainer}"


class Wizard(Pokemon):
    pass


class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = random.randint(5, 15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nPetarung menggunakan serangan super dengan kekuatan:{super_power} "
    