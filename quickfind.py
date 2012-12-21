#!/usr/bin/env python
from gi.repository import Gtk, WebKit
import os, sys

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
		label1=self.builder.get_object('label1')
		label1.set_text(uri)

	def on_button_clicked(self,button):
		if button.get_stock_id() == Gtk.STOCK_GO_BACK:
			self.webview.go_back()

	def on_exit_clicked(self,button):
		Gtk.main_quit()

	#def on_search_clicked(self,button):
		# apre una nuova finestra quella di ricerca

	#def on_language_changed(self):
		# cambia la lingua

def main():
	app = QuickHome()
	Gtk.main()

if __name__ == "__main__":
	main()
