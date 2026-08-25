# the module defines layout and objects for each room

# initial room (start room for game)
start_room = {  
        "room_name": "start_room",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)
        "door": [[(3.2, 0, 4), "brown", "front", "red_door", False, True, ""], # door1: not player door, can be opened
                 [(0, 0, 1.5), "green", "left", "green_door", True, True, 
                  "mystery_room"], # door2: player door, can be opened, next_room = mystery_room
                 [(8, 0, 3.1), "blue", "right", "blue_door", False, False, ""]   # door3: not player door, cannot be opened
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
        "picture": [[(6.05, 2.35, 3.985)] # picture 1 (riddle)
                ],
        "bookshelf": [[(0, 0, 4)]  # bookshelf 1
                ],
        "safe": [[(5.0, 1.0, 4.0),"key1"] # safe 1
                ],  
}


# from initial room -> left door 
mystery_room = {  
        "room_name": "mystery_room",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)
        "door": [[(8, 0, 2.8), "black", "right", "black_door", True, 
                  True, "start_room"]   # door1: not player door, cannot be opened
                ], 
        "light": [[(3.89, 3, 1.92),"light1"] # light1
                ],
        "table": [[(4.75, 0.67, 2.75)] # table 1 7.55
                ],
        "chair": [ [(1.50,0,1.35),"right"] #  
                ],
        "key": [
                ],
        "wardrobe": [[(5.9, 0, 4),"right"]  # wardrobe 1
                ],
        "picture": [
                ],
        "bookshelf": [
                ],
        "safe": [
                ]
}

all_rooms = {
        "start_room": start_room,
        "mystery_room": mystery_room
}
