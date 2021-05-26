'''
This is heavily inspired by https://github.com/rtkdannable/dorian/blob/master/dorian.py
'''
import discord

COL_CRIT_SUCCESS=0xFFFFFF
COL_EXTR_SUCCESS=0xf1c40f
COL_HARD_SUCCESS=0x2ecc71
COL_NORM_SUCCESS=0x2e71cc
COL_NORM_FAILURE=0xe74c3c
COL_CRIT_FAILURE=0x992d22

def roll(user, skill, value, bonus, penalty, advancement):
    return discord.embed(COL_NORM_SUCCESS, 'Success!', 'Roll PH')

