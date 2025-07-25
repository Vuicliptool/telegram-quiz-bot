import random
import re
import sqlite3
from datetime import datetime
import hashlib
import requests
import os
import time
import logging
import pathlib
from collections import Counter
import telebot
if os.name == 'nt':os.system('cls')
else:os.system('clear')
#API TOKEN BOT
API_TOKEN = '6737085704:AAFuXOG0aQ6xBldCJYfiqWOIquOcH8PNNek'
#NHÓM BÁO LÀM NHIỆM VỤ
member = '@Tbruttele_bot'
#NHÓM BÁO LỆNH RÚT TIỀN
money = '@Tbruttele_bot'

bot = telebot.TeleBot(API_TOKEN)
conn = sqlite3.connect('phone.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        ID INTEGER PRIMARY KEY,
        phone_number TEXT, Tien INT
    )
''')
conn.commit()
conn.close()

def TimeStamp():
    now = datetime.now().strftime('%d-%m-%Y')
    return now
def xemtien(ID):
    conn = sqlite3.connect('phone.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE ID = ?", (ID,))
    tien = cursor.fetchone()
    return tien[2]
def themtien(ID, tien):
    conn = sqlite3.connect('phone.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE ID = ?", (ID,))
    tiencu = cursor.fetchone()
    tienmoi = tiencu[2] + tien
    cursor.execute("UPDATE users SET tien = ? WHERE ID = ?", (tienmoi, ID))
    conn.commit()
    conn.close()
    return tienmoi

def trutien(ID, tien):
    conn = sqlite3.connect('phone.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE ID = ?", (ID,))
    tiencu = cursor.fetchone()
    tienmoi = tiencu[2] - tien
    cursor.execute("UPDATE users SET tien = ? WHERE ID = ?", (tienmoi, ID))
    conn.commit()
    conn.close()
    return tienmoi

def checkphone(ID):
    conn = sqlite3.connect('phone.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE ID = ?", (ID,))
    phone = cursor.fetchone()
    return phone[1]

def testtien(ID, tien):
    db = sqlite3.connect('phone.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE ID = ?", (ID,))
    tiencu = cursor.fetchone()
    new_coin = tiencu[2] - tien
    if new_coin < 0:
        return False
    else:
        return True
#menu button
start = telebot.types.ReplyKeyboardMarkup(True).add("💳 TÀI KHOẢN","💵 KIẾM TIỀN").add("💲RÚT TIỀN","📩THỂ LỆ").add("🏆TOP VƯỢT LINK","🔑ADMIN")
link = telebot.types.ReplyKeyboardMarkup(True).add("🕔LỊCH SỬ LÀM NV").add("💰OCTOLINKZ", "💰LINK4M").add("💰DILINK","💰1SHORT").add("🏠 HOME")

octolink = telebot.types.ReplyKeyboardMarkup(True).add("🔒NHẬP KEY OCTOLINK").add("🔙TRỞ VỀ NHIỆM VỤ")
fvip = telebot.types.ReplyKeyboardMarkup(True).add("🔒NHẬP KEY 1SHORT").add("🔙TRỞ VỀ NHIỆM VỤ")
lsu = telebot.types.ReplyKeyboardMarkup(True).add("🔙TRỞ VỀ NHIỆM VỤ")
link4m = telebot.types.ReplyKeyboardMarkup(True).add("🔒NHẬP KEY LINK4M").add("🔙TRỞ VỀ NHIỆM VỤ")
dilink = telebot.types.ReplyKeyboardMarkup(True).add("🔒NHẬP KEY DILINK").add("🔙TRỞ VỀ NHIỆM VỤ")
quaylai = telebot.types.ReplyKeyboardMarkup(True).add("🔙TRỞ VỀ NHIỆM VỤ")

rut = telebot.types.ReplyKeyboardMarkup(True).add("MOMO").add("🏠 HOME")

ve = telebot.types.ReplyKeyboardMarkup(True).add("💲RÚT TIỀN").add("🏠 HOME")
quay = telebot.types.ReplyKeyboardMarkup(True).add("🔙QUAY LẠI")
tle = telebot.types.ReplyKeyboardMarkup(True).add("🔃LOAD LẠI").add("💵 KIẾM TIỀN","🔑ADMIN").add("🏠 HOME")
tlee = telebot.types.ReplyKeyboardMarkup(True).add("💵 KIẾM TIỀN","🔑ADMIN").add("🏠 HOME")
gt = telebot.types.ReplyKeyboardMarkup(True).add("💵 KIẾM TIỀN","💲RÚT TIỀN").add("🏠 HOME")
nhaplai = telebot.types.ReplyKeyboardMarkup(True).add("NHẬP LẠI SDT")
@bot.message_handler(func=lambda message: message.text == "NHẬP LẠI SDT")
def handler_lai(message):
  ID = message.from_user.id
  conn = sqlite3.connect('phone.db')
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users WHERE ID = ?", (ID,))
  user = cursor.fetchone()
  if user is None:
    text = '''
VUI LÒNG NHẬP LẠI SỐ ĐIỆN THOẠI:
    '''
    bot.send_message(message.chat.id,text)
    bot.register_next_step_handler(message,sdt)
  else:
    text = '''
CHÀO MỪNG BẠN QUAY LẠI BOT CHÚC BẠN NGÀY MỚI VUI VẺ
'''
    bot.send_message(message.chat.id, text, reply_markup=start)
  conn.close()
def sdt(message):
  ID = message.chat.id
  phone_number = message.text.strip()
  phone_number = re.sub(r'\D', '', phone_number)
  if len(phone_number) != 10:
    bot.send_message(message.chat.id,text="SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ ! VUI LÒNG NHẬP LẠI!", reply_markup=nhaplai)
    return
  conn = sqlite3.connect('phone.db')
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users WHERE phone_number = ?", (phone_number,))
  user = cursor.fetchone()
  if user is None:
    cursor.execute("INSERT INTO users (ID, phone_number, tien) VALUES (?, ?, 0)", (ID, phone_number))
    conn.commit()
    text = '''
ĐĂNG KÍ TÀI KHOẢN THÀNH CÔNG BẠN CÓ THỂ KIẾM TIỀN!
'''
    bot.send_message(message.chat.id,text, reply_markup=start)
  else:
    text = '''
SỐ ĐIỆN THOẠI ĐÃ ĐƯỢC ĐĂNG KÝ TRÊN HỆ THỐNG
'''
    bot.send_message(message.chat.id,text,reply_markup=nhaplai)
  conn.close()
#BẮT ĐẦU 
@bot.message_handler(commands=['start','help'])
def handler_start(message):
  ID = message.from_user.id
  conn = sqlite3.connect('phone.db')
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users WHERE ID = ?", (ID,))
  user = cursor.fetchone()
  if user is None:
    text = '''
CHÀO MỪNG NGƯỜI MỚI!
📱 VUI LÒNG NHẬP SỐ ĐIỆN THOẠI ĐỂ ĐĂNG KÝ
⚠️ LƯU Ý: PHẢI LÀ SỐ ĐIỆN THOẠI ĐĂNG KÝ MOMO CHÍNH CHỦ ĐỂ CÓ THỂ RÚT TIỀN 

VUI LÒNG NHẬP SỐ ĐIỆN THOẠI:
    '''
    bot.send_message(message.chat.id,text)
    bot.register_next_step_handler(message,sdt)
  else:
    text = '''
CHÀO MỪNG BẠN QUAY LẠI BOT CHÚC BẠN NGÀY MỚI VUI VẺ
'''
    bot.send_message(message.chat.id, text, reply_markup=start)
  conn.close()
def sdt(message):
  ID = message.chat.id
  phone_number = message.text.strip()
  phone_number = re.sub(r'\D', '', phone_number)
  if len(phone_number) != 10:
    bot.send_message(message.chat.id,text="SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ ! VUI LÒNG NHẬP LẠI!", reply_markup=nhaplai)
    return
  conn = sqlite3.connect('phone.db')
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users WHERE phone_number = ?", (phone_number,))
  user = cursor.fetchone()
  if user is None:
    cursor.execute("INSERT INTO users (ID, phone_number, tien) VALUES (?, ?, 0)", (ID, phone_number))
    conn.commit()
    text = '''
ĐĂNG KÍ TÀI KHOẢN THÀNH CÔNG BẠN CÓ THỂ KIẾM TIỀN!
'''
    bot.send_message(message.chat.id,text, reply_markup=start)
  else:
    text = '''
SỐ ĐIỆN THOẠI ĐÃ ĐƯỢC ĐĂNG KÝ TRÊN HỆ THỐNG
'''
    bot.send_message(message.chat.id,text,reply_markup=nhaplai)
  conn.close()

#NHIỆM VỤ OCTOLINK

@bot.message_handler(func=lambda message: message.text == "💰OCTOLINKZ")
def handler_nv(message):
  username = message.from_user.id
  with open('key.txt', 'a') as f:
    f.close()
  string = f'octolink-{username}+{TimeStamp()}'
  hash_object = hashlib.md5(string.encode())
  key = str(hash_object.hexdigest())
  print(key)
  f = open("key.txt","r")
  k = f.read()
  f.close()
  time = datetime.now().strftime("%H")
  if int(time) < 6:
    text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 22H"
    bot.send_message(message.chat.id, text, reply_markup=start)
    return
  if int(time) > 22:
    text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 22H"
    bot.send_message(message.chat.id, text, reply_markup=start)
    return
  if key in k:
    text = "BẠN ĐÃ LÀM NHIỆM VỤ NÀY RỒI VUI LÒNG LÀM NHIỆM VỤ KHÁC"
    bot.send_message(message.chat.id, text, reply_markup=quaylai)
  else:
    url_key = requests.get(f'https://octolinkz.com/api?api=dbcf90ff8d4affed9cd8eb89895e9037c6d477cf&url=https://abcxyzok.blogspot.com/p/click-vao-o-ben-duoi-se-tu-ong-sao-chep.html?key={key}').json()['shortenedUrl']
    text = f'''
💵 Lấy Nhiệm Vụ Thành Công
💲 Vượt Link Và Nhận 250Đ
⭐ Link: {url_key}
     '''
    bot.send_message(message.chat.id, text, reply_markup=octolink)
@bot.message_handler(func=lambda message: message.text == "🔒NHẬP KEY OCTOLINK")
def handler_nv(message):
  bot.send_message(message.chat.id, text="VUI LÒNG NHẬP KEY:")
  bot.register_next_step_handler(message,nv1)
def nv1(message):
  try:
    key = message.text
    if key == "🔙TRỞ VỀ NHIỆM VỤ":
      ID = message.from_user.id
      now = TimeStamp()
      with open("key.txt", "r") as file:
        lines = file.readlines()
      nvt = 0
      for line in lines:
        if f"{now}:{ID}" in line:
          nvt += 1
      text = f'''
HÔM NAY: {TimeStamp()}
BẠN ĐÃ LÀM: {nvt} NHIỆM VỤ
      '''
      text += '''
VUI LÒNG CHỌN 👇
      '''
      bot.send_message(message.chat.id, text, reply_markup=link)
    if key == "🔒NHẬP KEY OCTOLINK":
      text = "VUI LÒNG KHÔNG SPAM NÚT NHẬP KEY HÃY NHẤN LẦN NỮA ĐỂ NHẬP"
      bot.send_message(message.chat.id, text)
    else:
      f = open("key.txt","r")
      k = f.read()
      f.close()
      username = message.from_user.id
      string = f'octolink-{username}+{TimeStamp()}'
      hash_object = hashlib.md5(string.encode())
      d_key = str(hash_object.hexdigest())
      if key in k:
        bot.send_message(message.chat.id, 'KEY ĐÃ ĐƯỢC SỬ DỤNG VUI LÒNG LÀM NHIỆM VỤ KHÁC')
      else:
        if key == d_key:
          ID = message.from_user.id
    #đặt số tiền	
          tien = int(300)
          tong = themtien(ID, tien)
          bot.send_message(message.chat.id, text = f'KEY ĐÚNG +{tien} XU | SỐ DƯ: {tong}',reply_markup=link)
          a = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={member}&text=ID: {ID}, LÀM THÀNH CÔNG NHIỆM VỤ <OCTOLINK> NHẬN {tien}Đ').text
          now = TimeStamp()
          f = open("key.txt","a+")
          k = f.write(f"{now}:{ID}_octolink/{key}"+"\n")
          f.close()
        else:
          bot.send_message(message.chat.id, 'KEY KHÔNG ĐÚNG VUI LÒNG GỬI [NHẬP KEY OCTOLINK] VÀ THỬ LẠI')
  except:
    bot.send_message(message.chat.id, text = "KEY KHÔNG ĐÚNG ĐỊNH DẠNG VUI LÒNG GỬI [NHẬP KEY OCTOLINK] VÀ THỬ LẠI", reply_markup=octolink)

#Nhập LINK4M
@bot.message_handler(func=lambda message: message.text == "💰LINK4M")
def handler_nv(message):
  username = message.from_user.id
  with open('key.txt', 'a') as f:
    f.close()
  string = f'link4m-{username}+{TimeStamp()}'
  hash_object = hashlib.md5(string.encode())
  key = str(hash_object.hexdigest())
  print(key)
  f = open("key.txt","r")
  k = f.read()
  f.close()
  time = datetime.now().strftime("%H")
  if int(time) < 6:
    text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 22H"
    bot.send_message(message.chat.id, text, reply_markup=start)
    return
  if int(time) > 22:
    text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 22H"
    bot.send_message(message.chat.id, text, reply_markup=start)
    return
  if key in k:
    text = "BẠN ĐÃ LÀM NHIỆM VỤ NÀY RỒI VUI LÒNG LÀM NHIỆM VỤ KHÁC"
    bot.send_message(message.chat.id, text, reply_markup=quaylai)
  else:
    url_key = requests.get(f'https://link4m.co/api-shorten/v2?api=64ac9e1b2995f32940090060&url=https://abcxyzok.blogspot.com/p/click-vao-o-ben-duoi-se-tu-ong-sao-chep.html?key={key}').json()['shortenedUrl']
    text = f'''
💵 Lấy Nhiệm Vụ Thành Công
💲 Vượt Link Và Nhận 300D
⭐ Link: {url_key}
     '''
    bot.send_message(message.chat.id, text, reply_markup=link4m)
@bot.message_handler(func=lambda message: message.text == "🔒NHẬP KEY LINK4M")
def handler_nv(message):
  bot.send_message(message.chat.id, text="VUI LÒNG NHẬP KEY:")
  bot.register_next_step_handler(message,nv2)
def nv2(message):
  try:
    key = message.text
    if key == "🔙TRỞ VỀ NHIỆM VỤ":
      ID = message.from_user.id
      now = TimeStamp()
      with open("key.txt", "r") as file:
        lines = file.readlines()
      nvt = 0
      for line in lines:
        if f"{now}:{ID}" in line:
          nvt += 1
      text = f'''
HÔM NAY: {TimeStamp()}
BẠN ĐÃ LÀM: {nvt} NHIỆM VỤ
      '''
      text += '''
VUI LÒNG CHỌN 👇
      '''
      bot.send_message(message.chat.id, text, reply_markup=link)
    if key == "🔒NHẬP KEY LINK4M":
      text = "VUI LÒNG KHÔNG SPAM NÚT NHẬP KEY HÃY NHẤN LẦN NỮA ĐỂ NHẬP"
      bot.send_message(message.chat.id, text)
    else:
      f = open("key.txt","r")
      k = f.read()
      f.close()
      username = message.from_user.id
      string = f'link4m-{username}+{TimeStamp()}'
      hash_object = hashlib.md5(string.encode())
      d_key = str(hash_object.hexdigest())
      if key in k:
        bot.send_message(message.chat.id, 'KEY ĐÃ ĐƯỢC SỬ DỤNG VUI LÒNG LÀM NHIỆM VỤ KHÁC')
      else:
        if key == d_key:
          ID = message.from_user.id
    #đặt số tiền	
          tien = int(300)
          tong = themtien(ID, tien)
          bot.send_message(message.chat.id, text = f'KEY ĐÚNG +{tien} XU | SỐ DƯ: {tong}',reply_markup=link)
          a = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={member}&text=ID: {ID}, LÀM THÀNH CÔNG NHIỆM VỤ <LINK4M> NHẬN {tien}Đ').text
          now = TimeStamp()
          f = open("key.txt","a+")
          k = f.write(f"{now}:{ID}_link4m/{key}"+"\n")
          f.close()
        else:
          bot.send_message(message.chat.id, 'KEY KHÔNG ĐÚNG VUI LÒNG GỬI [NHẬP KEY LINK4M] VÀ THỬ LẠI',reply_markup=link4m)
  except:
    bot.send_message(message.chat.id, text = "KEY KHÔNG ĐÚNG ĐỊNH DẠNG VUI LÒNG GỬI [NHẬP KEY LINK4M] VÀ THỬ LẠI", reply_markup=link4m)
#DILINK
@bot.message_handler(func=lambda message: message.text == "💰DILINK")
def handler_nv(message):
  username = message.from_user.id
  with open('key.txt', 'a') as f:
    f.close()
  string = f'dilink-{username}+{TimeStamp()}'
  hash_object = hashlib.md5(string.encode())
  key = str(hash_object.hexdigest())
  print(key)
  f = open("key.txt","r")
  k = f.read()
  f.close()
  time = datetime.now().strftime("%H")
  if int(time) < 6:
    text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 22H"
    bot.send_message(message.chat.id, text, reply_markup=start)
    return
  if int(time) > 22:
    text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 22H"
    bot.send_message(message.chat.id, text, reply_markup=start)
    return
  if key in k:
    text = "BẠN ĐÃ LÀM NHIỆM VỤ NÀY RỒI VUI LÒNG LÀM NHIỆM VỤ KHÁC"
    bot.send_message(message.chat.id, text, reply_markup=quaylai)
  else:
    link = f'https://dilink.net/QL_api.php?token=c5bd23bf304b304799286baf0430dc7dff69d7a6b61df592ab526321f9e3a438&url=https://abcxyzok.blogspot.com/p/click-vao-o-ben-duoi-se-tu-ong-sao-chep.html?key={key}'
    url_key = requests.get(f'https://tinyurl.com/api-create.php?url={link}').text
    text = f'''
💵 Lấy Nhiệm Vụ Thành Công
💲 Vượt Link Và Nhận 300Đ
⭐ Link: {url_key}
     '''
    bot.send_message(message.chat.id, text, reply_markup=dilink)
@bot.message_handler(func=lambda message: message.text == "🔒NHẬP KEY DILINK")
def handler_nv(message):
  bot.send_message(message.chat.id, text="VUI LÒNG NHẬP KEY:")
  bot.register_next_step_handler(message,nv3)
def nv3(message):
  try:
    key = message.text
    if key == "🔙TRỞ VỀ NHIỆM VỤ":
      ID = message.from_user.id
      now = TimeStamp()
      with open("key.txt", "r") as file:
        lines = file.readlines()
      nvt = 0
      for line in lines:
        if f"{now}:{ID}" in line:
          nvt += 1
      text = f'''
HÔM NAY: {TimeStamp()}
BẠN ĐÃ LÀM: {nvt} NHIỆM VỤ
      '''
      text += '''
VUI LÒNG CHỌN 👇
      '''
      bot.send_message(message.chat.id, text, reply_markup=link)
    if key == "🔒NHẬP KEY DILINK":
      text = "VUI LÒNG KHÔNG SPAM NÚT NHẬP KEY HÃY NHẤN LẦN NỮA ĐỂ NHẬP"
      bot.send_message(message.chat.id, text)
    else:
      f = open("key.txt","r")
      k = f.read()
      f.close()
      username = message.from_user.id
      string = f'dilink-{username}+{TimeStamp()}'
      hash_object = hashlib.md5(string.encode())
      d_key = str(hash_object.hexdigest())
      if key in k:
        bot.send_message(message.chat.id, 'KEY ĐÃ ĐƯỢC SỬ DỤNG VUI LÒNG LÀM NHIỆM VỤ KHÁC')
      else:
        if key == d_key:
          ID = message.from_user.id
    #đặt số tiền	
          tien = int(300)
          tong = themtien(ID, tien)
          bot.send_message(message.chat.id, text = f'KEY ĐÚNG +{tien} XU | SỐ DƯ: {tong}',reply_markup=link)
          a = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={member}&text=ID: {ID}, LÀM THÀNH CÔNG NHIỆM VỤ <DILINK> NHẬN {tien}Đ').text
          now = TimeStamp()
          f = open("key.txt","a+")
          k = f.write(f"{now}:{ID}_dilink/{key}"+"\n")
          f.close()
        else:
          bot.send_message(message.chat.id, 'KEY KHÔNG ĐÚNG VUI LÒNG GỬI [NHẬP KEY DILINK] VÀ THỬ LẠI')
  except:
    bot.send_message(message.chat.id, text = "KEY KHÔNG ĐÚNG ĐỊNH DẠNG VUI LÒNG GỬI [NHẬP KEY DILINK] VÀ THỬ LẠI", reply_markup=dilink)
#1SHORT
@bot.message_handler(func=lambda message: message.text == "💰1SHORT")
def handler_nv(message):
  username = message.from_user.id
  with open('key.txt', 'a') as f:
    f.close()
  string = f'1short-{username}+{TimeStamp()}'
  hash_object = hashlib.md5(string.encode())
  key = str(hash_object.hexdigest())
  print(key)
  f = open("key.txt","r")
  k = f.read()
  f.close()
  time = datetime.now().strftime("%H")
  if int(time) < 6:
    text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 22H"
    bot.send_message(message.chat.id, text, reply_markup=start)
    return
  if int(time) > 22:
    text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 22H"
    bot.send_message(message.chat.id, text, reply_markup=start)
    return
  if key in k:
    text = "BẠN ĐÃ LÀM NHIỆM VỤ NÀY RỒI VUI LÒNG LÀM NHIỆM VỤ KHÁC"
    bot.send_message(message.chat.id, text, reply_markup=quaylai)
  else:
    url_key = requests.get(f'https://1shorten.com/api?api=232806f68d1fb76e55428daa60fb01dece9734b9&url=https://abcxyzok.blogspot.com/p/click-vao-o-ben-duoi-se-tu-ong-sao-chep.html?key={key}').json()['shortenedUrl']
    text = f'''
💵 Lấy Nhiệm Vụ Thành Công
💲 Vượt Link Và Nhận 300Đ
⭐ Link: {url_key}
     '''
    bot.send_message(message.chat.id, text, reply_markup=fvip)
@bot.message_handler(func=lambda message: message.text == "🔒NHẬP KEY 1SHORT")
def handler_nv(message):
  bot.send_message(message.chat.id, text="VUI LÒNG NHẬP KEY:")
  bot.register_next_step_handler(message,nv5)
def nv5(message):
  try:
    key = message.text
    if key == "🔙TRỞ VỀ NHIỆM VỤ":
      ID = message.from_user.id
      now = TimeStamp()
      with open("key.txt", "r") as file:
        lines = file.readlines()
      nvt = 0
      for line in lines:
        if f"{now}:{ID}" in line:
          nvt += 1
      text = f'''
HÔM NAY: {TimeStamp()}
BẠN ĐÃ LÀM: {nvt} NHIỆM VỤ
      '''
      text += '''
VUI LÒNG CHỌN 👇
      '''
      bot.send_message(message.chat.id, text, reply_markup=link)
    if key == "🔒NHẬP KEY 1SHORT":
      text = "VUI LÒNG KHÔNG SPAM NÚT NHẬP KEY HÃY NHẤN LẦN NỮA ĐỂ NHẬP"
      bot.send_message(message.chat.id, text)
    else:
      f = open("key.txt","r")
      k = f.read()
      f.close()
      username = message.from_user.id
      string = f'1short-{username}+{TimeStamp()}'
      hash_object = hashlib.md5(string.encode())
      d_key = str(hash_object.hexdigest())
      if key in k:
        bot.send_message(message.chat.id, 'KEY ĐÃ ĐƯỢC SỬ DỤNG VUI LÒNG LÀM NHIỆM VỤ KHÁC')
      else:
        if key == d_key:
          ID = message.from_user.id
    #đặt số tiền	
          tien = int(300)
          tong = themtien(ID, tien)
          bot.send_message(message.chat.id, text = f'KEY ĐÚNG +{tien} XU | SỐ DƯ: {tong}',reply_markup=link)
          a = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={member}&text=ID: {ID}, LÀM THÀNH CÔNG NHIỆM VỤ <1SHORT> NHẬN {tien}Đ').text
          now = TimeStamp()
          f = open("key.txt","a+")
          k = f.write(f"{now}:{ID}_1short/{key}"+"\n")
          f.close()
        else:
          bot.send_message(message.chat.id, 'KEY KHÔNG ĐÚNG VUI LÒNG GỬI [NHẬP KEY 1SHORT] VÀ THỬ LẠI')
  except:
    bot.send_message(message.chat.id, text = "KEY KHÔNG ĐÚNG ĐỊNH DẠNG VUI LÒNG GỬI [NHẬP KEY 1SHORT] VÀ THỬ LẠI", reply_markup=fvip)
#WEB1S

@bot.message_handler(func=lambda message: message.text == "🕔LỊCH SỬ LÀM NV")
def handler_lsu(message):
  ID = message.from_user.id
  now = TimeStamp()
  with open("key.txt", "r") as file:
    lines = file.readlines()
  link = 0
  nvt = 0
  l = 0
  l1 = 0
  l2 = 0 
  l3 = 0 
  l4 = 0 
  l5 = 0
  l6 = 0
  l7 = 0
  for line in lines:
    if f"{ID}" in line:
        link += 1
  for line in lines:
    if f"{ID}_octolink/" in line:
        l += 1
  for line in lines:
    if f"{ID}_dilink/" in line:
        l1 += 1
  for line in lines:
    if f"{ID}_link4m/" in line:
        l2 += 1
  for line in lines:
    if f"{ID}_1short/" in line:
        l3 += 1
  for line in lines:
    if f"{now}:{ID}" in line:
        nvt += 1
  text = f'''
HÔM NAY: {TimeStamp()}
-TỔNG NHIỆM VỤ HÔM NAY ĐÃ LÀM: {nvt} LINK
-TỔNG TẤT CẢ NHIỆM VỤ ĐÃ LÀM THỜI GIAN QUA: {link} LINK

_NV OCTOLINK: ĐÃ LÀM ĐƯỢC {l} LINK

_NV DILINK: ĐÃ LÀM ĐƯỢC {l1} LINK

_NV LINK4M: ĐÃ LÀM ĐƯỢC {l2} LINK

_NV 1SHORT: ĐÃ LÀM ĐƯỢC {l3} LINK
'''
  bot.send_message(message.chat.id, text, reply_markup=lsu)

@bot.message_handler(func=lambda message: message.text == "🏠 HOME")
def handler_ql(message):
  text = "VUI LÒNG CHỌN 👇"
  bot.send_message(message.chat.id, text, reply_markup=start)
@bot.message_handler(func=lambda message:
   message.text == "📩THỂ LỆ")
def handler_tle(message):
  text = "💵 BOT KIẾM TIỀN TELEGRAM UY TÍN HÀNG ĐẦU VIỆT NAM | 📩 BOT AUTO TỰ ĐỘNG 100% | 🔑 ADMIN HỖ TRỢ 24/7 | MỌI NGƯỜI VUI LÒNG KHÔNG GIAN LẬN HOẶC BUG LINK TRONG KHI LÀM NHIỆM VỤ NẾU BỊ PHÁT HIỆN BAND TRỰC TIẾP ! CẢM ƠN 💵"
  bot.send_message(message.chat.id, text, reply_markup=tlee)
@bot.message_handler(func=lambda message:
   message.text == "🔑ADMIN")
def handler_tle(message):
  text = "GẶP LỖI HAY VẤN ĐỀ GÌ ĐÓ LH :https://t.me/cong131206"
  bot.send_message(message.chat.id, text, reply_markup=start)
@bot.message_handler(func=lambda message: message.text == "🔙TRỞ VỀ NHIỆM VỤ")
def handler_ql(message):
  ID = message.from_user.id
  now = TimeStamp()
  with open("key.txt", "r") as file:
    lines = file.readlines()
  nvt = 0
  for line in lines:
    if f"{now}:{ID}" in line:
      nvt += 1
  text = f'''
HÔM NAY: {TimeStamp()}
BẠN ĐÃ LÀM: {nvt} NHIỆM VỤ
  '''
  text += '''
VUI LÒNG CHỌN 👇
  '''
  bot.send_message(message.chat.id, text, reply_markup=link)
@bot.message_handler(func=lambda message: message.text == "💵 KIẾM TIỀN")
def handler_ktien(message):
  ID = message.from_user.id
  time = datetime.now().strftime("%H")
  if int(time) < 6:
    text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 22H"
    bot.send_message(message.chat.id, text, reply_markup=start)
    return
  if int(time) > 22:
    text = "NHIỆM VỤ MỞ TỪ 6H ĐẾN 22H"
    bot.send_message(message.chat.id, text, reply_markup=start)
    return
  now = TimeStamp()
  with open('key.txt', 'a') as file:
    file.close()
  with open("key.txt", "r") as file:
    lines = file.readlines()
  nvt = 0
  for line in lines:
    if f"{now}:{ID}" in line:
        nvt += 1
  text = f'''
HÔM NAY: {TimeStamp()}
BẠN ĐÃ LÀM: {nvt} NHIỆM VỤ
'''
  text += '''
VUI LÒNG CHỌN 👇
   '''

  bot.send_message(message.chat.id, text, reply_markup=link)
@bot.message_handler(func=lambda message: message.text == "💲RÚT TIỀN")
def handler_rut(message):
  text = "VUI LÒNG CHỌN PHƯƠNG THỨC RÚT"
  bot.send_message(message.chat.id, text, reply_markup=rut)
@bot.message_handler(func=lambda message: message.text == "🔙QUAY LẠI")
def handler_rut(message):
  text = "VUI LÒNG CHỌN PHƯƠNG THỨC RÚT"
  bot.send_message(message.chat.id, text, reply_markup=rut)
############
@bot.message_handler(func=lambda message: message.text == "🏆TOP VƯỢT LINK")
def handler_tle(message):
  text = "ĐÂY LÀ TOP VƯỢT LINK 🏆"
  bot.send_message(message.chat.id, text, reply_markup=tle)
  with open("key.txt", "r") as file:
    lines = file.readlines()
  name_counts = {}
  pattern = r"(?<=:)([^:_]+)"
  for line in lines:
    matches = re.findall(pattern, line)
    for name in matches:
        name = name.strip()
        if name not in name_counts:
            name_counts[name] = 1
        else:
            name_counts[name] += 1
  sorted_names = sorted(name_counts.items(), key=lambda x: x[1], reverse=True)

  for i in range(min(10, len(sorted_names))):
    text = f"🏆TOP{i+1} <> ID: {sorted_names[i][0]} - VƯỢT ({sorted_names[i][1]} LINK)"
    bot.send_message(message.chat.id, text, reply_markup=tle)
@bot.message_handler(func=lambda message: message.text == "🔃LOAD LẠI")
def handler_load(message):
  text = "ĐÂY LÀ TOP VƯỢT LINK 🏆"
  bot.send_message(message.chat.id, text, reply_markup=tle)
  with open("key.txt", "r") as file:
    lines = file.readlines()
  name_counts = {}
  pattern = r"(?<=:)([^:_]+)"
  for line in lines:
    matches = re.findall(pattern, line)
    for name in matches:
        name = name.strip()
        if name not in name_counts:
            name_counts[name] = 1
        else:
            name_counts[name] += 1
  sorted_names = sorted(name_counts.items(), key=lambda x: x[1], reverse=True)

  for i in range(min(10, len(sorted_names))):
    text = f"🏆TOP{i+1} <> ID: {sorted_names[i][0]} - VƯỢT ({sorted_names[i][1]} LINK)"
    bot.send_message(message.chat.id, text, reply_markup=tle)

@bot.message_handler(func=lambda message: message.text == "💳 TÀI KHOẢN")
def handler_tkhoan(message):
   ID = message.from_user.id
   tien = xemtien(ID)
   phone = checkphone(ID)
   text = f'''
- ID ACC: {ID}
- SỐ DƯ: {tien}Đ
- SĐT: {phone}
   '''
   bot.send_message(message.chat.id, text, reply_markup=ve)
@bot.message_handler(func=lambda message: message.text == "MOMO")
def handler_rut(message):
  ID = message.from_user.id
  phone = checkphone(ID)
  text = f'''
👉MIN RÚT 5000Đ👈

- THÔNG TIN TÀI KHOẢN
- SĐT MOMO: {phone}
_____________________________________
_ HÃY NHẬP SỐ TIỀN VÀ TÊN MOMO
*Mẫu: 5000 Giáp Văn Công
  '''
  bot.send_message(message.chat.id, text, reply_markup=quay)
  bot.register_next_step_handler(message,stien)
def stien(message):
  ID = message.from_user.id
  phone = checkphone(ID)
  ss = message.text
  s = message.text.split()
  if ss == "🔙QUAY LẠI":
    bot.send_message(message.chat.id, text="NHẬP PHƯƠNG THỨC RÚT TIỀN",reply_markup=rut)
  else:
    try:
      stien = int(s[0])
      if testtien(ID, stien) == False:
        bot.send_message(message.chat.id, text="SỐ DƯ KHÔNG ĐỦ HÃY LÀM THÊM NHIỆM VỤ",reply_markup=rut)
      else:
        if float(stien) < 1000:
          bot.send_message(message.chat.id, text="MIN TỐI THIỂU 1000",reply_markup=rut)
        else:
          tong = trutien(ID, stien)
          text = f'''
---TẠO PHIẾU RÚT THÀNH CÔNG ---
∆ LỆNH:[{phone} {ss}]
_SỐ DƯ CÒN: {tong}
          '''
          print(text)
          a = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={money}&text={ID}:[{phone} {ss}]').text
          bot.send_message(message.chat.id, text, reply_markup=rut)
    except:
      bot.send_message(message.chat.id, text="NHẬP SỐ TIỀN CHỈ (NHẬP SỐ) CHỌN MOMO LẠI ĐỂ RÚT",reply_markup=rut)
while True:
  try:
    bot.polling(none_stop=True)
  except Exception as e:
        time.sleep(5)
