from src.escape_room.actions import action

# specific action sequences
sherlock_client_appears = [
    [action.time_elapse,3], # 3 hours to pass until client comes
    [action.figure_appears,"Mortimer Jackson","sherlock_client.png",
        880,660,160,300] # client of Sherlock! x + y coordinates, width, height
]

game_over = [
    [action.game_over]
]