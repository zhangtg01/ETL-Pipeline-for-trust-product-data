
import requests
from bs4 import BeautifulSoup
import datetime
import time
import pandas as pd
import traceback
import jsdata as js
import logging as logg
import config as conf
from DBConn import DBConn


def send_eail(subject, content, to_addr=['zhangtg01@jsfund.cn']):
    js.send_mail(subject, content, to_addr)


def setup_logger(logger_name, log_file, level=logg.INFO):
    l = logg.getLogger(logger_name)
    formatter = logg.Formatter('%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s ')
    fileHandler = logg.FileHandler(log_file, mode='a', encoding='utf-8')
    fileHandler.setFormatter(formatter)
    streamHandler = logg.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)


def get_format_date():
    """
    格式化日期
    :return:
    """
    monday, friday = datetime.date.today(), datetime.date.today()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    while friday.weekday() != 4:
        friday += one_day

    millis = int(round(time.time() * 1000))
    dt = friday.strftime('%Y%m%d')
    return monday, friday, millis, dt


def crawler_data():
    count = 0
    while count < 11:
        count += 1
        monday, friday, millis, dt = get_format_date()
        params = {'mode': 'Jhxtlbstatistics', 'dp_Search_Way': '0', 'starttime': monday, 'txtendtime': friday,
                  '_': millis}

        try:
            r = requests.get('https://www.yanglee.com/Action/AjaxData.ashx', params=params, headers=conf.header, proxies=conf.proxies)
            soup = BeautifulSoup(r.text, "html.parser")
            result = soup.select('tr[class="tr1"]')
            result2 = soup.select('tr[class="tr2"]')
            result += result2

            df = pd.DataFrame()
            for site in result:
                category = site.select('td')[0].get_text().strip()
                numbers = site.select('td ')[1].get_text().strip()[:-1]
                scale = site.select('td ')[2].get_text().strip()[:-1]
                time_limit = site.select('td ')[3].get_text().strip()[:-1]
                max_1 = site.select('td ')[4].get_text().strip()[:-1]
                min_1 = site.select('td ')[5].get_text().strip()[:-1]
                average_1 = site.select('td ')[6].get_text().strip()[:-1]
                rise_fall = site.select('td ')[7].get_text().strip()
                df_1 = pd.DataFrame([{'信托类别': category, '数量': numbers, '规模': scale, '平均期限': time_limit, '最高收益': max_1,
                                      '最低收益': min_1, '平均收益': average_1, '涨跌幅': rise_fall}])
                df = df.append(df_1)
            df['dt'] = dt
            df['hcreateby'] = 'zhangtg'
            df['hupdateby'] = 'zhangtg'
            df['hisvalid'] = '1'
            df['hcreatetime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df['hupdatetime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            insert_list = df.values.tolist()

            try:
                db_mysql.bulk_insert_mysql(conf.sql_insert_sql, insert_list)
                logg.info('用益信托网插入数据为：' + str(insert_list))
            except Exception as e:
                err = traceback.format_exc()
                logg.info('用益信托网插入数据报错：' + str(err))
                send_eail('用益信托网插入数据报错：', str(err))

            return 1
        except Exception as e:
            logg.info('用益信托网请求数据报错：' + str(e))
            send_eail('用益信托网请求数据报错：', str(e))


if __name__ == '__main__':

    log_filename = conf.LOG_FILE
    setup_logger('log', log_filename)
    logg = logg.getLogger('log')

    db_mysql = DBConn(dbtype='mysql', host=conf.db_server, port=conf.db_port, user=conf.username,
                      passwd=conf.password, dbname=conf.dbname)

    crawler_data()