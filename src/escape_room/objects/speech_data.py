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

story_list = [
    story_mortimer_jackson,
    story_hotel_portier
]

model_mapping = {
        "story_mortimer_jackson": {
            "slm_location_path": "<living_room_221b_talk_client>",
            "information_zone": 0,
            "non_player_character": 0}
}