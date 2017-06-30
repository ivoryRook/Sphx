import os

class SphxData():

	MAIN_PATH = os.path.dirname(__file__)
	GUI_PIECE_DIR = 'GuiPieces'
	SCRIPT_DIR = 'Scripts'
	
	GUI_ACTIONS = ['exists?','wait_to_appear','wait_to_disappear','click','double_click','rapid_click','mouse_release','mouse_hold','hover']
	KEYBOARD_ACTIONS = ['type_text','send_key']
	WINDOW_ACTIONS = ['name_active_window','activate_window','minimize_window']
	OTHER_ACTIONS = ['sleep','set_threshold']


