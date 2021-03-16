def rec(text):
    number = text[0].encode('windows-1251') # переводим в Windows-1251
    number = ord(number)
    if 61 <= number <= 122:
        print('eng')
    elif 224 <= number <= 255:
        print('rus')

rec('e')