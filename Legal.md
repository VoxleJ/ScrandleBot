# Legal, Terms of Service & Privacy Policy

## ⚠️ Disclaimer & Attribution
**This bot is a fan-made, open-source project and is NOT meant to replace the actual Scrandle game.** 

All Scrandle concepts, images, daily matchups, ratings, and data belong entirely to the original creators at [scrandle.com](https://scrandle.com) and the fantastic [@FootyScran](https://twitter.com/FootyScran) community. This bot was built purely as a fun, non-commercial way to experience the daily Scrandle with friends in a multiplayer Discord setting. 

If you enjoy the bot, please go support the official game, build your daily streaks, and suffer the pain of Evil Mode directly on their website!

---

## Privacy Policy
*Last Updated: [Insert Date]*

This Privacy Policy explains how the Scrandle Discord Bot ("the Bot") collects, uses, and protects your information when you interact with it in any Discord server.

### 1. Data We Collect
The Bot collects the absolute minimum amount of data required to function. When you interact with the Bot (e.g., by clicking a voting button or using a slash command), we temporarily process:
* **Discord User IDs:** Used exclusively to prevent users from voting twice in the same round and to track scores across the game session.
* **Discord Display Names:** Used to generate the end-of-game podium leaderboard and display who voted for which option.
* **Discord Channel/Server IDs:** Used to route the active game states and ensure multiple games can run simultaneously across different servers without overlapping.

### 2. Data Usage & Storage
* **In-Memory Only:** The Bot does **not** use a persistent database. All User IDs, Display Names, and temporary scores are stored solely in the bot's live RAM (via the `active_games` Python dictionary). 
* **Data Deletion:** The moment a 10-round game concludes (or if the game is stopped via the `/scrandlestop` command), all data associated with that session is permanently wiped from memory.
* **No Message Content Reading:** The Bot relies entirely on Discord Slash Commands and Interaction Buttons. It does not read, log, or store the content of standard chat messages in your server.

### 3. Data Sharing
We do not share, sell, or distribute your Discord data to any third parties. The bot fetches daily matchup data from the public `scrandle.com` API, but no user data is sent in those requests.

---

## Terms of Service
*Last Updated: [Insert Date]*

By inviting the Bot to your Discord server or interacting with its commands, you agree to these Terms of Service.

### 1. Acceptable Use
The Bot is provided "as is" for casual, non-commercial entertainment. You agree not to:
* Intentionally spam the Bot's commands to cause rate-limiting issues or disruption to the Scrandle API.
* Attempt to exploit, modify, or break the Bot's asynchronous game loops.
* Use the Bot in any way that violates Discord's global Terms of Service or Community Guidelines.

### 2. Availability & Uptime
Because this is a free, hobbyist project, there are no guarantees regarding uptime, latency, or availability. The Bot may go offline for maintenance, or its functionality may break if the official Scrandle website updates its API structure. The developer reserves the right to shut down or restart the Bot at any time.

### 3. Limitation of Liability
The developer of this Bot is not responsible for any issues, damages, or moderation actions (including rate limits or IP bans) that occur as a result of using this Bot in your server. You assume all responsibility for the Bot's interactions within your community.

### 4. Changes to Terms
We reserve the right to update this Privacy Policy and Terms of Service at any time. Significant changes to how data is handled will be reflected in this document. Continued use of the Bot constitutes agreement to the updated terms.

---
*For any questions, issues, or to report a bug, please open an Issue in this GitHub repository.*