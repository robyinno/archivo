#!/usr/bin/env python
from gi.repository import Gtk, WebKit
import os, sys
import locale
import gettext

APP = 'quickfind'
DIR = 'locale'

locale.setlocale(locale.LC_ALL,'')
gettext.bindtextdomain(APP,DIR)
gettext.textdomain(APP)
_ = gettext.gettext

UI_FILE='quickfindhome.ui'
ARCHIVO_DIR='/home/roby/Archivo/'
LANG='Italiano'

class QuickHome:
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)
		self.window = self.builder.get_object('qfhome')
		self.webview = WebKit.WebView()
		scrolled_window = self.builder.get_object('scrolledwindow')
		scrolled_window.add(self.webview)
		self.window.show_all()

	def destroy(self, window):
		Gtk.main_quit()

	def on_home_clicked(self,button):
		uri='file://%s%s/archital.htm'%(ARCHIVO_DIR,LANG)
		self.webview.load_uri(uri)
		label1=self.builder.get_object('lab_lang_selected')
		label1.set_text(uri)

	def on_button_clicked(self,button):
		if button.get_stock_id() == Gtk.STOCK_GO_BACK:
			self.webview.go_back()

	def on_exit_clicked(self,button):
		Gtk.main_quit()

	def lang_changed(self,button):
		change_language()

	def on_search_clicked(self,button):
		# apre una nuova finestra quella di ricerca
		Gtk.main_quit() # provvisorio

	def on_lang_changed(self,button,data=None):
		# cambia la lingua
		list_store = button.get_model()
		active_index = button.get_active()
		active_text = list_store[active_index][0]
		if active_text != None:
			label1=self.builder.get_object('lab_lang_selected')
			label1.set_text(active_text)

def main():
	app = QuickHome()
	Gtk.main()

if __name__ == "__main__":
	main()
