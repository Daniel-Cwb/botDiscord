import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# Acessa o token armazenado
TOKEN = os.getenv("TOKEN")

# Definindo as permissões, a permissão default não permite  leitura de mensagens
permisoes = discord.Intents.default()
# Adicionando outras permissões
permisoes.typing            = True
permisoes.message_content   = True
permisoes.members           = True

# Salvando os comandos em uma variavel, e colocando o prefix para chama-lo
bot = commands.Bot(command_prefix=".", intents=permisoes)

# usa o @bot.command para comandos
@bot.command()
async def ola(ctx:commands.Context): # tipificando o ctx como objeto context
    # Envia uma mensagem para o canal - Usa send ou reply
    # Send so responde e Reply ele marca a pessoa
    usuario = ctx.author
    canal = ctx.channel
    await ctx.reply(f"Olá {usuario.display_name}, eu estou aqui!\nVocê esta me chamando do canal: {canal.name}")


@bot.command()
async def somar(ctx:commands.Context, num1:float, num2:float): # nesse caso ele intende o espaço como delimitador entre um numero e o outro
    resp = num1 + num2 # Se quisece uma frase ficaria (ctx:commands.Context, * ,frase)
    await ctx.reply(f"O resultado da soma é: {resp}")


@bot.command()
async def enviar_embed(ctx:commands.Context):
    usuario = ctx.author
    canal = ctx.channel
    # Cria um embed -  Para enviar imagem se estiver na internet: meu_embed.set_image(url='URL DA IMAGEM')
    meu_embed = discord.Embed(title="Seja bem-vindo(a) ! 🎉", description=f"👋 Olá {usuario.display_name}\nVocê acabou de entra no servidor **{canal.guild.name}**! 🎉\nDiverta-se e aproveite muito!!!")
    # Adiciona uma imagem
    #imagem_arquivo = discord.File('imagens/LogoCheckmate.png', 'logo.png')
    #meu_embed.set_image(url="attachment://logo.png")

    # Adiciona Thumb
    imagem_thumb = discord.File('imagens/LogoCheckmate.png', 'thumb.png')
    meu_embed.set_thumbnail(url="attachment://thumb.png")

    # Adiciona colunas
    meu_embed.add_field(name='📢 **Fique atento!**', value='Não se esqueça de ler a sala{#📌┃regras}!', inline=False)
    meu_embed.add_field(name='📢 **Live na Twitch**', value='https://www.twitch.tv/itscheckmate', inline=False)
    meu_embed.add_field(name='📢 **🖼 Siga no Instagram!**', value='https://instagram.com/_dfialho', inline=False)

    # Adiciona uma cor para o embed
    meu_embed.color = discord.Color.red()

    await ctx.reply(file= imagem_thumb,embed=meu_embed)
    #await ctx.reply(files=[imagem_arquivo, imagem_thumb],embed=meu_embed)


# usa o @bot.event para eventos
@bot.event
async def on_ready():
    print(f"O bot {bot.user} está online!")

#@bot.event
#async def on_guild_channel_create(canal:discord.abc.GuildChannel): # Reconhece quando um novo canal e criado
#    await canal.send(f"Novo Canal criado: {canal.name}")

# Evento de novo integrante no servidor
@bot.event
async def on_member_join(membro:discord.Member): # Reconhece quando um novo integrante entra
    canal = bot.get_channel(1342918853407281294) # Pega o canal pelo id
    if canal:
        meu_embed = discord.Embed(title="Seja bem-vindo(a) ! 🎉", description=f"👋 Olá {membro.mention}\nVocê acabou de entra no servidor **{membro.guild.name}**! 🎉\nDiverta-se e aproveite muito!!!")
        
        # Adiciona Thumb
        meu_embed.set_thumbnail(url=membro.avatar)

        # Adiciona colunas
        meu_embed.add_field(name='📢 **Fique atento!**', value='Não se esqueça de ler a sala{#📌┃regras}!', inline=False)
        meu_embed.add_field(name='📢 **Live na Twitch**', value='https://www.twitch.tv/itscheckmate', inline=False)
        meu_embed.add_field(name='📢 **🖼 Siga no Instagram!**', value='https://instagram.com/_dfialho', inline=False)

        # Adiciona uma cor para o embed
        meu_embed.color = discord.Color.red()

        # Envia mensagem em um canal, que alguem entrou no canal
        await canal.send(embed=meu_embed) 

# Evento um integrante sair do servidor
#@bot.event
#async def on_member_remove(membro:discord.Member): # Reconhece quando um novo integrante entra
#    canal = bot.get_channel(1342918853407281294) # Pega o canal pelo
#    if canal: 
#        # Envia mensagem em um canal, que alguem entrou no canal
#        await canal.send(f"👋 Olá {membro.mention},\nSeja bem-vindo(a) ao servidor **{membro.guild.name}**! 🎉\n"
#                "Aproveite o servidor e não se esqueça de conferir as regras. 😉"
#            )



# iniciando o Bot, todos os eventos e comando tem que ser antes do run
bot.run(TOKEN)


