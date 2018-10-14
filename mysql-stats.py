from prometheus_client import start_http_server, Gauge
from multiprocessing import Process, Manager
import time
import string
from scapy.all import *
import re

def func1(select, insert, delete, update, lock):

  def pkt_callback(pkt):
    pkt.show()
    ts = int(time.time())
    if Raw in pkt:
      if 'select' in pkt.getlayer(Raw).load.lower():
        select.append(ts)
      if 'insert' in pkt.getlayer(Raw).load.lower():
        insert.append(ts)
      if 'update' in pkt.getlayer(Raw).load.lower():
        update.append(ts)
      if 'delete' in pkt.getlayer(Raw).load.lower():
        delete.append(ts)
      if 'lock' in pkt.getlayer(Raw).load.lower():
        lock.append(ts)
      print str(pkt.getlayer(Raw).load)
  
  sniff(prn=pkt_callback, filter='dst port 3306', store=0)

def statement_list(statement, ts):
    for item in statement:
      if item < ts:
        statement.remove(item)

def func2(select, insert, delete, update, lock):
  while True:
    ts = int(time.time())-30
    statement_list(select, ts)
    statement_list(insert, ts)
    statement_list(update, ts)
    statement_list(delete, ts)
    statement_list(lock, ts)
    time.sleep(1)

def func3(select, insert, delete, update, lock):
  
  start_http_server(9100)
  print 'Started on port 9100'

  select_statement = Gauge('select_statements', '')
  insert_statement = Gauge('insert_statements', '')
  delete_statement = Gauge('delete_statements','')
  update_statement = Gauge('update_statements','')
  lock_statement = Gauge('lock_statements','')

  while True:
    select_statement.set(len(select))
    insert_statement.set(len(insert))
    delete_statement.set(len(delete))
    update_statement.set(len(update))
    lock_statement.set(len(lock))
    time.sleep(1)

def runInParallel(*fns):
  with Manager() as manager:
    select = manager.list()
    insert = manager.list()
    delete = manager.list()
    update = manager.list()
    lock = manager.list()
    proc = []
    for fn in fns:
      p = Process(target=fn, args=[select, insert, delete, update, lock])
      p.start()
      proc.append(p)
    for p in proc:
      p.join()

runInParallel(func1, func2, func3)
