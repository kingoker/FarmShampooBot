
import requests
# from data.config import ESKIZ_TOKEN



def send_sms(sms_text, phone_number):

  url = "https://notify.eskiz.uz/api/message/sms/send"
  phone_number = phone_number.translate({ord("+") : "", ord(" ") : ""})
  payload={'mobile_phone': phone_number,
  'message': sms_text,
  'from': '4546',
  }
  files=[]
  print(phone_number)
  headers = {
    'Authorization': f'Bearer {ESKIZ_TOKEN}'
  }


  response = requests.request("POST", url, headers=headers, data=payload, files=files)


  print(response.text)