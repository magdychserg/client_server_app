'''2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность
кодов (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.'''
import ast


def str_to_bytes(word):
    to_bytes= eval(f"b'{word}'")
    print(f'Type: {type(to_bytes)} | Value: {to_bytes} | Lenght: {len(to_bytes)}')

str_to_bytes('class')
str_to_bytes('function')
str_to_bytes('method')

