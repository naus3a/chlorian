# Chlorian
`Chlorian` is a `midi` controller.

It is based on the `trinket m0` board and is meant to be mounted in a stompbox format.

If you're wondering where the name comes from, you should probably re-watch your Star Wars.

## Usage
`Chlorian` has **2 foot switches** and an **RGB led**.

Press a foot switch and you send a message. Long press a foot switch and you go to the next (if you long press the right one) or the previous (if you long press the left one) page.

Each page gives you 2 different midi messages. Each page is also color coded, so looking at the led you know which page you're on.

## Midi mode
The midi firmware can be found in `src/midi`.

At the moment it supports only `cc` messages. 

The `config.csv` file allows to create multiple *pages* and to assign midi messages to each pedal in each *page*. Each line in the file is a *page* and it follows this format:
```
R,G,B,lx_msg,rx_msg
```
where: 
* `R`,`G` and `B` are `int` numbers ranged beween `0 and 255`. They are used to assign a specific led color to the page.
* `lx_msg` and `rx_msg` are the midi messages associated to the left and right button for that specific page.
The messages themselves are formatted like this:
```
cc 3 44
``` 
The program will split the string using spaces as separators and expects to find:
* `cc` to define the type of midi message
* the first number is the `cc` number
* the second number is the `cc` value

## Hid mode
Since autoating `ableton live` with simple midi messages proved to be a pain in the back, I also made a firmware emating a `hid keyboard`, which basically sends keystrokes instead of `midi`. This firmware is in `src/hid`.

The config file for this firmare is basically the same as the midi one: the only difference is that the *message* fields are simply letters.