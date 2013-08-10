#!/usr/bin/env python
from gi.repository import Gtk, WebKit
import os, sys
import locale
import gettext
import logging
logging.basicConfig(filename='/tmp/quickfind.log',level=logging.DEBUG,format="%(asctime)s - %(levelname)s - %(message)s")

APP = 'quickfindhome'
DIR = 'po'
HTM_RESULT ='Quickfind.htm'
HTM_RES_SX ='qf_sx.htm'
TMP_DIR = 'tmp'
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

g_language,spare = locale.getlocale()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class QuickHome:
	def __init__(self):
		self.language = g_language
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
		# open new search windows
		app = QuickSearch()

	def on_lang_changed(self,button,data=None):
		# change language
		global g_language
		list_store = button.get_model()
		active_index = button.get_active()
		active_text = list_store[active_index][0]
		# get language index 
		if active_text != None:
			try:
				# get language name code-page from index
				g_language= self.language = locale.setlocale(locale.LC_ALL,languages[active_index])
				#self.builder.set_translation_domain(APP)
			except locale.Error:
				g_language = self.language = languages[active_index]
				
			lang = gettext.translation(APP, DIR,languages=[self.language])
			self.load_lang_labels(lang)
			self.go_home(lang)
			#label1=self.builder.get_object('lab_lang_selected')
			#label1.set_text(active_text)

	def load_lang_labels(self,lang):
		_ = lang.gettext
		self.window.set_title(_('Archivio dei documenti'))
		self.builder.get_object('homepage').set_tooltip_text(_('home page'))
		self.builder.get_object('homepage').set_label(_('home page'))
		self.builder.get_object('cerca').set_tooltip_text(_('cerca'))
		self.builder.get_object('cerca').set_label(_('cerca'))
		self.builder.get_object('back').set_tooltip_text(_('indietro'))
		self.builder.get_object('back').set_label(_('indietro'))
		self.builder.get_object('risultati ricerca').set_tooltip_text(_('risultato ricerca'))
		self.builder.get_object('risultati ricerca').set_label(_('risultato ricerca'))
		self.builder.get_object('uscita').set_tooltip_text(_('Uscita'))
		self.builder.get_object('uscita').set_label(_('Uscita'))
		
		
		
	def go_home(self,lang):
		_ = lang.gettext
		uri='file://%s/%s'%(ARCHIVO_DIR,_('path_file_home_page'))
		#label1=self.builder.get_object('lab_lang_selected')
		#label1.set_text(uri)
		self.webview.load_uri(uri)
		
class QuickResult:
	def __init__(self,result):
		self.language = g_language
		self.type_search = None
		
		try:
			lang = gettext.translation(APP, DIR,languages=[self.language])
		except locale.Error,e:
			logging.exception(e)
			self.language,spare = locale.getlocale()
			
		self.builder = Gtk.Builder()
		self.builder.set_translation_domain(APP)
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)
		self.window = self.builder.get_object('qfresult')
		#self.window.set_back_pixmap('trovaing.jpg')
		self.webview = WebKit.WebView()
		scrolled_window = self.builder.get_object('scrolledwindow')
		scrolled_window.add(self.webview)
		self.load_lang_labels(lang)
		self.view_result(result)
		self.window.show_all()
		
	def load_lang_labels(self,lang):
		_ = lang.gettext
		self.window.set_title(_('Risultato'))
	
	def _prep_qf_sx(self,result):
		from cStringIO import StringIO
		file_html = StringIO()
		html = """<html>
   <head>
      <link rel='stylesheet' type='text/css' href='quickfind.css'>
   </head>
   <body bgproperties='fixed' background='sfondosx.jpg' oncontextmenu='return false;'>"""
	  	file_html.write(html)
	  	
		row_html ="""&nbsp;<a target='f_dx' href='%s' title='%s'><img border='0' src='check.gif'></a>
	<font face='Arial' size='2' color='#000000'><b>&nbsp;&nbsp;&nbsp;<a target='f_dx' href='%s' title='%s'>%s</a>
	</b></font><br>"""
	
		for row in result:
			file_name = os.path.splitext(os.path.basename(row['nome_doc_pdf']))[0] # estract only file_name, without extension
			file_html.write(row_html%(row['nome_doc_rtf'],row['nome_doc_rtf'],row['nome_doc_pdf'],row['nome_doc_pdf'],file_name))	
		
		file_html.write("""</body></html>""")
		return file_html.getvalue()
		
	def view_result(self,result):
		#qf_sx.htm
		html_sx = self._prep_qf_sx(result)
		f = open(os.getcwd() + '/' + TMP_DIR + '/' + HTM_RES_SX,'w')
		f.write(html_sx)
		f.close()
		
		#prepare others html
		#qf_dx.htm # fixed
		#qf_top.htm 
		uri='file://%s/%s'%(os.getcwd() + '/' + TMP_DIR,HTM_RESULT)
		#label1=self.builder.get_object('lab_lang_selected')
		#label1.set_text(uri)
		self.webview.load_uri(uri) 
		
class QuickSearch:
	def __init__(self):
		self.language = g_language
		self.type_search = None
		#locale.setlocale(locale.LC_ALL,self.language)
		
		try:
			lang = gettext.translation(APP, DIR,languages=[self.language])
		except locale.Error,e:
			logging.exception(e)
			self.language,spare = locale.getlocale()
			
		self.builder = Gtk.Builder()
		self.builder.set_translation_domain(APP)
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)
		self.window = self.builder.get_object('qfsearch')
		
		#self.window.set_back_pixmap('trovaing.jpg')
		self.load_lang_labels(lang)
		self.window.show_all()
		
	def on_type_search_change(self,button):
		list_store = button.get_model()
		active_index = button.get_active()
		if active_index != -1:
			self.type_search = list_store[active_index][0]
	
	def on_start_search(self,button):
		import sqlite3
		conn = sqlite3.connect('quickfind.db')
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		text_to_search = self.builder.get_object('testo_da_cercare').get_text()
		
		type_search = self.type_search
		if type_search != None:
			if len(type_search) > 8:
				type_search = type_search[0:8].lower()
		
		sql = """SELECT tab_rows.id_doc, tab_rows.txt_row, tab_docs.ds_lang, tab_docs.nome_doc_rtf, tab_docs.nome_doc_pdf
				FROM tab_rows INNER JOIN tab_docs ON tab_rows.id_doc = tab_docs.id_doc where ds_lang=:lang and txt_row like '%:text_to_search%' """
				
		if language_directory.has_key(self.language):
			lang = language_directory[self.language]
			lang = lang[0:3].lower()
		else:
			lang = 'ita'
			
		#param = {'lang':lang,'text_to_search':text_to_search}
		
		sql = """SELECT tab_rows.id_doc, tab_rows.txt_row, tab_docs.ds_lang, tab_docs.nome_doc_rtf, tab_docs.nome_doc_pdf
				FROM tab_rows INNER JOIN tab_docs ON tab_rows.id_doc = tab_docs.id_doc where ds_lang='""" + lang + "' and txt_row like '%" + text_to_search +"%'"
				
		if type_search != None:		
			sql = sql + " and nome_doc_pdf like '%" + type_search + "%'"
			#param.append(type_search)
		
		#cursor.execute(sql,param)
		cursor.execute(sql)
		result = cursor.fetchall()
		QuickResult(result)
				
	def load_lang_labels(self,lang):
		_ = lang.gettext
		self.window.set_title(_('Ricerca'))
		self.builder.get_object('testo_da_cercare').set_tooltip_text(_('Scrivi qui...'))
		self.builder.get_object('testo_da_cercare').set_text(_('Scrivi qui...'))
		self.builder.get_object('inizia_ricerca').set_tooltip_text(_('inizia ricerca'))
		self.builder.get_object('inizia_ricerca').set_label(_('inizia ricerca'))
		self.builder.get_object('chiudi').set_tooltip_text(_('chiudi'))
		self.builder.get_object('chiudi').set_label(_('chiudi'))
		self.builder.get_object('pausa').set_tooltip_text(_('pausa'))
		self.builder.get_object('pausa').set_label(_('pausa'))
		self.builder.get_object('interrompi').set_tooltip_text(_('interrompi'))
		self.builder.get_object('interrompi').set_label(_('interrompi'))
		liststore = self.builder.get_object('liststore2')
		liststore.clear()
		liststore.append([_('in tutte le cartelle')])
		liststore.append([_('Appunti')])
		liststore.append([_('Conferenze')])
		liststore.append([_('Interviste')])
		liststore.append([_('Libri')])
		liststore.append([_('Materiali')])
		liststore.append([_('Riunioni')])
		liststore.append([_('Seminari')])

		#liststore.set(0,0,'cippa')
	#def on_type_search_change(self):
		# change type of search
	
		
def main():
	app = QuickHome()
	Gtk.main()

if __name__ == "__main__":
	main()
