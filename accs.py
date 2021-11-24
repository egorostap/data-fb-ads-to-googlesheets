import requests
my_access_token = 'my_access_token'
my_app_id = 'my_app_id'
my_app_secret = 'my_app_secret'

# def get_new_token():
#     # r = requests.get(
#     #     "https://graph.facebook.com/oauth/access_token?client_id="+my_app_id+"&client_secret="+my_app_secret+"&grant_type=fb_exchange_token&fb_exchange_token=my_access_token"
#     # )
#     # r.json()
#     r = "https://graph.facebook.com/oauth/access_token?client_id="+my_app_id+"&client_secret="+my_app_secret+"&grant_type=fb_exchange_token&fb_exchange_token=my_access_token"
#     return r
#
#
# new_token = get_new_token()
# print(new_token)