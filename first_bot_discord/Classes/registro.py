import discord
import json
import os

DADOS_JSON = "dados_usuarios.json"

class RegistroModal(discord.ui.Modal, title="Registro de Usuário"):
    def __init__(self):
        super().__init__()

        self.nome = discord.ui.TextInput(label="Nome", placeholder="Digite seu nome", required=True)
        self.jogo_favorito = discord.ui.TextInput(label="Jogo Favorito", placeholder="Digite seu jogo favorito", required=True)

        self.add_item(self.nome)
        self.add_item(self.jogo_favorito)

    async def on_submit(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)  # ID do usuário como string
        user_name = interaction.user.name   # Nome do usuário do Discord
        nome = self.nome.value              # Nome informado no modal
        jogo_favorito = self.jogo_favorito.value  # Jogo favorito informado

        # Criar um dicionário no formato desejado
        user_data = {
            "Nome": nome,
            "Jogo Favorito": jogo_favorito
        }

        # Salvar no JSON
        self.salvar_dados(user_id, user_name, user_data)

        # Responder ao usuário
        await interaction.response.send_message(f"✅ Registro concluído!\n**Nome:** {nome}\n**Jogo Favorito:** {jogo_favorito.upper()}", ephemeral=True)

        # Adicionar o cargo "Membro"
        role = discord.utils.get(interaction.guild.roles, name="Membro")
        if role:
            try:
                await interaction.user.add_roles(role)
            except discord.Forbidden:
                await interaction.followup.send("❌ Não tenho permissão para adicionar o cargo 'Membro'.", ephemeral=True)

    @staticmethod
    def salvar_dados(user_id, user_name, user_data):
        # Se o arquivo não existir, criar um novo
        if not os.path.exists(DADOS_JSON):
            with open(DADOS_JSON, "w") as f:
                json.dump({}, f, indent=4)

        # Carregar dados existentes
        with open(DADOS_JSON, "r") as f:
            dados = json.load(f)

        # Atualizar os dados do usuário
        dados[user_id] = user_data

        # Salvar novamente no arquivo
        with open(DADOS_JSON, "w") as f:
            json.dump(dados, f, indent=4)
