import discord
from discord.ext import commands
from discord.ui import View
import aiohttp
import os
import asyncio
import random
import time
from datetime import date, timedelta, datetime, timezone
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

active_games = {}

class ScrandleSession:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vote_time = 32.0
        self.wait_time = 17.0
        self.is_stopped = False
        self.phase = "starting"
        self.current_view = None
        self.skip_wait = asyncio.Event()
        self.scores = {}

def get_country_flag(country_name):
    if not country_name or country_name == 'Unknown':
        return "🌍"
        
    cleaned_name = str(country_name).lower().strip()
    
    flags = {
        "eng": ":england:", "sco": ":scotland:", "wal": ":wales:", "gbr": ":flag_gb:",
        "usa": ":flag_us:", "ger": ":flag_de:", "deu": ":flag_de:", "esp": ":flag_es:", 
        "ita": ":flag_it:", "fra": ":flag_fr:", "ned": ":flag_nl:", "nld": ":flag_nl:",
        "bel": ":flag_be:", "por": ":flag_pt:", "prt": ":flag_pt:", "bra": ":flag_br:", 
        "arg": ":flag_ar:", "mex": ":flag_mx:", "aus": ":flag_au:", "jpn": ":flag_jp:", 
        "kor": ":flag_kr:", "can": ":flag_ca:", "irl": ":flag_ie:", "swe": ":flag_se:", 
        "nor": ":flag_no:", "den": ":flag_dk:", "dnk": ":flag_dk:", "sui": ":flag_ch:", 
        "che": ":flag_ch:", "aut": ":flag_at:", "tur": ":flag_tr:", "gre": ":flag_gr:", 
        "grc": ":flag_gr:", "pol": ":flag_pl:", "cro": ":flag_hr:", "hrv": ":flag_hr:",
        "brb": ":flag_bb:", "gua": ":flag_gt:",
        
        "england": ":england:", "scotland": ":scotland:", "wales": ":wales:",
        "uk": ":flag_gb:", "united kingdom": ":flag_gb:", "gb": ":flag_gb:",
        "united states": ":flag_us:", "us": ":flag_us:", "germany": ":flag_de:",
        "spain": ":flag_es:", "italy": ":flag_it:", "france": ":flag_fr:",
        "netherlands": ":flag_nl:", "belgium": ":flag_be:", "portugal": ":flag_pt:",
        "brazil": ":flag_br:", "argentina": ":flag_ar:", "mexico": ":flag_mx:",
        "australia": ":flag_au:", "japan": ":flag_jp:", "south korea": ":flag_kr:", 
        "canada": ":flag_ca:", "ireland": ":flag_ie:", "sweden": ":flag_se:", 
        "norway": ":flag_no:", "denmark": ":flag_dk:", "switzerland": ":flag_ch:", 
        "austria": ":flag_at:", "turkey": ":flag_tr:", "greece": ":flag_gr:", 
        "poland": ":flag_pl:", "croatia": ":flag_hr:"
    }
    return flags.get(cleaned_name, "🌍")

def create_matchup_embeds(round_data, reveal=False):
    left_item, right_item = round_data[0], round_data[1]
    
    title_left = f"🅰️ {left_item['title']}"
    title_right = f"🅱️ {right_item['title']}"
    
    if reveal:
        title_left += f" — {left_item.get('rating', 'N/A')}%"
        title_right += f" — {right_item.get('rating', 'N/A')}%"
        
        l_rating = left_item.get('rating') or 0
        r_rating = right_item.get('rating') or 0
        if l_rating > r_rating:
            title_left = f"🏆 {title_left}"
        elif r_rating > l_rating:
            title_right = f"🏆 {title_right}"

    def get_details(item):
        raw_price = item.get('price')
        if raw_price is not None:
            try:
                price = f"£{float(raw_price):.2f}"
            except (ValueError, TypeError):
                price = str(raw_price)
        else:
            price = "N/A"
            
        country = item.get('country', 'Unknown')
        flag = get_country_flag(country)
        
        lines = [f"📍 **Country:** {flag} {country}"]
        
        venue = item.get('stadium') or item.get('venue') or item.get('club') or item.get('location')
        if venue:
            lines.append(f"🏟️ **Venue:** {venue}")
            
        match = item.get('match') or item.get('team') or item.get('event')
        if match:
            lines.append(f"⚽ **Match:** {match}")
            
        lines.append(f"💰 **Price:** {price}")
        
        desc = item.get('description') or item.get('text')
        if desc and desc != item.get('title'):
            if len(desc) > 85:
                desc = desc[:82] + "..."
            lines.append(f"📝 **Info:** {desc}")
            
        return "\n".join(lines)

    embed_left = discord.Embed(title=title_left, description=get_details(left_item), color=discord.Color.blue())
    embed_right = discord.Embed(title=title_right, description=get_details(right_item), color=discord.Color.red())
    
    if not reveal and left_item.get('images_new'):
        embed_left.set_image(url=left_item['images_new'][0])
    if not reveal and right_item.get('images_new'):
        embed_right.set_image(url=right_item['images_new'][0])
    
    return [embed_left, embed_right]

class ScrandleVoteView(View):
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.votes = {}

    @discord.ui.button(label="Option A", emoji="🅰️", style=discord.ButtonStyle.primary, custom_id="vote_left")
    async def vote_left(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.register_vote(interaction, "Option A")

    @discord.ui.button(label="Option B", emoji="🅱️", style=discord.ButtonStyle.danger, custom_id="vote_right")
    async def vote_right(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.register_vote(interaction, "Option B")

    async def register_vote(self, interaction: discord.Interaction, choice_name: str):
        self.votes[interaction.user.id] = (choice_name, interaction.user.display_name)
        await interaction.response.send_message(f"Vote locked in for **{choice_name}**!", ephemeral=True)

async def fetch_scrandle_data(target_date=None):
    if target_date:
        url = f"https://scrandle.com/history/{target_date}"
    else:
        url = "https://scrandle.com/daily"
        
    async with aiohttp.ClientSession() as session:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                payload = await response.json()
                return payload.get("data", [])
            return []

async def play_scrandle_loop(ctx, session, all_rounds):
    active_games[ctx.channel.id] = session
    
    for i, round_data in enumerate(all_rounds):
        if session.is_stopped:
            break
            
        embeds = create_matchup_embeds(round_data, reveal=False)
        session.current_view = ScrandleVoteView(timeout=session.vote_time)
        session.phase = "voting"
        
        end_time = int(time.time() + session.vote_time)
        msg = await ctx.send(
            content=f"⏳ **Round {i + 1} of {len(all_rounds)}!**\nWhich scran do you think fans rated higher?\nVoting ends <t:{end_time}:R>!", 
            embeds=embeds, 
            view=session.current_view
        )
        
        await session.current_view.wait()
        
        if session.is_stopped:
            await msg.edit(view=None)
            break
            
        for child in session.current_view.children:
            child.disabled = True
        await msg.edit(view=session.current_view)
        
        left_item, right_item = round_data[0], round_data[1]
        l_rating = left_item.get('rating') or 0
        r_rating = right_item.get('rating') or 0
        
        votes_a_names = [name for choice, name in session.current_view.votes.values() if choice == "Option A"]
        votes_b_names = [name for choice, name in session.current_view.votes.values() if choice == "Option B"]
        
        if l_rating > r_rating:
            winner_text = f"🏆 **{left_item.get('title', 'Option A')}** takes the crown!"
            round_winners = votes_a_names
        elif r_rating > l_rating:
            winner_text = f"🏆 **{right_item.get('title', 'Option B')}** takes the crown!"
            round_winners = votes_b_names
        else:
            winner_text = "It's a dead heat!"
            round_winners = votes_a_names + votes_b_names
            
        for winner in round_winners:
            session.scores[winner] = session.scores.get(winner, 0) + 1
            
        a_voters = ", ".join(votes_a_names) if votes_a_names else "Nobody"
        b_voters = ", ".join(votes_b_names) if votes_b_names else "Nobody"
        winners_display = ", ".join(round_winners) if round_winners else "Nobody"
        
        results_text = (
            f"**Round {i + 1} Over!** {winner_text}\n"
            f"👑 **Correct Guesses:** {winners_display}\n\n"
            f"**How the channel voted:**\n"
            f"🅰️ **Option A:** {a_voters}\n"
            f"🅱️ **Option B:** {b_voters}"
        )
        
        revealed_embeds = create_matchup_embeds(round_data, reveal=True)
        await ctx.send(content=results_text, embeds=revealed_embeds)
        
        if i < len(all_rounds) - 1:
            session.phase = "waiting"
            session.skip_wait.clear()
            next_time = int(time.time() + session.wait_time)
            await ctx.send(f"⏱️ *Next round starts <t:{next_time}:R>... (Type `/scrandlenext` to skip)*")
            
            try:
                await asyncio.wait_for(session.skip_wait.wait(), timeout=session.wait_time)
            except asyncio.TimeoutError:
                pass 

    if not session.is_stopped:
        if session.scores:
            sorted_scores = sorted(session.scores.items(), key=lambda item: item[1], reverse=True)
            podium_lines = []
            medals = ["🥇", "🥈", "🥉"]
            for i, (name, score) in enumerate(sorted_scores):
                medal = medals[i] if i < 3 else "🏅"
                podium_lines.append(f"{medal} **{name}** ({score}/{len(all_rounds)})")
            
            podium_text = "\n".join(podium_lines)
            await ctx.send(f"🏁 **That's all the matchups for this Scrandle!**\n\n🏆 **Final Podium:**\n{podium_text}")
        else:
            await ctx.send("🏁 **That's all the matchups for this Scrandle!**\n\nNo one scored any points!")
    
    if ctx.channel.id in active_games:
        del active_games[ctx.channel.id]

@bot.hybrid_command(name='scrandle', description="Starts today's live Scrandle matchup in the current channel.")
@commands.cooldown(1, 30, commands.BucketType.guild)
async def start_scrandle(ctx):
    await ctx.defer()
    if ctx.channel.id in active_games:
        await ctx.send("A Scrandle game is already running in this channel! Type `/scrandlestop` to end it.")
        return
        
    all_rounds = await fetch_scrandle_data()
    if not all_rounds:
        await ctx.send("Failed to fetch today's Scrandle data.")
        return
        
    await ctx.send("🏟️ **Starting today's Scrandle!**")
    session = ScrandleSession(ctx)
    await play_scrandle_loop(ctx, session, all_rounds)

@bot.hybrid_command(name='scrandlerandom', description="Fetches a random date from Scrandle's history and runs a full game.")
@commands.cooldown(1, 30, commands.BucketType.guild)
async def start_random_scrandle(ctx):
    await ctx.defer()
    if ctx.channel.id in active_games:
        await ctx.send("A Scrandle game is already running in this channel!")
        return
        
    start_date = date(2025, 12, 1)
    time_between = date.today() - start_date
    random_date = start_date + timedelta(days=random.randrange(time_between.days))
    date_str = random_date.strftime("%Y-%m-%d")
    
    await ctx.send(f"🎲 **Fetching random Scrandle from {date_str}...**")
    all_rounds = await fetch_scrandle_data(target_date=date_str)
    
    if not all_rounds:
        await ctx.send("Failed to fetch data for that date. The endpoint might have been empty.")
        return
        
    session = ScrandleSession(ctx)
    await play_scrandle_loop(ctx, session, all_rounds)

@bot.hybrid_command(name='scrandlestop', description="Instantly halts any active game in the channel.")
async def stop_scrandle(ctx):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("❌ You need the `Manage Messages` permission to stop a game.", ephemeral=True)
        return
        
    session = active_games.get(ctx.channel.id)
    if not session:
        await ctx.send("There is no active Scrandle game to stop.", ephemeral=True)
        return
        
    session.is_stopped = True
    await ctx.send("🛑 **Stopping the current Scrandle game...**")
    
    if session.phase == "voting" and session.current_view:
        session.current_view.stop()
    elif session.phase == "waiting":
        session.skip_wait.set()

@bot.hybrid_command(name='scrandlenext', description="Immediately forces the game to skip its current timer.")
async def next_scrandle(ctx):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("❌ You need the `Manage Messages` permission to skip timers.", ephemeral=True)
        return
        
    session = active_games.get(ctx.channel.id)
    if not session:
        await ctx.send("There is no active Scrandle game.", ephemeral=True)
        return
        
    if session.phase == "voting" and session.current_view:
        await ctx.send("⏭️ **Voting ended early!**")
        session.current_view.stop()
    elif session.phase == "waiting":
        await ctx.send("⏭️ **Skipping wait time!**")
        session.skip_wait.set()

@bot.hybrid_command(name='scrandledelay', description="Dynamically overrides the default timers for an active game.")
async def set_scrandle_delay(ctx, vote_seconds: float, wait_seconds: float):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("❌ You need the `Manage Messages` permission to change delays.", ephemeral=True)
        return
        
    if vote_seconds < 5 or wait_seconds < 3:
        await ctx.send("Timers are too short! Minimum is 5s for voting and 3s for waiting.", ephemeral=True)
        return
    if vote_seconds > 300 or wait_seconds > 120:
        await ctx.send("Timers are too long! Maximum is 300s for voting and 120s for waiting.", ephemeral=True)
        return
        
    session = active_games.get(ctx.channel.id)
    if not session:
        await ctx.send("Start a Scrandle game first to adjust its delays.", ephemeral=True)
        return
        
    session.vote_time = vote_seconds
    session.wait_time = wait_seconds
    await ctx.send(f"⏱️ **Delays updated!** Next rounds will use {vote_seconds}s for voting and {wait_seconds}s between rounds.")

@bot.hybrid_command(name='scrandlecountdown', description="Shows the time remaining until the next daily Scrandle.")
async def scrandle_countdown(ctx):
    now = datetime.now(timezone.utc)
    tomorrow = now.date() + timedelta(days=1)
    midnight = datetime.combine(tomorrow, datetime.min.time(), tzinfo=timezone.utc)
    
    # Convert midnight UTC to a Unix timestamp integer
    midnight_ts = int(midnight.timestamp())
    
    await ctx.send(f"⏳ The next daily Scrandle drops <t:{midnight_ts}:R> (at <t:{midnight_ts}:t> your local time).")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Please wait {error.retry_after:.0f} seconds before starting another game in this server.", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name}. Slash commands synced.')

bot.run(os.getenv('DISCORD_TOKEN'))