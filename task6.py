'''6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет»,
 «декоратор». Далее забыть о том, что мы сами только что создали этот файл и исходить из того, что перед нами
 файл в неизвестной кодировке. Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке
 он был создан.'''

import chardet

words = ['сетевое программирование', 'сокет', 'декоратор']

with open('file.txt', 'w') as f:
    for word in words:
        f.write(f'{word}\n')

file = open('file.txt', 'rb').read()
coding_file = chardet.detect(file)['encoding']
print(f"File encoding: {coding_file}\n")

file_utf8 = file.decode(coding_file).encode('utf-8').decode('utf-8', 'replace')

print("File contents:")
file_data = file_utf8.split('\n')
for line in file_data:
    print(line)
