#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext, ConversationHandler

from prase import parse_bookmarks
from price import calculate_price
from prompts import prompt_vector
from utils import choose_bookmarks_file
from loader import get_loader
from vector_db import show_search, db_init, docs_add, token_count
from restruct import restruct
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import Document

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
load_dotenv()


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def add_docs(docs: str) -> str:
    vectorstore = db_init()
    docs = [Document(page_content=docs)]
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    splits = splitter.split_documents(docs)
    print(splits)
    vectorstore.add_documents(splits)
    vectorstore.persist()
    return "add success."

async def ask_chatgpt(question: str) -> str:
    vectorstore = db_init()
    result = ""
    model = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = ChatPromptTemplate.from_template(prompt_vector)
    chain = prompt | model | StrOutputParser()
    result_str = show_search(query=question, db=vectorstore)
    result = chain.invoke({"context": result_str, "question": question})
    return result

async def collect_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        "Please type the message you want to collect.",
        reply_markup=ForceReply(selective=True),
    )
    return COLLECT

async def answer_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        "Please type the message you want to send to ChatGPT.",
        reply_markup=ForceReply(selective=True),
    )
    return ANSWER

# Function to handle the user's response to the /collect command
async def handle_collect(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    chatgpt_response = await add_docs(user_message)
    await update.message.reply_text(chatgpt_response)
    return ConversationHandler.END

async def handle_answer(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    chatgpt_response = await ask_chatgpt(user_message)
    await update.message.reply_text(chatgpt_response)
    return ConversationHandler.END

COLLECT, ANSWER = range(2)

def main() -> None:
    """Start the bot."""
    # print(os.environ.get('OPENAI_API_KEY'))
    # print(os.environ.get('OPENAI_API_BASE'))
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('collect', collect_command),
            CommandHandler('answer', answer_command),
        ],
        states={
            COLLECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_collect)],
            ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)],
        },
        fallbacks=[],
    )
    application.add_handler(conv_handler)
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()