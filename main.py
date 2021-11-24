# !pip install facebookads==2.5.0
# !pip install facebook_business
# !pip install gspread==3.6.0
# !pip install gspread_dataframe==3.6.0
# from matplotlib import pyplot as plt
import schedule
import time
from facebookads.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adreportrun import AdReportRun
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adaccountuser import AdAccountUser as AdUser
from facebook_business import adobjects
from facebook_business.api import FacebookAdsApi
from pandas import DataFrame, to_datetime
import gspread
from gspread_dataframe import set_with_dataframe
from accs import my_app_id, my_app_secret, my_access_token
from datetime import datetime
# from threading import Thread


# Написание скрипта Создадим три переменных, в которые запишем access token, App ID и App Secret. Авторизуемся через метод init() класса FacebooksAdsApi и добавляем пользователя. Метод get_ad_accounts() вернёт нам данные по всем нашим рекламным аккаунтам в виде словаря. По этим же данным можем получить информацию о кампаниях методом get_campaigns().
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
my_account = AdAccount('act_426823688657953')
my_accounts = [my_account]
campaigns = my_account.get_campaigns()
print('аккаунты загружены', my_accounts, sep='\n')
# me = AdUser(fbid='me')
# my_accounts = list(me.get_ad_accounts())
# my_account = my_accounts[0]
# print(my_accounts)
# print(my_account)

# ACCES GOOGLE SHEET
sa = gspread.service_account(filename="service_account.json")
sh = sa.open_by_key('1P3vTJeEnowD_Q1z9UO32hdI-tofzVcdi6fEeAKGdUKw')
worksheet = sh.worksheet("zag_dom")

# Попробуем получить amount spent через my_account. Для этого воспользуемся методом api_get(), передав в параметр fields поле AdAccount.Field.amount_spent. Теперь, чтобы получить желаемые данные, выведем поле у переменной my_account, поделив на 100, чтобы обрубить копейки. Расходы получаем в валюте аккаунта, в нашем случае это RUB. То, ради чего мы всё это затеваем — получить данные о расходах на рекламные кампании для последующего анализа.
# my_account.api_get(fields=[AdAccount.Field.amount_spent])
# print(int(my_account[AdAccount.Field.amount_spent])/100)


# Объявим переменную fields — в этом списке будут храниться поля, которые мы хотим получать: id кампании, количество кликов, затрат и просмотров. Теперь опишем две функции. Первая будет асинхронно отправлять запросы к Facebook и возвращать результаты. Вторая — формирует эти запросы и передает в первую функцию. В результате будем получать список словарей.
fields = [
    AdsInsights.Field.campaign_id,
    AdsInsights.Field.campaign_name,
    AdsInsights.Field.clicks,
    AdsInsights.Field.spend,
    AdsInsights.Field.impressions,
    AdsInsights.Field.actions
]
print('fields заданы')

count = 0
def wait_for_async_job(async_job):
    global count
    async_job = async_job.api_get()
    while async_job[AdReportRun.Field.async_status] != 'Job Completed' or async_job[
        AdReportRun.Field.async_percent_completion] < 100:
        time.sleep(2)
        async_job = async_job.api_get()
    else:
        print("Job " + str(count) + " completed")
        count += 1
    return async_job.get_result(params={"limit": 1000})


def get_insights(account, date_preset='last_7d'):
    leads = [{'field': "action_type", 'operator': "IN", 'value': ["lead"]}]
    account = AdAccount(account["id"])
    i_async_job = account.get_insights(
        params={
            'level': 'ad',
            'date_preset': date_preset,
            'time_increment': 1,
            'filtering' : leads
            },
            fields=fields,
            is_async=True)

    results = [dict(item) for item in wait_for_async_job(i_async_job)]
    return results
# get_insights(my_account, date_preset='last_7d')


# Следующий шаг — получение искомых данных о затратах. Будем собирать данные за всё время, поэтому заведём переменную date_preset, значение которой поставим lifetime. И для каждого аккаунта вызовем функцию get_insights(), а список, который она возвращает, положим в insights_lists. Создадим DataFrame и вытащим из insights_lists интересующие данные — это id кампании, количество кликов, затраты и просмотры.
def all_in():
    elem_insights = []
    insights_lists = []
    date_preset = 'last_90d'

    for elem in my_accounts:
        elem_insights = get_insights(elem, date_preset)
        insights_lists.append(elem_insights)

    insight_campaign_id_list = []
    insight_clicks_list = []
    insight_spend_list = []
    insight_impressions_list = []
    insight_date_start_list = []
    insight_date_stop_list = []
    insight_leads_list = []
    insight_campaign_name = []
    for elem1 in insights_lists:
        for elem2 in elem1:
            insight_campaign_id_list.append(str(elem2['campaign_id']))
            insight_clicks_list.append(int(elem2['clicks']))
            insight_spend_list.append(str(elem2['spend']).replace('.', ','))
            insight_impressions_list.append(int(elem2['impressions']))
            insight_date_start_list.append(to_datetime(elem2['date_start'], format="%Y/%m/%d"))
            insight_date_stop_list.append(to_datetime(elem2['date_stop'], format="%Y/%m/%d"))
            insight_campaign_name.append(str(elem2['campaign_name']))
            insight_leads_list.append(int(elem2['actions'][0]['value'] if 'actions' in elem2 else 0))
            # print(elem2['actions'])
    print('данные получены')

    df = DataFrame()
    df['campaign_name'] = insight_campaign_name
    df['campaign_id'] = insight_campaign_id_list
    df['spend'] = insight_spend_list
    df['leads'] = insight_leads_list
    df['clicks'] = insight_clicks_list
    df['impressions'] = insight_impressions_list
    df['date_start'] = insight_date_start_list
    df['date_stop'] = insight_date_stop_list
    print('сформирована таблица')
    # df.groupby(['campaign_name']).sum()
    # df.head(100)

    # CLEAR SHEET CONTENT
    range_of_cells = worksheet.range('A2:H1000') #-> Select the range you want to clear
    for cell in range_of_cells:
        cell.value = ''
    worksheet.update_cells(range_of_cells)

    # APPEND DATA TO SHEET
    set_with_dataframe(worksheet, df) #-> THIS EXPORTS YOUR DATAFRAME TO THE GOOGLE SHEET

    print('данные отправлены в гугл таблицы')
    # worksheet.update('A1:B2', [[1, 2], [3, 4]])

print('функции заданы')

all_in()

# scheduler
# def scheduler():
#     schedule.every().day.at("20:06").do(all_in)
#     # # schedule.every(10).minutes.do(job)
#     # # schedule.every().hour.do(job)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
#         print(datetime.now().time())
#
# scheduler()
# # Создаём и запускаем планировщик в отдельном потоке
# t = Thread(target=scheduler)
# t.start()






