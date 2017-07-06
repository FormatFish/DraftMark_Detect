#coding=utf-8


def check_words(words):
    num = words.strip().split()
    number = 0
    cnt = 0
    for item in num[::-1]:
        
        if not item.isdigit() and item != 'M' and item != 'm':
            if item == 'I':
                number += 1*(10**cnt)
            elif item == 'B':
                number += 8*(10**cnt)
        elif item == 'M' or item == 'm':
            continue
        else:
            number += int(item) * (10**cnt)
            cnt += 1

    return number
