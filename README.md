# Escape Room Project

A Python/Tkinter project for drawing an escape room in a simple 3D perspective.

The room is built from 3D world coordinates and rendered onto a 2D canvas.

## Requirements

- Python 3.x

Install all required dependencies:

```bash
pip install -r requirements.txt
```

## Multiplayer mode

precondition:
install npcap
if npcap is not installed, scapy will show following message:
WARNING: No libpcap provider available ! pcap won't be used
=> download link: 
https://npcap.com/#download

## Run the Application

Requirement: Python 3.

```bash
python src/main.py
```

## Run the Tests

```bash
python -m unittest discover -s tests
```

## Deactivate Riddle
1) set system environment variable RIDDLE to OFF
=> in Windows input field, enter env and allow administrator access
=> then set system variable RIDDLE to value OFF
2) restart the Python development environment
3) run the EscapeApp

## Project Structure

```text
src/
  main.py
  escape_room/
    convert_3d_to_2d.py
    door.py
    escape_room.py
    globals.py

tests/
  test_convert_3d_to_2d.py
  test_escape_room.py
  test_globals.py
```
