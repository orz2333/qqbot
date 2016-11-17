#!/usr/bin/python
# -*- coding: utf-8 -*-

from qqbot import QQBot
import re, requests

class MyQQBot(QQBot):
    def onPollComplete(self, msgType, from_uin, buddy_uin, message):
        reply = ''
        message = message.split()
        if message:
            if message[0] == 'command:':
                if re.search('ss',message[1]):
                     reply = requests.get('https://ss.aong.cn', verify = 'ss.pem').text
                elif message[1] == '-help':
                    reply = '欢迎使用QQBot，使用方法：\n' + \
                            '\t-help\n' + \
                            '\t-refetch\n' + \
                            '\t-stop\n'
                elif message[1][:6] == '-list ':
                    reply = getattr(self, message[1][6:].strip()+'Str', '')
                elif message[1][:6] == '-send ':
                    args = message[1][6:].split(' ', 2)
                    if len(args) == 3 and args[1].isdigit() and args[0] in ['buddy', 'group', 'discuss']:
                        n = int(args[1])
                        try:
                            if args[0] == 'buddy':
                                uin = self.buddiesDictQ[n]['uin']
                            elif args[0] == 'group':
                                uin = self.groupsDictQ[n]['uin']
                            else:
                                uin = self.discussesDict[n]['uin']
                        except KeyError:
                            reply = '接收者账号错误'
                        else:
                            self.send(args[0], uin, args[2].strip())
                            reply = '消息发送成功'
                elif message[1] == '-refetch':
                    self.refetch()
                    reply = '重新获取 好友/群/讨论组 成功'
                elif message[1] == '-stop':
                    reply = '系统已关闭'
                    self.stopped = True
                else:
                    reply = "sb"
        self.send(msgType, from_uin, reply)

myqqbot = MyQQBot()
myqqbot.Login()
myqqbot.Run()
