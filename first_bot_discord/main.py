import discord
from discord.ext import commands
from discord import app_commands
from Classes.registro import RegistroModal
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# Acessa o token armazenado
TOKEN = os.getenv("TOKEN")
CANAL_REGISTRO_ID = 1342918853407281296

# Definindo as permissões, a permissão default não permite  leitura de mensagens
permisoes = discord.Intents.default()
# Adicionando outras permissões
permisoes.typing                    = True
permisoes.message_content           = True
permisoes.members                   = True
permisoes.guilds                      = True
permisoes.moderation                = True

# Salvando os comandos em uma variavel, e colocando o prefix para chama-lo
bot = commands.Bot(command_prefix="!", intents=permisoes)

# usa o @bot.command para comandos
@bot.command()
async def ola(ctx:commands.Context): # tipificando o ctx como objeto context
    # Envia uma mensagem para o canal - Usa send ou reply
    # Send so responde e Reply ele marca a pessoa
    usuario = ctx.author
    canal = ctx.channel
    await ctx.reply(f"Olá {usuario.display_name}, eu estou aqui!\nVocê esta me chamando do canal: {canal.name}")


# Ola com slash commands, description nada mais é que a descrição do comando
@bot.tree.command(description='Responde o usuario com Ola')
async def ola(interact:discord.Integration): 
    # resposta do bot, o ephemeral significa que so quem chamou vai ver a resposta
    await interact.response.send_message(f"Olá {interact.user.name}, eu estou aqui!\nVocê esta me chamando do canal: {interact.guild.name}", ephemeral=True) 


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


# Criando botões
@bot.command()
async def enviar_botao(ctx:commands.Context):

    # Resposta para quandfo o botão for precionado
    async def resposta_botao(interact:discord.Integration):
        await interact.response.send_message("Botão precionado....")


    view = discord.ui.View()
    button = discord.ui.Button(label="Clique aqui!", style=discord.ButtonStyle.green)
    button.callback = resposta_botao

    view.add_item(button)
    await ctx.reply(view=view)


# Criando botões e seletores
@bot.command()
async def jogo_favorito(ctx:commands.Context):

    # Resposta para quando o botão for precionado
    async def response_game(interact:discord.Integration):
        escolha = interact.data['values'][0]
        jogos = {'1': 'GTA V', '2': 'Counter Strike', '3': 'Fortnite'}
        jogo_escolhido = jogos[escolha]
        await interact.response.send_message(f'O Jogo escolhido foi {jogo_escolhido} ...')


    menu_selecao = discord.ui.Select(placeholder="Selecione uma opção") # para selecionar mais de uma opção, adiciona , max_values=2 depois do opção ai selecionara 2 items nesse exemplo
    opcoes = [
        discord.SelectOption(label='GTA V', value='1'),
        discord.SelectOption(label='Counter Strike', value='2'),
        discord.SelectOption(label='Fortnite', value='3')
    ]
    # adicionando as opções no menu
    menu_selecao.options = opcoes
    menu_selecao.callback = response_game
    view = discord.ui.View()
    view.add_item(menu_selecao)
    await ctx.reply(view=view)



# Mandando Imagem
@bot.tree.command()
async def farm(interact:discord.Integration, argumento:discord.Attachment):
    await argumento.save(argumento.filename)


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

@bot.tree.command(name="registro", description="Abra o formulário de registro")
async def registro(interaction: discord.Interaction):
    """Slash command que abre o modal"""
    await interaction.response.send_modal(RegistroModal())


# usa o @bot.event para eventos
@bot.event
async def on_ready():
    # Sincronizando os commandos slash
    try:
        synced = await bot.tree.sync()
        print(f"Comandos sincronizados: {len(synced)}")
        print(f"🤖 O bot {bot.user} está online!")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")



# iniciando o Bot, todos os eventos e comando tem que ser antes do run
bot.run(TOKEN)


