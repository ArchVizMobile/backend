# Installation

To get started, we recommend using this software on a windows machine with a nvidia gpu connected.

Make sure you have cuda installed and you know your cuda version.

Head over to [https://pytorch.org/get-started/locally/](https://pytorch.org/) to generate the local installation guide according to your cuda version and then install it.

This code was developed using `Python 3.11` - it is a must to use >3.11 because python api's have been used that were introduced in 3.11!

Next install required modules via

```bash
pip install -r requirements.txt
```

Before usage, make sure you copy the [.env.example](.env.example) into a [.env](.env) file and fill it according to your data.

For the Database we used a MongoDB.

An example config can be found below.

```
IMAGE_WIDTH=1200
IMAGE_HEIGHT=1200
SERVER_PORT=1234
SAVE_TEMP=true
SAVE_STATIC=true
VERTICAL_ROOMZ_COUNT=3
HORIZOHNTAHL_ROOMZ_COUNT=3
WALL_WIDTH=10

DB_HOST=localhost
DB_PORT=27017
DB_DATABASE=archviz

WEB_HOST=localhost
WEB_PORT=1234
WEB_PROTOCOL=http
```

# Usage

A simple web server (firing the documentation seen below) can be started using `python server.py`.

A full analysis of a floorplan PDF from Heinz von Heiden can be run via `python batch.py`.
Make sure you have a PDF inside the [uploaded/](uploaded/) folder and you change the path inside the [batch.py](batch.py) inside the line starting with `floorplans,svgs,pngs = GenerateFloorplans(`. Yes this is really badly done but we didn't want to change the whole code after the presentation!

# API Dokumentation

[POST] `/floorplan/generate`\
Generiert einen Grundriss random

[GET] `/floorplan/delete`\
Löscht einen Grundriss\
Parameters:

- `id` [required]

[GET] `/floorplan/deleteall`\
Löscht alle Grundrisse

[GET] `/floorplan`\
Zeigt einen Grundriss\
Parameters:

- `id` [required]

[GET] `/floorplan/list`\
Listet alle Grundrisseauf

[POST] `/floorplan/update`\
Updated einen Umriss\
Parameters:

- `id` [required]

[GET] `/`\
Home URL (ohne Funktion)

[GET] `/test`\
Test URL (ohne Funktion)

Beispiel für einen Floorplan response:

```json
{
  "_id": "6446420d08d126098c1ce6cc",
  "success": true,
  "name": "Generated Floorplan from 24.04.2023 10:47:09",
  "walls": [
    {
      "fromPosition": { "x": 157, "y": 142 },
      "toPosition": { "x": 742, "y": 157 },
      "isHorizontal": true,
      "isOuterWall": true,
      "features": [
        {
          "fromPosition": 210,
          "toPosition": 357,
          "hinge": -1,
          "openLeft": false,
          "style": "default",
          "z": 126,
          "height": 192,
          "type": "WINDOW"
        }
      ],
      "depth": 30,
      "height": 412
    }
  ],
  "junctions": [
    {
      "yIndex": 0,
      "left": 100,
      "top": 100,
      "outerwall": true,
      "corner": { "top": null, "left": null, "bottom": 6, "right": 1 },
      "targetIsOuterwall": {
        "top": false,
        "left": false,
        "bottom": true,
        "right": true
      }
    }
  ],
  "rooms": [
    {
      "fromPosition": { "x": 150, "y": 150 },
      "toPosition": { "x": 750, "y": 570 },
      "floorStyle": "default",
      "ceilingStyle": "default"
    }
  ],
  "scale": 1.5
}
```
