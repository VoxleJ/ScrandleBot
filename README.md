# 🏟️ ScrandleBot for Discord

A feature-rich, asynchronous Discord bot that brings the fun of [Scrandle](https://scrandle.com) directly to your server. 

This bot handles the data fetching, interactive voting, and competitive scoring so you and your friends can argue about stadium food.

---

## ✨ Features
* **Daily & Historical Integration:** Play the current day's Scrandle or pull a random match from the archives.
* **Interactive Gameplay:** Utilizes Discord's native UI buttons for seamless voting. Users can switch their votes before the timer expires to fix accidental misclicks.
* **Dynamic Leaderboards:** Tracks correct guesses across the 10-round game and generates a final 🥇🥈🥉 podium to crown the server's food critic.


---

## 🛠️ Prerequisites
* Python 3.8 or higher
* A Discord Bot Token (grab one from the [Discord Developer Portal](https://discord.com/developers/applications))
* Required Python packages: `discord.py`, `aiohttp`, `python-dotenv`

---

## 🚀 Installation & Setup

**1. Clone the repository:**
```bash
git clone [https://github.com/VoxleJ/ScrandleBot.git](https://github.com/YourUsername/ScrandleBot.git)
cd ScrandleBot
```

**2. Install dependencies:**
```bash
pip install discord.py aiohttp python-dotenv
```

**3. Configure your environment variables:**
Create a `.env` file in the root directory of the project and add your Discord token:
```env
DISCORD_TOKEN=your_bot_token_here
```
*⚠️ Note: Ensure your `.env` file is listed in your `.gitignore` before pushing any changes to GitHub to prevent your token from being leaked and revoked.*

**4. Run the bot:**
```bash
python main.py
```

---

## 🎮 Commands List

| Command | Description | Permissions |
| :--- | :--- | :--- |
| `/scrandle` | Starts today's live Scrandle matchup. | Everyone |
| `/scrandlerandom` | Fetches a random date from Scrandle's history and runs a full game. | Everyone |
| `/scrandlecountdown` | Shows the exact, localized time remaining until the next daily Scrandle drop. | Everyone |
| `/scrandlestop` | Instantly halts any active game in the channel. | `Manage Messages` |
| `/scrandlenext` | Immediately forces the game to skip its current wait timer. | `Manage Messages` |
| `/scrandledelay` | Dynamically overrides the default timers for an active game (Min: 5s/3s, Max: 300s/120s). | `Manage Messages` |

---

## ⚖️ Legal & Attribution
**This bot is a fan-made, open-source project and is NOT meant to replace the actual Scrandle game.** 

All Scrandle concepts, images, daily matchups, ratings, and data belong entirely to the original creators at [scrandle.com](https://scrandle.com) and the [@FootyScran](https://twitter.com/FootyScran) community. Please review the [Legal.md](Legal.md) file for the full Terms of Service and Privacy Policy regarding data usage within Discord. Go support the official creators!