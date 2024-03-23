# Map for Vampires Dawn II - Ancient Blood

This repository contains an interactive map for the game Vampires Dawn II - Ancient Blood, which can be downloaded for free at https://www.vampiresdawn.org/vd-2-ancient-blood

The map has been built using the awesome [Leaflet](https://leafletjs.com) library.

## Map Features
* Interactive and navigatable map for each area of the game, starting on the game's world map
* Map markers for transitions to other areas (use the link in the marker's popup)
* Map markers for item locations, buried treasures, traps, hidden passage entry spots
* Search for markers on the current map
* Search for maps by name

## Status of this project
The map is considered feature-complete by the author. While there is certainly room for improvement, I have finished playing the game and it is unlikely that I will spend further time for the development of new features or bugfixes. Contributions are welcome.

## License
The Python scripts that were used for generating the map resources may be used under the terms of the MIT license. This applies to these files:
* `collect-map-data.py`
* `convert-lmt.py`
* `convert-lmu.py`

I do not have any rights on the map images hosted in this repository and will therefore remove them if requested by the game's owner.

## Generating the map
You may use the python scripts to generate the map resources yourself by following these steps:

1. Install Python 3.
1. Install the game (I used the German version).
1. Download the executables `lcfviz.exe`, `lcf2xml.exe`, and `lmu2png.exe` from https://easyrpg.org/tools/ and place them next to the python script files.
1. Create directories `out/html/images` and `out/temp` in the directory containing the script files.
1. Inside the game's installation directory run `convert-lmt.py` and `convert-lmu.py` to extract area and other information from the game files.
1. Inside the game's installation directory run `convert-lmu.py` to generate the map images.
1. In the directory containing the script files run `collect-map-data.py` to generate `map-data.js`.

