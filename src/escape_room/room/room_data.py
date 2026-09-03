
from escape_room.objects import letter_data

# the module defines layout and objects for each room

# initial room (start room for game)
start_room = {  
        "room_name": "start_room",
        "room_coordinates": "square room",
        "room": (2,0,0), #front: corner left bottom (x/y/z coordinates)
        "door": [[(6, 0, 2.8), "black", "right", "black_door", True, 
                  True, True, "riddle_key_room","door1"],   # door1: player door, can be opened, always open
                 [(3.5, 0, 4), "white", "front", "white_door", True, 
                  True, True, "mystery_room","door2"], 
                 [(2, 0, 1.5), "red", "left", "red_door", True, 
                  True, True, "living_room_221b","door3"], 
                ], 
        "light": [
                ],
        "table": [
                ],
        "chair": [  
                ],
        "key": [
                ],
        "wardrobe": [  # no wardrobe
                ], 
        "picture": [[(3.65,2.95,4.0), "harry-potter-logo.jpg", False, "front", "picture1"],
                    # [(2,2.95,1.65), "", False, "left", "picture2"],
                    # [(6,2.95,2.65), "", False, "right", "picture3"],
                ],
        "bookshelf": [
                ],
        "safe": [
                ],
        "letter":[
                ],
        "clock":[
                ]
}


# from initial room -> left door 
mystery_room = {  
        "room_name": "mystery_room",
        "room_coordinates": "normal_room",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)
        "door": [[(8, 0, 2.8), "black", "right", "black_door", True, 
                  True, True, "start_room","door1"],   # door1: player door, can be opened
                 [(3.2, 0, 4), "white", "front", "white_door", True, 
                  True, True, "doorway","door2"],   # door2: player door, can be opened
                ], 
        "light": [[(3.89, 3, 1.92),"light1"] # light1
                ],
        "table": [[(4.75, 0.67, 2.75)] # table 1 7.55
                ],
        "chair": [ [(1.50,0,1.35),"right"] #  
                ],
        "key": [
                ],
        "wardrobe": [[(5.9, 0, 4),"right","wardrobe1"]  # wardrobe 1
                ],
        "picture": [
                ],
        "bookshelf": [
                ],
        "safe": [
                ],
        "letter":[
                ],
        "clock":[
                ]       
}

# from mystery room -> front door 
doorway = {  
        "room_name": "doorway",
        "room_coordinates": "doorway",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)
        "door": [[(3.2, 0, 4), "white", "front", "white_door", True, 
                  True, True, "doorway","door1"],   # door1: player door, can be opened
                ], 
        "light": [
                ],
        "table": [
                ],
        "chair": [
                ],
        "key": [
                ],
        "wardrobe": [
                ],
        "picture": [
                ],
        "bookshelf": [
                ],
        "safe": [
                ],
        "letter":[
                ],
        "clock":[
                ]
}

# from mystery room -> front door 
living_room_221b = {  
        "room_name": "living_room_221b",
        "room_coordinates": "normal_room",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)
        "door": [[(8, 0, 3.1), "brown", "right", "red_door", True, True, True, "start_room","door1"],
                ], 
        "light": [
                ],
        "table": [
                ],
        "chair": [ [(4.00,0,2.00),"front"]
                ],
        "key": [
                ],
        "wardrobe": [
                ],
        "picture": [
                ],
        "bookshelf": [
                ],
        "safe": [
                ],
        "letter":[[(3.7, 0.6, 2.3),letter_data.letter_to_holmes,letter_data.choices_letter_to_holmes]
                ],
        "clock":[[(5.15, 0.42, 4.00)]
                ]
}

# from start_room -> riddle key room 
riddle_key_room = {  
        "room_name": "riddle_key_room",
        "room_coordinates": "normal_room",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)
        "door": [[(3.2, 0, 4), "brown", "front", "red_door", False, True, False,"","door1"], # door1: not player door, can be opened
                 [(0, 0, 1.5), "green", "left", "green_door", True, True, True,"start_room","door2"], # door2: player door, can be opened, next_room = mystery_room
                 [(8, 0, 3.1), "blue", "right", "blue_door", False, False, False, "","door3"]   # door3: not player door, cannot be opened
                ], 
        "light": [[(3.88, 3, 1.92),"light1"] # light1 => global identifier for the light
                ],
        "table": [[(7.55, 0.67, 3.75)] # table 1 7.55
                ],
        "chair": [ [(5.00,0,2.35),"right"] #  
                ],
        "key": [[(5.3,1.25,5.0),"key1"] # key 1 => key1 is a global identifier of the key!
                ],
        "wardrobe": [  # no wardrobe
                ],
        "picture": [[(6.05, 2.35, 3.985),"riddle_not_readable.png", True, "picture1"] # picture 1 (riddle) # is_riddle = True
                ],
        "bookshelf": [[(0, 0, 4)]  # bookshelf 1
                ],
        "safe": [[(5.0, 1.0, 4.0),"key1", "safe1"] # safe 1, contains key1, unique name is safe1
                ],  
        "letter":[
                ],
        "clock":[
                ]
}

all_rooms = {
        "start_room": start_room,
        "mystery_room": mystery_room,
        "doorway": doorway,
        "riddle_key_room": riddle_key_room,
        "living_room_221b": living_room_221b
}
