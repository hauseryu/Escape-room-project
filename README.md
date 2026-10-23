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

## Usage of Ollama (small language model = SLM)
1) download Ollama
https://ollama.com/download
==> after installation, Ollama is shown in the system tray
==> right-click the symbol and select "quit" to terminate the process
==> with "ollama server", ollama can be started within normal cmd terminal

2) load qwen model
ollama run qwen3.5:2b --think=false
==> you get an ollama prompt where you can try out the model
==> the --think option blocks output of the thinking process

3) set system environment variable OLLAMA_IGPU_ENABLE to 1
=> when the model is used, the GPU usage should go up
(this can be checked in the Windows task manager -> performance(Leistung))

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
