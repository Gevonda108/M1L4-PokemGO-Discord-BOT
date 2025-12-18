import discord
from discord.ext import commands
from config import token
from logic import Pokemon, Wizard, Fighter

import random
import os
import sys



# Setting up intents for the bot
intents = discord.Intents.default()  
intents.messages = True              
intents.message_content = True       
intents.guilds = True                


bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Gooning to {bot.user}')

# The '!go' command
@bot.command()
async def go(ctx):
    author = ctx.author.name  # Getting the name of the message's author
    # Check whether the user already has a Pokémon. If not, then...
    if author not in Pokemon.pokemons.keys():
        chance = random.randint(1, 3)  # Menghasilkan angka acak dari 1 hingga 3
        # Buat objek Pokémon tergantung pada nomor acak
        if chance == 1:
            pokemon = Pokemon(author)  # Membuat Pokémon standar
        elif chance == 2:
            pokemon = Wizard(author)  # Membuat Pokémon Wizard
        elif chance == 3:
            pokemon = Fighter(author)
        info_text = await pokemon.info()
        embed = discord.Embed(title=f"{author}'s New Pokémon", description=info_text, color=0x00ff00)
        image_url = await pokemon.show_img()
        if image_url:
            embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="You've already created your own Pokémon.", color=0xff0000)
        await ctx.send(embed=embed)

@bot.command()
async def start(ctx):
    embed = discord.Embed(title="Welcome to Pokémon Bot!", description="Hi, I am a Pokémon game bot!\n\nCommands:\n!go - Create your Pokémon\n!info - View your Pokémon\n!attack @user - Battle another trainer\n!train - Battle a wild Pokémon\n!shop - Buy food\n!feed <type> - Feed your Pokémon\n!reroll - Reroll your Pokémon (costs 200 coins)\n\nEarn coins by winning battles, buy food to level up!", color=0x00ff00)
    await ctx.send(embed=embed)

@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None
    if target:
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]
            attacker = Pokemon.pokemons[ctx.author.name]

            # Full battle
            battle_log = []
            turn = 1
            while attacker.hp > 0 and enemy.hp > 0 and turn <= 20:
                # Attacker attacks enemy
                damage = min(attacker.power, enemy.hp)
                enemy.hp -= damage
                battle_log.append(f"**Turn {turn}:** ⚔️ {attacker.pokemon_trainer}'s Pokémon attacks! {enemy.pokemon_trainer}'s HP: {enemy.hp}")

                if enemy.hp <= 0:
                    coins_gained = random.randint(10, 50)
                    attacker.coins += coins_gained
                    exp_gained = random.randint(30, 50)
                    level_msg = await attacker.gain_exp(exp_gained)
                    heal_amount = random.randint(30, 100)
                    attacker.hp = min(attacker.hp + heal_amount, attacker.max_hp)
                    battle_log.append(f"🎉 **Victory!** {attacker.pokemon_trainer} defeated {enemy.pokemon_trainer}!\n💰 +{coins_gained} coins\n⭐ +{exp_gained} EXP\n❤️ Healed {heal_amount} HP{level_msg}")
                    break

                # Enemy attacks attacker
                damage = min(enemy.power, attacker.hp)
                attacker.hp -= damage
                battle_log.append(f"**Turn {turn}:** 🗡️ {enemy.pokemon_trainer}'s Pokémon strikes back! {attacker.pokemon_trainer}'s HP: {attacker.hp}")

                if attacker.hp <= 0:
                    if random.random() < 0.4:  # 40% chance to revive
                        revive_hp = random.randint(40, 50)
                        attacker.hp = revive_hp
                        battle_log.append(f"💔 **Defeat!** {attacker.pokemon_trainer}'s Pokémon fainted but miraculously revived with {revive_hp} HP!")
                    else:
                        # Pokemon dies
                        del Pokemon.pokemons[ctx.author.name]
                        battle_log.append(f"💀 **Fatal Defeat!** {attacker.pokemon_trainer}'s Pokémon died in battle. Use !go to get a new Pokémon.")
                    break

                turn += 1

            result = "\n\n".join(battle_log)
            embed = discord.Embed(title="⚔️ Pokémon Battle", description=result, color=0xff0000)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description="Both participants must have a Pokémon to battle!", color=0xff0000)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="Mention the user you want to attack.", color=0xff0000)
        await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        info_text = await pokemon.info()
        embed = discord.Embed(title=f"{author}'s Pokémon", description=info_text, color=0x00ff00)
        image_url = await pokemon.show_img()
        if image_url:
            embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="You don't have a Pokémon yet.", color=0xff0000)
        await ctx.send(embed=embed)

@bot.command()
async def shop(ctx, food_type=None, quantity: int = 1):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        embed = discord.Embed(title="Error", description="You don't have a Pokémon yet.", color=0xff0000)
        await ctx.send(embed=embed)
        return
    pokemon = Pokemon.pokemons[author]
    if food_type is None:
        embed = discord.Embed(title="Pokémon Shop", description="Buy food to level up your Pokémon!\n\n**Prices:**\nBasic: 20 coins (10 EXP)\nRare: 50 coins (25 EXP)\nEpic: 100 coins (50 EXP)\n\nUse `!shop <type> [quantity]` to buy.", color=0x0000ff)
        await ctx.send(embed=embed)
    else:
        result = pokemon.buy_food(food_type.lower(), quantity)
        embed = discord.Embed(title="Shop Purchase", description=result, color=0x00ff00 if "Bought" in result else 0xff0000)
        await ctx.send(embed=embed)

@bot.command()
async def feed(ctx, food_type=None):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        embed = discord.Embed(title="Error", description="You don't have a Pokémon yet.", color=0xff0000)
        await ctx.send(embed=embed)
        return
    if food_type is None:
        embed = discord.Embed(title="Feed Pokémon", description="Feed your Pokémon to gain EXP!\n\nAvailable food types:\n- basic (10 EXP)\n- rare (25 EXP)\n- epic (50 EXP)\n\nUse `!feed <type>` to feed.", color=0x00ff00)
        await ctx.send(embed=embed)
    else:
        pokemon = Pokemon.pokemons[author]
        result = await pokemon.feed(food_type.lower())
        embed = discord.Embed(title="Feeding Pokémon", description=result, color=0x00ff00 if "Fed" in result else 0xff0000)
        await ctx.send(embed=embed)

@bot.command()
async def reroll(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        embed = discord.Embed(title="Error", description="You don't have a Pokémon yet.", color=0xff0000)
        await ctx.send(embed=embed)
        return
    pokemon = Pokemon.pokemons[author]
    result = await pokemon.reroll_superpower()
    embed = discord.Embed(title="Reroll Superpower", description=result, color=0x00ff00 if "Rerolled" in result else 0xff0000)
    if "Rerolled" in result:
        image_url = await pokemon.show_img()
        if image_url:
            embed.set_image(url=image_url)
    await ctx.send(embed=embed)

@bot.command()
async def train(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        embed = discord.Embed(title="Error", description="You don't have a Pokémon yet.", color=0xff0000)
        await ctx.send(embed=embed)
        return
    attacker = Pokemon.pokemons[author]
    # Create wild pokemon scaled to player level
    player_level = attacker.level
    wild_level = max(1, player_level + random.randint(-1, 1))
    wild = Pokemon("Wild")
    wild.pokemon_trainer = "Wild Pokémon"
    wild.hp = 80 + wild_level * 10
    wild.power = 8 + wild_level * 2
    wild.level = wild_level

    # Battle loop
    battle_log = []
    turn = 1
    while attacker.hp > 0 and wild.hp > 0 and turn <= 20:  # Limit turns to prevent too long
        # Attacker attacks wild
        damage = min(attacker.power, wild.hp)
        wild.hp -= damage
        battle_log.append(f"**Turn {turn}:** ⚔️ Your Pokémon attacks! Wild HP: {wild.hp}")

        if wild.hp <= 0:
            coins_gained = random.randint(10, 50)
            attacker.coins += coins_gained
            exp_gained = random.randint(30, 50)
            level_msg = await attacker.gain_exp(exp_gained)
            heal_amount = random.randint(30, 100)
            attacker.hp = min(attacker.hp + heal_amount, attacker.max_hp)
            battle_log.append(f"🎉 **Victory!** You defeated the wild Pokémon!\n💰 +{coins_gained} coins\n⭐ +{exp_gained} EXP\n❤️ Healed {heal_amount} HP{level_msg}")
            break

        # Wild attacks attacker
        damage = min(wild.power, attacker.hp)
        attacker.hp -= damage
        battle_log.append(f"**Turn {turn}:** 🐾 Wild Pokémon strikes back! Your HP: {attacker.hp}")

        if attacker.hp <= 0:
            coins_gained = random.randint(5, 15)  # Some coins even on defeat
            attacker.coins += coins_gained
            if random.random() < 0.4:  # 40% chance to revive
                revive_hp = random.randint(40, 50)
                attacker.hp = revive_hp
                battle_log.append(f"💔 **Defeat!** Your Pokémon fainted but miraculously revived with {revive_hp} HP!\n💰 +{coins_gained} coins")
            else:
                # Pokemon dies
                del Pokemon.pokemons[author]
                battle_log.append(f"💀 **Fatal Defeat!** Your Pokémon died in battle.\n💰 +{coins_gained} coins\nUse !go to get a new Pokémon.")
            break

        turn += 1

    result = "\n\n".join(battle_log)
    embed = discord.Embed(title="🏞️ Training Battle", description=result, color=0xffa500)
    await ctx.send(embed=embed)

# Simple lock to prevent multiple instances
lock_file = 'bot.lock'
if os.path.exists(lock_file):
    print("Bot is already running. Exiting.")
    sys.exit(1)

with open(lock_file, 'w') as f:
    f.write('running')

# Running the bot
bot.run(token)
