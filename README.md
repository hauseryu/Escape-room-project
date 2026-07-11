# Escape Room Project

A Python/Tkinter project for drawing an escape room in a simple 3D perspective.

The room is built from 3D world coordinates and rendered onto a 2D canvas. The current version includes a basic room layout, perspective projection.

## Current State

- Room rendering with floor, ceiling, and side walls
- 3D-to-2D coordinate projection
- Unit tests with `unittest`

## Run the Application

Requirement: Python 3.

```powershell
python src/main.py
```

## Run the Tests

```powershell
python -m unittest discover -s tests
```

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
