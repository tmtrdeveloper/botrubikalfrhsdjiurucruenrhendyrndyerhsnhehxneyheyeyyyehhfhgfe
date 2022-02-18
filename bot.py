import asyncio
import base64
import concurrent.futures
import datetime
import glob
import json
import math
import os
import pathlib
import random
import sys
import time
from json import dumps, loads
from random import randint
import re
import requests
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from requests import post
from googletrans import Translator
import io
from PIL import Image , ImageFont, ImageDraw 
import arabic_reshaper
from bidi.algorithm import get_display
from mutagen.mp3 import MP3
from gtts import gTTS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#lisence by bahman ahmadi this classes
#this classes opened sourse and free
class encryption:
    def __init__(self, auth):
        self.key = bytearray(self.secret(auth), "UTF-8")
        self.iv = bytearray.fromhex('00000000000000000000000000000000')

    def replaceCharAt(self, e, t, i):
        return e[0:t] + i + e[t + len(i):]

    def secret(self, e):
        t = e[0:8]
        i = e[8:16]
        n = e[16:24] + t + e[24:32] + i
        s = 0
        while s < len(n):
            e = n[s]
            if e >= '0' and e <= '9':
                t = chr((ord(e[0]) - ord('0') + 5) % 10 + ord('0'))
                n = self.replaceCharAt(n, s, t)
            else:
                t = chr((ord(e[0]) - ord('a') + 9) % 26 + ord('a'))
                n = self.replaceCharAt(n, s, t)
            s += 1
        return n

    def encrypt(self, text):
        raw = pad(text.encode('UTF-8'), AES.block_size)
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        enc = aes.encrypt(raw)
        result = base64.b64encode(enc).decode('UTF-8')
        return result

    def decrypt(self, text):
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        dec = aes.decrypt(base64.urlsafe_b64decode(text.encode('UTF-8')))
        result = unpad(dec, AES.block_size).decode('UTF-8')
        return result

class Bot:
	def __init__(self, auth):
		self.auth = auth
		self.enc = encryption(auth)
		
	def sendMessage(self, chat_id, text, message_id=None):
		if message_id == None:
			t = False
			while t == False:
				try:
					p = post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/")
					p = loads(self.enc.decrypt(p.json()["data_enc"]))
					t = True
				except:
					t = False
			return p
		else:
			return post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"sendMessage",
				"input":{
					"object_guid":chat_id,
					"rnd":f"{randint(100000,900000)}",
					"text":text,
					"reply_to_message_id":message_id
				},
				"client":{
					"app_name":"Main",
					"app_version":"3.2.1",
					"platform":"Web",
					"package":"web.rubika.ir",
					"lang_code":"fa"
				}
			}))},url="https://messengerg2c17.iranlms.ir/")
	
	def deleteMessages(self, chat_id, message_ids):
		return post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"deleteMessages",
			"input":{
				"object_guid":chat_id,
				"message_ids":message_ids,
				"type":"Global"
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c66.iranlms.ir/")

	def requestFile(self, name, size , mime):
		o = ''
		while str(o) != '<Response [200]>':
			o = post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"requestSendFile",
				"input":{
					"file_name":name,
					"size":size,
					"mime":mime
				},
				"client":{
					"app_name":"Main",
					"app_version":"3.2.1",
					"platform":"Web",
					"package":"web.rubika.ir",
					"lang_code":"fa"
				}
			}))},url="https://messengerg2c66.iranlms.ir/")
			try:
				k = loads(self.enc.decrypt(o.json()["data_enc"]))
				if k['status'] != 'OK' or k['status_det'] != 'OK':
					o = '502'
			except:
				o = '502'
		return k['data']

	def fileUpload(self, bytef ,hash_send ,file_id ,url):		
		if len(bytef) <= 131072:
			h = {
				'auth':self.auth,
				'chunk-size':str(len(bytef)),
				'file-id':str(file_id),
				'access-hash-send':hash_send,
				'total-part':str(1),
				'part-number':str(1)
			}
			t = False
			while t == False:
				try:
					j = post(data=bytef,url=url,headers=h).text
					j = loads(j)['data']['access_hash_rec']
					t = True
				except:
					t = False
			
			return j
		else:
			t = len(bytef) / 131072
			t += 1
			t = random._floor(t)
			for i in range(1,t+1):
				if i != t:
					k = i - 1
					k = k * 131072
					t2 = False
					while t2 == False:
						try:
							o = post(data=bytef[k:k + 131072],url=url,headers={
								'auth':self.auth,
								'chunk-size':str(131072),
								'file-id':file_id,
								'access-hash-send':hash_send,
								'total-part':str(t),
								'part-number':str(i)
							}).text
							o = loads(o)['data']
							t2 = True
						except:
							t2 = False
					j = k + 131072
					j = round(j / 1024)
					j2 = round(len(bytef) / 1024)
					print(str(j) + 'kb / ' + str(j2) + ' kb')                
				else:
					k = i - 1
					k = k * 131072
					t2 = False
					while t2 == False:
						try:
							p = post(data=bytef[k:],url=url,headers={
								'auth':self.auth,
								'chunk-size':str(len(bytef[k:])),
								'file-id':file_id,
								'access-hash-send':hash_send,
								'total-part':str(t),
								'part-number':str(i)
							}).text
							p = loads(p)['data']['access_hash_rec']
							t2 = True
						except:
							t2 = False
					j2 = round(len(bytef) / 1024)
					print(str(j2) + 'kb / ' + str(j2) + ' kb') 
					return p

	def sendFile(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name, size, text=None, message_id=None):
			if text == None:
				if message_id == None:
					t = False
					while t == False:
						try:
							p = loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
								"method":"sendMessage",
								"input":{
									"object_guid":chat_id,
									"rnd":f"{randint(100000,900000)}",
									"file_inline":{
										"dc_id":str(dc_id),
										"file_id":str(file_id),
										"type":"File",
										"file_name":file_name,
										"size":size,
										"mime":mime,
										"access_hash_rec":access_hash_rec
									}
								},
								"client":{
									"app_name":"Main",
									"app_version":"3.2.1",
									"platform":"Web",
									"package":"web.rubika.ir",
									"lang_code":"fa"
								}
							}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
							t = True
						except:
							t = False
					return p
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"File",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))    
			else:
				if message_id == None:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"File",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"File",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc'])) 

	def sendImage(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name,  size, thumb_inline , width , height, text=None, message_id=None):
			if text == None:
				if message_id == None:
					t = False
					while t == False:
						try:
							p = loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
								"method":"sendMessage",
								"input":{
									"object_guid":chat_id,
									"rnd":f"{randint(100000,900000)}",
									"file_inline":{
										"dc_id":str(dc_id),
										"file_id":str(file_id),
										"type":"Image",
										"file_name":file_name,
										"size":size,
										"mime":mime,
										"access_hash_rec":access_hash_rec,
										'thumb_inline':thumb_inline,
										'width':width,
										'height':height
									}
								},
								"client":{
									"app_name":"Main",
									"app_version":"3.2.1",
									"platform":"Web",
									"package":"web.rubika.ir",
									"lang_code":"fa"
								}
							}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
							t = True
						except:
							t = False
					return p
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Image",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'thumb_inline':thumb_inline,
								'width':width,
								'height':height
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))    
			else:
				if message_id == None:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Image",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'thumb_inline':thumb_inline,
								'width':width,
								'height':height
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Image",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'thumb_inline':thumb_inline,
								'width':width,
								'height':height
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc'])) 

	def sendVoice(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name,  size, duration, text=None, message_id=None):
			if text == None:
				if message_id == None:
					t = False
					while t == False:
						try:
							p = loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
								"method":"sendMessage",
								"input":{
									"object_guid":chat_id,
									"rnd":f"{randint(100000,900000)}",
									"file_inline":{
										"dc_id":str(dc_id),
										"file_id":str(file_id),
										"type":"Voice",
										"file_name":file_name,
										"size":size,
										"mime":mime,
										"access_hash_rec":access_hash_rec,
										'time':duration,
									}
								},
								"client":{
									"app_name":"Main",
									"app_version":"3.2.1",
									"platform":"Web",
									"package":"web.rubika.ir",
									"lang_code":"fa"
								}
							}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
							t = True
						except:
							t = False
					return p
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Voice",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'time':duration,
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))    
			else:
				if message_id == None:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Voice",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'time':duration,
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Voice",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'time':duration,
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc'])) 

	def getUserInfo(self, chat_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getUserInfo",
			"input":{
				"user_guid":chat_id
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c37.iranlms.ir/").json()["data_enc"]))
	
	def getMessages(self, chat_id,min_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMessagesInterval",
			"input":{
				"object_guid":chat_id,
				"middle_message_id":min_id
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c67.iranlms.ir/").json().get("data_enc"))).get("data").get("messages")
		
	def getInfoByUsername(self, username):
		''' username should be without @ '''
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getObjectByUsername",
			"input":{
				"username":username
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c23.iranlms.ir/").json().get("data_enc")))

	def banGroupMember(self, chat_id, user_id):
		return post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"banGroupMember",
			"input":{
				"group_guid": chat_id,
				"member_guid": user_id,
				"action":"Set"
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c21.iranlms.ir/")

	def invite(self, chat_id, user_ids):
		return post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"addGroupMembers",
			"input":{
				"group_guid": chat_id,
				"member_guids": user_ids
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c22.iranlms.ir/")
	
	def getGroupAdmins(self, chat_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"client":{
				"app_name":"Main",
				"app_version":"2.9.5",
				"lang_code":"fa",
				"package":"ir.resaneh1.iptv",
				"platform":"Android"
			},
			"input":{
				"group_guid":chat_id
			},
			"method":"getGroupAdminMembers"
		}))},url="https://messengerg2c22.iranlms.ir/").json().get("data_enc")))

	def getMessagesInfo(self, chat_id, message_ids):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMessagesByID",
			"input":{
				"object_guid": chat_id,
				"message_ids": message_ids
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))}, url="https://messengerg2c24.iranlms.ir/").json()["data_enc"])).get("data").get("messages")

	def setMembersAccess(self, chat_id, access_list):
		return post(json={
			"api_version": "4",
			"auth": self.auth,
			"client": {
				"app_name": "Main",
				"app_version": "2.9.5",
				"lang_code": "fa",
				"package": "ir.resaneh1.iptv",
				"platform": "Android"
			},
			"data_enc": self.enc.encrypt(dumps({
				"access_list": access_list,
				"group_guid": chat_id
			})),
			"method": "setGroupDefaultAccess"
		}, url="https://messengerg2c24.iranlms.ir/")

	def getGroupInfo(self, chat_id):
		return loads(self.enc.decrypt(post(
			json={
				"api_version":"5",
				"auth": self.auth,
				"data_enc": self.enc.encrypt(dumps({
					"method":"getGroupInfo",
					"input":{
						"group_guid": chat_id,
					},
					"client":{
						"app_name":"Main",
						"app_version":"3.2.1",
						"platform":"Web",
						"package":"web.rubika.ir",
						"lang_code":"fa"
					}
			}))}, url="https://messengerg2c24.iranlms.ir/").json()["data_enc"]))
	
	def get_updates_all_chats(self):
		time_stamp = str(random._floor(datetime.datetime.today().timestamp()) - 200)
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getChatsUpdates",
			"input":{
				"state":time_stamp,
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c67.iranlms.ir/").json().get("data_enc"))).get("data").get("chats")
	
	def get_updates_chat(self, chat_id):
		time_stamp = str(random._floor(datetime.datetime.today().timestamp()) - 200)
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMessagesUpdates",
			"input":{
				"object_guid":chat_id,
				"state":time_stamp
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c67.iranlms.ir/").json().get("data_enc"))).get("data").get("updated_messages")
	
	def my_sticker_set(self):
		time_stamp = str(random._floor(datetime.datetime.today().timestamp()) - 200)
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMyStickerSets",
			"input":{},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c67.iranlms.ir/").json().get("data_enc"))).get("data")

	def getThumbInline(self,image_bytes:bytes):
		im = Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		if height > width:
			new_height = 40
			new_width  = round(new_height * width / height)
		else:
			new_width  = 40
			new_height = round(new_width * height / width)
		im = im.resize((new_width, new_height), Image.ANTIALIAS)
		changed_image = io.BytesIO()
		im.save(changed_image, format='PNG')
		changed_image = changed_image.getvalue()
		return base64.b64encode(changed_image)

	def getImageSize(self,image_bytes:bytes):
		im = Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		return width , height

	def hex_to_rgb(self,value):
		value = value.lstrip('#')
		lv = len(value)
		return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

	def write_text_image(self,text:str,bc_color:str='yellow',size:int=40,color='#3d3d3d',x=50,y=100):
		try:
			file_name = 'image/'+ bc_color +'.jpg'
			image = Image.open(file_name) 
			size = int(size)
			font = ImageFont.truetype('Vazir-Regular.ttf', size, encoding='unic')
			draw = ImageDraw.Draw(image) 
			print(text)
			reshaped_text = arabic_reshaper.reshape(text) # correct its shape
			print(reshaped_text)
			bidi_text = get_display(reshaped_text) # correct its direction
			print(bidi_text)
			changed_image = io.BytesIO()
			if color.startswith('#') and len(color) < 8:
				color = self.hex_to_rgb(color)
				draw.text((x, y), bidi_text,color, font = font)
				image.save(changed_image, format='PNG')
				changed_image = changed_image.getvalue()
				return changed_image
			elif color.startswith('(') and len(color) < 14 and color.count(',') == 2:
				color = color.replace('(', '').replace(')', '')
				list_c = color.split(',')
				list_c2 = []
				for i in list_c:
					list_c2.append(int(i))
					color = tuple(list_c2)
					draw.text((x, y), bidi_text,color, font = font)
					image.save(changed_image, format='PNG')
					changed_image = changed_image.getvalue()
					return changed_image
				else:
					return 'err'
		except:
			return 'err'

def hasInsult(msg):
	swData = [False,None]
	for i in open("dontReadMe.txt").read().split("\n"):
		if i in msg:
			swData = [True, i]
			break
		else: continue
	return swData

def hasAds(msg):
	links = list(map(lambda ID: ID.strip()[1:],findall("@[\w|_|\d]+", msg))) + list(map(lambda link:link.split("/")[-1],findall("rubika\.ir/\w+",msg)))
	joincORjoing = "joing" in msg or "joinc" in msg

	if joincORjoing: return joincORjoing
	else:
		for link in links:
			try:
				Type = bot.getInfoByUsername(link)["data"]["chat"]["abs_object"]["type"]
				if Type == "Channel":
					return True
			except KeyError: return False

auth = "jyrymbbrwkmqcksimqavrasuhqfvxpid"
bot = Bot(auth)
list_message_seened = []
time_reset = random._floor(datetime.datetime.today().timestamp()) + 350
while(2 > 1):
    try:
        chats_list:list = bot.get_updates_all_chats()
        if chats_list != []:
            for chat in chats_list:
                access = chat['access']
                if chat['abs_object']['type'] == 'User' or chat['abs_object']['type'] == 'Group':
                    text:str = chat['last_message']['text']
                    if 'SendMessages' in access and chat['last_message']['type'] == 'Text' and text.strip() != '':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            if text == '!start':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سلام \n به ابر سرویس کروز خوش آمدید ❤\n\n لطفا جهت راهنما !help را ارسال کنید',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            elif text.startswith('!nim http://') == True or text.startswith('!nim https://') == True:
                                try:
                                    bot.sendMessage(chat['object_guid'], "در حال آماده سازی لینک ...",chat['last_message']['message_id'])
                                    print('sended response')
                                    link = text[4:]
                                    nim_baha_link=requests.post("https://www.digitalbam.ir/DirectLinkDownloader/Download",params={'downloadUri':link})
                                    pg:str = nim_baha_link.text
                                    pg = pg.split('{"fileUrl":"')
                                    pg = pg[1]
                                    pg = pg.split('","message":""}')
                                    pg = pg[0]
                                    nim_baha = pg    
                                    try:
                                        bot.sendMessage(chat['object_guid'], 'لینک نیم بها شما با موفقیت آماده شد ✅ \n لینک : \n' + nim_baha ,chat['last_message']['message_id'])
                                        print('sended response')    
                                    except:
                                        print('server bug2')
                                except:
                                    print('server bug3')
                            elif text.startswith('!info @'):
                                try:
                                    user_info = bot.getInfoByUsername(text[7:])	
                                    if user_info['data']['exist'] == True:
                                        if user_info['data']['type'] == 'User':
                                            bot.sendMessage(chat['object_guid'], 'name:\n  ' + user_info['data']['user']['first_name'] + ' ' + user_info['data']['user']['last_name'] + '\n\nbio:\n   ' + user_info['data']['user']['bio'] + '\n\nguid:\n  ' + user_info['data']['user']['user_guid'] , chat['last_message']['message_id'])
                                            print('sended response')
                                        else:
                                            bot.sendMessage(chat['object_guid'], 'کانال است' , chat['last_message']['message_id'])
                                            print('sended response')
                                    else:
                                        bot.sendMessage(chat['object_guid'], 'وجود ندارد' , chat['last_message']['message_id'])
                                        print('sended response')
                                except:
                                    print('server bug6')
                            elif text.startswith('!search ['):
                                try:
                                    search = text[9:-1]    
                                    if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                               
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
                                        results = jd['results']['webs']
                                        text = ''
                                        for result in results:
                                            text += result['title'] + '\n\n'
                                        bot.sendMessage(chat['object_guid'], 'نتایج به پیوی شما ارسال شد', chat['last_message']['message_id'])
                                        bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
                                    elif chat['abs_object']['type'] == 'User':
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
                                        results = jd['results']['webs']
                                        text = ''
                                        for result in results:
                                            text += result['title'] + '\n\n'
                                        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('server bug 7')
                            elif text.startswith('!wiki-s ['):
                                try:
                                    search = text[9:-1]    
                                    search = search + ' ویکی پدیا'
                                    if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                               
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
                                        results = jd['results']['webs'][0:4]
                                        text = ''
                                        for result in results:
                                            if ' - ویکی‌پدیا، دانشنامهٔ آزاد' in result['title']:
                                                title = result['title'].replace(' - ویکی‌پدیا، دانشنامهٔ آزاد','')
                                                text += title + ' :\n\n' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\nمقاله کامل صفحه 1 : \n' + '!wiki [1:' + title + ']\n\n' 
                                        bot.sendMessage(chat['object_guid'], 'نتایج به پیوی شما ارسال شد', chat['last_message']['message_id'])
                                        bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
                                    elif chat['abs_object']['type'] == 'User':
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
                                        results = jd['results']['webs'][0:4]
                                        text = ''
                                        for result in results:
                                            if ' - ویکی‌پدیا، دانشنامهٔ آزاد' in result['title']:
                                                title = result['title'].replace(' - ویکی‌پدیا، دانشنامهٔ آزاد','')
                                                text += title + ' :\n\n' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\nمقاله کامل صفحه 1 : \n' + '!wiki [1:' + title + ']\n\n'
                                        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('server bug 7')
                            elif text.startswith('!jok'):
                                try:                        
                                    jd = requests.get('https://api.codebazan.ir/jok/').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                except:
                                    print('server bug 8')
                            elif text.startswith('!name_shakh'):
                                try:                        
                                    jd = requests.get('https://api.codebazan.ir/name/').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                except:
                                    print('server bug 8')
                            elif text.startswith('!khatere'):
                                try:                        
                                    jd = requests.get('https://api.codebazan.ir/jok/khatere/').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                except:
                                    print('server bug 8')
                            elif text.startswith('!danesh'):
                                try:                        
                                    jd = requests.get('https://api.codebazan.ir/danestani/').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                except:
                                    print('server bug 8')
                            elif text.startswith('!pa_na_pa'):
                                try:                        
                                    jd = requests.get('https://api.codebazan.ir/jok/pa-na-pa/').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                except:
                                    print('server bug 8')
                            elif text.startswith('!alaki_masala'):
                                try:                        
                                    jd = requests.get('https://api.codebazan.ir/jok/alaki-masalan/').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                except:
                                    print('server bug 8')
                            elif text.startswith('!dastan'):
                                try:                        
                                    jd = requests.get('https://api.codebazan.ir/dastan/').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                except:
                                    print('server bug 8')
                            elif text.startswith('!bio'):
                                try:                        
                                    jd = requests.get('https://api.codebazan.ir/bio/').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                except:
                                    print('server bug 8')
                            elif text.startswith('!search-k ['):
                                try:
                                    search = text[11:-1]
                                    if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                                
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
                                        results = jd['results']['webs']
                                        text = ''
                                        for result in results:
                                            text += result['title'] + ':\n\n  ' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\n'
                                        bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
                                        bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
                                    elif chat['abs_object']['type'] == 'User':
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
                                        results = jd['results']['webs']
                                        text = ''
                                        for result in results:
                                            text += result['title'] + ':\n\n  ' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\n'
                                        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('server bug 7')
                            elif text.startswith('!ban [') and chat['abs_object']['type'] == 'Group' and 'BanMember' in access:
                                try:
                                    user = text[6:-1].replace('@', '')
                                    guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
                                    admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
                                    if not guid in admins and chat['last_message']['author_object_guid'] in admins:
                                        bot.banGroupMember(chat['object_guid'], guid)
                                        bot.sendMessage(chat['object_guid'], 'انجام شد' , chat['last_message']['message_id'])
                                except:
                                    print('server bug 7')
                            elif text.startswith('!search-i ['):
                                try:
                                    search = text[11:-1]
                                    if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':
                                        bot.sendMessage(chat['object_guid'], 'نتایج کامل به زودی به پیوی شما ارسال میشوند', chat['last_message']['message_id'])                           
                                        jd = json.loads(requests.get('https://zarebin.ir/api/image/?q=' + search + '&chips=&page=1').text)
                                        jd = jd['results']
                                        a = 0
                                        for j in jd:
                                            if a <= 10:
                                                res = requests.get(j['image_link'])
                                                if res.status_code == 200 and res.content != b'' and j['cdn_thumbnail'] != '':
                                                    thumb = str(j['cdn_thumbnail'])
                                                    thumb = thumb.split('data:image/')[1]
                                                    thumb = thumb.split(';')[0]
                                                    if thumb == 'png':
                                                        b2 = res.content
                                                        tx = bot.requestFile(j['title'] + '.png', len(b2), 'png')
                                                        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                                        b.sendFile(chat['last_message']['author_object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, j['title'] + '.png', len(b2), j['title'])
                                                        print('sended file')
                                                    elif thumb == 'webp':
                                                        b2 = res.content
                                                        tx = bot.requestFile(j['title'] + '.webp', len(b2), 'webp')
                                                        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                                        bot.sendFile(chat['last_message']['author_object_guid'] ,tx['id'] , 'webp', tx['dc_id'] , access, j['title'] + '.webp', len(b2), j['title'])
                                                        print('sended file')
                                                    else:
                                                        b2 = res.content
                                                        tx = bot.requestFile(j['title'] + '.jpg', len(b2), 'jpg')
                                                        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                                        bot.sendFile(chat['last_message']['author_object_guid'] ,tx['id'] , 'jpg', tx['dc_id'] , access, j['title'] + '.jpg', len(b2), j['title'])
                                                        print('sended file')
                                                a += 1
                                            else:
                                                break                                    
                                    elif chat['abs_object']['type'] == 'User':
                                        bot.sendMessage(chat['object_guid'], 'در حال یافتن کمی صبور باشید...', chat['last_message']['message_id'])
                                        print('ss')
                                        jd = json.loads(requests.get('https://zarebin.ir/api/image/?q=' + search + '&chips=&page=1').text)
                                        jd = jd['results']
                                        print(jd)
                                        a = 0
                                        for j in jd:
                                            if a < 10:    
                                                print(j)                     
                                                res = requests.get(j['image_link'])
                                                print(res)
                                                if res.status_code == 200 and res.content != b'' and j['cdn_thumbnail'] != '' and j['cdn_thumbnail'].startswith('data:image'):
                                                    thumb = str(j['cdn_thumbnail'])
                                                    thumb = thumb.split('data:image/')[1]
                                                    thumb = thumb.split(';')[0]
                                                    print(thumb)
                                                    if thumb == 'png':
                                                        b2 = res.content
                                                        tx = bot.requestFile(j['title'] + '.png', len(b2), 'png')
                                                        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                                        bot.sendFile(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, j['title'] + '.png', len(b2), j['title'], chat['last_message']['message_id'])
                                                        print('sended file')
                                                    elif thumb == 'webp':
                                                        b2 = res.content
                                                        tx = bot.requestFile(j['title'] + '.webp', len(b2), 'webp')
                                                        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                                        bot.sendFile(chat['object_guid'] ,tx['id'] , 'webp', tx['dc_id'] , access, j['title'] + '.webp', len(b2), j['title'], chat['last_message']['message_id'])
                                                        print('sended file')
                                                    else:
                                                        b2 = res.content
                                                        tx = bot.requestFile(j['title'] + '.jpg', len(b2), 'jpg')
                                                        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                                        bot.sendFile(chat['object_guid'] ,tx['id'] , 'jpg', tx['dc_id'] , access, j['title'] + '.jpg', len(b2), j['title'], chat['last_message']['message_id'])
                                                        print('sended file')
                                                a += 1  
                                except:
                                    print('server bug 7')
                            elif text.startswith('!ytb ['):
                                try:
                                    link = text[6:-1]
                                    if hasInsult(link)[0] == False and chat['abs_object']['type'] == 'Group':
                                        bot.sendMessage(chat['object_guid'], 'نتایج کامل به زودی به پیوی شما ارسال میشوند', chat['last_message']['message_id'])                           
                                        jd = json.loads(requests.get('https://www.wirexteam.ga/youtube?type=donwload&url=' + link).text)
                                        jd = jd['youtube']
                                        if jd[1] == 200:
                                            jd = jd[0]
                                            a = 0
                                            res = requests.get(jd['mp4'][7]['url'])
                                            if res.status_code == 200 and res.content != b'':
                                                b2 = res.content
                                                tx = bot.requestFile(jd['title'] + '.mp4', len(b2), 'mp4')
                                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                                bot.sendFile(chat['last_message']['author_object_guid'] ,tx['id'] , 'mp4', tx['dc_id'] , access, jd['title'] + '.mp4', len(b2), jd['title'])
                                                print('sended file')                               
                                    elif chat['abs_object']['type'] == 'User':
                                        bot.sendMessage(chat['object_guid'], 'در حال یافتن کمی صبور باشید...', chat['last_message']['message_id'])
                                        jd = json.loads(requests.get('https://www.wirexteam.ga/youtube?type=donwload&url=' + link).text)
                                        print('ss')
                                        jd = jd['youtube']
                                        if jd[1] == 200:
                                            print(jd[0]['mp4'][7]['url'])
                                            jd = jd[0]
                                            a = 0
                                            res = requests.get(jd['mp4'][7]['url'])
                                            print('downloaded')
                                            if res.status_code == 200 and res.content != b'':
                                                b2 = res.content
                                                tx = bot.requestFile(jd['title'] + '.mp4', len(b2), 'mp4')
                                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                                bot.sendFile(chat['last_message']['author_object_guid'] ,tx['id'] , 'mp4', tx['dc_id'] , access, jd['title'] + '.mp4', len(b2), jd['title'])
                                                print('sended file')     
                                except:
                                    print('server bug 7')
                            elif text.startswith('!remove') and chat['abs_object']['type'] == 'Group' and 'BanMember' in access:
                                try:
                                    admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
                                    if chat['last_message']['author_object_guid'] in admins:
                                        c_id = chat['last_message']['message_id']
                                        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
                                        msg_data = msg_data[0]
                                        if 'reply_to_message_id' in msg_data.keys():
                                            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
                                            if not msg_data['author_object_guid'] in admins:
                                                bot.banGroupMember(chat['object_guid'], msg_data['author_object_guid'])
                                                bot.sendMessage(chat['object_guid'], 'انجام شد' , chat['last_message']['message_id'])
                                except:
                                    print('server ban bug')
                            elif text.startswith('!trans ['):
                                try:
                                    t = text[8:-1]
                                    t = t.split(':')
                                    lang = t[0]
                                    t2 = ''
                                    for i in range(1,len(t)):
                                        t2 += t[i]
                                    text_trans = t2
                                    if hasInsult(text_trans)[0] == False:
                                        t = Translator()
                                        text = t.translate(text_trans,lang).text
                                        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
                                    elif chat['abs_object']['type'] == 'User':
                                        t = Translator()
                                        text = t.translate(text_trans,lang).text
                                        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
                                except:
                                    print('server bug 7')
                            elif text.startswith('!myket-s ['):
                                try:
                                    search = text[10:-1]
                                    if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':
                                        bot.sendMessage(chat['object_guid'], 'نتایج کامل به زودی به پیوی شما ارسال میشوند', chat['last_message']['message_id'])                           
                                        jd = json.loads(requests.get('https://www.wirexteam.ga/myket?type=search&query=' + search).text)
                                        jd = jd['search']
                                        a = 0
                                        text = ''
                                        for j in jd:
                                            if a <= 7:
                                                text += '🔸 عنوان : ' + j['title_fa'] + '\nℹ️ توضیحات : '+ j['tagline'] + '\n🆔 نام یکتا برنامه : ' + j['package_name'] + '\n⭐️امتیاز: ' + str(j['rate']) + '\n✳ نام نسخه : ' + j['version'] + '\nقیمت : ' + j['price'] + '\nحجم : ' + j['size'] + '\nبرنامه نویس : ' + j['developer'] + '\n\n' 
                                                a += 1
                                            else:
                                                break     
                                        if text != '':
                                            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)                               
                                    elif chat['abs_object']['type'] == 'User':
                                        jd = json.loads(requests.get('https://www.wirexteam.ga/myket?type=search&query=' + search).text)
                                        jd = jd['search']
                                        a = 0
                                        text = ''
                                        for j in jd:
                                            if a <= 7:
                                                text += '🔸 عنوان : ' + j['title_fa'] + '\nℹ️ توضیحات : '+ j['tagline'] + '\n🆔 نام یکتا برنامه : ' + j['package_name'] + '\n⭐️امتیاز: ' + str(j['rate']) + '\n✳ نام نسخه : ' + j['version'] + '\nقیمت : ' + j['price'] + '\nحجم : ' + j['size'] + '\nبرنامه نویس : ' + j['developer'] + '\n\n' 
                                                a += 1
                                            else:
                                                break     
                                        if text != '':
                                            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('server bug 7')
                            elif text.startswith('!wiki ['):
                                try:
                                    t = text[7:-1]
                                    t = t.split(':')
                                    mozoa = ''
                                    t2 = ''
                                    page = int(t[0])
                                    for i in range(1,len(t)):
                                        t2 += t[i]
                                    mozoa = t2

                                    if hasInsult(mozoa)[0] == False and chat['abs_object']['type'] == 'Group' and page > 0:
                                        text_t = requests.get('https://api.codebazan.ir/wiki/?search=' + mozoa).text
                                        if not 'codebazan.ir' in text_t:
                                            CLEANR = re.compile('<.*?>') 
                                            def cleanhtml(raw_html):
                                                cleantext = re.sub(CLEANR, '', raw_html)
                                                return cleantext
                                            text_t = cleanhtml(text_t)
                                            n = 4200
                                            text_t = text_t.strip()
                                            max_t = page * n
                                            min_t = max_t - n
                                            
                                            text = text_t[min_t:max_t]
                                            print(text_t)
                                            bot.sendMessage(chat['object_guid'], 'مقاله "'+ mozoa + '" صفحه : ' + str(page) + ' به پیوی شما ارسال شد', chat['last_message']['message_id'])
                                            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + mozoa + ') : \n\n'+text)
                                    elif chat['abs_object']['type'] == 'User' and page > 0:
                                        text_t = requests.get('https://api.codebazan.ir/wiki/?search=' + mozoa).text
                                        if not 'codebazan.ir' in text_t:
                                            CLEANR = re.compile('<.*?>') 
                                            def cleanhtml(raw_html):
                                                cleantext = re.sub(CLEANR, '', raw_html)
                                                return cleantext
                                            text_t = cleanhtml(text_t)
                                            n = 4200
                                            text_t = text_t.strip()
                                            max_t = page * n
                                            
                                            min_t = max_t - n
                                            print('d')
                                            text = text_t[min_t:max_t]
                                            bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
                                except:
                                    print('server bug 7')
                            elif text.startswith('!currency'):
                                t = json.loads(requests.get('https://api.codebazan.ir/arz/?type=arz').text)
                                text = ''
                                for i in t:
                                    price = i['price'].replace(',','')[:-1] + ' تومان'
                                    text += i['name'] + ' : ' + price + '\n'
                                bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
                            elif text.startswith('!gold'):
                                t = requests.get('https://www.iribnews.ir/fa/gold').text
                                t = t.split('<div class="col-xs-36 container-info-price">')[1]
                                t = t.split('<div class="row-icon-price price-index col-xs-36">')[0]
                                t = t.split('<section class="row row-info">')[1]
                                t = t.split('                                                                               <div class="row content-table content-gold-currency">                                 ')[1:]
                                t = t[:-1]
                                text = ''
                                for i in t:
                                    i = i.split('</div>                                 <div class="col-xs-18 item-table">                                                                              ')
                                    name = i[0]
                                    name = name.replace('<div class="col-xs-18 item-table">', '')
                                    gheymat = i[1]
                                    gheymat = gheymat.split(' ریال')[0]
                                    gheymat = gheymat.strip()
                                    gheymat = gheymat.replace(',','')
                                    text += name + ' : ' + gheymat[:-1] + ' تومان' + '\n'
                                bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
                            elif text.startswith('!ping ['):
                                try:
                                    site = text[7:-1]
                                    jd = requests.get('https://api.codebazan.ir/ping/?url=' + site).text
                                    text = str(jd)
                                    bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('server bug 7')
                            elif text.startswith('!font ['):
                                try:
                                    site = text[7:-1]
                                    jd = json.loads(requests.get('https://api.codebazan.ir/font/?text=' + site).text)
                                    jd = jd['result']
                                    text = ''
                                    for i in range(1,100):
                                        text += jd[str(i)] + '\n'
                                    if hasInsult(site)[0] == False and chat['abs_object']['type'] == 'Group':
                                        bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
                                        bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + site + ') : \n\n'+text)                                        
                                    elif chat['abs_object']['type'] == 'User':
                                        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('server bug 7')
                            elif text.startswith('!font-fa ['):
                                try:
                                    site = text[10:-1]
                                    jd = json.loads(requests.get('https://api.codebazan.ir/font/?type=fa&text=' + site).text)
                                    jd = jd['Result']
                                    text = ''
                                    for i in range(1,10):
                                        text += jd[str(i)] + '\n'
                                    if hasInsult(site)[0] == False and chat['abs_object']['type'] == 'Group':
                                        bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
                                        bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + site + ') : \n\n'+text)                                        
                                    elif chat['abs_object']['type'] == 'User':
                                        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('server bug 7')
                            elif text.startswith('!whois ['):
                                try:
                                    site = text[8:-1]
                                    jd = json.loads(requests.get('https://api.codebazan.ir/whois/index.php?type=json&domain=' + site).text)
                                    text = 'مالک : \n'+jd['owner'] + '\n\n آیپی:\n' + jd['ip'] + '\n\nآدرس مالک : \n' + jd['address'] + '\n\ndns1 : \n' + jd['dns']['1'] + '\ndns2 : \n' + jd['dns']['2'] 
                                    bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('server bug 7')
                            elif text.startswith('!vaj ['):
                                try:
                                    vaj = text[6:-1]
                                    if hasInsult(vaj)[0] == False:
                                        jd = json.loads(requests.get('https://api.codebazan.ir/vajehyab/?text=' + vaj).text)
                                        jd = jd['result']
                                        text = 'معنی : \n'+jd['mani'] + '\n\n لغتنامه معین:\n' + jd['Fmoein'] + '\n\nلغتنامه دهخدا : \n' + jd['Fdehkhoda'] + '\n\nمترادف و متضاد : ' + jd['motaradefmotezad']
                                        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('server bug 7')
                            elif text.startswith('!weather ['):
                                try:
                                    city = text[10:-1]
                                    if hasInsult(city)[0] == False:
                                        jd = json.loads(requests.get('https://api.codebazan.ir/weather/?city=' + city).text)
                                        text = 'دما : \n'+jd['result']['دما'] + '\n سرعت باد:\n' + jd['result']['سرعت باد'] + '\n وضعیت هوا: \n' + jd['result']['وضعیت هوا'] + '\n\n بروز رسانی اطلاعات امروز: ' + jd['result']['به روز رسانی'] + '\n\nپیش بینی هوا فردا: \n  دما: ' + jd['فردا']['دما'] + '\n  وضعیت هوا : ' + jd['فردا']['وضعیت هوا']
                                        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('server bug 7')
                            elif text.startswith('!ip ['):
                                try:
                                    ip = text[5:-1]
                                    if hasInsult(vaj)[0] == False:
                                        jd = json.loads(requests.get('https://api.codebazan.ir/ipinfo/?ip=' + ip).text)
                                        text = 'نام شرکت:\n' + jd['company'] + '\n\nکشور : \n' + jd['country_name'] + '\n\nارائه دهنده : ' + jd['isp']
                                        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('server bug 7')  
                            elif text.startswith("!add [") and chat['abs_object']['type'] == 'Group' and 'AddMember' in access:
                                try:
                                    user = text[6:-1]
                                    bot.invite(chat['object_guid'], [bot.getInfoByUsername(user.replace('@', ''))["data"]["chat"]["object_guid"]])
                                    bot.sendMessage(chat['object_guid'], 'اضافه شد' , chat['last_message']['message_id'])                         
                                except:
                                    print('server bug 7')  
                            elif text.startswith('!math ['):
                                try:
                                    amal_and_value = text[7:-1]
                                    natije = ''
                                    if amal_and_value.count('*') == 1:
                                        value1 = float(amal_and_value.split('*')[0].strip())
                                        value2 = float(amal_and_value.split('*')[1].strip())
                                        natije = value1 * value2
                                    elif amal_and_value.count('/') > 0:
                                        value1 = float(amal_and_value.split('/')[0].strip())
                                        value2 = float(amal_and_value.split('/')[1].strip())
                                        natije = value1 / value2
                                    elif amal_and_value.count('+') > 0:
                                        value1 = float(amal_and_value.split('+')[0].strip())
                                        value2 = float(amal_and_value.split('+')[1].strip())
                                        natije = value1 + value2
                                    elif amal_and_value.count('-') > 0:
                                        value1 = float(amal_and_value.split('-')[0].strip())
                                        value2 = float(amal_and_value.split('-')[1].strip())
                                        natije = value1 - value2
                                    elif amal_and_value.count('**') > 0:
                                        value1 = float(amal_and_value.split('**')[0].strip())
                                        value2 = float(amal_and_value.split('**')[1].strip())
                                        natije = value1 ** value2
                                    
                                    if natije != '':
                                        bot.sendMessage(chat['object_guid'], natije , chat['last_message']['message_id'])
                                except:
                                    print('server bug 7')  
                            elif text.startswith('!shot'):
                                try:
                                    c_id = chat['last_message']['message_id']
                                    msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
                                    msg_data = msg_data[0]
                                    if 'reply_to_message_id' in msg_data.keys():
                                        msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
                                        if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                                            txt_xt = msg_data['text']
                                            res = requests.get('https://api.otherapi.tk/carbon?type=create&code=' + txt_xt + '&theme=vscode')
                                            if res.status_code == 200 and res.content != b'':
                                                b2 = res.content
                                                tx = bot.requestFile('code_image.png', len(b2), 'png')
                                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                                width, height = bot.getImageSize(b2)
                                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'code_image.png', len(b2) , str(bot.getThumbInline(b2))[2:-1] , width, height ,message_id= c_id)
                                                print('sended file')    
                                except:
                                    print('server ban bug')
                            elif text.startswith('!speak'):
                                try:
                                    c_id = chat['last_message']['message_id']
                                    msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
                                    msg_data = msg_data[0]
                                    if 'reply_to_message_id' in msg_data.keys():
                                        msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
                                        if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                                            txt_xt = msg_data['text']
                                            speech = gTTS(txt_xt)
                                            changed_voice = io.BytesIO()
                                            speech.write_to_fp(changed_voice)
                                            b2 = changed_voice.getvalue()
                                            tx = bot.requestFile('sound.ogg', len(b2), 'sound.ogg')
                                            access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                            f = io.BytesIO()
                                            f.write(b2)
                                            f.seek(0)
                                            audio = MP3(f)
                                            dur = audio.info.length
                                            bot.sendVoice(chat['object_guid'],tx['id'] , 'ogg', tx['dc_id'] , access, 'sound.ogg', len(b2), dur * 1000 ,message_id= c_id)
                                            print('sended voice')
                                except:
                                    print('server gtts bug')
                            elif text.startswith('!write ['):
                                try:
                                    c_id = chat['last_message']['message_id']
                                    msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
                                    msg_data = msg_data[0]
                                    if 'reply_to_message_id' in msg_data.keys():
                                        msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
                                        if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                                            txt_xt = msg_data['text']
                                            paramiters = text[8:-1]
                                            paramiters = paramiters.split(':')
                                            if len(paramiters) == 5:
                                                b2 = bot.write_text_image(txt_xt,paramiters[0],int(paramiters[1]),str(paramiters[2]),int(paramiters[3]),int(paramiters[4]))
                                                tx = bot.requestFile('code_image.png', len(b2), 'png')
                                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                                width, height = bot.getImageSize(b2)
                                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'code_image.png', len(b2) , str(bot.getThumbInline(b2))[2:-1] , width, height ,message_id= c_id)
                                                print('sended file')               
                                except:
                                    print('server ban bug')
                            elif chat['abs_object']['type'] == 'Group' and 'DeleteGlobalAllMessages' in access and hasInsult(text)[0] == True:
                                admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
                                if not chat['last_message']['author_object_guid'] in admins:
                                    bot.deleteMessages(chat['object_guid'], [chat['last_message']['message_id']])
                            elif chat['abs_object']['type'] == 'Group' and 'DeleteGlobalAllMessages' in access and hasAds(text) == True:
                                admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
                                if not chat['last_message']['author_object_guid'] in admins:
                                    bot.deleteMessages(chat['object_guid'], [chat['last_message']['message_id']])
                            elif text.startswith('!help'):
                                text = 'راهنمای ابر سرویس کروز : \n\nلینک نیم بها: \n !nim link \n به جای link لینکتون رو بگذارید حتما http یا https داشته باشه. \n\n جوک : \n !jok را بفرستید \n\n جستجو : \n !search [موضوع] \n این را بفرستید و به جای موضوع موضوع خود را بگذارید \n\n جستجو کامل: \n !search-k [موضوع] \n این را بفرستید و به جای موضوع موضوع خود را بگذارید \n\n نرخ ارز : \n !currency را بفرستید \n\n نرخ طلا : \n !gold را بفرستید \n\n گرفتن اطلاعات یک کاربر : \n !info @user \n این را بفرستید به جای user آیدی اون کاربر رو بگذارید \n\n خاطره : !khatere بفرستید \n\nنام شاخ : !name_shakh\n\nپه نه په گفتن : !pa_na_pa \n\nچیزای الکی مثلا : !alaki_masala \n\n دانستنی : !danesh \n\nداستان : !dastan\n\nبیوگرافی : !bio\n\n100 فونت شاخ انگلیسی \n!font [text] \n به جای text متنتون نتیجه با 100 فونت ارسال میشه \n\nفونت شاخ فارسی : \n !font-fa [text]\nبه جای text متنتون'
                                text2 = '\n\nسرویس ترجمه : \n !trans [lang:text] \n این را بفرستید به جای lang زبان مورد نظر مثلا en انگلیسی به جای text متن مورد نظر \n مثال : !trans [en:سلام] جواب : hi \n\n آب وهوا : \n !weather [city]\n بفرستید به جای city شهرتون رو بگذارید \nپینگ سایت : !ping [site] \n به جای site سایت مورد نظر بدون http و https و www \n\n اطلاعات یک دامنه : !whois [site] \n اینم بدون http و https و www به جای سایت سایتتون \n\n معنی و مفهوم کلمه : !vaj [کلمه ] \n به جای کلمه کلمتون رو بگذارید فقط کلمات فارسی پشتیبانی میشه \n\n گرفتن اطلاعات آیپی: \n !ip [your_ip] \n به جای your_ip آیپی تون رو بگذارید \n\n آوردن متن مقاله از ویکی پدیا : \n !wiki [page:name] \n به جای page صفحه چندم مقاله رو بزارید مثلا 1 یعنی صفحه اول و به جای name موضوع مقالتون و بعد بفرستید اگر اسم دقیق موضوع مقالتون رو نمیدونید از دستور بعدی جستجو اش کنید\n\nجستجو در مقاله های ویکی پدیا : \n\n !wiki-s [title]\n به جای title موضوعتون رو بنویسید تمام مقاله های مرتبط براتون لیست میشه'
                                if chat['abs_object']['type'] == 'Group':
                                    bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
                                    bot.sendMessage(chat['last_message']['author_object_guid'], text + text2)                                        
                                elif chat['abs_object']['type'] == 'User':
                                    bot.sendMessage(chat['object_guid'], text + text2 , chat['last_message']['message_id'])

                            list_message_seened.append(m_id)
        else:
            print('no update ')
    except:
        print('server bug5')
    time.sleep(1)
    time_reset2 = random._floor(datetime.datetime.today().timestamp())
    if list_message_seened != [] and time_reset2 > time_reset:
        list_message_seened = []
        time_reset = random._floor(datetime.datetime.today().timestamp()) + 350
