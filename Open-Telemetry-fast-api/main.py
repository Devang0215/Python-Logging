from fastapi import FastAPI
from random import randint
import copy

app = FastAPI()

dice_roll =[[],[],[]]

@app.get('/rolldice')
async def roll_dice():
    count = 0 
    
    while count < 15:
        if count < 5:
            dice_roll[0].append(roll())
        elif count < 10 :
            dice_roll[1].append(roll())
        else:
            dice_roll[2].append(roll())

        count += 1

    result = copy.deepcopy(dice_roll)

    dice_roll[0].clear()
    dice_roll[1].clear()
    dice_roll[2].clear()    

    return {"dice_rolled":result}

def roll():
    return randint(1,6) 