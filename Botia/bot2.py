import discord
import requests

# ---------------------
# Claves integradas directamente
# ---------------------
DISCORD_TOKEN = ""
OPENROUTER_API_KEY = "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"

# ---------------------
# Función para validar token de Discord
# ---------------------
def validar_token_discord(token):
    url = "https://discord.com/api/v10/users/@me"
    headers = {"Authorization": f"Bot {token}"}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            user = r.json()
            print(f"✅ Token válido. Usuario del bot: {user['username']}#{user['discriminator']}")
            return True
        else:
            print(f"❌ Token inválido. Status {r.status_code}: {r.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error al validar token: {e}")
        return False

# ---------------------
# Función para obtener respuesta de OpenRouter
# ---------------------
def obtener_respuesta(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "Eres un bot estilo Rndgamer: directo, relajado, profesional, con humor inteligente y motivador."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"⚠️ Error {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"⚠️ Error de conexión a OpenRouter: {e}"

# ---------------------
# Configurar cliente Discord
# ---------------------
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Eventos de Discord
@client.event
async def on_ready():
    print(f"✅ Bot conectado como {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!chill "):
        pregunta = message.content[len("!chill "):]
        respuesta = obtener_respuesta(pregunta)
        await message.channel.send(f"🧠 *Chillbot dice:* {respuesta}\n\n☮️ Siempre chill como Rndgamer 😌")

# ---------------------
# Iniciar bot solo si token es válido
# ---------------------
if validar_token_discord(DISCORD_TOKEN):
    client.run(DISCORD_TOKEN)
else:
    print("❌ No se puede iniciar el bot: token inválido")
