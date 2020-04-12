#!/usr/bin/env python3

from urllib.parse import parse_qsl, urlencode

from xyzzyy.actions import exam, word_train
from xyzzyy.select_menu import Menu
from xyzzyy.session import Session


if __name__ == "__main__":
    s = Session(
        input('站点（http://114.118.97.15）：') or 'http://114.118.97.15',
        f"iUserId=0&iGroupId=300&sDatabase={input('数据库（site_20180305000000）：') or 'site%5F20180305000000'}"
    )
    name = input('姓名：')
    for student in s.data.school_GetStudentList()['aUser']:
        if student['sName'] == name:
            pj = dict(parse_qsl(s.pj))
            pj['iUserId'] = student['iUserId']
            s.pj = urlencode(pj)
            break
    else:
        raise ValueError
    try:
        menu = Menu(['Exam', 'Word train'])()
    except Exception:
        menu = input('\r`exam` or `word train`: ')
    if menu.strip().lower() == 'exam':
        try:
            show_all = {'是': True, '否': False}[Menu(['是', '否'], '显示所有')()]
        except Exception:
            show_all = {'': True, 'y': True, 'n': False}[input('\r显示所有（Y/n）：').strip().lower()]
        for examContent in exam(s, show_all):
            for content in examContent['aContent']:
                print(content['sTitle'])
            for process in examContent['aProcess']:
                print('', process['iOrder'], process['sAnswer'], sep='\t')
            print()
    elif menu.strip().lower() == 'word train':
        unit = input('单元: ')
        try:
            expScore = 0
            while True:
                expScore += int(word_train(s, unit)['iExpScore'])
                print('\r' + str(expScore), end='', flush=True)
        except KeyboardInterrupt:
            print()
