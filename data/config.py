from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili
account_sid = 'AC358cbabe5036f4efb73aa7933864e1a4' # Twilio ma'lumotlar
auth_token = '06b1c6f8c58b78f38e69b08bb362c997'
PAYMENTS_PROVIDER_TOKEN = '398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065'
OFFICE_LOCATION = [41.269655, 69.319892]
