import discord
from discord.ext import commands
import openai
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is connected and ready.")

@bot.tree.command(name="ask", description="Ask AiAdam a question")
@discord.app_commands.describe(question="What do you want to ask AiAdam?")
async def ask(interaction: discord.Interaction, question: str):
    if str(interaction.channel_id) != "1400043075727917189":  # ask-adam channel ID
        await interaction.response.send_message("Please use this command in #ask-adam.", ephemeral=True)
        return

    await interaction.response.defer(thinking=True)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are AiAdam, a Discord bot that answers questions about the ONE Cardano project."},
            {"role": "user", "content": question},
        ]
    )

    answer = response.choices[0].message.content
    await interaction.followup.send(answer)

bot.run(DISCORD_TOKEN)
