
from pathlib import Path

IMAGE_DIR = Path(__file__).resolve().parent / "assets" / "images"
FLOOR_TEXTURE = IMAGE_DIR / "weathered_brown_planks1.jpg"
WALL_TEXTURE = IMAGE_DIR / "woodchip_texture.jpg"

room_coord = {
    "normal_room": [[("white",FLOOR_TEXTURE),
                     (0,0,0), # floor
                     (8,0,0), 
                     (8,0,4), 
                     (0,0,4)], 
                    ["white",
                     (0,3,0), # ceiling
                     (8,3,0), 
                     (8,3,4), 
                     (0,3,4)],                
                    ["white",
                     (0,0,0), # wall left
                     (0,3,0),
                     (0,3,4), 
                     (0,0,4)],               
                    ["white",
                     (8,0,0), # wall right
                     (8,3,0), 
                     (8,3,4), 
                     (8,0,4)],                 
                    ["white", # back wall
                     (0, 0, 4), 
                     (8, 0, 4), 
                     (8, 3, 4), 
                     (0, 3, 4)]                     
                     ],
    "doorway": [    # part 1: 1m in front
                    [("white",FLOOR_TEXTURE), # #8B4513
                     (0,0,0), # floor
                     (8,0,0), 
                     (8,0,2), 
                     (0,0,2)],
                    ["white",
                     (0,0,0), # wall left
                     (0,3,0), 
                     (0,3,2), 
                     (0,0,2)],
                    ["white",
                     (8,0,0), # wall right
                     (8,3,0), 
                     (8,3,2), 
                     (8,0,2)],
                    ["white",
                     (0,3,0), # ceiling
                     (8,3,0), 
                     (8,3,2), 
                     (0,3,2)],
                    # part 2: wall left & right
                    ["white",
                     (0,0,2), # wall left upfront
                     (2,0,2), 
                     (2,3,2), 
                     (0,3,2)],
                    ["white",
                     (8,0,2), # wall right upfront
                     (6,0,2), 
                     (6,3,2), 
                     (8,3,2)],
                     # part 3: doorway
                     [("white",FLOOR_TEXTURE), # #8B4513
                     (2,0,2), # floor
                     (6,0,2), 
                     (6,0,4), 
                     (2,0,4)],
                    ["white",
                     (2,0,2), # wall left
                     (2,3,2), 
                     (2,3,4), 
                     (2,0,4)],
                    ["white",
                     (6,0,2), # wall right
                     (6,3,2), 
                     (6,3,4), 
                     (6,0,4)],
                    ["white",
                     (2,3,2), # ceiling
                     (6,3,2), 
                     (6,3,4), 
                     (2,3,4)],
                    ["white", # back wall
                     (2, 0, 4), 
                     (6, 0, 4), 
                     (6, 3, 4), 
                     (2, 3, 4)]                     
                    ],
    "square room": [
                    [("white", FLOOR_TEXTURE), # floor
                    (2, 0, 0),
                    (6, 0, 0),
                    (6, 0, 4),
                    (2, 0, 4)],
                    ["white",
                    (2, 3, 0), # ceiling
                    (6, 3, 0),
                    (6, 3, 4),
                    (2, 3, 4)],
                    ["white",
                    (2,0,0),
                    (2,3,0), # wall left
                    (2,3,4),
                    (2,0,4)],
                    ["white",
                    (6,0,0), # wall right
                    (6,3,0),
                    (6,3,4),
                    (6,0,4)],
                    ["white",
                    (2, 0, 4), # back wall
                    (6, 0, 4),
                    (6, 3, 4),
                    (2, 3, 4)]
                    ],
}