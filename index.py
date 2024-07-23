import logging  
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters  
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove  
import random  
import pymongo  
  
# Database connection  
client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["bot_db"]  
users_collection = db["users"]  
games_collection = db["games"]  
  
# Bot token  
TOKEN = 'YOUR_BOT_TOKEN'  
  
# Logging  
logging.basicConfig(level=logging.INFO)  
  
# Bot commands  
def start(update, context):  
   user_id = update.effective_user.id  
   if users_collection.find_one({"user_id": user_id}) is None:  
      users_collection.insert_one({"user_id": user_id, "balance": 100, "referrals": 0})  
   context.bot.send_message(chat_id=update.effective_chat.id, text='Welcome to our bot!')  
  
def balance(update, context):  
   user_id = update.effective_user.id  
   user = users_collection.find_one({"user_id": user_id})  
   context.bot.send_message(chat_id=update.effective_chat.id, text=f'Your balance: {user["balance"]}')  
  
def refer(update, context):  
   user_id = update.effective_user.id  
   user = users_collection.find_one({"user_id": user_id})  
   context.bot.send_message(chat_id=update.effective_chat.id, text=f'Your referral link: https://t.me/your_bot?start={user_id}')  
  
def withdraw(update, context):  
   user_id = update.effective_user.id  
   user = users_collection.find_one({"user_id": user_id})  
   if user["balance"] &lt; 10:  
      context.bot.send_message(chat_id=update.effective_chat.id, text='Minimum withdrawal amount is 10')  
   else:  
      users_collection.update_one({"user_id": user_id}, {"$inc": {"balance": -10}})  
      context.bot.send_message(chat_id=update.effective_chat.id, text='Withdrawal successful')  
  
def head_tail_game(update, context):  
   user_id = update.effective_user.id  
   user = users_collection.find_one({"user_id": user_id})  
   if user["balance"] &lt; 1:  
      context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have enough balance to play')  
   else:  
      keyboard = [  
        [InlineKeyboardButton('Head', callback_data='head'), InlineKeyboardButton('Tail', callback_data='tail')]  
      ]  
      reply_markup = InlineKeyboardMarkup(keyboard)  
      context.bot.send_message(chat_id=update.effective_chat.id, text='Choose Head or Tail:', reply_markup=reply_markup)  
  
def dice_game(update, context):  
   user_id = update.effective_user.id  
   user = users_collection.find_one({"user_id": user_id})  
   if user["balance"] &lt; 1:  
      context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have enough balance to play')  
   else:  
      keyboard = [  
        [InlineKeyboardButton('Roll', callback_data='roll')]  
      ]  
      reply_markup = InlineKeyboardMarkup(keyboard)  
      context.bot.send_message(chat_id=update.effective_chat.id, text='Roll the dice:', reply_markup=reply_markup)  
  
def tic_tac_toe_game(update, context):  
   user_id = update.effective_user.id  
   user = users_collection.find_one({"user_id": user_id})  
   if user["balance"] &lt; 1:  
      context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have enough balance to play')  
   else:  
      keyboard = [  
        [InlineKeyboardButton('X', callback_data='x'), InlineKeyboardButton('O', callback_data='o')]  
      ]  
      reply_markup = InlineKeyboardMarkup(keyboard)  
      context.bot.send_message(chat_id=update.effective_chat.id, text='Play Tic Tac Toe:', reply_markup=reply_markup)  
  
def button_callback(update, context):  
   query = update.callback_query  
   user_id = query.from_user.id  
   user = users_collection.find_one({"user_id": user_id})  
   if query.data == 'head':  
      outcome = random.choice(['head', 'tail'])  
      if outcome == 'head':  
        users_collection.update_one({"user_id": user_id}, {"$inc": {"balance": 1.98}})  
        context.bot.send_message(chat_id=query.message.chat_id, text='You win!')  
      else:  
        users_collection.update_one({"user_id": user_id}, {"$inc": {"balance": -1}})  
        context.bot.send_message(chat_id=query.message.chat_id, text='You lose!')  
   elif query.data == 'tail':  
      outcome = random.choice(['head', 'tail'])  
      if outcome == 'tail':  
        users_collection.update_one({"user_id": user_id}, {"$inc": {"balance": 1.98}})  
        context.bot.send_message(chat_id=query.message.chat_id, text='You win!')  
      else:  
        users_collection.update_one({"user_id": user_id}, {"$inc": {"balance": -1}})  
        context.bot.send_message(chat_id=query.message.chat_id, text='You lose!')  
   elif query.data == 'roll':  
      dice_value = random.randint(1, 6)  
      context.bot.send_message(chat_id=query.message.chat_id, text=f'You rolled a {dice_value}')  
      # Implement dice game logic here  
   elif query.data == 'x' or query.data == 'o':  
      # Implement Tic Tac Toe game logic here  
      pass  
  
def admin_panel(update, context):  
   user_id = update.effective_user.id  
   if user_id == YOUR_ADMIN_ID:  
      keyboard = [  
        [InlineKeyboardButton('Minimum withdrawal amount', callback_data='min_withdrawal'), InlineKeyboardButton('Refer bonus', callback_data='refer_bonus')],  
        [InlineKeyboardButton('Broadcast', callback_data='broadcast'), InlineKeyboardButton('Ban/unban user', callback_data='ban_unban')]  
      ]  
      reply_markup = InlineKeyboardMarkup(keyboard)  
      context.bot.send_message(chat_id=update.effective_chat.id, text='Admin panel:', reply_markup=reply_markup)  
   else:  
      context.bot.send_message
