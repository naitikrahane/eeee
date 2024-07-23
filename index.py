import logging  
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler  
import random  
  
logging.basicConfig(level=logging.INFO)  
  
TOKEN = 'YOUR_BOT_TOKEN'  
MIN_WITHDRAWAL_AMOUNT = 10  
REFER_BONUS = 5  
CHANNEL_LINK = 'https://t.me/YOUR_CHANNEL_LINK'  
ADMIN_ID = 123456789  
  
users = {}  
games = {}  
  
def start(update, context):  
   user_id = update.effective_user.id  
   if user_id not in users:  
      users[user_id] = {'balance': 0, 'eferrals': 0}  
   context.bot.send_message(chat_id=update.effective_chat.id, text='Welcome to the bot!')  
  
def balance(update, context):  
   user_id = update.effective_user.id  
   balance = users[user_id]['balance']  
   context.bot.send_message(chat_id=update.effective_chat.id, text=f'Your balance: {balance}')  
  
def refer(update, context):  
   user_id = update.effective_user.id  
   users[user_id]['referrals'] += 1  
   context.bot.send_message(chat_id=update.effective_chat.id, text='You have referred a new user!')  
  
def statistics(update, context):  
   total_users = len(users)  
   total_bets = sum(user['balance'] for user in users.values())  
   context.bot.send_message(chat_id=update.effective_chat.id, text=f'Total users: {total_users}\nTotal bets: {total_bets}')  
  
def withdraw(update, context):  
   user_id = update.effective_user.id  
   amount = int(context.args)  
   if amount &lt; MIN_WITHDRAWAL_AMOUNT:  
      context.bot.send_message(chat_id=update.effective_chat.id, text='Minimum withdrawal amount is 10')  
   elif amount &gt; users[user_id]['balance']:  
      context.bot.send_message(chat_id=update.effective_chat.id, text='Insufficient balance')  
   else:  
      users[user_id]['balance'] -= amount  
      context.bot.send_message(chat_id=update.effective_chat.id, text=f'Withdrawal successful! Your new balance: {users[user_id]["balance"]}')  
  
def head_tail_game(update, context):  
   user_id = update.effective_user.id  
   amount = int(context.args)  
   if amount &lt; 1:  
      context.bot.send_message(chat_id=update.effective_chat.id, text='Minimum bet amount is 1')  
   elif amount &gt; users[user_id]['balance']:  
      context.bot.send_message(chat_id=update.effective_chat.id, text='Insufficient balance')  
   else:  
      users[user_id]['balance'] -= amount  
      outcome = random.choice(['head', 'tail'])  
      if outcome == 'head':  
        users[user_id]['balance'] += amount * 1.98  
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'You won! Your new balance: {users[user_id]["balance"]}')  
      else:  
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'You lost! Your new balance: {users[user_id]["balance"]}')  
  
def dice_game(update, context):  
   user_id = update.effective_user.id  
   amount = int(context.args)  
   if amount &lt; 1:  
      context.bot.send_message(chat_id=update.effective_chat.id, text='Minimum bet amount is 1')  
   elif amount &gt; users[user_id]['balance']:  
      context.bot.send_message(chat_id=update.effective_chat.id, text='Insufficient balance')  
   else:  
      users[user_id]['balance'] -= amount  
      dice_value = random.randint(1, 6)  
      context.bot.send_message(chat_id=update.effective_chat.id, text=f'You rolled a {dice_value}')  
      if dice_value == 6:  
        users[user_id]['balance'] += amount * 6  
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'You won! Your new balance: {users[user_id]["balance"]}')  
      else:  
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'You lost! Your new balance: {users[user_id]["balance"]}')  
  
def tic_tac_toe_game(update, context):  
   user_id = update.effective_user.id  
   context.bot.send_message(chat_id=update.effective_chat.id, text='Tic Tac Toe game is not implemented yet')  
  
def admin_panel(update, context):  
   user_id = update.effective_user.id  
   if user_id == ADMIN_ID:  
      context.bot.send_message(chat_id=update.effective_chat.id, text='Admin panel')  
   else:  
      context.bot.send_message(chat_id=update.effective_chat.id, text='Access denied')  
  
def main():  
   updater = Updater(TOKEN, use_context=True)  
  
   dp = updater.dispatcher  
  
   dp.add_handler(CommandHandler('start', start))  
   dp.add_handler(CommandHandler('balance', balance))  
   dp.add_handler(CommandHandler('refer', refer))  
   dp.add_handler(CommandHandler('statistics', statistics))  
   dp.add_handler(CommandHandler('withdraw', withdraw))  
   dp.add_handler(CommandHandler('head_tail', head_tail_game))  
   dp.add_handler(CommandHandler('dice', dice_game))  
   dp.add_handler(CommandHandler('tic_tac_toe', tic_tac_toe_game))  
   dp.add_handler(CommandHandler('admin', admin_panel))  
  
   updater.start_polling()  
   updater.idle()  
  
if __name__ == '__main__':  
   main()  
