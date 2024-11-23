def cls_over(row, overbuy:int|float=75, oversold:int|float=25) -> int:
    if row > overbuy: return 1
    elif row < oversold: return -1
    else: return 0