import os

class SphxData():

	MAIN_PATH = os.path.dirname(__file__)
	GUI_PIECE_DIR = 'GuiPieces/'
	SCRIPT_DIR = 'Scripts/'
	TXT_FILE_DIR = 'TxtFiles/'
	
	GUI_ACTIONS = [
		('exists?','exists? {0};\n'),
		('wait_to_appear','wait_to_appear {0} max_wait=60;\n'),
		('wait_to_disappear','wait_to_disappear {0} max_wait=60;\n'),
		('click','click {0} button=1;\n'),
		('double_click','double_click {0} button=1;\n'),
		('rapid_click','rapid_click {0} button=1 clicks=3;\n'),
		('mouse_hold','mouse_hold {0} button=1;\n'),
		('mouse_release','mouse_release {0} button=1;\n'),
		('hover','hover {0};\n')
	]
	
	KEYBOARD_ACTIONS = [
		('type_text','type_text {0};\n'),
		('type_text_file','type_text_file {0};\n'),
		('send_key','send_key {0};\n'),
		('send_keydown','send_keydown {0};\n'),
		('send_keyup','send_keyup {0};\n')
	]
	WINDOW_ACTIONS = [
		('name_active_window','name_active_window {0};\n'),
		('activate_window','activate_window {0};\n'),
		('minimize_window','minimize_window {0};\n')
	]
	OTHER_ACTIONS = [
		('set_threshold','set_threshold percent=90;\n'),
		('sleep','sleep seconds=1;\n')
	]


