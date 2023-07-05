from pymongo import MongoClient
from random import choices
from string import ascii_uppercase

uri = "mongodb+srv://minicloacking:tq5c7Ud3xX9btA0z@cluster0.ug5vzft.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)
db = client.cloacking
traffers = db.traffers


def generate_random_code(k: int = 2):
    return "".join(choices(ascii_uppercase, k=k))


def add_traffer(username: str):
    try:
        traffer = traffers.insert_one({'_id': username, 'links': []})
        return traffer.inserted_id
    except:
        return False


def get_traffer(username: str):
    return traffers.find_one({'_id': username})
    

def get_all_traffers():
    return list(traffers.find())


def delete_traffer(username: str):
    return traffers.delete_one({'_id': username}).acknowledged
    

def add_traffer_links(username: str, tg_link: str, cloacking_code: str):
    traffer = get_traffer(username=username)
    if not traffer:
        return False
    traffer_links: list = traffer.get('links')
    traffer_links.append({'tg_link': tg_link, 'cloacking_code': cloacking_code})
    traffers.update_one({'_id': username}, {"$set": {'links': traffer_links}})
    return get_traffer(username=username)
    
    
def delete_traffer_link(username: str, link_index: int):
    traffer = get_traffer(username=username)
    if not traffer:
        return False
    traffer_links: list = traffer.get('links')
    traffer_links.pop(int(link_index))
    traffers.update_one({'_id': username}, {"$set": {'links': traffer_links}})
    return get_traffer(username=username)


def get_all_cloacking_codes():
    codes = {}
    traffers = get_all_traffers()
    for traffer in traffers:
        links = traffer.get('links')
        if links:
            for link in links:
                cloacking_code = link.get('cloacking_code')
                tg_link = link.get('tg_link')
                if cloacking_code:
                    codes.update({cloacking_code: tg_link})
                
    return codes


def generate_cloacking_code(tg_link: str, username: str):
    cloacking_code = generate_random_code()
    while cloacking_code in get_all_cloacking_codes().keys():
        cloacking_code = generate_random_code()
    add_traffer_links(username=username, tg_link=tg_link, cloacking_code=cloacking_code)
    return cloacking_code