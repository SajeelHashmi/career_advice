from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ParseMode
import os
from dotenv import load_dotenv
import uuid
## telegram token
from career_advice import CareerAdvice
from mock_inteview import Interviewer


load_dotenv()


TOKEN: Final = os.getenv('TELEGRAM_BOT_TOKEN')



async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Entry point to telegram bot sends a message with 2 options assessment book questions and past year questions
    """
    keyboard = [
        [InlineKeyboardButton("Career advice", callback_data="career_advice")],
        [InlineKeyboardButton("Mock Interviews", callback_data="mock_interviews")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text("Choose an option:", reply_markup=reply_markup)
    else:
        # For callback queries without message
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Choose an option:", reply_markup=reply_markup)

async def helphandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Welcome to the Career Advice and planing bot Help!\n\n"
        "Here's how you can use this bot:\n\n"
        "/start - Start interacting with the bot.\n"
        "/help - Show this help message.\n\n"
        "You have the following main options:\n"
        "1. Career advice\n"
        "2. CV review\n"
        
        "Navigation Tips:\n"
        "- Use the buttons provided to navigate through options.\n"
        "- If you ever get lost, you can always return to the main menu by typing /start\n\n"
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "career_advice":
        context.user_data['career_advice'] = True
        cr = CareerAdvice()
        context.user_data['conversation_id'] = cr.chat_id
        context.user_data['conversation_type'] = "career_advice"
        await query.message.reply_text(
            cr.first_response()
        )


    elif query.data == "mock_interviews":
        context.user_data['mock_interviews'] = True
        i = Interviewer()
        context.user_data['conversation_id'] = i.chat_id
        context.user_data['conversation_type'] = "mock_interview"
        await query.message.reply_text(
            i.first_response()
        )

    else:
        await query.message.reply_text("Invalid Option")





async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.user_data.get("conversation_id",False) and context.user_data.get("conversation_type",False):
        
        conversation_id = context.user_data.get("conversation_id")
        convo_type = context.user_data.get("conversation_type")
        if convo_type == "career_advice":
            cr = CareerAdvice(id=conversation_id)
            # get the user text here
            user_text = update.message.text.strip()
            response = cr.invoke(user_text)
            await update.message.reply_text(response)

            pass
        elif convo_type == "mock_interview":
            i = Interviewer(id=conversation_id)
            user_text = update.message.text.strip()
            response = i.invoke(user_text)
            await update.message.reply_text(response)



def main():
    app = Application.builder().token(TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", helphandler))

    # Callback Query Handlers
    app.add_handler(CallbackQueryHandler(menu_callback, pattern="^(career_advice|mock_interviews|job_search)$"))


    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    # app.add_handler(CallbackQueryHandler(cat_callback, pattern="^(grade_.*|back_to_grades)$"))
    # app.add_handler(CallbackQueryHandler(topic_callback, pattern="^(subject_.*|back_to_subjects|back_to_grades)$"))
    # app.add_handler(CallbackQueryHandler(generate_questions, pattern="^(topic_.*|back_to_topics|show_answer|new_question)$"))
    # app.add_handler(CallbackQueryHandler(show_answer, pattern="^show_answer$"))
    # app.add_handler(CallbackQueryHandler(new_question, pattern="^new_question$"))
    # app.add_handler(CallbackQueryHandler(give_feedback, pattern="^give_feedback$"))

    # app.add_handler(
    #     CallbackQueryHandler(
    #         main_menu_callback_handler, pattern="^(ai_generated|real_paper|back_to_start)$"
    #     )
    # )
    # app.add_handler(
    #     CallbackQueryHandler(
    #         ai_generated_selection_callback, pattern="^(upload_image|type_topic)$"
    #     )
    # )

    # app.add_handler(
    #     CallbackQueryHandler(
    #         ai_generated_callback_handler, pattern="^(ai_show_answer|ai_next_question)$"
    #     )
    # )


    # Message Handlers
    # app.add_handler(MessageHandler(filters.PHOTO, handle_image_upload))
    # app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    # # Error Handler
    # app.add_error_handler(error)

    # Run the bot
    print("Starting bot...")
    app.run_polling(poll_interval=0.5)




if __name__ == '__main__':
    main()