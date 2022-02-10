### 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и
# проверить тип и содержание соответствующих переменных.
# Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
# и также проверить тип и содержимое переменных.

words = ('разработка', 'сокет', 'декоратор')
words_u = ('\u0440\u0430\u0437\u0440\u0430\u0431\u043E\u0442\u043A\u0430',
           '\u0441\u043E\u043A\u0435\u0442',
           '\u0434\u0435\u043A\u043E\u0440\u0430\u0442\u043E\u0440')

print('\n### Task 1 ###')
print(*((item,type(item)) for item in words))
print(*((item,type(item)) for item in words_u))

### 2.Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования
# в последовательность кодов (не используя методы encode и decode) и определить тип,
# содержимое и длину соответствующих переменных.

words_b = (b'class', b'function', b'method')

print('\n### Task 2 ###')
print('task2', *((item, type(item), len(item)) for item in words_b))


### 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

words = ('attribute','класс','функция','type')

isascii = lambda s: len(s) == len(s.encode())

print('\n### Task 3 ###')
for word in words:
    if isascii(word):
        print(f'The word "{word}" can be written in bytes')
    else:
        print(f'The word "{word}" cannot be written in bytes')

### 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового
# представления в байтовое и выполнить обратное преобразование (используя методы encode и decode).

words = ('разработка', 'администрирование', 'protocol', 'standard')
words_enc = [s.encode('utf-8') for s in words]
words_dec = [bw.decode('utf-8') for bw in words_enc]

print('\n### Task 4 ###')
print('words:', words, '\nwords encoded:', words_enc, '\nwords decoded:', words_dec)

### 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в
# строковый тип на кириллице.
import locale
import subprocess

print('\n### Task 5 ###')
print(locale.getpreferredencoding())

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

print(results)

### 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет»,
# «декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и
# вывести его содержимое. Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке он был создан.

import chardet

print('\n### task6 ###')
print('Default encoding: ', locale.getpreferredencoding())

lines = ['сетевое программирование\n', 'сокет\n', 'декоратор\n']
path = 'lesson_1/test_file.txt'

with open  (path, encoding='windows-1251', mode='w') as f:
    f.writelines(lines)
    print('File test_file.txt was created with windows-1251 encoding')

with open(path, 'rb') as f:
    text = f.read()
    encoding = chardet.detect(text)['encoding']
    print(text.decode(encoding))

