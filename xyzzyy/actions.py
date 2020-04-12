def word_train(s, unit):
    return s.data.word_AddWordTrainDetails(
        iUnit=unit, iTrainId=s.data.word_BeginWordTrain(
            sSubmodule='train', sTrainMode='batch', iTrainType='2', iUnit=unit, sSummary='%00'
        )['iTrainId'],
        sSerialIds='0', sAnswers='%00', sSolutions='%00', sIsPasses='1', sScores='100'
    )
