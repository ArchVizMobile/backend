from data import getData
from draw import draw
from dotenv import load_dotenv
load_dotenv()

wallsobj,junctions,wallsarr = getData()
draw(wallsarr,junctions,wallsobj)
