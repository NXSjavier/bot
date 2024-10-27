from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Token del bot proporcionado por BotFather
TOKEN = "7858475030:AAGst4DO_pmLLK8BQhA6KVHyiGE6nVIBuvQ"
ADMIN_USER_ID = 7310171462  # Reemplaza con tu propio ID de usuario

# Lista de IDs de usuarios suscritos
suscriptores = set()

# Datos de los artistas
artistas = [
    {
        "nombre": "DFT",
        "foto": "https://drive.google.com/uc?id=1Vf7-QXCOowOj92RpSAzigK6acNqblyF7",
        "audio": "G:/code/chatbost/audio/FALAME.mp3",
        "redes": {
            "Instagram": "https://www.instagram.com/dftier.pimp?igsh=MWRqcmEydmxicmw4cQ==",
            "TikTok": "https://www.tiktok.com/@dftier.pimp?_t=8qqHRqjXZ82&_r=1",
            "Facebook": "https://www.facebook.com/dftier"
        }
    },
    {
        "nombre": "NEXUS",
        "foto": "https://drive.google.com/uc?id=1Qso1vz4D84W0I3wRN3A_foAm2rEvLcm-",
        "audio": "G:/code/chatbost/audio/IGNORA.mp3",
        "redes": {
            "Instagram": "https://www.instagram.com/nexxsus2.0/profilecard/?igsh=MXB0Nml4ZWYxc3RzbQ==",
            "TikTok": "https://www.tiktok.com/@n.e.x.u.s?_t=8qqH1X1aBHi&_r=1",
            "Facebook": "https://www.facebook.com/javierjoel.solisvivero"
        }
    }
]

# Comando start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Botón Suscribirse
    subscribe_button = InlineKeyboardButton("Suscribirse", callback_data="subscribe")
    button_markup = InlineKeyboardMarkup([[subscribe_button]])
    
    await update.message.reply_text("¡Bienvenido al Bot de Publicidad de Artistas! Haz clic en 'Continuar' para ver más opciones.", reply_markup=button_markup)

    # Botón Continuar
    continue_button = InlineKeyboardButton("Continuar", callback_data="continuar")
    reply_markup = InlineKeyboardMarkup([[continue_button]])
    await update.message.reply_text("Haz clic en 'Continuar' para ver más opciones.", reply_markup=reply_markup)

# Manejar la lista de artistas
async def continuar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    for artista in artistas:
        # Enviar foto del artista con botones de redes
        keyboard = [
            [InlineKeyboardButton("Instagram", url=artista["redes"]["Instagram"])],
            [InlineKeyboardButton("TikTok", url=artista["redes"]["TikTok"])],
            [InlineKeyboardButton("Facebook", url=artista["redes"]["Facebook"])]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Enviar la foto con los botones de redes sociales
        await query.message.reply_photo(photo=artista["foto"], caption=artista["nombre"], reply_markup=reply_markup)
        
        # Enviar el fragmento de música inmediatamente después de la foto usando la ruta local
        try:
            with open(artista["audio"], "rb") as audio_file:
                await query.message.reply_audio(audio=audio_file, caption=f"Escucha un fragmento de la música de {artista['nombre']}")
        except Exception as e:
            await query.message.reply_text(f"No se pudo enviar el audio de {artista['nombre']}: {str(e)}")

# Comando para suscribirse
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    if user_id not in suscriptores:
        suscriptores.add(user_id)
        await update.callback_query.answer("Te has suscrito a las actualizaciones.")
    else:
        await update.callback_query.answer("Ya estás suscrito.")

# Comando para cancelar la suscripción
async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    if user_id in suscriptores:
        suscriptores.remove(user_id)
        await update.callback_query.answer("Te has dado de baja de las actualizaciones.")
    else:
        await update.callback_query.answer("No estás suscrito.")

# Comando help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Comandos disponibles:\n/start - Iniciar bot\n/help - Ver ayuda\n/subscribe - Suscribirse a las actualizaciones\n/unsubscribe - Cancelar suscripción")

# Comando para enviar notificaciones
async def send_notification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == ADMIN_USER_ID:
        message = " ".join(context.args)
        if message:
            for user_id in suscriptores:
                try:
                    await context.bot.send_message(chat_id=user_id, text=message)
                except Exception as e:
                    print(f"Error al enviar mensaje a {user_id}: {str(e)}")
            await update.message.reply_text("Notificación enviada a todos los suscriptores.")
        else:
            await update.message.reply_text("Por favor, proporciona un mensaje para enviar.")
    else:
        await update.message.reply_text("No tienes permisos para enviar notificaciones.")

# Configuración del bot
def main():
    app = Application.builder().token(TOKEN).build()
    
    # Añadir comandos y handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))
    app.add_handler(CommandHandler("notify", send_notification))  # Nuevo comando para enviar notificaciones
    app.add_handler(CallbackQueryHandler(continuar, pattern="continuar"))
    app.add_handler(CallbackQueryHandler(subscribe, pattern="subscribe"))

    # Ejecutar el bot
    app.run_polling()

# Ejecuta el bot
if __name__ == "__main__":
    main()
