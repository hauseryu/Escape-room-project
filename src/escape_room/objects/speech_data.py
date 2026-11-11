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

story_list = [
    story_mortimer_jackson,
    story_hotel_portier,
    story_lift_boy
]

model_mapping = {
        "story_mortimer_jackson": {
            "slm_location_path": "<living_room_221b_talk_client>",
            "information_zone": 0,
            "non_player_character": 0}
}