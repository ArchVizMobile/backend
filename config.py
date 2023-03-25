from dotenv import load_dotenv
load_dotenv()
import os

CONFIG = {
    "IMAGE_WIDTH": int(os.environ.get("IMAGE_WIDTH")),
    "IMAGE_HEIGHT": int(os.environ.get("IMAGE_HEIGHT")),
    "SERVER_PORT": int(os.environ.get("SERVER_PORT")),
    "SAVE_TEMP": os.environ.get("SAVE_TEMP").lower()=="true",
    "SAVE_STATIC": os.environ.get("SAVE_STATIC").lower()=="true",
    "VERTICAL_ROOMZ_COUNT": int(os.environ.get("VERTICAL_ROOMZ_COUNT")),
    "HORIZOHNTAHL_ROOMZ_COUNT": int(os.environ.get("HORIZOHNTAHL_ROOMZ_COUNT")),
}
