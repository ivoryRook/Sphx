# python 2.7 code

from subprocess import call,check_output,Popen,PIPE
from itertools import combinations
import pyscreenshot
import numpy as np
import cv2
import os,time

class XdoPy(object):

	def __init__(self,window_index=0):
		
		# for building shpx scripts, if opening script midway
		# then remember to restore window_index to continue building correctly
		# there might be no way to get the correct window index
		# because for get_active_window to increment the index
		# it must check the list of others for repeats (self.window_id_links.values())
		# and that list of others can't be restored because it might change
		self.window_index = window_index
		
		# restore upon open_script
		self.window_id_links = []
		self._cmd_args = ['xdotool']
		
		

		return
	
	def get_active_window(self):
		self._cmd_args += ['getactivewindow']
		xdo_out = check_output(self._cmd_args).strip()
		self.active_window_id = xdo_out
		self._cmd_args=['xdotool']
		return
		
	def get_window_geometry(self,window_id=None):
		self._cmd_args += ['getwindowgeometry',window_id]
		xdo_out = check_output(self._cmd_args).strip()
		x,y = map(int,xdo_out.partition('Position: ')[2].partition(' (screen')[0].split(','))
		w,h = map(int,xdo_out.partition('Geometry: ')[2].split('x'))
		self._cmd_args=['xdotool']
		return x,y,w,h

	def minimize_window(self,window_id=None):
		self._cmd_args += ['windowminimize',window_id]
		call(self._cmd_args)
		self._cmd_args=['xdotool']
		return

	def activate_window(self,window_id=None):
		self._cmd_args += ['windowactivate',window_id]
		call(self._cmd_args)
		self._cmd_args=['xdotool']
		return

	# 				mouse functions, todo: hold, release

	def get_mouse_location(self):
		self._cmd_args += ['getmouselocation']
		xdo_out = check_output(self._cmd_args).strip()
		mouse_x = int(xdo_out.partition('x:')[2].partition('y:')[0])
		mouse_y = int(xdo_out.partition('y:')[2].partition('screen')[0])
		self._cmd_args=['xdotool']
		return mouse_x,mouse_y

	def mouse_moveto(self,x,y):
		self._cmd_args += ['mousemove',str(x),str(y)]
		call(self._cmd_args)
		self._cmd_args=['xdotool']
		return
			
	def mouse_click(self,button='1',click_count=1,wait_between=0.0):
		
		self._cmd_args += ['click',button]
		for clicks in range(click_count):		
			call(self._cmd_args)
			if wait_between > 0.0:
				time.sleep(wait_between)
		self._cmd_args=['xdotool']
		return

	def mouse_moveto_click(self,x,y,button='1',click_count=1,wait_between=0.0):
		self._cmd_args += ['mousemove',str(x),str(y),'click',button]
		for clicks in range(click_count):		
			call(self._cmd_args)
			if wait_between > 0.0:
				time.sleep(wait_between)
		self._cmd_args=['xdotool']
		return
	
	def drag(self,x0,y0,x1,y1):
		self._cmd_args += ['mousemove',str(x0),str(y0),'mousedown','1','mousemove',str(x1),str(y1),'mouseup','1']
		call(self._cmd_args)
		self._cmd_args=['xdotool']
		return


	
	# 				keyboard functions

	def type_to(self,text,window_id=None):
		if window_id is None:
			self._cmd_args += ['type',"{0}".format(text)]
		else:
			self._cmd_args += ['type','--window',window_id,"{0}".format(text)]
		call(self._cmd_args)
		self._cmd_args=['xdotool']
		return

	def send_key(self,text,window_id=None):
		if window_id is None:
			self._cmd_args += ['key',"{0}".format(text)]
		else:
			self._cmd_args += ['key','--window',window_id,"{0}".format(text)]
		call(self._cmd_args)
		self._cmd_args=['xdotool']
		return


class GuiPiece(object):
	
	def __init__(self,main_path,gui_dir='GuiPieces',threshold=.9):
		self.main_path = main_path
		self.gui_dir = gui_dir
		self.threshold = threshold
		self.gui_bbox = None
		self.gui_piece_cv = None
		self.gui_screenshot_cv = None
		return

	# generate new gui_piece filename, assign self.gui_piece_filename
	def __new_gui_piece_filename(self):
		import string
		from random import choice
		self.used_gui_pieces = os.listdir(self.gui_dir)
		while True:
			random_id = ''.join(choice(string.ascii_letters + string.digits) for _ in range(9))
			new_piece = '{}.png'.format(random_id)
			if new_piece not in self.used_gui_pieces:
				self.used_gui_pieces.append(new_piece)
				break
		self.gui_piece_filename = new_piece
		return
	
	# take a full screenshot of gui
	# if self.gui_bbox is provided earlier take screenshot within bounds
	def __take_gui_screenshot_cv(self):
		if self.gui_bbox:
			gui_screenshot = pyscreenshot.grab(bbox=self.gui_bbox)
		else:
			gui_screenshot = pyscreenshot.grab()
		self.gui_screenshot_cv = cv2.cvtColor(np.array(gui_screenshot), cv2.COLOR_BGR2GRAY)
		self.match_found = False
		return

	# remove points that are within w,h of the first point and each other
	def __fix_overlap(self,points):
		new_points = points
		if len(points) > 1:
			for combo in list(combinations(sorted(points,key=lambda point:point[1]),2)):
				x0,y0,x1,y1 = combo[0]+combo[1]
				sum_dim = self.gui_piece_width+self.gui_piece_height
				if abs(x1-x0)+abs(y1-y0) < sum_dim and combo[1] in new_points:
					new_points.remove(combo[1])
		return new_points

	# fill self.centers and self.top_lefts with points
	def __match_template_cv(self):
		self.__take_gui_screenshot_cv()
		gui_match = cv2.matchTemplate(self.gui_screenshot_cv,self.gui_piece_cv,cv2.TM_CCOEFF_NORMED)
		zip_loc = zip(*np.where(gui_match >= self.threshold)[::-1])
		if len(zip_loc) > 0:
			self.match_found = True
			w,h = self.gui_piece_width,self.gui_piece_height
			centers = [(point[0]+w/2,point[1]+h/2) for point in zip_loc]
			self.centers = self.__fix_overlap(centers)
			top_lefts = [(point[0],point[1]) for point in zip_loc]
			self.top_lefts = self.__fix_overlap(top_lefts)
		else:
			self.match_found = False
			self.centers,self.top_lefts = [],[]
		return

	# convert gui piece to cv
	def convert_png_to_cv(self,gui_piece_filename):
		gui_piece_full_path = os.path.join(self.gui_dir,gui_piece_filename)
		gui_piece_cv = cv2.imread(gui_piece_full_path,0)
		return gui_piece_cv
	
	
	#			NEXT THREE FUNCTIONS DIFF WAYS OF GETTING NEW GUIPIECE
	
	# load a pre-saved gui_piece from 'GuiPieces/', reassign self.gui_piece_filename
	# assign self.gui_piece_cv,self.gui_piece_width,self.gui_piece_height
	def load_saved_gui_piece(self,gui_piece_filename):
		self.gui_piece_filename = gui_piece_filename
		self.gui_piece_cv = self.convert_png_to_cv(self.gui_piece_filename)
		self.gui_piece_width,self.gui_piece_height = self.gui_piece_cv.shape[::-1]
		return

	def load_saved_gui_piece_cv(self,gui_piece_cv):
		self.gui_piece_cv = gui_piece_cv
		self.gui_piece_width,self.gui_piece_height = self.gui_piece_cv.shape[::-1]
		return
	
	# load an image into gui_piece_cv and copy/rename into 'GuiPieces/'
	def load_foreign_gui_piece(self,path_to_file):
		gui_piece_cv = cv2.imread(path_to_file,0)
		self.__new_gui_piece_filename()
		cv2.imwrite(os.path.join(self.gui_dir,self.gui_piece_filename),gui_piece_cv)
#		print("\tGUI Piece saved in {0} as {1}".format(self.gui_dir,self.gui_piece_filename))
		self.gui_piece_cv = gui_piece_cv
		self.gui_piece_width,self.gui_piece_height = self.gui_piece_cv.shape[::-1]
		return
	
	# activate gnome-screenshot to select an area of screen 
	# for new gui_piece_cv and save/name into 'GuiPieces'
	def take_new_gui_piece(self):
		# context manager for clean gnome-screenshot open and close
		from contextlib import contextmanager
		@contextmanager
		def gnomepopen(cmd_args):
			popen = Popen(cmd_args,stdout=PIPE,stderr=PIPE)
			yield popen
			popen.stdout.close()
			popen.stderr.close()
		self.__new_gui_piece_filename()
		full_gui_piece_filename = os.path.join(self.main_path,self.gui_dir,self.gui_piece_filename)
		cmd_args = ['gnome-screenshot','-a','--file={0}'.format(full_gui_piece_filename)]
#		print("\tSelect a GUI Piece")
		with gnomepopen(cmd_args) as popen_:
			popen_.wait()
		self.gui_piece_cv = self.convert_png_to_cv(self.gui_piece_filename)
#		print("\tGUI Piece saved in {0} as {1}".format(self.gui_dir,self.gui_piece_filename))
		self.gui_piece_width,self.gui_piece_height = self.gui_piece_cv.shape[::-1]
		return

	# PRIMARY GUIPIECE LOCATE FUNCTION
	# return top_left or center point of templates within w,h away from each other
	def get_current_locations(self,click_region='center'):
		if self.gui_piece_cv is None:
#			print('NO TEMPLATE SAVED')
			return None
		self.__match_template_cv()
		if click_region is 'center':
			return self.centers
		if click_region is 'top_left':
			return self.top_lefts
	
	# if timed out, returns false, otherwise true if found
	def wait_for_template(self,max_wait):
		start_wait = time.time()
		while True:
			self.__match_template_cv()
			if self.match_found:
				break
			else:
				if time.time()-start_wait > max_wait:
					break
		return self.match_found

	def wait_for_template_disappear(self,max_wait):
		start_wait = time.time()
		while True:
			self.__match_template_cv()
			if not self.match_found:
				break
			else:
				if time.time()-start_wait > max_wait:
					break
		return not self.match_found









