from src.escape_room.actions import action
from src.escape_room.objects import speech_data

# specific action sequences
sherlock_client_talk = [
    [action.figure_talks,"Mortimer Jackson",speech_data.story_mortimer_jackson, 0, 0],
    # [action.process_entry]
]

sherlock_client_appears = [
    [action.time_elapse,3,"clock_tick.wav"], # 3 hours to pass until client comes, w/ sound
    [action.figure_appears,"Mortimer Jackson","sherlock_client.png",
        880,660,160,300,sherlock_client_talk] # client of Sherlock! x + y coordinates, width, height
]

sherlock_client_disappears = [
    [action.time_elapse,1], # 1 hour to pass until client disappears
    [action.figure_disappears,"Mortimer Jackson"], # client of Sherlock! 
    [action.time_elapse,5,"clock_tick.wav"], # 5 hours to pass until postman arrives
    [action.play_sound,"bell.wav"]
]

postman_appears = [
    [action.time_elapse,1], # 1 hours to pass until postman comes
    [action.figure_appears,"Postman","postman.png",
            115,605,240,480,sherlock_client_talk], # client of Sherlock! x + y coordinates, width, height
    [action.play_sound,"man_saying_hello.wav"],
    [action.letter_appears,"letter2"],    
]

game_over = [
    [action.game_over]
]

# action sequences including check actions that return a value
check_postman_in_room = [
    [action.check_figure_in_room,"Postman"]
]