from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from src.config import SITE_URL

MENU_STEP = 5

ADMIN_MENU_TEXT = "Адміністрація"
TRAFFER_LINKS_TEXT = "Список посилань трафера"
TRAFFERS_MENU_TEXT = "Список траферів"


async def show_admin_menu(message: Message | None = None, callback: CallbackQuery | None = None):
    link_button = InlineKeyboardButton(text='?', callback_data='slava')
    traffers_button = InlineKeyboardButton(text='Трафери', callback_data='show_traffers:0:5')
    ikb = InlineKeyboardMarkup()
    ikb.add(link_button).add(traffers_button)
    if message:
        await message.delete()
        await message.answer(
            text=ADMIN_MENU_TEXT,
            reply_markup=ikb
        )
    if callback:
        await callback.message.edit_text(
            text=ADMIN_MENU_TEXT,
            reply_markup=ikb
        )

        
def get_traffers_keyboard(
        traffers: list[dict[str, str]],
        current_range: tuple[int, int]
    ) -> InlineKeyboardMarkup:
    
    start, end = current_range
    traffers_len = len(traffers)
    
    if end - start > traffers_len:
        current_range = (0, traffers_len)
        
    if start - MENU_STEP <= 0:
        previous_start = 0
        previous_end = MENU_STEP
    else:
        previous_start = start - MENU_STEP
        previous_end = end - MENU_STEP
    if end + MENU_STEP >= traffers_len:
        next_end = traffers_len
        next_start = next_end - MENU_STEP
    else:
        next_end = end + MENU_STEP
        next_start = start + MENU_STEP
        
    ikb = InlineKeyboardMarkup()
    
    for key_index in range(*current_range):
        
        traffer = traffers[key_index]
        username = traffer.get('_id')
        
        traffer_title_button = InlineKeyboardButton(text=username, callback_data="none")
        traffer_check_button = InlineKeyboardButton(text="🔗", callback_data=f"show_traffer_links:0:5:{username}")
        traffer_delete_button = InlineKeyboardButton(text="❌", callback_data=f"delete_traffer:{username}")
        
        ikb.add(traffer_title_button)
        ikb.add(traffer_check_button, traffer_delete_button)
        
    if not (traffers_len + 1 <= end):
        previous_button = InlineKeyboardButton(
            text="<-",
            callback_data=f"show_traffers:{previous_start}:{previous_end}"
        )
        next_button = InlineKeyboardButton(
            text="->",
            callback_data=f"show_traffers:{next_start}:{next_end}"
        )
        ikb.add(previous_button, next_button)
            
    back_button = InlineKeyboardButton(text="Назад", callback_data="admin_menu")
    add_button = InlineKeyboardButton(text='👥Додати трафера', callback_data='add_traffer')
    ikb.add(add_button).add(back_button)
    return ikb
    

def get_links_keyboard(
        username: str,
        links: list[dict[str, str]],
        current_range: tuple[int, int]
    ) -> InlineKeyboardMarkup:
    
    start, end = current_range
    links_len = len(links)
    
    if end - start > links_len:
        current_range = (0, links_len)
        
    if start - MENU_STEP <= 0:
        previous_start = 0
        previous_end = MENU_STEP
    else:
        previous_start = start - MENU_STEP
        previous_end = end - MENU_STEP
    if end + MENU_STEP >= links_len:
        next_end = links_len
        next_start = next_end - MENU_STEP
    else:
        next_end = end + MENU_STEP
        next_start = start + MENU_STEP
        
    ikb = InlineKeyboardMarkup()
    
    for key_index in range(*current_range):
        
        link = links[key_index]
        tg_link = link.get('tg_link')
        cloacking_code = link.get('cloacking_code')
        
        link_title_button = InlineKeyboardButton(text=tg_link, callback_data=f"show_alert:{f'{SITE_URL}/{cloacking_code}'}")
        link_delete_button = InlineKeyboardButton(text="❌", callback_data=f"delete_link:{username}:{key_index}")
        
        ikb.add(link_title_button, link_delete_button)
        
    if not (links_len + 1 <= end):
        previous_button = InlineKeyboardButton(
            text="<-",
            callback_data=f"show_traffer_links:{previous_start}:{previous_end}:{username}"
        )
        next_button = InlineKeyboardButton(
            text="->",
            callback_data=f"show_traffer_links:{next_start}:{next_end}:{username}"
        )
        ikb.add(previous_button, next_button)
            
    back_button = InlineKeyboardButton(text="Назад", callback_data="show_traffers:0:5")
    add_button = InlineKeyboardButton(text='Додати посилання', callback_data=f'add_link:{username}')
    ikb.add(add_button).add(back_button)
        
    return ikb
    
    
async def show_traffers(
    traffers: list[dict[str, str]], 
    current_range=tuple[int, int],
    callback: CallbackQuery | None = None, 
    message: Message | None = None, 
    
):
    traffers_ikb = get_traffers_keyboard(traffers=traffers, current_range=current_range)
    if callback:
        await callback.message.edit_text(
            text=TRAFFERS_MENU_TEXT,
            reply_markup=traffers_ikb
        )
    if message:
        await message.delete()
        await message.answer(
            text=TRAFFERS_MENU_TEXT,
            reply_markup=traffers_ikb    
        )
    
     
async def show_traffer_links(
    username: str, 
    links: list[dict[str, str]], 
    current_range: tuple[int, int],
    callback: CallbackQuery | None = None,
    message: Message | None = None
):
    links_ikb = get_links_keyboard(username=username, links=links, current_range=current_range)
    if callback:
        await callback.message.edit_text(
            text=TRAFFER_LINKS_TEXT + f' {username}',
            reply_markup=links_ikb
        )
    if message:
        await message.delete()
        await message.answer(
            text=TRAFFER_LINKS_TEXT + f' {username}',
            reply_markup=links_ikb   
        )