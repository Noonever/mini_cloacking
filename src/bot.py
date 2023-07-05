from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery
from config import BOT_TOKEN, ACCESSED_UIDS, SITE_URL
from bot_menus import show_admin_menu, show_traffer_links, show_traffers
from mongo import get_all_traffers, get_traffer, delete_traffer, add_traffer, generate_cloacking_code, delete_traffer_link
from time import sleep

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot)

filling_new_redirect_url = False
filling_new_traffer = False
filling_new_traffer_link = False

@dp.message_handler(commands=["start"])
async def start(message: Message):
    uid = message.from_id
    if str(uid) not in ACCESSED_UIDS:
        return
    await show_admin_menu(message=message)
    
    
@dp.message_handler()
async def messages(message: Message):
    
    global filling_new_traffer, filling_new_traffer_link
    
    uid = message.from_id
    if str(uid) not in ACCESSED_UIDS:
        return
    text = message.text
    
    if filling_new_traffer:
        username = text
        add_traffer(username=username)
        filling_new_traffer = False
        traffers = get_all_traffers()
        message_id = message.message_id
        await bot.delete_message(chat_id=uid, message_id=message_id-1)
        await show_traffers(message=message, traffers=traffers, current_range=(0, 5))
        
    elif filling_new_traffer_link:
        tg_link = text
        username = filling_new_traffer_link
        code = generate_cloacking_code(tg_link=tg_link, username=username)
        filling_new_traffer_link = False
        await message.delete()
        message_id = message.message_id
        await bot.delete_message(chat_id=uid, message_id=message_id-1)
        answer_message = await message.answer(
            text=SITE_URL+f'/{code}'
        )
        sleep(3)
        traffer = get_traffer(username=username)
        links = traffer.get('links')
        await show_traffer_links(username=username, links=links, current_range=(0, 5), message=answer_message)
        
    else:
        await message.delete()
        
        
@dp.callback_query_handler()
async def callback_handler(callback: CallbackQuery):
    
    global filling_new_traffer, filling_new_traffer_link
    
    command = callback.data
    uid = callback.from_user.id
    if str(uid) not in ACCESSED_UIDS:
        return
    
    if command == 'admin_menu':
        await show_admin_menu(callback=callback)
    
    elif 'show_traffers:' in command:
        start, end = command.replace('show_traffers:', '').split(':')
        traffers = get_all_traffers()
        await show_traffers(callback=callback, traffers=traffers, current_range=(int(start), int(end)))
        
    elif 'show_traffer_links:' in command:
        start, end, username = command.replace('show_traffer_links:', '').split(':')
        traffer = get_traffer(username=username)
        links = traffer.get('links')
        await show_traffer_links(callback=callback, username=username, links=links, current_range=(int(start), int(end)))
     
    elif 'add_traffer' in command:
        await callback.message.delete()
        filling_new_traffer = True
        await callback.message.answer(
            text='Enter traffer username: '
        )
    
    elif 'delete_traffer:' in command:
        username, = command.replace('delete_traffer:', '').split(':')
        delete_traffer(username=username)
        traffers = get_all_traffers()
        await show_traffers(callback=callback, traffers=traffers, current_range=(0, 5))

    elif 'add_link:' in command:
        await callback.message.delete()
        username, = command.replace('add_link:', '').split(':')
        filling_new_traffer_link = username
        await callback.message.answer(
            text=f'Введіть запрошувальне посилання {username}: '
        )
    
    elif 'delete_link:' in command:
        username, link_index = command.replace('delete_link:', '').split(':')
        delete_traffer_link(username=username, link_index=link_index)
        traffer = get_traffer(username=username)
        links = traffer.get('links')
        await show_traffer_links(callback=callback, username=username, links=links, current_range=(0, 5))
        
        
    elif 'show_alert:' in command:
        text = command.replace('show_alert:', '')
        await callback.answer(text=text)
        
    elif command == 'slava':
        await callback.answer("Слава Україні!")
        
    
    elif command == 'none':
        pass
        
        
def startup_message():
    print('Bot has been started.')


def run_bot():
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=startup_message())
    
    
if __name__ == '__main__':
    run_bot()