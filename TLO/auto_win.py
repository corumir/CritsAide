import curses

class auto_win():

	def __init__(self):
		self.win = None 
		self.cursor = {'x_pos': 0, 'y_pos': 0, 'x_str': 0, 'y_str': 0}
		self.h_pos = -1
		self.string = ''
		self.disp_opt = []
		
	def win_init(self):
		self.win = curses.initscr()
		curses.start_color()
		curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
		curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
		curses.noecho()
		curses.cbreak()
		self.win.clear()
		self.win.keypad(True)

	def win_close(self):
		self.win.keypad(False)
		curses.nocbreak()
		curses.echo()
		curses.endwin()
	
	def display(self, options, i):
		self.win.move(self.cursor['x_str'] + 1, self.cursor['y_str'])
		for loop in range(len(self.disp_opt)):
			self.win.deleteln()

		self.disp_opt = []
		for option in options:
			if (self.string != '') and option[0:-1].lower().startswith(self.string.lower()):
				self.disp_opt.append(option)
		option_pos = [self.cursor['x_pos'] + 1, self.cursor['y_str']]

		if i-1 < self.h_pos < len(self.disp_opt)-1+i:
			pass
		elif self.h_pos < i-1:
			self.h_pos = i-1
		elif self.h_pos > len(self.disp_opt)-1+i:
			self.h_pos = len(self.disp_opt)-1+i

		for x in range(len(self.disp_opt)):
			if x == self.h_pos-i:
				self.win.addstr(option_pos[0] + x, option_pos[1], self.disp_opt[x], curses.color_pair(1))
			else:
				self.win.addstr(option_pos[0] + x, option_pos[1], self.disp_opt[x], curses.color_pair(2))
		self.win.move(self.cursor['x_str'], self.cursor['y_pos'])
		self.win.refresh()

	def auto_complete(self, info):
		#info is a list of tuples of the format (field_value, required?, options)
		#field_value <type> = string
		#required? <type> = Boolean
		#options <type> = list of strings

		self.win_init()
		try:
			self.win.nodelay(1)
			results = {}
			for i in range(len(info)):
				if info[i][2] == None:
					options = ''
				else:
					options = info[i][2]
				
				field = info[i][0]+': '

				self.h_pos = i-1
				self.string = ''
				self.disp_opt = []
				self.cursor['y_str'] = len(field)
				self.cursor['y_pos'] = self.cursor['y_str']
				self.cursor['x_str'] = i
				self.cursor['x_pos'] = self.cursor['x_str']
				
				if info[i][1] == True:
					self.win.addstr(self.cursor['x_str'], 0, field, curses.color_pair(3))
				else:
					self.win.addstr(self.cursor['x_str'], 0, field)

				while True:
					c = self.win.getch()

					if c == 10: #return Key
						if self.h_pos-i >= 0:
							cursor_diff = len(self.disp_opt[self.h_pos-i])-len(self.string)
							self.cursor['y_pos'] = self.cursor['y_pos'] + cursor_diff
							self.string = self.disp_opt[self.h_pos-i]
							self.win.addstr(self.cursor['x_str'], self.cursor['y_str'], self.string)
							self.display(options, i)
							results[info[i][0]] = self.string
						else:
							results[info[i][0]] = self.string
						
						break

					elif (c in range(32, 127)): #alphanumeric, special chars, spacebar
						self.string = self.string + chr(c)
						self.win.addstr(self.cursor['x_str'], self.cursor['y_str'], self.string)
						self.cursor['y_pos'] += 1
						self.display(options, i)

					elif c == 127: #backspace
						if self.cursor['y_pos'] != self.cursor['y_str']:
							self.string = self.string[0:-1]
							self.cursor['y_pos'] -= 1
							self.win.delch(self.cursor['x_str'], self.cursor['y_pos'])
						self.display(options, i)

					elif c == curses.KEY_DOWN: #arrow down
						self.h_pos += 1
						self.display(options, i)

					elif c == curses.KEY_UP: #arrow up
						self.h_pos -= 1
						self.display(options, i)

					elif c == 9: #tab
						if len(self.disp_opt) > 0:
							cursor_diff = len(self.disp_opt[0])-len(self.string)
							self.cursor['y_pos'] = self.cursor['y_pos'] + cursor_diff
							self.string = self.disp_opt[0]
							self.win.addstr(self.cursor['x_str'], self.cursor['y_str'], self.string)
							self.display(options, i)

		except:
			self.win_close()
			raise
		
		self.win_close()
		return results