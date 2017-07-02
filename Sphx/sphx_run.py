from sphx import SphxRun
import os,sys
import time

if __name__ == '__main__':
	sphx = SphxRun()
	sphx.load_script(sys.argv[1])
	sphx.run_script()


# write readme that sudo apt install xdotool,
# installs opencv,tkinter, for ubuntu 16.04


