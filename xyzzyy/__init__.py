#!/usr/bin/env python3

from json import loads
import re
from urllib.parse import parse_qsl, urlencode
from urllib.request import urlopen, Request

from select_menu import Menu


class Session:

    def __init__(self, site, pj):
        self.site = site
        self.pj = pj

        class Data:
            def __init__(self, session):
                self.session = session

            def __getattr__(self, name):
                match = re.fullmatch(r'([a-z]+)_([A-Za-z]+)', name)
                if match:
                    module, sAct = match.groups()

                    def _act(**kwargs):
                        return self.session.act(module, sAct, **kwargs)
                    return _act
                raise AttributeError
        self.data = Data(self)

    def act(self, module, sAct, **kwargs):
        data = loads(urlopen(Request(
            f'{self.site}/data/module/{module}/all.asp?sAct={sAct}',
            urlencode(kwargs).encode(),
            headers={'Cookie': f'pj={self.pj}'}
        )).read())
        assert data['sRet'] == 'succeeded', data
        return data


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
    menu = Menu(['Exam', 'Word train'])()
    try:
        menu = Menu(['Exam', 'Word train'])()
    except Exception:
        menu = input('\r`exam` or `word train`: ')
    if menu.strip().lower() == 'exam':
        try:
            show_all = {'是': True, '否': False}[Menu(['是', '否'], '显示所有')()]
        except Exception:
            show_all = {'': True, 'y': True, 'n': False}[input('\r显示所有（Y/n）：').strip().lower()]
        for exam in s.data.homework_GetHomeworkListByStudent(
            iIsExam=1, iPageCount=s.data.homework_GetHomeworkListByStudent(iIsExam=1)['iCount']
        )['aHomework']:
            if show_all or not exam['sTimeFlag'] and not int(exam['iFinished']):
                examContent = s.data.exam_GetExamContent(iExamId=exam['sQuestionIds'])
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
                expScore += int(
                    s.data.word_AddWordTrainDetails(
                        iUnit=unit, iTrainId=s.data.word_BeginWordTrain(
                            sSubmodule='train', sTrainMode='batch', iTrainType='2', iUnit=unit, sSummary='%00'
                        )['iTrainId'],
                        sSerialIds='0', sAnswers='%00', sSolutions='%00', sIsPasses='1', sScores='100'
                    )['iExpScore']
                )
                print('\r' + str(expScore), end='', flush=True)
        except KeyboardInterrupt:
            print()
