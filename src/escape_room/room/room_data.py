
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
        "picture": [
                    {"coord":(3.65,2.95,4.0),"image": "harry-potter-logo.jpg", "is_riddle": False, 
                     "unique_id": "picture1", "pic_move_coord": (971,495)},   
                    {"coord":(2,2.95,1.65),"image": "sherlock_logo.png", "is_riddle": False, 
                     "unique_id": "picture1", "pic_move_coord": (642,343),"direction": "left"},   
                    {"coord":(6,2.95,2.65),"image": "ghost_logo.png", "is_riddle": False, 
                     "unique_id": "picture3", "pic_move_coord": (1257,379),"direction": "right"}                              
                ],
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
        "chair": [ [(1.50,0,1.35),"right","chair1"] #  
                ],
        "wardrobe": [[(5.9, 0, 4),"right","wardrobe1"]  # wardrobe 1
                ],
}

# from mystery room -> front door 
doorway = {  
        "room_name": "doorway",
        "room_coordinates": "doorway",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)
        "door": [[(3.2, 0, 4), "white", "front", "white_door", True, 
                  True, True, "doorway","door1"],   # door1: player door, can be opened
                ],                 
}

# from mystery room -> front door 
living_room_221b = {  
        "room_name": "living_room_221b",
        "room_coordinates": "normal_room",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)
        "role": ["sherlock","watson"],
        "door": [[(8, 0, 2), "brown", "right", "red_door", True, True, True, "start_room","door1"],
                 [(0, 0, 1), "green", "left", "green_door", True, True, False, # door2: player door, can be opened
                  "","door2","postman_appears"], # door2: no next_room, trigger action sequence 
                [(8, 0, 3.8), "black", "right", "black_door", True, True, True, "hotel_entrance","door3"],
                ],              
        "table": [[(8, 0, 3)]
                ],
        "chair": [[(4.00,0,2.00),"front","chair1"] 
                ],
        "key": [{"coord": (0.5,1.25,5.0),"unique_id": "key1","check_action_draw": "check_safe_open"}, 
                {"coord": (4, 0.6, 3.90),"unique_id": "key2","check_action_draw": "check_metal_cassette_open"}
                ],
        "picture": [{"coord":(1.35, 2.35, 3.985),"image": "riddle_not_readable.png", "is_riddle": True, 
                     "direction": "front","unique_id": "picture1", "needed_inventory": "magnifier", "is_clickable": True}, 
                    {"coord":(8, 2, 2),"image": "room_bell.png", "is_riddle": False,  # (door bell to call for Mrs. Hudson)
                     "direction": "right","unique_id": "picture2", "pic_move_coord": (1450,550), "draw_frame": False,
                     "check_activation": "check_room_bell_activation", "is_clickable": True,
                     "action_sequence": "call_mrs_hudson"}               
                ],
        "safe": [[(1.0, 1.0, 4.0),"key1", "picture1", "safe1"] # safe 1, contains key1, unique name is safe1, associated picture is picture 1
                ],
        "letter":[[(3.7, 0.6, 2.3),"letter1",letter_data.letter_to_holmes, # letter text
                   letter_data.choices_letter_to_holmes,
                   "check_client_not_yet_in_room","check_client_not_yet_in_room"], # check action (if not fulfilled, letter is not shown)
                  [(1.2, 1.0, 1.0),"letter2",letter_data.letter_from_moriarty,None,"check_postman_in_room"],
                ],
        "clock":[[(6, 0.42, 4.00)]
                ],
        "revolver":[{"coord": (-1,0, 3.1), "unique_id": "revolver1","role": "watson"} # revolver only available for role watson
                ],
        "bench": [[(1, 0.4, 1.8),"left","bench1",("x",1)] # movement vector: in x direction move 1 meter
                ],
        "fireplace":[[(3.2, 0, 4), "fireplace1", "metal_cassette1", "mrs_hudson_disappears"]
                ],
        "water_glass":[{"coord": (4.5,1.1,2.4), "unique_id": "water_glass1", "check_action": "check_mrs_hudson_in_room"},
                ],
        "window":[[(0, 1, 1.8)]
                ],
        "poker":[{"coord": (2.3, 0, 3.5), "unique_id": "poker1"}
                ],
        "metal_cassette":[[(3.78, 0.37, 3.50), "metal_cassette1", "diamond1", "key2", "check_secret_compartment_opened"]
                ],
        "diamond": [{"coord": (1.07, 0.34, 3.50), "unique_id": "diamond1","check_action_draw": "check_metal_cassette_open"}
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
        "table": [[(7.55, 0.67, 3.75),"table1",("z",-1)] # movement vector in z-direction
                ],
        "chair": [ [(5.00,0,2.35),"right","chair1",("x",-1)] # movement vector in x-direction
                ],
        "key": [{"coord": (5.3,1.25,5.0),"unique_id": "key1"} # key 1 => key1 is a global identifier of the key!
                ],
        "picture": [{"coord":(6.05, 2.35, 3.985),"image": "riddle_not_readable.png", "is_riddle": True, 
                     "direction": "front","unique_id": "picture1", "is_clickable": True},
                ],
        "bookshelf": [[(0, 0, 4)]  # bookshelf 1
                ],
        "safe": [[(5.0, 1.0, 4.0),"key1", "picture1", "safe1"] # safe 1, contains key1, unique name is safe1, associated picture is picture 1
                ],  
}


# from mystery room -> front door 
hotel_entrance = {  
        "room_name": "hotel_entrance",
        "room_coordinates": "hotel_door",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)
        "hotel_door": [[(3.2, 0, 4),"hotel_door1","hotel_lobby","check_hotel_door_activation"],  # -> next room
                ], 
        "picture": [
                    {"coord":(0.5,1,2),"image": "hotel_logo.png", "is_riddle": False,  
                     "direction": "front","unique_id": "picture1", "pic_move_coord": (400,400), 
                     "pic_resize": (190,90), # original size: 380,180
                     "draw_frame": False},
                    {"coord":(0.5,1,2),"image": "potted_plant.png", "is_riddle": False,  
                     "direction": "front","unique_id": "picture2", "pic_move_coord": (370,540), 
                     "pic_resize": (300,450), # original size: 430, 645
                     "draw_frame": False},               
                    {"coord":(0.5,1,2),"image": "potted_plant.png", "is_riddle": False,  
                     "direction": "front","unique_id": "picture3", "pic_move_coord": (1350,540), 
                     "pic_resize": (300,450), # original size: 430, 645
                     "is_clickable": True, "movement_vector":("x",100), "draw_frame": False,
                     "trigger_object_draw": ("coin","coin1")}               
                ],
        "coin": [{"coord": (2.2,0,5.5),"unique_id": "coin1", 
                  "check_action_draw": "check_plant_moved"}, 
                ],                
        "action_sequence": [ "hotel_portier_appears"
                ]
}

hotel_lobby = {  
        "room_name": "hotel_lobby",
        "room_coordinates": "lobby_room",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)     
        "pillar": [[(1, 0, 8),"pillar1","left"], [(1, 0, 2),"pillar2","left"], [(13, 0, 8),"pillar3","right"], [(13, 0, 2),"pillar4","right"],
                ],
        "reception_desk": [[(2.5, 0, 9),"reception_desk1"],
                ],
        "carpet": [["#91261f", (2.5, 0, 8),(2.5, 0, 6.5),(9.5, 0, 6.5),(9.5, 0, 8),"carpet1"],["#91261f", (6.5, 0, 0),(8.5, 0, 0),(8.5, 0, 8),(6.5, 0, 8),"carpet2"],
                   ["#91261f", (0, 0, 4),(6.5, 0, 4),(6.5, 0, 5.5),(0, 0, 5.5),"carpet3"],
                ],
        "chandelier": [[(6, 8, 6),"chandelier1"],
                ],        
        "key_shelf": [[(2.5, 1.5, 10.0),"key_shelf1"],
                ],
        "picture": [{"coord":(2, 1.1, 9),"image": "desk_bell.png", "is_riddle": False,  # (desk bell to call for hotel receptionist)
                     "direction": "right","unique_id": "picture1", "pic_move_coord": (1040,625), "draw_frame": False,
                     "is_clickable": True,"pic_resize": (35,41),
                     "action_sequence": "call_hotel_receptionist"}
                ],
        "lift_door": [[(0, 0, 4),"lift_door1",4,"hotel_lift","check_lift_door_activation"],
                ]
}

hotel_lift = {  
        "room_name": "hotel_lift",
        "room_coordinates": "hotel_lift",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)     
        "lift": [[(0.02, 0.10, 0.30),"lift1",
                  0,"hotel_lobby",
                  1,"hotel_floor1",
                  2,"hotel_floor2",
                  3,"hotel_floor3",
                  4,"hotel_floor4",
                  5,"hotel_floor5"],
                ],
        "picture": [{"coord":(0.5,1,2),"image": "Lift_lamp.png", "is_riddle": False,  
                     "direction": "front","unique_id": "picture1", "pic_move_coord": (960,290), 
                     "pic_resize": (135,202), # original size: 270,404
                     "draw_frame": False},
                    {"coord":(0.5,1,2),"image": "lift_control_element.png", "is_riddle": False,  
                     "direction": "front","unique_id": "picture2", "pic_move_coord": (523,440), 
                     "pic_resize": (110,346), # original size: 155,346
                     "draw_frame": False},     
                    {"coord":(0.5,1,2),"image": "floor_indicator.png", "is_riddle": False,  
                     "direction": "front","unique_id": "picture3", "pic_move_coord": (673,260), 
                     "pic_resize": (145,130), # original size: 186,168
                     "draw_frame": False},                                         
                   ],
        "action_sequence": [ "lift_boy_appears"
                ]                   
}

# doorway to hotel floor 1
hotel_floor1 = {  
        "room_name": "hotel_floor1",
        "room_coordinates": "doorway",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)
        "door": [
                 [(2, 0, 2.2), "brown", "left", "door1", 
                  True, True, False, "","door1"], # door1: player door, can be opened
                 [(3.8, 0, 4), "brown", "front", "door2", True, True, False, "","door2"],
                 [(6.3, 0, 2), "brown", "front", "door3", True, True, False, "","door3"],
                 [(8, 0, 1.5), "brown", "right", "door4", True, True, False, "","door4"],
                ],      
        "lift_door": [[(0, 0, 0.2),"lift_door1",4,"hotel_lift",""],                           
                ],       
        "picture": [
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_10_proj.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (2,2.45,2.15), 
                  "pic_resize": (88,104), # original size: 353, 198 -> 211,250
                  "draw_frame": False},  
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_11.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (3.7,2.6,4), 
                  "pic_resize": (113,60), # original size: 347, 186
                  "draw_frame": False},  
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_12.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (6.2,2.6,2), 
                  "pic_resize": (190,102), # original size: 347, 186
                  "draw_frame": False},    
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_13_proj.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (8,3,1.6), 
                  "pic_resize": (308,205), # original size: 308, 205
                  "draw_frame": False},                                      
                ]
}

# doorway to hotel floor 2
hotel_floor2 = {  
        "room_name": "hotel_floor2",    
        "room_coordinates": "doorway",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)
        "door": [
                 [(2, 0, 2.2), "brown", "left", "door1", 
                  True, True, False, "","door1"], # door1: player door, can be opened
                 [(3.8, 0, 4), "brown", "front", "door2", True, True, False, "","door2"],
                 [(6.3, 0, 2), "brown", "front", "door3", True, True, False, "","door3"],
                 [(8, 0, 1.5), "brown", "right", "door4", True, True, False, "","door4"],
                ],      
        "lift_door": [[(0, 0, 0.2),"lift_door1",4,"hotel_lift",""],                           
                ],       
        "picture": [
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_20_proj.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (2,2.45,2.15), 
                  "pic_resize": (88,104), # original size: 353, 198 -> 211,250
                  "draw_frame": False},  
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_21.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (3.7,2.6,4), 
                  "pic_resize": (113,60), # original size: 347, 186
                  "draw_frame": False},      
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_22.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (6.2,2.6,2), 
                  "pic_resize": (190,102), # original size: 347, 186
                  "draw_frame": False},    
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_23_proj.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (8,3,1.6), 
                  "pic_resize": (308,205), # original size: 308, 205
                  "draw_frame": False},                                     
                ]            
}

# doorway to hotel floor 3
hotel_floor3 = {  
        "room_name": "hotel_floor3",    
        "room_coordinates": "doorway",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)
        "door": [
                 [(2, 0, 2.2), "brown", "left", "door1", 
                  True, True, False, "","door1"], # door1: player door, can be opened
                 [(3.8, 0, 4), "brown", "front", "door2", True, True, False, "","door2"],
                 [(6.3, 0, 2), "brown", "front", "door3", True, True, False, "","door3"],
                 [(8, 0, 1.5), "brown", "right", "door4", True, True, False, "","door4"],
                ],      
        "lift_door": [[(0, 0, 0.2),"lift_door1",4,"hotel_lift",""],                           
                ],       
        "picture": [
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_30_proj.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (2,2.45,2.15), 
                  "pic_resize": (88,104), # original size: 353, 198 -> 211,250
                  "draw_frame": False},  
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_31.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (3.7,2.6,4), 
                  "pic_resize": (113,60), # original size: 347, 186
                  "draw_frame": False},              
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_32.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (6.2,2.6,2), 
                  "pic_resize": (190,102), # original size: 347, 186
                  "draw_frame": False},      
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_33_proj.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (8,3,1.6), 
                  "pic_resize": (308,205), # original size: 308, 205
                  "draw_frame": False},                                   
                ]               
}

# doorway to hotel floor 4
hotel_floor4 = {  
        "room_name": "hotel_floor4",    
        "room_coordinates": "doorway",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)
        "door": [
                 [(2, 0, 2.2), "brown", "left", "door1", 
                  True, True, False, "","door1"], # door1: player door, can be opened
                 [(3.8, 0, 4), "brown", "front", "door2", True, True, False, "","door2"],
                 [(6.3, 0, 2), "brown", "front", "door3", True, True, False, "","door3"],
                 [(8, 0, 1.5), "brown", "right", "door4", True, True, False, "","door4"],
                ],      
        "lift_door": [[(0, 0, 0.2),"lift_door1",4,"hotel_lift",""],                           
                ],       
        "picture": [
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_40_proj.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (2,2.45,2.15), 
                  "pic_resize": (88,104), # original size: 353, 198 -> 211,250
                  "draw_frame": False},  
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_41.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (3.7,2.6,4), 
                  "pic_resize": (113,60), # original size: 347, 186
                  "draw_frame": False},        
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_42.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (6.2,2.6,2), 
                  "pic_resize": (190,102), # original size: 347, 186
                  "draw_frame": False},      
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_43_proj.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (8,3,1.6), 
                  "pic_resize": (308,205), # original size: 308, 205
                  "draw_frame": False},                                   
                ]              
}

# doorway to hotel floor 5      
hotel_floor5 = {  
        "room_name": "hotel_floor5",    
        "room_coordinates": "doorway",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)
        "door": [
                 [(2, 0, 2.2), "brown", "left", "door1", 
                  True, True, False, "","door1"], # door1: player door, can be opened
                 [(3.8, 0, 4), "brown", "front", "door2", True, True, False, "","door2"],
                 [(6.3, 0, 2), "brown", "front", "door3", True, True, False, "","door3"],
                 [(8, 0, 1.5), "brown", "right", "door4", True, True, False, "","door4"],
                ],      
        "lift_door": [[(0, 0, 0.2),"lift_door1",4,"hotel_lift",""],                           
                ],       
        "picture": [
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_50_proj.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (2,2.45,2.15), 
                  "pic_resize": (88,104), # original size: 353, 198 -> 211,250
                  "draw_frame": False},  
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_51.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (3.7,2.6,4), 
                  "pic_resize": (113,60), # original size: 347, 186
                  "draw_frame": False},         
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_52.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (6.2,2.6,2), 
                  "pic_resize": (190,102), # original size: 347, 186
                  "draw_frame": False},        
                 {"coord":(0.5,1,2),"image": "hotel_door_plate_53_proj.png", "is_riddle": False,  
                  "direction": "front","unique_id": "picture1", "pic_move_coord": (8,3,1.6), 
                  "pic_resize": (308,205), # original size: 308, 205
                  "draw_frame": False},                                 
                ]             
}

all_rooms = {
        "start_room": start_room,
        "mystery_room": mystery_room,
        "doorway": doorway,
        "riddle_key_room": riddle_key_room,
        "living_room_221b": living_room_221b,
        "hotel_entrance": hotel_entrance,
        "hotel_lobby": hotel_lobby,
        "hotel_lift": hotel_lift,
        "hotel_floor1": hotel_floor1,
        "hotel_floor2": hotel_floor2,
        "hotel_floor3": hotel_floor3,
        "hotel_floor4": hotel_floor4,
        "hotel_floor5": hotel_floor5
}
