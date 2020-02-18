#!/usr/bin/env python3
  
from json import loads
from urllib.request import urlopen, Request


COOKIE = 'pj=' + input('pj=')
UNIT = input('Unit: ')

try:
    expScore = 0
    while True:
        # wordTrainUnfinished = loads(urlopen(Request('http://114.118.97.15/data/module/word/all.asp', b'sAct=GetWordTrainUnfinished&sTrainFrom=train', headers={'Cookie': COOKIE})).read())
        # assert wordTrainUnfinished['sRet'] == 'succeeded', wordTrainUnfinished
        # if wordTrainUnfinished['iTrainId']:
        #     assert loads(urlopen(Request('http://114.118.97.15/data/module/word/all.asp?sAct=DelWordTrain', ('iTrainId=' + wordTrainUnfinished['iTrainId']).encode(), headers={'Cookie': COOKIE})).read())['sRet'] == 'succeeded'
        wordTrain = loads(urlopen(Request('http://114.118.97.15/data/module/word/all.asp?sAct=BeginWordTrain', ('sSubmodule=train&sTrainMode=batch&iTrainType=2&sSummary=%20&iUnit=' + UNIT).encode(), headers={'Cookie': COOKIE})).read())
        assert wordTrain['sRet'] == 'succeeded', wordTrain
        wordContent = loads(urlopen(Request('http://114.118.97.15/data/module/word/all.asp?sAct=GetWordContent', ('iUnitId=' + UNIT).encode(), headers={'Cookie': COOKIE})).read())
        assert wordContent['sRet'] == 'succeeded', wordContent
        wordTrainDetails = loads(urlopen(Request('http://114.118.97.15/data/module/word/all.asp?sAct=AddWordTrainDetails', ('iTrainId=' + wordTrain['iTrainId'] + '&iUnit=' + UNIT + '&sSerialIds=' + '%0D%0A%09+%09%0D%0A'.join([str(i) for i in range(len(wordContent['aWord']))]) + '&sAnswers=' + '%0D%0A%09+%09%0D%0A' * (len(wordContent['aWord']) - 1) + '&sSolutions=' + '%0D%0A%09+%09%0D%0A' * (len(wordContent['aWord']) - 1) + '&sIsPasses=' + '%0D%0A%09+%09%0D%0A'.join(['1'] * len(wordContent['aWord'])) + '&sScores=' + '%0D%0A%09+%09%0D%0A'.join(['100'] * len(wordContent['aWord']))).encode(), headers={'Cookie': COOKIE})).read())
        assert wordTrainDetails['sRet'] == 'succeeded', wordTrainDetails
        expScore += int(wordTrainDetails['iExpScore'])
        print('\r' + str(expScore), end='', flush=True)
except KeyboardInterrupt:
    print()
