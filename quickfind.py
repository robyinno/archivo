#!/usr/bin/env python
from gi.repository import Gtk, WebKit
import os, sys
import locale
import gettext

APP = 'quickfindhome'
DIR = 'po'
#DIR ='/home/roby/software/quickfind/pygtk_quickfind/proto/po'

#locale_str = locale.setlocale(locale.LC_ALL,"en_US.utf8")

gettext.bindtextdomain(APP,DIR)
gettext.textdomain(APP)
lang = gettext.translation(APP, DIR)#,languages=[locale_str]
_ = lang.gettext

#gettext.install(APP, DIR)
#_ = gettext.gettext


languages={0:'it_IT.utf8',1:'en_US.utf8',2:'es_ES.utf8',3:'fr_FR.utf8',4:'pt_PT.utf8',5:'de_DE.utf8',6:'nl_NL.utf8'}
language_directory = {'it_IT':'Italiano','en_US.utf8':'English','es_ES.utf8':'Espanol','fr_FR':'Francais','pt_PT':'Portugue','de_DE':'Deutsch'}
UI_FILE='quickfindhome.ui'
ARCHIVO_DIR='/home/roby/Archivo/'

class QuickHome:
	def __init__(self):
		self.language,spare = locale.getlocale()
		self.builder = Gtk.Builder()
		self.builder.set_translation_domain(APP)
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)
		self.window = self.builder.get_object('qfhome')
		self.webview = WebKit.WebView()
		scrolled_window = self.builder.get_object('scrolledwindow')
		scrolled_window.add(self.webview)
		self.go_home(lang)
		self.window.show_all()

	def destroy(self, window):
		Gtk.main_quit()

	def on_home_clicked(self,button):
		self.go_home()

	def on_button_clicked(self,button):
		if button.get_stock_id() == Gtk.STOCK_GO_BACK:
			self.webview.go_back()

	def on_exit_clicked(self,button):
		Gtk.main_quit()

	def on_search_clicked(self,button):
		# apre una nuova finestra quella di ricerca
		app = QuickSearch()
		#Gtk.main_quit() # provvisorio

	def on_lang_changed(self,button,data=None):
		# cambia la lingua
		list_store = button.get_model()
		active_index = button.get_active()
		active_text = list_store[active_index][0]
		if active_text != None:
			try:
				self.language = locale.setlocale(locale.LC_ALL,languages[active_index])
				#self.builder.set_translation_domain(APP)
			except locale.Error:
				self.language = languages[active_index]
			lang = gettext.translation(APP, DIR,languages=[self.language])
			self.load_lang_labels(lang)
			self.go_home(lang)
			label1=self.builder.get_object('lab_lang_selected')
			label1.set_text(active_text)

	def load_lang_labels(self,lang):
		_ = lang.gettext
		self.window.set_title(_('Archivio dei documenti'))
		self.builder.get_object('homepage').set_tooltip_text(_('home page'))
		self.builder.get_object('cerca').set_tooltip_text(_('cerca'))
		self.builder.get_object('back').set_tooltip_text(_('indietro'))
		self.builder.get_object('risultati ricerca').set_tooltip_text(_('risultato ricerca'))
		self.builder.get_object('uscita').set_tooltip_text(_('Uscita'))
		
	def go_home(self,lang):
		_ = lang.gettext
		uri='file://%s/%s'%(ARCHIVO_DIR,_('path_file_home_page'))
		label1=self.builder.get_object('lab_lang_selected')
		label1.set_text(uri)
		self.webview.load_uri(uri)
		
	
class QuickSearch:
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.set_translation_domain(APP)
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)
		self.window = self.builder.get_object('qfsearch')
		#self.window.set_back_pixmap('trovaing.jpg')
		self.window.show_all()
	
def main():
	app = QuickHome()
	Gtk.main()

if __name__ == "__main__":
	main()
