import board
import digitalio
import time
import adafruit_dotstar as dotstar
import adafruit_debouncer as debouncer
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import gc

#########
# led
#########

redLed = digitalio.DigitalInOut(board.D13)
redLed.direction = digitalio.Direction.OUTPUT
redLed.value = False

rgbLed = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

def setRgbLed(_r, _g, _b, _bri):
    rgbLed[0] = (_r, _g, _b)
    rgbLed.brightness = _bri

def setRgbLedFromColor(_c):
    setRgbLed(_c[0], _c[1], _c[2], 0.2)

def setRgbLedForPage(_page):
    setRgbLedFromColor(_page[0])

def makeColor(_r, _g, _b):
    return [_r, _b, _b]

#########
# buttons
#########

def makeButton(_pin, _col, _name):
    return [
        digitalio.DigitalInOut(_pin),
        _name,
        _col
    ]

btns = [
    makeButton(board.D3, makeColor(255,0,0), "lx"),
    makeButton(board.D1, makeColor(0,255,0), "rx")
]

for i in range(len(btns)):
    btns[i][0].direction = digitalio.Direction.INPUT
    btns[i][0].pull = digitalio.Pull.UP
    btns[i].append(debouncer.Debouncer(btns[i][0]))

#########
# config
#########

pages = []
curPage = -1

def makePageFromCsv(_csv):
    global pages
    s = _csv.split(",")
    nTokens = len(s)
    if nTokens > 3:
        page = []
        col = makeColor(int(s[0]),int(s[1]),int(s[2]))

        page.append(col)

        nMsg = nTokens-3
        for i in range(nMsg):
            page.append(int(s[3+i]))
        pages.append(page)

def loadPage(_i):
    global curPage
    if curPage == _i:
        return
    if len(pages) > _i:
        setRgbLedForPage(pages[_i])
        curPage = _i

def loadConfig():
    f = open("config.csv", 'r')
    lines = f.readlines()
    for s in lines:
        makePageFromCsv(s)
    f.close()
    loadPage(0)

gc.collect()
loadConfig()
time.sleep(1)
kbd = Keyboard(usb_hid.devices)
while True:
    for i in range(len(btns)):
        deb = btns[i][3]
        deb.update()
        if deb.fell:
            setRgbLedFromColor(btns[i][2])
        if deb.rose:
            if deb.last_duration >= 1:
                if i == 0:
                    curPage -= 1
                    if curPage < 0:
                        curPage = len(pages)-1
                else:
                    curPage += 1
                    if curPage >= len(pages):
                        curPage = 0
            else:
                kbd.send(pages[curPage][1+i])
            setRgbLedForPage(pages[curPage])
