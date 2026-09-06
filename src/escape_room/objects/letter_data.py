from src.escape_room.actions import action_data 

letter_to_holmes =  "Dear Mr. Holmes, \n" + \
                    "my name is Mortimer Jackson and there is an issue I would like to get your advice on. \nI want to visit you at 4 o'clock in " + \
                    "the afternoon, if this suits you.\nIs this fine for you?\n\nYours, Mortimer Jackson"
                    
choices_letter_to_holmes = [
    ("--> yes, sure. Please come at 4 o'clock.",action_data.sherlock_client_appears),
    ("--> no, sorry, no time at 4 o'clock.",action_data.game_over)
]