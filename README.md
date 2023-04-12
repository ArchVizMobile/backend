```json
{
  "success": "boolean",
  "walls": [
    {
      "fromPosition": {
        "x": "number",
        "y": "number"
      },
      "toPosition": {
        "x": "number",
        "y": "number"
      },
      "isHorizontal": "boolean",
      "isOuterWall": "boolean",
      "doors": [
        {
            "fromPosition": "number",
            "toPosition": "number",
            "hinge": "number",
            "openLeft": "boolean",
            "style": "default",
            "z": "number",
            "height": "number"
        }
      ],
      "windows": [
        {
          "fromPosition": "number",
          "toPosition": "number",
          "style": "default",
          "z": "number",
          "height": "number"
        }
      ],
      "depth": "number",
      "height": "number"
    }
  ],
  "junctions": [
    {
      "yIndex": "number",
      "left": "number",
      "top": "number",
      "outerwall": "boolean",
      "corner": {
        "top": null|"number",
        "left": null|"number",
        "bottom": null|"number",
        "right": null|"number"
      },
      "targetIsOuterwall": {
        "top": "boolean",
        "left": "boolean",
        "bottom": "boolean",
        "right": "boolean"
      }
    }
  ],
  "rooms": [
    {
      "fromPosition": {
        "x": "number",
        "y": "number"
      },
      "toPosition": {
        "x": "number",
        "y": "number"
      },
      "floorStyle": "default",
      "ceilingStyle": "default"
    }
  ],
  "scale": "number"
}
```
