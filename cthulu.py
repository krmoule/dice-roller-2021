'''
This is heavily inspired/copied from https://github.com/rtkdannable/dorian/blob/master/dorian.py
'''
from random import randint

import discord
import sheets

COL_CRIT_SUCCESS=0xFFFFFF
COL_EXTR_SUCCESS=0xf1c40f
COL_HARD_SUCCESS=0x2ecc71
COL_NORM_SUCCESS=0x2e71cc
COL_NORM_FAILURE=0xe74c3c
COL_CRIT_FAILURE=0x992d22

class DiceResult:
    def __init__(self):
        self.title=""
        self.desc=""
        self.colour=COL_NORM_SUCCESS

def RollDie(min=1, max=10):
    result = randint(min,max)
    return result

def ResolveDice(BonusDie, PenaltyDie, Threshold):
    TenResultPool = []
    TenResultPool.append(RollDie(0, 9))

    TenResult = min(TenResultPool)
    OneResult = RollDie(0, 9)

    for _ in range(BonusDie):
        TenResultPool.append(RollDie(0, 9))
        TenResult = min(TenResultPool)
  
    for _ in range(PenaltyDie):
        TenResultPool.append(RollDie(0, 9))
        TenResult = max(TenResultPool)

    CombinedResult = (TenResult*10) + OneResult
    if CombinedResult == 0:
        CombinedResult = 100
    desc = str(TenResult*10) + '(' + '/'.join([str(i*10) for i in TenResultPool]) + ') + ' + str(OneResult) + ' = ' + str(CombinedResult)

    ret = DiceResult()
    if CombinedResult == 1:
        ret.title = "Critical Success!"
        ret.colour = COL_CRIT_SUCCESS
    elif CombinedResult == 100:
        ret.title = "Fumble!"
        ret.colour = COL_CRIT_FAILURE
    elif Threshold < 50 and CombinedResult > 95:
        ret.title = "Fumble!"
        ret.colour = COL_CRIT_FAILURE
    elif CombinedResult <= Threshold/5:
        ret.title = "Extreme Success!"
        ret.colour = COL_EXTR_SUCCESS
    elif CombinedResult <= Threshold/2:
        ret.title = "Hard Success!"
        ret.colour = COL_HARD_SUCCESS
    elif CombinedResult <= Threshold:
        ret.title = "Success"
        ret.colour = COL_NORM_SUCCESS
    else:
        ret.title = "Failure"
        ret.colour = COL_NORM_FAILURE

    ret.desc = desc
    return ret

def roll(value, bonus, penalty, advancement):
    if advancement:
        return discord.embed(0xff0000, 'Oops!', 'Come back next week, maybe this will work ¯\_(ツ)_/¯.')

    if bonus and penalty:
        bonus = False
        penalty = False

    BonusDie = 1 if bonus else 0
    PenaltyDie = 1 if penalty else 0
    result = ResolveDice(BonusDie, PenaltyDie, value.threshold)
    desc = f'{value.character} rolls {value.skill} -- {result.desc} against {value.threshold}%'
    return discord.embed(result.colour, result.title, desc)

def main():
    print(roll(sheets.Value('character1', 'skill1', 5), True, False, True))
    print(roll(sheets.Value('character1', 'skill2', 10), True, False, False))
    print(roll(sheets.Value('character2', 'skill3', 47), False, True, False))
    print(roll(sheets.Value('character3', 'skill4', 90), True, True, False))

if __name__ == '__main__':
    main()
