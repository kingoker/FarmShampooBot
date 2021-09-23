from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili
ESKIZ_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvbm90aWZ5LmVza2l6LnV6XC9hcGlcL2F1dGhcL2xvZ2luIiwiaWF0IjoxNjMxOTY5Nzg1LCJleHAiOjE2MzQ1NjE3ODUsIm5iZiI6MTYzMTk2OTc4NSwianRpIjoiZW1JSFRYcjAweUhpNXlNQyIsInN1YiI6NSwicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.rprwfwNiC-yTpK1muFG1QXy-xdklPYUHveAL18QtraU"
PAYMENTS_PROVIDER_TOKEN = '371317599:TEST:1632159259339'
OFFICE_LOCATION = [41.269655, 69.319892]
