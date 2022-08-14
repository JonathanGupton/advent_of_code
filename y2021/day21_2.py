import sys
from functools import cache


@cache
def play_dice(
    p1_position,
    p2_position,
    dice_roll_n=0,
    dice_sum=0,
    p1_score=0,
    p2_score=0,
    next_player=1,
    winning_score=21,
    board_size=10,
):
    p1_wins = 0
    p2_wins = 0
    if next_player == 1:
        if dice_roll_n < 3:
            for i in range(1, 4):
                next_dice_sum = dice_sum + i
                next_dice_roll_n = dice_roll_n + 1
                wins = play_dice(
                    p1_position,
                    p2_position,
                    next_dice_roll_n,
                    next_dice_sum,
                    p1_score,
                    p2_score,
                    next_player,
                )
                p1_wins += wins[0]
                p2_wins += wins[1]
        else:
            dice_roll_n = 0
            next_p1_position = p1_position + dice_sum
            if next_p1_position > board_size:
                next_p1_position %= board_size
                if next_p1_position == 0:
                    next_p1_position = board_size
            next_p1_score = p1_score + next_p1_position
            if next_p1_score >= winning_score:
                p1_wins += 1
            else:
                wins = play_dice(
                    next_p1_position,
                    p2_position,
                    dice_roll_n,
                    dice_sum=0,
                    p1_score=next_p1_score,
                    p2_score=p2_score,
                    next_player=2,
                )
                p1_wins += wins[0]
                p2_wins += wins[1]

    if next_player == 2:
        if dice_roll_n < 3:
            for i in range(1, 4):
                next_dice_sum = dice_sum + i
                next_dice_roll_n = dice_roll_n + 1
                wins = play_dice(
                    p1_position,
                    p2_position,
                    next_dice_roll_n,
                    next_dice_sum,
                    p1_score,
                    p2_score,
                    next_player,
                )
                p1_wins += wins[0]
                p2_wins += wins[1]
        else:
            dice_roll_n = 0
            next_p2_position = p2_position + dice_sum
            if next_p2_position > board_size:
                next_p2_position %= board_size
                if next_p2_position == 0:
                    next_p2_position = board_size
            next_p2_score = p2_score + next_p2_position
            if next_p2_score >= winning_score:
                p2_wins += 1
            else:
                wins = play_dice(
                    p1_position,
                    next_p2_position,
                    dice_roll_n,
                    dice_sum=0,
                    p1_score=p1_score,
                    p2_score=next_p2_score,
                    next_player=1,
                )
                p1_wins += wins[0]
                p2_wins += wins[1]

    return p1_wins, p2_wins


p1_pos = 4
p2_pos = 8
p1_wins, p2_wins = play_dice(p1_pos, p2_pos)
print(max(p1_wins, p2_wins))