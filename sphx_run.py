# add sphx to python path and place sphx folder in home (maybe place it in python path heh)
# WRITE FUNCTIONS TO COMMUNICATE WITH PARENT SELENIUM SCRIPT
# SphxRun() IMPORT INTO SELENIUM SCRIPT  

from sphx_BETA import SphxRun
import os,sys
import time

if __name__ == '__main__':
	sphx = SphxRun()
	sphx.load_script(sys.argv[1])
	sphx.run_script()


	
	# add new name:window_id  key:value pair if api parses that out
	# if name arrives last in the script, window_id can be found here
	# window_name_id_links = {}

	
	# if 'nameActiveWindow' in line:
		# window_name_id_links[name] = self.xdopy.get_active_window()

# write readme that sudo apt install xdotool,
# installs opencv,tkinter, for ubuntu 16.04


