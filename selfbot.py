import discord
from discord.ext import commands
import json
import datetime
import os

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_update(before, after):
    if before.display_name!= after.display_name:
        user_id = after.id
        with open('prevnames.json', 'r+', encoding='utf-8') as f:
            prevnames_data = json.load(f)
            if user_id not in prevnames_data:
                prevnames_data[user_id] = []
            prevnames_data[user_id].append({
                'name': after.display_name,
                'timestamp': datetime.datetime.now().isoformat()
            })
            f.seek(0)
            json.dump(prevnames_data, f, ensure_ascii=False, indent=4)
            f.truncate()

@bot.command(name='prevnames', help='Afficher les anciens pseudos d\'un utilisateur')
async def prevnames(ctx, user: discord.User = None):
    with open('prevnames.json', 'r', encoding='utf-8') as f:
        prevnames_data = json.load(f)
    if user.id not in prevnames_data:
        await ctx.send(f"Aucun ancien pseudo trouvé pour {user.name}.")
        return
    prevnames_list = prevnames_data[user.id]
    prevnames_list = [prevname for prevname in prevnames_list if prevname['name']!= user.display_name]
    prevnames_str = ''
    for i, prevname in enumerate(prevnames_list, start=1):
        prevnames_str += f"{i}. {prevname['name']} ({prevname['timestamp']}), "
    prevnames_str = prevnames_str.rstrip(', ')
    await ctx.send(f"Anciens pseudos pour {user.name}:\n{prevnames_str}")

if not os.path.exists('prevnames.json'):
    with open('prevnames.json', 'w', encoding='utf-8') as f:
        json.dump({}, f, ensure_ascii=False, indent=4)

bot.run('YOUR_TOKEN')