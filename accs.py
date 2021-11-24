import requests
my_access_token = 'EAAwDjsTCk8kBAFKa464KR8NMb4ooSDie7BZCnHS6iaRvehTk8LkmES3YZApFOxYN0Ev4C1PmxZBOaaF428sBmEbY2gJ4cA9at1Q6fz7XTeCjhektKGbSZC0r25Gz8QZC0h7ScUo0FknDMtLz6rAP4JCIayBlbZAjpVkn2knK5xCaYYZBELLMZBHqr2mwmLX7Hj0ZD'
my_app_id = '3381611441853385'
my_app_secret = 'a0d38d2d8eba2fa13ff2d7246f344dd1'

# def get_new_token():
#     # r = requests.get(
#     #     "https://graph.facebook.com/oauth/access_token?client_id="+my_app_id+"&client_secret="+my_app_secret+"&grant_type=fb_exchange_token&fb_exchange_token=EAAwDjsTCk8kBAFKa464KR8NMb4ooSDie7BZCnHS6iaRvehTk8LkmES3YZApFOxYN0Ev4C1PmxZBOaaF428sBmEbY2gJ4cA9at1Q6fz7XTeCjhektKGbSZC0r25Gz8QZC0h7ScUo0FknDMtLz6rAP4JCIayBlbZAjpVkn2knK5xCaYYZBELLMZBHqr2mwmLX7Hj0ZD"
#     # )
#     # r.json()
#     r = "https://graph.facebook.com/oauth/access_token?client_id="+my_app_id+"&client_secret="+my_app_secret+"&grant_type=fb_exchange_token&fb_exchange_token=EAAwDjsTCk8kBADZCDCSE3U9S18ydDnuTr20zE7s3B5GcUvCcEt1h9z9sRokdwxx60pCGaKc52JriQ3eWvSIeefBDLUITwD2FmiRwQ0ZAJcgfGLdQuMe9pwy7ivIZBvpJS2yZChZCIEPvtwCTH7V6XzyMMvFR5Uv1riLdhTX0vTwAxdhWCZAPuR2FePJh6beyB35BKTLGHriTvE86Kgto2KRYwecCJZCKkrwyjYa2WjSfwZDZD"
#     return r
#
#
# new_token = get_new_token()
# print(new_token)