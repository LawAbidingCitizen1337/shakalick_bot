#for linux
#run programm whit root rights


import telebot
from datetime import datetime
from os import getcwd
from os import chdir
from os import mkdir
from random import randint
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


path = getcwd()
try:
    mkdir(path + '/database')
except Exception:
    pass


token = '<Your Token>'
lenght_simvol = 20#(in pixels)interconnected
size_font = 45#interconnected

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_message(message.chat.id, 'Привет, я Шакалик Бот! Отправьте мне фото, чтобы я добавил смешнявую подпись;)')


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.send_message(message.chat.id, 'Я бот Шакалик, отправьте мне фото, чтобы я добавил смешнявую подпись;)')

@bot.message_handler(content_types=['text'])
def command_help(message):
    bot.send_message(message.chat.id, 'Я бот Шакалик, отправьте мне фото, чтобы я добавил смешнявую подпись;)')


@bot.message_handler(content_types=['photo'])
def processing_photo(message):
    idphoto = message.photo[-1].file_id
    user_id = str(message.from_user.id)
    file_info = bot.get_file(idphoto)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = downloads_photo_in_database(user_id, downloaded_file)
    img = Image.open(path+'/database/'+file_name)
    (width, height) = img.size
    img.close()
    line_signature = split_signature(width, random_signature())
    photo_edit(line_signature, width, height, file_name)
    photo = open(path+'/database/'+file_name, 'rb')
    bot.send_photo(message.chat.id, photo)


#return date time in format YYYY-MM-DD_HH-mm-ss(str)
def all_time_now():
    day_now = datetime.now().isoformat(sep='_', timespec='seconds')
    date_time = ''
    for a in day_now:
        if a == ':':
            a = "-"
        date_time += a
    return date_time


#return file name in format YYYY-MM-DD_HH-mm-ss_<user_id>.jpg(str)
def post_file_name(id):
    file_name = all_time_now() + '_' + id + '.jpg'
    return file_name


#downlad file and return him name(str)
def downloads_photo_in_database(id, file):
    chdir(path + '/database')
    file_name = post_file_name(id)
    with open(file_name, 'wb') as new_file:
        new_file.write(file)
    chdir(path)
    return file_name


#random sugnature
def random_signature():
    with open('signatures.txt', 'r') as sign_up:
        str_sign = sign_up.read()
        list_sign = str_sign.split('\n')
    return list_sign[randint(0, len(list_sign)-1)]


#separates the caption into lines according to the width of the image
#return list lines(str)
def split_signature(width, signature):
    split_signature = signature.split(' ')
    lenght_line_pix = width - (2 * lenght_simvol)
    lenght_line_simvol = int(lenght_line_pix / lenght_simvol)
    list = ['']
    list_result = []
    for a in split_signature:
        if (len(list[0])+1) < lenght_line_simvol and \
                ((len(list[0])+1) + len(a)) < lenght_line_simvol:
            list[0] += (a + ' ')
        else:
            list_result.append(list.pop(0))
            list.append('')
            list[0] = (a + ' ')
        if a == split_signature[-1]:
            list_result.append(list[0])
    return list_result

#edit image
#adjusts the height according to the image of the lines
def photo_edit(list, width, height, file_name):

    img = Image.open(path+'/database/'+file_name)
    I1 = ImageDraw.Draw(img)
    myfont = ImageFont.truetype('Lobster-Regular.ttf',size_font)
    height -=len (list)*3*lenght_simvol
    ImageDraw.Draw(img)

    for a in list:
        pix_lenght = len(a) * 20
        start = (width-pix_lenght)/2
        I1.text((start, height), a, font=myfont, fill=(1000, 1000, 1000))
        height += 3 * lenght_simvol
        img.save(path + '/database/' + file_name)


if __name__ == '__main__':
    bot.polling(non_stop=True, timeout=999999, none_stop=True)