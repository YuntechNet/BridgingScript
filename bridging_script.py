#!/usr/bin/python3
import subprocess, smtplib, traceback

SMTP_ACCOUNT = 'SMTP_ACCOUNT'
SMTP_PASSWD = 'SMTP_PASSWD'
SMTP_HOST = 'SMTP_HOST'
SMTP_PORT = 25
SMTP_USE_TLS = False
SMTP_ANNOUNCE = ['SMTP_RECIEVER']

BR_IP = ['BR_IP']
BR_MASK = ['BR_MASK']
BR_GATE = ['BR_GATE']

BR_NAME = ['BR_IF_NAME']
IF_NET = ['IF_NET_NAME']
IF_LAN = ['IF_LAN_NAME']

try:
    for IP, MASK, GATE, NAME, NET, LAN in zip(BR_IP, BR_MASK, BR_GATE, BR_NAME, IF_NET, IF_LAN):
        print('==========[ Bridging: %s, NET IFACE: %s, LAN IFACE: %s ]==========' % (NAME, NET, LAN))
        print('----- Clearing BRIDGE Setting.')
        subprocess.call('ifconfig %s down' % NAME, shell=True)
        subprocess.call('brctl delbr %s' % NAME, shell=True)
        print('----- Clearing IFACE Setting.')
        subprocess.call('ifconfig %s 0.0.0.0 up' % NET, shell=True)
        subprocess.call('ifconfig %s 0.0.0.0 up' % LAN, shell=True)
        print('----- Bridging.')
        subprocess.call('brctl addbr %s' % NAME, shell=True)
        subprocess.call('brctl addif %s %s' % (NAME, NET), shell=True)
        subprocess.call('brctl addif %s %s' % (NAME, LAN), shell=True)
        print('----- Bridge Info:')
        subprocess.call('brctl show %s' % NAME, shell=True)
        print('----- Upping Bridge.')
        subprocess.call('ifconfig %s %s netmask %s up' % (NAME, IP, MASK), shell=True)
        print('----- Default routing.')
        subprocess.call('ip route add default via %s' % GATE, shell=True)
    print('==========[              All  Bridges  Setup  Down              ]==========')
except Exception as exception:
    smtpObj = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    smtpObj.login(SMTP_ACCOUNT, SMTP_PASSWD)
    title = u'FireWall Error Traceback'
    content = str(traceback.format_exc())
    smtpObj.sendmail(to_addr_list=SMTP_ANNOUNCE, message='Subject: %s/n/n%s' % (title, content))
