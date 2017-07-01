## Description

Sphx is an automation tool for Python 2.7 using Tkinter, Opencv3, Xdotool, and gnome-screenshot.
SphxUI collects 'Gui Pieces' which are snapshots from the Desktop GUI that are located at any point.
SphxRun will run a script built in the SphxUI, including mouse actions, keyboard actions, and window actions.


## Run

To run Sphx UI, cd to Sphx directory and type:

python sphx.py

To run a .sphx script, cd to Sphx directory and type:

python sphy_run.py script_name.sphx


## Screenshots

![Sphx Script Example](/img/gmail_login.png?raw=true "Sphx")

## Motivation

Sphx is inspired by the Sikuli project [Sikuli](http://sikulix.com), written in Python 2.7 using Tkinter, Opencv3, Xdotool, and gnome-screenshot utility for a vm or normal (X)Ubuntu 16.04.

## Installation

To install Opencv3 for Python 2.7:
[Opencv3 installation script for Python 2.7](https://gist.github.com/sbrugman/f9d897f28e674f7a89bbf131e26b98b0)

To install xdotool and gnome-screenshot:

sudo apt update

sudo apt install xdotool gnome-screenshot

## Sphx UI Reference

GUI PIECES

The GUI PIECES column on the left side of the Sphx UI is a list of 50 buttons with which to store "Gui Pieces". Gui Pieces are selected snapshots of the desktop interface to be matched against current full desktop screenshots.
This matching returns the current location of the Gui Piece. Sphx Script actions can identify if a Gui Piece exists, wait for it to appear or disappear, and find the location of this piece which can then be acted upon with mouse actions.
Clicking on a populated Gui Piece button causes a popup window showing the Gui Piece.
The 'Take New' button drops the Sphx UI and waits until a selection of the Desktop is taken. The saved Gui Piece is assigned a unique 9 character name and stored in /path/to/Sphx/GuiPieces.
The 'Load Png' button (not currently active) opens a dialog to select a .png to add to the Sphx script Gui Piece library. This is for cases with which the capture of certain images, such as popup windows, might be quite difficult without using other methods.
The 'Remove' button turns all buttons red and waits for the user to select which Gui Piece to remove. This also will replace all instances of the Gui Piece in the Script Pad with right-click, which will result in a faulty script unless these are replaced.

SCRIPT BUILD

The SCRIPT BUILD column in the center of the Sphx UI is for building a Sphx script. Actions to be appended to the script are in the SCRIPT ACTIONS column with default values, but a Sphx script can be written into the Script Pad without needing to click the buttons if it is written properly.
With any Gui Piece action, which involves locating a Gui Piece, the chosen Gui Piece filename is highlighted in blue. If this filename does not match any of the Gui Pieces in the GUI PIECES column, it can be right-clicked upon for further options.
Upon right-clicking a Gui Piece in the Script Pad a menu pops up with 'Take New','View', and 'Choose From Others'. 'Take New' replaces this Gui Piece with a new snapshot. 'View' opens a popup window to view the Gui Piece png. 'Choose From Others' turns all the Gui Pieces buttons red to the left of the Script Pad and locks the interface until a new Gui Piece is chosen (the same Gui Piece can be chosen).
For any text or key action, the text or key-codes to be sent are highlighted in green. For all actions except 'type_text_file', right-clicking this highlighted text will open a window to allow typing of either a string or set of key-codes (Example:  Return+Backspace), which is then added to the Script Pad upon pressing Return. With 'type_text_file', the highlighted text is the name of a file that is stored in /path/to/Sphx/TxtFiles, which when right-clicked upon will open a file dialog to select a .txt file.   
For the 'name_active_window' action, a name ('window00' to start and increment for new windows) is linked to the current id of the active window. Later in the script, this name can be referenced if the window is to be minimized or activated. The 'name_active_window' action has the window name highlighted in gray, with no right-click options. Any usage of this window in further actions will result in a pink highlight that can be right-clicked upon to replace with other available window names.

SCRIPT ACTIONS

The SCRIPT ACTIONS column is a list of action buttons which will append to the Script Pad in the SCRIPT BUILD column. Each action button will append the proper script line to the Script Pad with the default values of all variables that must be included. Click, Type, Key, and Window actions are self-explanatory and are described in the previous section. 'set_threshold' will append a line that allows the threshold of the Gui Piece match to be adjusted. A lower threshold percent (percent<90) allows for matches that might have a slight variation from the original Gui Piece or are more oblong. The sleep action allows for a pause in the script measured in seconds.
When 'Auto-snap' is checked, every action that requires a Gui Piece will automatically hide the Sphx UI to capture a snapshot of the desktop. Unchecked, this will append blank Gui Pieces to the Script Pad.
 

## SphxRun API Reference

Example:

from Sphx import SphxRun

sphx_script = SphxRun()

sphx_script.load_script('script.sphx')

sphx_script.run_script()



