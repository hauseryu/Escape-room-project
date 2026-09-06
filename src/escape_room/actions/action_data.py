from src.escape_room.actions import action
from src.escape_room.objects import speech_data

# specific action sequences
sherlock_client_talk = [
    [action.figure_talks,"Mortimer Jackson",speech_data.story_mortimer_jackson, 0, 0],
    # [action.process_entry]
]

sherlock_client_appears = [
    [action.time_elapse,3], # 3 hours to pass until client comes
    [action.figure_appears,"Mortimer Jackson","sherlock_client.png",
        880,660,160,300,sherlock_client_talk] # client of Sherlock! x + y coordinates, width, height
]

game_over = [
    [action.game_over]
]