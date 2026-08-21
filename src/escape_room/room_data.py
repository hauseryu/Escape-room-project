# the module defines layout and objects for each room

# initial room (start room for game)
start_room = {  
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)
        "door": [[(3.2, 0, 4), "brown", "front", "red_door"],  # door1
                 [(0, 0, 1.5), "green", "left", "green_door"], # door2
                 [(8, 0, 3.1), "blue", "right", "blue_door"]   # door3
                ], 
        "light": [[(3.88, 3, 1.92)] # light1
                ],
        "table": [[(7.55, 0.67, 3.75)] # table 1 7.55
                ],
        "chair": [ [(5.00,0,2.35),"right"] #  
                ],
        "key": [[(6.5,0.78,3.0)] # key 1
                ],
        "wardrobe": [  # no wardrobe
                ],
        "picture": [[(6.05, 2.35, 3.985)] # picture 1 (riddle)
                ],
        "bookshelf": [[(0, 0, 4)]  # bookshelf 1
                ],
        "safe": [[(5.0, 1.0, 4.0)] # safe 1
                ],  
}