# File name: __main__.py
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout 
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.uix.scatter import Scatter
from kivy.uix.scatter import ScatterPlane
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import SlideTransition

from melodymatrix import MelodyMatrix
from fundmatrix import FundMatrix
from settingsjson import general_settings_json, fund_settings_json, melody_settings_json


class Tutorial(Screen):
	pass

class FundScatterPlane(ScatterPlane):
	def __init__(self, **kwargs):
		super(FundScatterPlane, self).__init__(**kwargs)
		self.do_scale = True
		self.do_translation = True

	def lock(self, state):
		if state == 'normal':
			self.do_scale = True
			self.do_translation = True
			return True
		if state == 'down':
			self.do_scale = False
			self.do_translation = False
			return True

class MelodyScatter(Scatter):
	def __init__(self, **kwargs):
		self.do_scale = True
		self.do_translation = True
		super(MelodyScatter,self).__init__(**kwargs)

	def lock(self, state):
		if state == 'normal':
			self.do_scale = True
			self.do_translation = True
			return True
		if state == 'down':
			self.do_scale = False
			self.do_translation = False
			return True

class RootWidget(RelativeLayout):
	def __init__(self, **kwargs):
		super(RootWidget, self).__init__(**kwargs)
		self.last_harmony_note = 'C'

class NoteGameApp(App):
	def __init__(self, **kwargs):
		super(NoteGameApp, self).__init__(**kwargs)
		self.link_to_fundmatrix = None
		self.link_to_melodymatrix = None

	def build(self):	
		self.title = "NoteGame"				#name displayed in menubar
		self.use_kivy_settings = False		#hide kivy options on settings screen
		config = self.config
		return RootWidget()

	#creates a config file if not present
	def build_config(self, config):
		config.setdefaults('Fundamental', {
			'octaves_up': 2,
			'octaves_down': 1,
			'fifths_up': 2,
			'fifths_down': 1,
			'thirds_up': 1,
			'thirds_down': 0,})
		config.setdefaults('Melody', {
			'octaves_up': 2,
			'octaves_down': 1,
			'fifths_up': 2,
			'fifths_down': 1,
			'thirds_up': 1,
			'thirds_down': 0,})
		config.setdefaults('General', {
			'boolexample': True,
			'scale': 'Major',
			'key': 'C',
			'stringexample': 'some_string',
			'pathexample': '/'})

	def build_settings(self, settings):
		settings.add_json_panel('General Options', self.config, data=general_settings_json)
		settings.add_json_panel('Fundamental Matrix', self.config, data=fund_settings_json)
		settings.add_json_panel('Melody Matrix', self.config, data=melody_settings_json)

	#executes the config changes
	def on_config_change(self, config, section, key, value):
		#this is an overwrought way to find the instances of MelodyMatrix & FundMatrix amongst the nested instances.
		if self.link_to_fundmatrix:
			if self.link_to_melodymatrix:
				pass
		else:
			for a in self.root.children:
				for b in a.children:
					for c in b.children:
						for d in c.children:
							for e in d.children:
								for f in e.children:
									f_name = str(type(f))
									if "FundMatrix" in f_name:
										self.link_to_fundmatrix = f
									for g in f.children:
										g_name = str(type(g))
										if "MelodyMatrix" in g_name:
											self.link_to_melodymatrix = g

		for i in self.link_to_fundmatrix.children:
			i.find_layouts()
		for i in self.link_to_melodymatrix.children:
			i.find_layouts()

		if section == 'General':		
			self.link_to_fundmatrix.get_config_variables()
			self.link_to_fundmatrix.redraw_layout()
			self.link_to_melodymatrix.get_config_variables()
			self.link_to_melodymatrix.redraw_layout()
			
		elif section == 'Fundamental':
			self.link_to_fundmatrix.get_config_variables()
			self.link_to_fundmatrix.redraw_layout()
			
		elif section == 'Melody':
			self.link_to_melodymatrix.get_config_variables()
			self.link_to_melodymatrix.redraw_layout()


if __name__ == '__main__':
	NoteGameApp().run()
