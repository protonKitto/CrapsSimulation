# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 10:40:56 2020

@author: DrJ

This is a craps game simulation. 
There is no system for beating Craps.  Playing odds is a way to
minimize the house advantage.

This simulation is set up with two banks:
    1. bankPlay -- the number of bet units available for play.  
       Initial value is how much one brings to the game
    2. bankSave -- the net result of playing through bankPlay.
       This starts at 0 and at the end is the accumulated 
       winnings.  
    3. Games start with 1 unit bet on pass line.
    4. if a point is established, make an odds bet, and 
         continue play until bet is resolved. 
         
3-point Molly assumes a point is established, then a 1 unit
bet is made on the 'come,' taking odds. Continue to bet on
the come until three points are in play. Once 3 points
(including the pass line bet) are in play, no further come 
bets are made until either a point is made and paid, then a 1 
unit come bet is again made so that 3 points are covered, OR
7 is rolled and bets are resolved. When a 7 is rolled, bets
are resolved and the game begins with a 1 unit bet on the pass
line and proceeds as indicated above. 

This simulation is set up to illustrate how odds work.  One
pass bet is made and followed through until a win/loss. 

Simulation assumes a 1-unit bet on the pass line for each play
    
Here's how it works: 
Begin with 'bankPlay' units.  Play through bankPlay, then stop.
That is, every play you either win orlose. If you lose, bets 
go to the house; if you win, total winnings go to 'bankSave.'  
Continue play until you have exhausted the bankPlay, then
see how you did by looking at units in bankSave
 
This simulation assumes 3,4,5 odds.  That is if the point is:
 
 4 or 10: bettor can play 3x the pass bet 'behind the line' for 
 an odds bet. Odds on 4 or 10 pay 2:1.  This is because there
 are 6 ways to get a 7 (craps out) and 3 ways to get a 4 or a 9.
 6:3 is 2:1 odds 
 
 In odds bets the house has no advantage.
 
 5 or 9: bettor can play 4 times the pass bet 'behind the
 line' for an odds bet.  Odds on 5 or 9 are 3:2 because there 
 are 4 ways to get either a 5 or a 9 
 6:4 is 3:2 payout
 
 6 or 8: bettor can play 5 times the pass bet 'behind the 
 line' for an odds bet.  Odds on 6 or 8 pay 6:5 because
 there are 5 ways to get a 6 or an 8
 
Some Casinos ($10 min bet) play 1x odds, that is bettor
 may play only the amount of the pass line bet 'behind
 the line'  The odds are handled the same way.
 In that case if the point is 4,or 10 and 4 or
 10 is thrown before a 7, bettor wins 1:1 on pass line bet 
 and 2:1 on the odds bet.  If the point is 5 or 9 and the 
 point is made, the bettor is paid 1:1 for the pass line
 bet, and 3:2 on the odds bet. If the point is 6 or 8 and 
 the point is made, the bettor is paid 1:1 for the pass
 line bet and 12:10 on the odds bet.
 
 In summary:
 When you put odds behind pass line, you???re ???taking??? odds.

2:1 payout on point numbers of 4 and 10 
3:2 on points of 5 and 9 
6:5 on points of 6 and 8

If you play the don't pass line, you can also play odds
When you put odds behind don???t pass line, you???re ???laying??? odds.
Here are the payouts for laying odds.

That is if the 
 point is:
 
 4 or 10: bettor can play 6x don't pass bet 'behind the line' for 
 an odds bet. Odds on 4 or 10 pay 1:2. Payoff is 1:2 that is,
 payoff is 3 for 6 bet units if the shooter does not pass.  
 
 5 or 9: bettor can play 6x times the don't pass bet 'behind the
 line' for an odds bet.  If the shooter does not pass, payoff
 is 2:3. Payoff is 4 for 6 bet units
 
 6 or 8: bettor can play 6x times the don't pass bet 'behind the 
 line' for an odds bet.  Odds on 6 or 8 pay If the shooter does 
 not pass pay off is 5:6.  Payoff is 5 for 6

1:2 payout for point numbers of 4 and 10
2:3 for points of 5 and 9 
5:6 for points of 6 and 8
 
 3-point Molly:
     1. make a pass/don't pass bet
     2. if pass/don't pass wins/loses, update banks,
        go to step 1
     3. if point, play odds behind the bet. If there are
        fewer than 3 points in play, make a Come or Don't Come
        bet, take/lay odds.
     4. if Come/Don't Come bet wins/loses, update the banks
        go to step 3
     5. if new point, dealer moves Come/Don't Come bet to
           number, play odds, go to step 2.
     6. When 3 numbers are in play no more Come/Don't Come bets
     7. As a point is resolved, make a Pass/Come  or 
        Don't Pass/Don't Come bet to keep 3 numbers in play
 
This simulation is set for one run through your 'play Bank'
It does single bet, not the 3-point Molly.
"""

import numpy as np
import random
from sys import exit
import matplotlib.pyplot as plt
from math import floor, ceil

def rollDice():
    d1 = random.randint(1,6)
    d2 = random.randint(1,6)
    return (d1,d2)


# start a game
#  first roll: 7,11 => win
#              2,3,12 = lose
#              4,5,6,8,9,10 => 'point'

def FirstRoll():
    d1, d2 = rollDice()
    
    sumDice = d1+d2
    
    if (sumDice in [7,11]):
        return('natural')
    if (sumDice in [2,3,12] ):
        return 'loser'
    return sumDice


# if no win/loss on first roll, point is set
# bank is how much $$ you have, totalWagered is 
# $$ at risk on the table 

# function play assumes first roll was not 7, 11 (win)
#  or 2,3,12 (loss). The puck goes on the point
    
def play(point, oddsWager):
    '''
       point is the point (4,5,6,8,9,or 10)
       totalWagered is $$ at risk on the table
    '''

# roll the dice until either a 7 comes up (lose), or 
#  the point comes up (win)     
   
    while (True):
        d1,d2=rollDice()
        sumDice = d1+d2
        moveFROMbankPlay = 0
        moveTObankSave = 0
        
        if sumDice == 7:
#           7 comes up, all $$ on the table goes to the house
               moveFROMbankPlay = oddsWager
               return (moveFROMbankPlay, moveTObankSave)
                       
        if sumDice == point:
#           point comes up pay the winner
                win = 1  # passline  bet
                win += 6 # odds payoff based on 3,4,5x
                # 1 is from pass line
                moveTObankSave = win + 1 + oddsWager
                moveFROMbankPlay = oddsWager
                return(moveFROMbankPlay,moveTObankSave) 
          

# simulate the craps game
# start with a bank (say 150), and play until
# bankPlay is exhausted.  Save the result of each play
# and get the final amount in bankSave

profitSave = []
nSims = 5000
for gameNumber in range(nSims):
    
#    print('gameNumber: {}'.format(gameNumber))

    startBank = 150  # units to start 
    bankPlay = startBank  # play until exhausted
    bankSave = 0 # what you keep


    while (bankPlay>5):  # play until bank exhausted        
        bankPlay -= 1  # pass line bet comes out of bankPlay
#        print('bankPlay: {}'.format(bankPlay)) 
        
        moveFROMbankPlay=0
        moveTObankSave=0
    
        while (True):  # roll until game resolved
       
            result = FirstRoll()    
        
            if result == 'natural':
                print('natural')
                win = 1 # pass pays 1:1
                moveTObankSave = 2
                moveFROMbankPlay=0
                bankSave += moveTObankSave
                break

            if result == 'loser':
                print('craps')
                moveTObankSave = 0
                moveFROMbankPlay = 0 #lost pass line
                break
    
            if result in [4,5,6,8,9,10]:
                point = result
                print('point: {}\n'.format(point))
                if (point == 4 or point == 10): oddsWager = 3
                if (point == 5 or point == 9): oddsWager = 4
                if (point == 6 or point == 8): oddsWager = 5
            
                (moveFROMbankPlay, moveTObankSave) = \
                play(point, oddsWager)
#                print('moveFROMbankPlay {}, moveTObankSave {}\n'.\
#                      format(moveFROMbankPlay, moveTObankSave))
                
                bankSave += moveTObankSave
                bankPlay -= moveFROMbankPlay
                break
#        print('end')
#        print(bankSave)
    profitSave.append(bankSave-startBank)
        
#print(profitSave)
plt.hist(profitSave)
plt.grid()
expectedReturn = round(np.mean(profitSave),2)
print('expected value: {}'.format(expectedReturn))
plt.axvline(expectedReturn, color='r', ls='--')

print('house edge: {}%'.\
      format(round((-expectedReturn)/startBank*100,2)))
sortProfit = np.sort(profitSave)
    
print('95% CI: (${} , ${})'.format(sortProfit[floor(0.025*nSims)],\
                   sortProfit[ceil(0.975*nSims)] ))

            