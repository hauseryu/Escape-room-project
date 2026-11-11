story_mortimer_jackson = { 
                    'text': f"""
                    Mr. Holmes! Please help me!
                    I got a threatening letter and I don't know what to do!
                    Who knows what will happen to me! What should I...! I don't know...!
                    """,
                    'name': 'story_mortimer_jackson',
                    'story_index': 0
}

story_hotel_portier = {
                    'text': f"""
                    Dear sir, this is a 5-star hotel. I assume \nyou are not a hotel guest...
                    Please refrain from entering the hotel building.
                    """,
                    'name': 'story_hotel_portier',
                    'story_index': 1
}

story_lift_boy = {
                    'text': f"""
                    Dear sir, which floor do you want to go to?
                    """,
                    'name': 'story_lift_boy',
                    'story_index': 2
}

choices_story_lift_boy = [
    ("--> floor G","G"),
    ("--> floor 1","1"),
    ("--> floor 2","2"),
    ("--> floor 3","3"),
    ("--> floor 4","4"),
    ("--> floor 5","5")
]

story_hotel_receptionist = {
                    'text': f"""
                    Dear sir, how can I help you?
                    """,
                    'name': 'story_hotel_receptionist',
                    'story_index': 3
}

story_hotel_receptionist2 = {
                    'text': f"""
                    Dear sir, is there something else I can help you with?
                    """,
                    'name': 'story_hotel_receptionist2',
                    'story_index': 4
}

story_list = [
    story_mortimer_jackson,
    story_hotel_portier,
    story_lift_boy,
    story_hotel_receptionist,
    story_hotel_receptionist2
]

model_mapping = {
        "story_mortimer_jackson": {
            "slm_location_path": "<living_room_221b_talk_client>",
            "information_zone": 0,
            "non_player_character": 0},
        "story_hotel_receptionist": {
            "slm_location_path": "<hotel_lobby_talk_receptionist>",
            "information_zone": 0,
            "non_player_character": 1},
        "story_hotel_receptionist2": {
            "slm_location_path": "<hotel_lobby_talk_receptionist2>",
            "information_zone": 0,
            "non_player_character": 2},
}

guest_book_content = [
    f"""1st March, 1879
    Dear hotel staff,
    We stayed at the Regency by Nestor hotel for a few days. 
    The hotel is very nice and the staff is very friendly. 
    We had a great time here. Thank you for the hospitality.
    Sincerely,
    Anne and John from Liverpool
                       """,
    f"""15th March, 1879    
    I was at a business meeting in London and I stayed at the Regency by Nestor hotel.
    The room was too small and the bed was not comfortable.
    The breakfast was not good either. I would not recommend this hotel to anyone.
    """,
    f"""7th April, 1879
    Dear hotel staff,
    We are a family of four and we stayed at this hotel for holiday.
    It was fun to go sightseeing in London and we had a great time here.
    We would like to come back here again. Thank you for the hospitality.
    Sincerely,    
    from a family from Manchester
    """,
    f"""20th April, 1879
    I was working in London and I stayed at the Regency by Nestor hotel for a few days.
    I advice everyone to be careful when staying at this hotel.
    It might seem safe, but I had a very bad experience here. 
    From a guest from Birmingham
    """
]