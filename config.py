import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(os.path.join(BASE_DIR, 'logs'), 'crawl_trust.log')


proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'www.yanglee.com',
        'Referer': 'https://www.yanglee.com/Studio/?i=1050240036',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'}

sql_insert_sql = """
        INSERT INTO analytics_re_data.USE_TRUST(truset_category,numbers,scale,average_maturity,max_earning,
        min_earning,average_earning,rise_fall,dt,create_by,update_by,hisvalid,hcreatetime,hupdatetime)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) on duplicate key update 
        truset_category = values(truset_category), numbers = values(numbers), scale = values(scale),
        average_maturity = values(average_maturity), max_earning = values(max_earning),min_earning = values(min_earning),
        average_earning = values(average_earning), 
        rise_fall = values(rise_fall), dt = values(dt),create_by = values(create_by),
        update_by = values(update_by), hisvalid = values(hisvalid),
        hupdatetime = values(hupdatetime)
"""
