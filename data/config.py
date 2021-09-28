from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
# BOT_TOKEN = "2045379423:AAHQu_US3v4BFtaUSxZjbZSi8XSVHMasiGA" 
BOT_TOKEN = "1936771362:AAHlnu9ACW27yVLcqhX52xxO3dpaD_W5mFI" # Bot toekn
# ADMINS = ['1600170280', '3513638', '1019865273', '99940983']
ADMINS = ['915850675']# adminlar ro'yxati
IP = "localhost"  # Xosting ip manzili
# account_sid = 'AC7586a0983c8b415abe41f7a803c5e61a' # Twilio ma'lumotlar
# auth_token = '1b6e0f6bf10df049c0b68ee44dbeedc8'
# PAYMENTS_PROVIDER_TOKEN = '387026696:LIVE:6149b6f02dfdc60f985e6b91'
PAYMENTS_PROVIDER_TOKEN = '398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065'#Токен оплаты по Клик
OFFICE_LOCATION = [41.269655, 69.319892]
