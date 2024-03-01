from config_bot import TOKEN
import logging
from members import Register, Member
from datetime import datetime
from dateutil.relativedelta import relativedelta
import threading

from telegram import ForceReply, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

NAME_ADD, TELEPHONE_ADD, ENTRY_DATE_ADD, FINAL_DATE_ADD, PAY_PLAT_ADD = range(5)
NAME_REM = range(1)
NAME_UPD = range(1)

register = Register()
new_member = {}

file_NAME_ADD = 'register_file.txt'
current_time = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Read register_file.txt and """
    register.get_register(file_NAME_ADD)


    if (message := register.show_members()) == "":
        message = "No Members"

    await update.message.reply_text(message)


async def show_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    message = ""
    if len(register.members) > 0:
        for member in register.members:
            message = register.show_members()
    else:
        message = "Não existem membros no grupo"
    
    await update.message.reply_text(message)

## ADD MEMBER FUNCTIONS ##

async def add_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the process of add member"""
    await update.message.reply_text("Insira o nome do membro")

    return NAME_ADD  

async def capture_NAME_ADD(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Capturing new member NAME_ADD"""
    text = update.message.text
    new_member["NAME_ADD"] = text
    await update.message.reply_text(f"Insira o telefone: ")

    return TELEPHONE_ADD

async def capture_TELEPHONE_ADD(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Capturing new member TELEPHONE_ADD"""
    text = update.message.text
    new_member["TELEPHONE_ADD"] = text

    await update.message.reply_text(f"Insira data de entrada")

    return ENTRY_DATE_ADD

async def capture_ENTRY_DATE_ADD(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Capturing new member ENTRY_DATE_ADD"""
    text = update.message.text
    new_member["ENTRY_DATE_ADD"] = text
    await update.message.reply_text(f"Insira data de saída: ")

    return FINAL_DATE_ADD

async def capture_FINAL_DATE_ADD(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Capturing new member FINAL_DATE_ADD"""
    text = update.message.text
    new_member["FINAL_DATE_ADD"] = text
    await update.message.reply_text(f"Insira plataforma de pagamento: ")

    return PAY_PLAT_ADD


async def capture_payment_plataform(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Capturing new member payment plataform"""
    text = update.message.text
    new_member["payment_plataform"] = text
    message = ""
    
    NAME_ADD, TELEPHONE_ADD, ENTRY_DATE_ADD, FINAL_DATE_ADD, payment_plataform = new_member["NAME_ADD"], new_member["TELEPHONE_ADD"], new_member["ENTRY_DATE_ADD"], new_member["FINAL_DATE_ADD"], new_member["payment_plataform"] 
    try:
        register.add_member(Member(new_member["NAME_ADD"], new_member["TELEPHONE_ADD"], new_member["ENTRY_DATE_ADD"], new_member["FINAL_DATE_ADD"], new_member["payment_plataform"]))
        message = f"Novo usuário adicionado!\nNome: {NAME_ADD}\nTelefone: {TELEPHONE_ADD}\nData de entrada: {ENTRY_DATE_ADD}\nData de saida: {FINAL_DATE_ADD}\nPlataforma de Pagamento: {payment_plataform}"
        register.set_register(file_NAME_ADD)
        
    except ValueError:
        message = "Não foi possível adicionar o membro: data inválida"
        
    await update.message.reply_text(message)

    return ConversationHandler.END

## END OF ADD MEMBER FUNCTIONS ##

## REMOVE MEMBER FUNCTIONS ##

async def remove_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the process of remove member"""
    await update.message.reply_text("Insira o nome do membro que deseja remover: ")

    return NAME_REM 

async def capture_NAME_REM(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Capturing member name and removing it if it's in the group"""
    text = update.message.text
    message = ""

    if text in register.members:
        message = f"Membro removido"
        register.members.pop(text)
        register.set_register(file_NAME_ADD)
    else:
        message = "Este membro não está presente no grupo" 
    
    await update.message.reply_text(message)

    return ConversationHandler.END

## END OF REMOVE MEMBER FUNCTIONS ##

## UPDATE MEMBER DATE  FUNCTIONS ##

async def update_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the process of remove member"""
    await update.message.reply_text("Insira o nome do membro que deseja atualizar a data de assinatura: ")

    return NAME_UPD 

async def capture_NAME_UPD(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ Capturing member name and updating date """
    text = update.message.text
    message = ""

    if text in register.members:
        message = f"Concedido +1 mês de assinatura para o membro: {text}"
        register.members[text].final_date += relativedelta(months=1)
        register.set_register(file_NAME_ADD)
    else:
        message = "este membro não está presente no grupo" 
    
    await update.message.reply_text(message)

    return ConversationHandler.END

## END OF UPDATE MEMBER FUNCTIONS ##

## SHOW MEMBERS STATUS FUNCTIONS ##

async def show_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Showing member status"""
    current_time = datetime.now()
    yellow_register = Register() #those whose monthly fee is five days away from ending
    red_register = Register() #those whose monthly fee already ended
    message = ""
    print(current_time)

    for name, member in register.members.items():
        difference =  (member.final_date - current_time).days

        if difference < 0:  #irregular membership
            red_register.add_member(member) 
        elif difference <= 5 : #almost  irregular membership
            yellow_register.add_member(member)

    if len(red_register.members) != 0:
        message += "🟥 USUÁRIOS FORA DO PRAZO DE MENSALIDADE 🟥\n"
        message += red_register.show_members()
    else:
        message += "Não há usuários fora do prazo da mensalidade!\n\n"

    if len(yellow_register.members) != 0:
        message += f"🟨USUÁRIOS QUE ESTÃO QUASE FORA DO PRAZO DE MENSALIDADE 🟨\n"
        message += yellow_register.show_members()
    
    await update.message.reply_text(message)
    
## END OF SHOW MEMBERS STATUS FUNCTIONS ##

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("op cancelada")

    return ConversationHandler.END

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    
    # Schedule the tasks
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    conv_handler_add = ConversationHandler(
        entry_points=[CommandHandler("add_member", add_member)],
        states={
            NAME_ADD: [
                MessageHandler(
                    filters.TEXT, capture_NAME_ADD
                )
            ],
            TELEPHONE_ADD: [
                MessageHandler(
                    filters.TEXT, capture_TELEPHONE_ADD 
                )
            ],
            ENTRY_DATE_ADD: [
                MessageHandler(
                    filters.TEXT, capture_ENTRY_DATE_ADD 
                )
            ],
            FINAL_DATE_ADD: [
                MessageHandler(
                    filters.TEXT, capture_FINAL_DATE_ADD 
                )
            ],
            PAY_PLAT_ADD: [
                MessageHandler(
                    filters.TEXT, capture_payment_plataform 
                )
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    conv_handler_rem = ConversationHandler(
        entry_points=[CommandHandler("remove_member", remove_member)],
        states={
            NAME_REM: [
                MessageHandler(
                    filters.TEXT, capture_NAME_REM
                )
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    conv_handler_upd = ConversationHandler(
        entry_points=[CommandHandler("update_member", update_member)],
        states={
            NAME_UPD: [
                MessageHandler(
                    filters.TEXT, capture_NAME_UPD
                )
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler_add)
    application.add_handler(conv_handler_rem)
    application.add_handler(conv_handler_upd)
    application.add_handler(CommandHandler("show_members", show_members))
    application.add_handler(CommandHandler("show_status", show_status))

    
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    
if __name__ == "__main__":
    main()
    

    