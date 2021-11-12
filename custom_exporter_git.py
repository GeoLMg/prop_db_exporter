from typing import Counter
import prometheus_client
import time
import threading
from threading import *
from prometheus_client import Gauge,start_http_server
import subprocess

# Подключеие к базе данных
import cx_Oracle as ora
dsnStr = ora.makedsn(host="ww.host.com", port="####", service_name='ser_name')
conn = ora.connect(user="user", password="***", dsn='dsn' ) 

# Создание данных
information = prometheus_client.Info("build_version","v0.1")
bash_metric = prometheus_client.Gauge("bash_prop_count","bash status of counting shop")
DB_metrics = prometheus_client.Gauge("shop_complite_count","DB props count")




def count_metric(timer):
    #Поучение данных о пропах
    ps = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
    grepFirst = subprocess.Popen(['grep', 'pstop03'], stdout=subprocess.PIPE, stdin=ps.stdout)
    grepSecond = subprocess.Popen(['grep', '-v', 'grep'], stdout=subprocess.PIPE, stdin=grepFirst.stdout)
    wc = subprocess.check_output(['wc', '-l',], stdin=grepSecond.stdout, text=True)
    bashResult =int(wc)
    # Получение данных от базы
    cur = conn.cursor()
    cur.execute("select count(*) from (SELECT DISTINCT rep_site FROM REFGWR.LMV_INTSTOCKREP_V2 liv WHERE trunc(rep_dcre)=trunc(sysdate))")
    res = cur.fetchall()
    DBResult = res[0][0]



    DB_metrics.set(DBResult)
    bash_metric.set(bashResult) 

    time.sleep(timer)



if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(9000)
    # Generate some requests.
    while True:
        count_metric(10)