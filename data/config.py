from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = "2045379423:AAHQu_US3v4BFtaUSxZjbZSi8XSVHMasiGA"  # Bot toekn
ADMINS = ["1600170280, "]  # adminlar ro'yxati
IP = "localhost"  # Xosting ip manzili
# account_sid = 'AC7586a0983c8b415abe41f7a803c5e61a' # Twilio ma'lumotlar
# auth_token = '1b6e0f6bf10df049c0b68ee44dbeedc8'
PAYMENTS_PROVIDER_TOKEN = '387026696:LIVE:6149b6f02dfdc60f985e6b91' #Токен оплаты по Клик
OFFICE_LOCATION = [41.269655, 69.319892]