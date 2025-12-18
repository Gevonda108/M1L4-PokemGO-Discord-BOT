# PokéGO Discord Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-green.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A fun and interactive Discord bot that brings the excitement of Pokémon training, battling, and exploration right into your Discord server! Engage in epic battles, level up your Pokémon, and compete with friends in this text-based Pokémon adventure.

## 🌟 Features

- **Pokémon Creation**: Randomly generate your own Pokémon with unique stats and abilities.
- **Battling System**: Challenge other trainers or battle wild Pokémon to gain experience and coins.
- **Shop & Feeding**: Buy food to level up your Pokémon and increase their power.
- **Rerolling**: Change your Pokémon's superpower for a fee.
- **Rich Embeds**: Beautiful Discord embeds with Pokémon images and detailed information.
- **Multiplayer**: Battle friends and climb the ranks.
- **Anti-Spam**: Built-in lock mechanism to prevent multiple bot instances.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A Discord Bot Token (from [Discord Developer Portal](https://discord.com/developers/applications))

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Gevonda108/M1L4-PokemGO-Discord-BOT.git
   cd M1L4-PokemGO-Discord-BOT
   ```

2. **Install dependencies**:
   ```bash
   pip install discord.py aiohttp
   ```

3. **Create configuration file**:
   - Create a file named `config.py` in the project root.
   - Add your Discord bot token:
     ```python
     token = 'YOUR_DISCORD_BOT_TOKEN_HERE'
     ```
   > **Note**: `config.py` is not included in the repository for security reasons. You must create it manually.

4. **Run the bot**:
   ```bash
   python main.py
   ```

### Inviting the Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Select your application and navigate to the "OAuth2" section.
3. Under "Scopes", check "bot".
4. Under "Bot Permissions", select:
   - Send Messages
   - Use Slash Commands
   - Embed Links
   - Read Message History
5. Copy the generated URL and invite the bot to your server.

## 🎮 Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `!start` | Display welcome message and command list | `!start` |
| `!go` | Create your Pokémon (one-time only) | `!go` |
| `!info` | View your Pokémon's stats | `!info` |
| `!attack @user` | Battle another trainer | `!attack @username` |
| `!train` | Battle a wild Pokémon | `!train` |
| `!shop` | View shop items | `!shop` |
| `!shop <type> [quantity]` | Buy food for your Pokémon | `!shop basic 5` |
| `!feed <type>` | Feed your Pokémon to gain EXP | `!feed rare` |
| `!reroll` | Reroll your Pokémon's superpower (costs 200 coins) | `!reroll` |

### Pokémon Types

- **Standard Pokémon**: Balanced stats.
- **Wizard Pokémon**: Special abilities in battle.
- **Fighter Pokémon**: Increased attack power.

## 📖 How to Play

1. **Get Started**: Use `!go` to create your first Pokémon.
2. **Explore**: Check your Pokémon's info with `!info`.
3. **Battle**: Use `!train` to fight wild Pokémon and gain coins/EXP, or `!attack @user` to challenge friends.
4. **Level Up**: Buy food from the shop with `!shop` and feed your Pokémon with `!feed` to increase levels.
5. **Customize**: Use `!reroll` to change your Pokémon's abilities (requires coins).

### Battle Mechanics

- Battles are turn-based with a 20-turn limit.
- Winner gains coins and EXP, loser may faint or revive.
- Fatal defeats result in Pokémon death (use `!go` for a new one).

## 🛠️ Development

### Project Structure

```
M1L4/
├── main.py          # Main bot file with commands
├── logic.py         # Pokémon classes and game logic
├── config.py        # Configuration (create manually)
└── README.md        # This file
```

### Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -am 'Add feature'`.
4. Push to branch: `git push origin feature-name`.
5. Submit a pull request.


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Pokémon data sourced from [PokeAPI](https://pokeapi.co/).
- Built with [discord.py](https://discordpy.readthedocs.io/).
- Inspired by classic RPG games.

## 📞 Support

If you encounter issues or have suggestions, please [open an issue](https://github.com/Gevonda108/M1L4-PokemGO-Discord-BOT/issues) on GitHub.

---

*Made with ❤️ for Pokémon fans everywhere!* 🚀</content>
<parameter name="filePath">c:\Users\ASUS\M1L1\M1L4\ENG-PythonLVL3-M1L4\README.md
