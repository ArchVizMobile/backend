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
