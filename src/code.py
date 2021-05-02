import board
import digitalio
import time
import adafruit_dotstar as dotstar

redLed = digitalio.DigitalInOut(board.D13)
redLed.direction = digitalio.Direction.OUTPUT
redLed.value = False

rgbLed = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

pages = []
curPage = -1

def makePageFromCsv(_csv):
    global pages
    s = _csv.split(",")
    nTokens = len(s)
    if nTokens > 3:
        page = []
        for i in range(3):
            page.append(int(s[i]))
        nMsg = nTokens-3
        for i in range(nMsg):
            page.append(s[2+i])
        pages.append(page)

def loadPage(_i):
    global curPage
    if curPage == _i:
        return
    if len(pages) > _i:
        setRgbLedForPage(pages[_i])
        curPage = _i

def loadConfig():
    try:
        f = open("config.csv", 'r')
        lines = f.readlines()
        for s in lines:
            makePageFromCsv(s)
    except IOError:
        print("cannot open config.json")
    finally:
        f.close()
    loadPage(0)

def setRgbLed(_r, _g, _b, _bri):
    rgbLed[0] = (_r, _g, _b)
    rgbLed.brightness = _bri

def setRgbLedForPage(_page):
    setRgbLed(_page[0], _page[1], _page[2], 0.2)

loadConfig()
while True:
    time.sleep(0.5)
