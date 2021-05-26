'''
This is heavily inspired by https://github.com/rtkdannable/dorian/blob/master/dorian.py
'''
import discord

from random import randint

COL_CRIT_SUCCESS=0xFFFFFF
COL_EXTR_SUCCESS=0xf1c40f
COL_HARD_SUCCESS=0x2ecc71
COL_NORM_SUCCESS=0x2e71cc
COL_NORM_FAILURE=0xe74c3c
COL_CRIT_FAILURE=0x992d22

def RollDie(min=1, max=10):
    result = randint(min,max)
    return result

def ResolveDice(BonusDie, PenaltyDie, Threshold):
  TenResultPool = []
  TenResultPool.append(RollDie(0, 9))

  TenResult = min(TenResultPool)
  OneResult = RollDie()

  if BonusDie > 0 and PenaltyDie > 0:
      return "Can't chain bonus and penalty dice"

  for i in range(BonusDie):
      TenResultPool.append(RollDie(0, 9))
      TenResult = min(TenResultPool)
  
  for i in range(PenaltyDie):
      TenResultPool.append(RollDie(0, 9))
      TenResult = max(TenResultPool)

  CombinedResult = (TenResult*10) + OneResult
  desc = str(TenResult*10) + '(' + '/'.join([str(i*10) for i in TenResultPool]) + ') + ' + str(OneResult) + ' = ' + str(CombinedResult)

  if Threshold:
    ret = DiceResult()
    if CombinedResult == 1:
      ret.title = "Critical Success!"
      ret.colour = COL_CRIT_SUCCESS
    elif CombinedResult == 100:
      ret.title = "Critical Failure!"
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
  else:
    ret = desc
    return ret

def roll(user, skill, value, bonus, penalty, advancement):
    return discord.embed(COL_NORM_SUCCESS, 'Success!', 'Roll PH')

def main():
    r = roll('user1', 'skill1', 5, True, False, True)
    print(r)

if __name__ == '__main__':
    main()
