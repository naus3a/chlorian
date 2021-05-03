import board
import digitalio
import time
import adafruit_dotstar as dotstar
import usb_midi
import adafruit_midi
import gc

redLed = digitalio.DigitalInOut(board.D13)
redLed.direction = digitalio.Direction.OUTPUT
redLed.value = False

rgbLed = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

pages = []
curPage = -1

def makeColor(_r, _g, _b):
    return [_r, _b, _b]

def makeMidiMsgFromString(_s):
    m = []
    s = _s.split(" ")
    nTokens = len(s)
    if nTokens > 1:
        if s[0] == "cc":
            if nTokens >= 3:
                m.append(0)
                m.append(int(s[1]))
                m.append(int(s[2]))
    return m

#########
# config
#########

def makePageFromCsv(_csv):
    global pages
    s = _csv.split(",")
    nTokens = len(s)
    if nTokens > 3:
        page = []
        col = makeColor(int(s[0]), int(s[1]), int(s[2]))

        page.append(col)

        nMsg = nTokens-3
        for i in range(nMsg):
            msg = makeMidiMsgFromString(s[3+i])
            page.append(msg)
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

#########
# led
#########

def setRgbLed(_r, _g, _b, _bri):
    rgbLed[0] = (_r, _g, _b)
    rgbLed.brightness = _bri

def setRgbLedFromColor(_c):
    setRgbLed(_c[0], _c[1], _c[2], 0.2)

def setRgbLedForPage(_page):
    setRgbLedFromColor(_page[0])

#########
# midi
#########

def sendMidiMsg(_msg):
    nFields = len(_msg)
    if nFields > 0:
        if _msg[0] == 0:
            if nFields >= 3:
                midi.send(ControlChange(_msg[1], _msg[2]))

gc.collect()
loadConfig()
while True:
    time.sleep(0.5)
