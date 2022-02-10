### 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и
# проверить тип и содержание соответствующих переменных.
# Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
# и также проверить тип и содержимое переменных.

words = ('разработка', 'сокет', 'декоратор')
words_u = ('\u0440\u0430\u0437\u0440\u0430\u0431\u043E\u0442\u043A\u0430',
           '\u0441\u043E\u043A\u0435\u0442',
           '\u0434\u0435\u043A\u043E\u0440\u0430\u0442\u043E\u0440')

print('task1', *((item,type(item)) for item in words))
print('task1', *((item,type(item)) for item in words_u))

### 2.Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования
# в последовательность кодов (не используя методы encode и decode) и определить тип,
# содержимое и длину соответствующих переменных.

words_b = (b'class', b'function', b'method')
print('task2', *((item, type(item), len(item)) for item in words_b))


### 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

w1 = b'attribute'
# w2 = b'класс'
## SyntaxError: bytes can only contain ASCII literal characters.
# w3 = b'функция'
## SyntaxError: bytes can only contain ASCII literal characters.
w4 = b'type'

### 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового
# представления в байтовое и выполнить обратное преобразование (используя методы encode и decode).

words = ('разработка', 'администрирование', 'protocol', 'standard')
words_enc = [s.encode('utf-8') for s in words]
words_dec = [bw.decode('utf-8') for bw in words_enc]

print('task4 - words:', words, '\ntask4 - words encoded:', words_enc, '\ntask4 - words decoded:', words_dec)

### 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в
# строковый тип на кириллице.
import locale
import subprocess

print('task5:', locale.getpreferredencoding())

results = ''

args = ['ping', '-c 1', 'ya.ru']
ping_exec = subprocess.Popen(args, stdout=subprocess.PIPE)

for line in ping_exec.stdout:
    results += line.decode('utf-8')

man_cmd = ['env', 'LANG=ru_RU.UTF-8', 'man', 'man']
head_cmd = ['head', '-n 1']
man_exec = subprocess.Popen(man_cmd, stdout=subprocess.PIPE)
head_exec = subprocess.Popen(head_cmd, stdin=man_exec.stdout, stdout=subprocess.PIPE)

for line in head_exec.stdout:
    results += line.decode('utf-8')

print('task5', results)

### 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет»,
# «декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и
# вывести его содержимое.

import chardet

#
print('task6', locale.getpreferredencoding())

#
# # UTF-8
#
lines = ['сетевое программирование\n', 'сокет\n', 'декоратор\n']
with open  ('lesson_1/test_file.txt', 'w') as f:
    f.writelines(lines)

with open('lesson_1/test_file.txt', 'rb') as f:
    s = f.read()
    print(s)
    print(chardet.detect(s))

# b'\xd1\x81\xd0\xb5\xd1\x82\xd0\xb5\xd0\xb2\xd0\xbe\xd0\xb5 \xd0\xbf\xd1\x80\xd0\xbe\xd0\xb3\xd1\x80\xd0\xb0\xd0\xbc\xd0\xbc\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5\n\xd1\x81\xd0\xbe\xd0\xba\xd0\xb5\xd1\x82\n\xd0\xb4\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80\n'
# {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}

with open('lesson_1/test_file.txt', encoding='windows-1251', errors='replace') as f:
    print(f.read())

# СЃРµС‚РµРІРѕРµ РїСЂРѕРіСЂР°РјРјРёСЂРѕРІР°РЅРёРµ
# СЃРѕРєРµС‚
# РґРµРєРѕСЂР°С‚РѕСЂ
