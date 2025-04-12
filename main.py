import discord
from discord.ext import commands, tasks
from yisona import Yisona
import random
import os
from dotenv import load_dotenv
import datetime
import time

load_dotenv()
Token = os.getenv("Token")
bot = commands.Bot(intents=discord.Intents.all())
economy = Yisona("./data/economy.json")
cooldown = Yisona("./data/cooldown.json")
color_wish = discord.Color.red()

# checks #
def check_user(user_id):
    if economy.get_json(user_id) is None:
        economy.create_json(user_id, value={"money": 0, "bank": 0, "level": 1, "xp": 0})
        cooldown.create_json(user_id, value={"daily": "0", "work": "0", "stream": "0"})
        return True

@tasks.loop(seconds=1)
async def scan():
    print("test")

async def exp(user_id):
    gg = int(economy.get_json(f"{user_id}.xp"))
    xp = gg + 4
    economy.write_json(f"{user_id}.xp", value=xp)
    if int(economy.get_json(f"{user_id}.xp")) > 200:
        economy.write_json(f"{user_id}.xp", value="0")
        old = int(economy.get_json(f"{user_id}.level")) + 1
        economy.write_json(f"{user_id}.level", value=old)


@bot.event
async def on_message(ctx):
    if ctx.author.bot:
        return
    check_user(ctx.author.id)
    await exp(ctx.author.id)    

@tasks.loop(seconds=1)
async def status():
    st = Yisona("./data/logs.json").get_json('counter')
    await bot.change_presence(activity=discord.Game(name=f"{st} Commands used!"))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} - {bot.user.id}")
    print("Bot is ready!")
    await status.start()
    
@bot.event
async def on_slash_command_error(ctx, error):
    if isinstance(error, discord.ApplicationCommandInvokeError):
        embed = discord.Embed(
            title="Error",
            description="An error occurred while executing the command.",
            color=0xff0000
        )
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        raise error

@bot.event
async def on_application_command(ctx):
    Yisona("./data/logs.json").create_json(f"Log.{random.randint(1,20000)}",value=f"Command: {ctx.command.name} | User: {ctx.user.name} | Guild: {ctx.guild.name}")
    Yisona("./data/logs.json").write_json(f"counter", value=int(Yisona("./data/logs.json").get_json("counter"))+1)
    await exp(ctx.author.id)    

# Stats #

@bot.slash_command(name="stats", description="Check your stats")
async def stats(ctx):
    check_user(ctx.user.id)
    money = economy.get_json(f"{ctx.user.id}.money")
    bank = economy.get_json(f"{ctx.user.id}.bank")
    level = economy.get_json(f"{ctx.user.id}.level")
    xp = economy.get_json(f"{ctx.user.id}.xp")
    embed = discord.Embed(
        title=f"{ctx.user.name}'s Stats",
        description=f"**Here are your stats:**\n\n"

                    f"**Money:**\n```{money}```"
                    f"**Bank:**\n```{bank}```"
                    f"**Level:**\n```{level}```"
                    f"**XP:**\n```{xp}```",
        color=color_wish,
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_thumbnail(url=ctx.user.avatar.url)
    await ctx.respond(embed=embed)

@bot.slash_command(name="balance", description="Check your balance")
async def balance(ctx):
    check_user(ctx.user.id)
    money = economy.get_json(f"{ctx.user.id}.money")
    bank = economy.get_json(f"{ctx.user.id}.bank")
    embed = discord.Embed(title="Balance", color=color_wish)
    embed.add_field(name="Money", value=money, inline=True)
    embed.add_field(name="Bank", value=bank, inline=True)
    await ctx.respond(embed=embed)

@bot.slash_command(name="level", description="Check your level")
async def level(ctx):
    check_user(ctx.user.id)
    level = economy.get_json(f"{ctx.user.id}.level")
    embed = discord.Embed(title="Level", color=color_wish)
    embed.add_field(name="Level", value=level, inline=True)
    await ctx.respond(embed=embed)

# cooldown cmds #

def check_cooldown(user_id, command):
    user_id = str(user_id)
    last_used = cooldown.get_json(f"{user_id}.{command}")
    
    if last_used is None:
        return True
    
    try:
        last_time = datetime.datetime.fromisoformat(last_used)
        now = datetime.datetime.now()
        
        if command == "daily":
            return (now - last_time).total_seconds() >= 86400  # 24 Stunden
        elif command == "work":
            return (now - last_time).total_seconds() >= 3600  # 1 Stunde
        elif command == "stream":
            return (now - last_time).total_seconds() >= 7200  # 2 Stunden
        elif command == "steal":
            return (now - last_time).total_seconds() >= 16400  # 4 Stunden
        
        return False
    except ValueError:
        return True

def update_cooldown(user_id, command):
    user_id = str(user_id)
    now = datetime.datetime.now().isoformat()
    cooldown.write_json(f"{user_id}.{command}", now)

@bot.slash_command(name="daily", description="Get your daily reward")
async def daily(ctx):
    check_user(ctx.user.id)
    
    if check_cooldown(ctx.user.id, "daily"):
        update_cooldown(ctx.user.id, "daily")
        
        old = economy.get_json(f"{ctx.user.id}.money")
        bonus = random.randint(100, 500)
        new = old + bonus
        
        economy.write_json(f"{ctx.user.id}.money", new)
        
        embed = discord.Embed(title="Daily Reward", color=color_wish, 
                             description=f"You got your daily bonus of {bonus}$.")
        embed.add_field(name="Money", value=f"```{old}$ --> {new}$```", inline=True)
        
        await ctx.respond(embed=embed)
    else:
        last_used = datetime.datetime.fromisoformat(cooldown.get_json(f"{ctx.user.id}.daily"))
        next_available = last_used + datetime.timedelta(days=1)
        now = datetime.datetime.now()
        
        time_left = next_available - now
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        embed = discord.Embed(title="Daily Reward", color=0xff0000,
                             description=f"You have already claimed your daily reward!")
        embed.add_field(name="Next reward available in", 
                       value=f"```{time_left.days} days, {hours} hours, {minutes} minutes```")
        
        await ctx.respond(embed=embed)
@bot.slash_command(name="work", description="Work for money")
async def work(ctx):
    check_user(ctx.user.id)
    
    if check_cooldown(ctx.user.id, "work"):
        update_cooldown(ctx.user.id, "work")
        
        sus = economy.get_json(f"{ctx.user.id}.bank")
        reb = random.randint(100, 300)
        new = sus + reb
        zahl = reb/60
        
        economy.write_json(f"{ctx.user.id}.bank", new)
        
        embed = discord.Embed(title="Work", color=color_wish, 
                             description=f"You've worked for {zahl:.1f}h and earned {reb}$ from it!")
        embed.add_field(name="Bank", value=f"```{sus}$ --> {new}$```", inline=True)
        
        await ctx.respond(embed=embed)
    else:
        last_used = datetime.datetime.fromisoformat(cooldown.get_json(f"{ctx.user.id}.work"))
        next_available = last_used + datetime.timedelta(hours=1)
        now = datetime.datetime.now()
        
        time_left = next_available - now
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        embed = discord.Embed(title="Work", color=0xff0000,
                             description="You need to rest before working again!")
        embed.add_field(name="Available in", 
                       value=f"```{hours} hours, {minutes} minutes```")
        
        await ctx.respond(embed=embed)

@bot.slash_command(name="stream", description="Stream for money")
async def stream(ctx):
    check_user(ctx.user.id)
    
    if check_cooldown(ctx.user.id, "stream"):
        update_cooldown(ctx.user.id, "stream")
        
        sus = economy.get_json(f"{ctx.user.id}.bank")
        reb = random.randint(100, 300)
        new = sus + reb
        zahl = reb/60
        
        economy.write_json(f"{ctx.user.id}.bank", new)
        
        embed = discord.Embed(title="Stream", color=color_wish, 
                             description=f"You streamed for {zahl:.1f}h and earned {reb}$")
        embed.add_field(name="Bank", value=f"```{sus}$ --> {new}$```", inline=True)
        
        await ctx.respond(embed=embed)
    else:
        last_used = datetime.datetime.fromisoformat(cooldown.get_json(f"{ctx.user.id}.stream"))
        next_available = last_used + datetime.timedelta(hours=2)
        now = datetime.datetime.now()
        
        time_left = next_available - now
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        embed = discord.Embed(title="Stream", color=0xff0000,
                             description="You need to rest before streaming again!")
        embed.add_field(name="Available in", 
                       value=f"```{hours} hours, {minutes} minutes```")
        
        await ctx.respond(embed=embed)

# bank cmds #

@bot.slash_command(name="deposit", description="Deposit money into your bank")
async def deposit(ctx, amount: int):
    check_user(ctx.user.id)
    if economy.get_json(f"{ctx.author.id}.money") < amount:
        await ctx.respond("You arent that rich homeboy :)", ephemeral =True)
    else:
        gg = economy.get_json(f"{ctx.author.id}.money")-amount
        ba = economy.get_json(f"{ctx.author.id}.bank")+amount
        gg1 = economy.get_json(f"{ctx.author.id}.money")
        ba1 = economy.get_json(f"{ctx.author.id}.bank")
        economy.write_json(f"{ctx.author.id}.bank", value=ba)
        economy.write_json(f"{ctx.author.id}.money", value=gg)

        new_bank = economy.get_json(f"{ctx.author.id}.bank")
        new_money = economy.get_json(f"{ctx.author.id}.money")

        embed = discord.Embed(
            description=f"** You deposited {amount}$ to your Bank**\n\n",
            color=color_wish,
            thumbnail=ctx.author.avatar.url
        )
        embed.add_field(name="Bank", value=f"```{ba1}$ --> {new_bank}$```")
        embed.add_field(name="Money", value=f"```{gg1}$ --> {new_money}$```")

        await ctx.respond(embed=embed)
        
@bot.slash_command(name="withdraw", description="Withdraw money from our bank account")
async def withdraw(ctx, amount : int):
    check_user(ctx.author.id)
    if amount > economy.get_json(f"{ctx.author.id}.bank"):
        await ctx.respond("You arent that rich homeboy :)", ephemeral =True)
    else:
        try:
            old_bank = economy.get_json(f"{ctx.author.id}.bank")
            new = economy.get_json(f"{ctx.author.id}.bank") - amount
            old_money = economy.get_json(f"{ctx.author.id}.money")
            new_money = economy.get_json(f"{ctx.author.id}.money")+ amount

            economy.write_json(f"{ctx.author.id}.bank", value=new)
            economy.write_json(f"{ctx.author.id}.money", value=new_money)

            embed = discord.Embed(
                description=f"** You withdrawed {amount}$ from your bank account**",
                color=color_wish,
                thumbnail=ctx.author.avatar.url
            )
            embed.add_field(name="Bank", value=f"```{old_bank}$ --> {new}$```")
            embed.add_field(name="Money", value=f"```{old_money}$ --> {new_money}$```")
            await ctx.respond(embed=embed)
        except:
            print("test")    

# Gambling Cmds (the best) #


@bot.slash_command(name="roulette", description="Play some roulette")
async def roulette(ctx, 
                  option: discord.Option(str, "Choose your bet", choices=["red", "black"]),
                  amount: discord.Option(int, "Amount to bet", min_value=1)):
    check_user(ctx.user.id)
    
    user_money = economy.get_json(f"{ctx.user.id}.money")
    
    if amount > user_money:
        embed = discord.Embed(title="Roulette", color=0xff0000,
                             description="You don't have enough money for this bet!")
        embed.add_field(name="Your balance", value=f"```{user_money}$```")
        await ctx.respond(embed=embed)
        return
    
    colors = ["red", "black"]
    weights = [18/37, 18/37]  
    result = random.choices(colors, weights=weights)[0]
    
    embed = discord.Embed(title="Roulette", color=color_wish,
                         description=f"Spinning the wheel...")
    embed.add_field(name="Your bet", value=f"```{option}: {amount}$```")
    message = await ctx.respond(embed=embed)
    time.sleep(5)
    
    if result == option:
        new_money = user_money + amount
        win_text = f"You won {amount}$!"
        result_color = 0x00ff00  
    else:
        new_money = user_money - amount
        win_text = f"You lost {amount}$!"
        result_color = 0xff0000  
    
    economy.write_json(f"{ctx.user.id}.money", new_money)
    
    embed = discord.Embed(title="Roulette", color=result_color,
                         description=f"The ball landed on **{result}**!\n{win_text}")
    embed.add_field(name="Money", value=f"```{user_money}$ → {new_money}$```", inline=True)
    
    await message.edit(embed=embed)

@bot.slash_command(name="dice", description="Play some dice")
async def dice(ctx, amount:int):
    if amount > economy.get_json(f"{ctx.author.id}.money"):
        await ctx.respond("You cant bet more than you have on hand!")
    else:
        bet = discord.Embed(
            description="Your Bet:",
            color=color_wish
        )    
        bet.add_field(name="Amount", value=amount, inline=False)

        message = await ctx.respond(embed = bet)

        time.sleep(2)

        user_number = random.randint(1, 6)
        user_number_2 = random.randint(1,6)
        enemmy_number = random.randint(1, 6)
        enemmy_number_2 = random.randint(1,6)
        user_final = user_number+user_number_2
        enemy_final = enemmy_number_2+enemmy_number

        def wurf(number, type):
            f"Your {type}.Number is {number}"

       
        yu =  discord.Embed(
            description=f"Your first Number is {user_number}!",
            color=color_wish
        )  
        await message.edit(embed=yu)

        time.sleep(5)
        yu2 =  discord.Embed(
            description=f"Your second Number is {user_number_2}!",
            color=color_wish
        )  
        await message.edit(embed=yu2)
        time.sleep(5)

        yu3 =  discord.Embed(
            description=f"Your final is {user_final}!",
            color=color_wish
        )  
        await message.edit(embed=yu3)
        time.sleep(5)

        st = discord.Embed(
            description="Enemy`s turn!",
            color=color_wish
        )
        await message.edit(embed=st)


        time.sleep(5)
        e =  discord.Embed(
            description=f"Enemy`s first Number is {enemmy_number}!",
            color=color_wish
        )  
        await message.edit(embed=e)

        time.sleep(5)
        ee =  discord.Embed(
            description=f"Enemy`s second Number is {enemmy_number_2}!",
            color=color_wish
        )  
        await message.edit(embed=ee)
        time.sleep(5)
        eee =  discord.Embed(
            description=f"Enemy`s final is {enemy_final}!",
            color=color_wish
        )  
        await message.edit(embed=eee)
        check = economy.get_json(f"{ctx.author.id}.money")
        time.sleep(2)
        if user_final > enemy_final:
            embed= discord.Embed(
                title="You won!",
                description=f"Your won {amount*2}$",
                color=color_wish
            )
            embed.add_field(name="The Bets:", value=f"{user_final} > {enemy_final}", inline=False)
            gg = economy.get_json(f"{ctx.author.id}.money")+amount*2
            embed.add_field(name="Your Money:", value=f"```{check}$ --> {gg}$```")
            economy.write_json(f"{ctx.author.id}.money", value=gg)
            await message.edit(embed=embed)
        else:
            embed= discord.Embed(
                title="You lost :(",
                description=f"Your lost {amount}$",
                color=color_wish
            )
            embed.add_field(name="The Bets:", value=f"{user_final} > {enemy_final}", inline=False)
            gg = economy.get_json(f"{ctx.author.id}.money")-amount

            embed.add_field(name="Your Money:", value=f"```{check}$ --> {gg}$```")
            economy.write_json(f"{ctx.author.id}.money", value=gg)
            
            await message.edit(embed=embed)                

# user interactions #
@bot.slash_command(name="give", description="give an user some cash")
async def give(ctx, user: discord.Member, amount:int):
    check_user(user.id)
    check_user(ctx.author.id)    
    if amount > economy.get_json(f"{ctx.author.id}.money"):
        await ctx.respond("You cant give more money than your own!")
    else:
        old_receive =economy.get_json(f"{user.id}.money")
        old_sender = economy.get_json(f"{ctx.author.id}.money")

        new_sender = economy.get_json(f"{ctx.author.id}.money")-amount
        new_receive = economy.get_json(f"{user.id}.money")+amount

        economy.write_json(f"{ctx.author.id}.money", value=new_sender)
        economy.write_json(f"{user.id}.money", value=new_receive)

        embed= discord.Embed(
            description=f"You successfully sent {amount}",
            color=color_wish,
            thumbnail=ctx.author.avatar.url
        )
        embed.add_field(name=f"{ctx.author.name}`s money", value=f"```{old_sender}$ --> {new_sender}$```")
        embed.add_field(name=f"{user.name}`s money", value=f"```{old_receive}$ --> {new_receive}$```")

        await ctx.respond(embed=embed)

@bot.slash_command(name="steal", description="steal money of an user")
async def steal(ctx, user : discord.Member):
    check_user(user.id)
    check_user(ctx.author.id)  
    gg = random.randint(30, 90)
    amount = random.randint(100, 300)
    if check_cooldown(ctx.user.id, "steal"):
        

        embed = discord.Embed(
            description=f"You stole {amount}$ from {user.mention}",
            color=color_wish
        )
        old_receive =economy.get_json(f"{user.id}.money")
        old_sender = economy.get_json(f"{ctx.author.id}.money")

        new_sender = economy.get_json(f"{ctx.author.id}.money")+amount
        new_receive = economy.get_json(f"{user.id}.money")-amount

        economy.write_json(f"{ctx.author.id}.money", value=new_sender)
        economy.write_json(f"{user.id}.money", value=new_receive)
        embed.add_field(name=f"{ctx.author.name}`s money", value=f"```{old_sender}$ --> {new_sender}$```")
        embed.add_field(name=f"{user.name}`s money", value=f"```{old_receive}$ --> {new_receive}$```")
        if gg > 70:
            if amount > old_receive:
                await ctx.respond("User is too broke to loose money")                
            else:
                await ctx.respond(user.mention,embed=embed)
                update_cooldown(ctx.user.id, "steal")
        else:
            await ctx.respond(f"You failed to steal Money from {user.mention}")  
            update_cooldown(ctx.user.id, "steal")
    else:
        last_used = datetime.datetime.fromisoformat(cooldown.get_json(f"{ctx.user.id}.steal"))
        next_available = last_used + datetime.timedelta(hours=2)
        now = datetime.datetime.now()
        
        time_left = next_available - now
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        embed = discord.Embed(title="Steal", color=0xff0000,
                             description="You need to rest before you steal again!")
        embed.add_field(name="Available in", 
                       value=f"```{hours} hours, {minutes} minutes```")
        
        await ctx.respond(embed=embed)




bot.run(Token)    