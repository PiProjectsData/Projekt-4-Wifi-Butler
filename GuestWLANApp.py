#!/usr/bin/env python3

from configparser import RawConfigParser
from glob import glob
from os.path import join
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock


class FilenameList:
	filename = []
	i = 0

	def addDirectory(self, name):
		self.filename.extend(glob(join(name, '*')))

	def current(self):
		if self.i >= len(self.filename):
			return ''
		else:
			return self.filename[self.i]

	def next(self):
		if self.i+1 >= len(self.filename):
			self.i = 0
		else:
			self.i += 1
		return self.current()

class SlideShow(Screen):
	slide = ObjectProperty(None)
	list = FilenameList()

	def on_touch_down(self, touch):
		global SM
		SM.get_screen('wlan').updatesettings()
		SM.transition.direction = 'left'
		SM.current = 'wlan'

	def addDirectory(self, name):
		self.list.addDirectory(name)

	def update(self):
		self.slide.source = self.list.current()

	def next(self, dt):
		self.slide.source = self.list.next()

class WLAN(Screen):
	wlanssid = StringProperty(None)
	wlanpsk = StringProperty(None)
	andorid_ios_qrcode = ObjectProperty(None)
	windows_qrcode = ObjectProperty(None)

	def updatesettings(self):
		wlancfg = RawConfigParser()
		wlancfg.read('/var/guestwlan/wlan.cfg')
		self.wlanssid = wlancfg.get('WLAN', 'wlanssid')
		self.wlanpsk =  wlancfg.get('WLAN', 'wlanpsk')
		self.android_ios_qrcode.reload()
		self.windows_qrcode.reload()

class ScreenManagement(ScreenManager):
	pass

class GuestWLAN(BoxLayout):
	pass

class GuestWLANApp(App):
	def build(self):
		global SM
		SM = self.root
		SlideShow = SM.get_screen('slideshow')
		SlideShow.addDirectory('/var/guestwlan/images')
		SlideShow.update()
		Clock.schedule_interval(SlideShow.next, 3)
		return SM

if __name__ == "__main__":
	GuestWLANApp().run()
