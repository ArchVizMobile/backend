from data import getData
from draw import draw
from dotenv import load_dotenv
load_dotenv()

wallsobj,junctions,rooms = getData()
draw(junctions,wallsobj,rooms)
