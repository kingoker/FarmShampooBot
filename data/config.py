from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = "2045379423:AAF0SFhTxhIEM5pW_46BB1yUFQlraBmakys" 
# BOT_TOKEN = "1936771362:AAHlnu9ACW27yVLcqhX52xxO3dpaD_W5mFI" # Bot toekn Test
ADMINS = ['1600170280', '3513638', '1019865273', '99940983']
# ADMINS = ['915850675']# adminlar ro'yxati Test
IP = "localhost"  # Xosting ip manzili
PAYMENTS_PROVIDER_TOKEN = '387026696:LIVE:6149b6f02dfdc60f985e6b91'
# PAYMENTS_PROVIDER_TOKEN = '398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065'#Токен оплаты по Клик Test
OFFICE_LOCATION = [41.269655, 69.319892]
