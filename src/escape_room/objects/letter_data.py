from src.escape_room.actions import action_data 

letter_to_holmes =  "Dear Mr. Holmes, \n" + \
                    "my name is Mortimer Jackson and there is an issue I would like to get your advice on. \nI want to visit you at 4 o'clock in " + \
                    "the afternoon, if this suits you.\nIs this fine for you?\n\nYours, Mortimer Jackson"
                    
choices_letter_to_holmes = [
    ("--> yes, sure. Please come at 4 o'clock.",action_data.sherlock_client_appears),
    ("--> no, sorry, no time at 4 o'clock.",action_data.game_over)
]

letter_from_moriarty = "Dear Mr. Holmes, \n" + \
                       "this is Moriarty speaking.\n" + \
                       "I have deposited a special item in your house.\n" + \
                       "If you don't find it in 1 hour, the police will arrest you thereafter for robbery....\n" + \
                       "Your fiend, Moriarty"