from geoip2 import database
from geoip2.types import IPAddress

reader = database.Reader('ip_db/GeoLite2-Country.mmdb')

def get_country_iso(ip: IPAddress):
    return reader.country(ip).country.iso_code
