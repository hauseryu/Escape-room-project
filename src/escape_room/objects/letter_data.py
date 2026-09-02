from src.escape_room.actions import action_data 

letter_to_holmes =  "Dear Mr. Holmes, \n" + \
                    "my name is Jeffrey Archer and I want to visit you at 4 o'clock in " + \
                    "the afternoon, if this suits you.\nIs this fine for you?\n\nYours, John Malcom"
                    
choices_letter_to_holmes = [
    ("--> yes, sure. Please come at 4 o'clock.",action_data.sherlock_client_appears),
    ("--> no, sorry, no time at 4 o'clock.",action_data.game_over)
]