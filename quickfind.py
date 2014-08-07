#!/usr/bin/env python
from gi.repository import GLib, Gtk, Gdk, GObject,WebKit

import threading, thread
import os, sys
import locale
import gettext
import logging
import helpers
import subprocess

import ConfigParser
config = ConfigParser.ConfigParser()
config.readfp(open(os.getcwd() + '/quickfind.ini'))
RootPath = config.get('QuickFind','RootPath')
DBName = config.get('QuickFind','DBName')

logging.basicConfig(filename='/tmp/quickfind.log',level=logging.DEBUG,format="%(asctime)s - %(levelname)s - %(message)s")

APP = 'quickfindhome'
DIR = 'po'
HTM_RESULT ='Quickfind.htm'
HTM_RES_SX ='qf_sx.htm'
HTM_RES_TOP ='qf_top.htm'

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
UI_FILE_HOME='quickhome.ui'
UI_FILE_SEARCH='quicksearch.ui'
UI_FILE_RESULT='quickresult.ui'
ARCHIVO_DIR=RootPath

g_language,spare = locale.getlocale()

class QuickHome:
	def __init__(self):
		handlers = { 
					"on_home_clicked" : self.on_home_clicked,
				  }
		self.language = g_language
		self.builder = Gtk.Builder()
		self.builder.set_translation_domain(APP)
		self.builder.add_from_file(UI_FILE_HOME)
		#self.builder.add_objects_from_file(UI_FILE,("qfhome"))
		
		self.builder.connect_signals(self)
		self.window = self.builder.get_object('qfhome')
		self.webview = WebKit.WebView()
		self.webview.connect("download-requested", self.on_download_requested)
		#self.webview.connect("navigation-requested", self.on_navigation_requested)
		self.webview.connect("mime-type-policy-decision-requested", self.on_mime_type_policy_decision_requested)
		scrolled_window = self.builder.get_object('scrolledwindow')
		scrolled_window.add(self.webview)
		self.go_home(lang)
		self.window.show_all()
		
	def on_mime_type_policy_decision_requested(self,web_view,frame,request,mimetype,policy_decision):
		if not web_view.can_show_mime_type(mimetype):
			path_file = request.get_uri()
			#policy_decision.download()
			policy_decision.ignore()
			web_view.stop_loading()
			if sys.platform.startswith('darwin'):
			    subprocess.call(('open', path_file))
			elif os.name == 'nt':
			    os.startfile(path_file)
			elif os.name == 'posix':
			    subprocess.call(('xdg-open', path_file))
			return True
		else:
			return False
		
	def on_download_requested(self, web_view,download):
		#dialog = Gtk.FileChooserDialog("Dove vuoi salvare", self.window,  Gtk.FileChooserAction.SAVE,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
		dialog = Gtk.FileChooserDialog("Aprire", self.window,  Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		dialog.set_uri(download.props.network_request.props.uri)
		
		if dialog.run() == Gtk.ResponseType.OK:
			path_file_save = dialog.get_filename()
			download.set_destination_uri(path_file_save) #download.props.network_request.props.uri
			download.connect('notify::status', self.on_download_status_change)
		dialog.destroy()
		return True
	
	def on_download_status_change(self,download,status):
		if download.get_status().value_name == 'WEBKIT_DOWNLOAD_STATUS_FINISHED':
			a = ''
		
		
	#def on_navigation_requested(self, frame,request,user_data):
	#	path_file_name = user_data.props.uri
	#	if os.path.splitext(path_file_name) == '.rtf':
	#		return WebKit.NavigationResponse.DOWNLOAD

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
	def __init__(self,result,text_search):
		self.language = g_language
		self.type_search = None
		
		try:
			lang = gettext.translation(APP, DIR,languages=[self.language])
		except locale.Error,e:
			logging.exception(e)
			self.language,spare = locale.getlocale()
			
		self.builder = Gtk.Builder()
		self.builder.set_translation_domain(APP)
		self.builder.add_from_file(UI_FILE_RESULT)
		self.builder.connect_signals(self)
		self.window = self.builder.get_object('qfresult')
		#self.window.set_back_pixmap('trovaing.jpg')
		self.webview = WebKit.WebView()
		self.webview.connect("mime-type-policy-decision-requested", self.on_mime_type_policy_decision_requested)
		self.webview.connect("navigation-policy-decision-requested", self.on_navigation_policy_decision_requested)
		self.webview.connect("download-requested", self.on_download_request)
		
		scrolled_window = self.builder.get_object('scrolledwindow1')
		scrolled_window.add(self.webview)
		self.load_lang_labels(lang)
		self.view_result(result,text_search)
		self.window.show_all()
	
	def on_notify_status(self,download,status):
		if status == WebKit.DownloadStatus.FINISHED:
			a=a
		
		
	def on_navigation_policy_decision_requested(self,web_view,frame,request,navigation_action,policy_decision):
		#path_file = request.get_uri()
		reason = navigation_action.get_reason()
		if reason == WebKit.WebNavigationReason.LINK_CLICKED:
			policy_decision.download()
			return True;
		
	def on_download_request(self,web_view,download):
		#dest = webkit_download_get_uri()
		#webkit_download_set_destination_uri(download, dest);
		download.set_destination_uri(download.get_uri())
		download.connect("notify::status", self.on_notify_status)
		return True;
		
	def on_mime_type_policy_decision_requested(self,web_view,frame,request,mimetype,policy_decision):
		#if not web_view.can_show_mime_type(mimetype):
			path_file = request.get_uri()
			if '/tmp/' in path_file == False:
				policy_decision.download()
				return True
				#policy_decision.ignore()
				web_view.stop_loading()
				if sys.platform.startswith('darwin'):
				    subprocess.call(('open', path_file))
				elif os.name == 'nt':
				    os.startfile(path_file)
				elif os.name == 'posix':
				    subprocess.call(('xdg-open', path_file))
				return True
			else:
				return False
		
	def load_lang_labels(self,lang):
		_ = lang.gettext
		self.window.set_title(_('Risultato'))
	
	def _prep_qf_dx(self,search_text):
		search_result = _('risultato della ricerca')
		text_for_display_edit = _('per visualizzare un documento...')
		
		html = """<html>
   <head>
      <link rel='stylesheet' type='text/css' href='quickfind.css'>
   </head>
   <body bgproperties='fixed' background='sfondo.jpg' oncontextmenu='return false;'>
      <div align='left'><br>&nbsp;{0}&nbsp;&quot;{1}&quot;</div>
      <div class='sottotitolo'>{2}<img border='0' src='check.gif'></div>
      <hr size='2' color='#990000' width='100%'>
   </body>
</html>""".format(search_result,search_text,text_for_display_edit)
		return html
	
	def _prep_qf_sx(self,result):
		from cStringIO import StringIO
		file_html = StringIO()
		html = """<html>
   <head>
      <link rel='stylesheet' type='text/css' href='quickfind.css'>
   </head>
   <body bgproperties='fixed' background='sfondosx.jpg' oncontextmenu='return false;'>"""
		file_html.write(html)
	
		row_html ="""&nbsp;<a href='%s' title='%s'><img border='0' src='check.gif'></a>
	<font face='Arial' size='2' color='#000000'><b>&nbsp;&nbsp;&nbsp;<a href='%s' title='%s'>%s</a>
	</b></font><br>"""
		row_media_html = "<a href='%s' title='%s'><img border='0' src='../Imagenes/%s.gif'></a><br/>"
	#target='f_dx'
		for row in result:
			nome_doc_pdf = row['nome_doc_pdf']
			nome_doc_rtf = row['nome_doc_rtf']
			if nome_doc_pdf != None:
				file_name = os.path.splitext(os.path.basename(nome_doc_pdf))[0] # estract only file_name, without extension
				uri_pdf = '..' + helpers.capitalize_lang_path(nome_doc_pdf) #RootPath
			else:
				uri_pdf ='javascript::void(0);'
				
			if nome_doc_rtf != None:
				uri_rtf = '..' + helpers.capitalize_lang_path(nome_doc_rtf)
			else:
				uri_rtf ='javascript::void(0);'
			
			file_html.write(row_html%(uri_rtf,uri_rtf,uri_pdf,uri_pdf,file_name))
			uri ={}
			for t_media in ['audio','foto','interv','video']:
				if row['nome_file_'+ t_media] != None and len(row['nome_file_'+ t_media])>0:
					uri[t_media] = '..' + helpers.capitalize_lang_path(row['nome_file_'+ t_media])
					file_html.write(row_media_html%(uri[t_media],uri[t_media],t_media))
			
		file_html.write("""</body></html>""")
		return file_html.getvalue()
		
	def view_result(self,result,search_text):
		#qf_sx.htm
		html_sx = self._prep_qf_sx(result)
		f = open(RootPath + '/' + TMP_DIR + '/' + HTM_RES_SX,'w') #os.getcwd() + '/' + TMP_DIR +
		f.write(html_sx)
		f.close()
		
		html_dx = self._prep_qf_dx(search_text)
		f = open(RootPath + '/' + TMP_DIR + '/' + HTM_RES_TOP,'w') #os.getcwd() + '/' + TMP_DIR +
		f.write(html_dx)
		f.close()
		
		#prepare others html
		#qf_dx.htm # fixed
		#qf_top.htm 
		uri='file://%s/%s'%(RootPath + '/' + TMP_DIR,HTM_RESULT)
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
		self.builder.add_from_file(UI_FILE_SEARCH)
		self.builder.connect_signals(self)
		self.window = self.builder.get_object('qfsearch')
		
		#self.window.set_back_pixmap('trovaing.jpg')
		self.load_lang_labels(lang)
		self.prog_search = self.builder.get_object('progress_ricerca')
		self.prog_search.set_pulse_step(0.005)
		self.num_progress = self.builder.get_object('num_progress')
		self.window.show_all()
	
	def on_close(self,button):
		Gtk.main_quit()
		
	def on_interrupt(self,button):
		self.conn.interrupt()
			
	def on_type_search_change(self,button):
		list_store = button.get_model()
		active_index = button.get_active()
		if active_index != -1:
			self.type_search = list_store[active_index][0]
	
	def progressbar(self):
		#Gdk.threads_enter()
		self.prog_search.pulse()
		#self.num_progress.set_label()
		#gtk.main_iteration()
		while Gtk.events_pending():
			Gtk.main_iteration()
	
	def on_start_search(self,button):
		#threading.Thread(target = self._start_search_core())
		self._start_search_core()
	
	def on_close(self,buttom):
		pass
		
	def _start_search_core(self):
		import sqlite3
		self.conn = sqlite3.connect(DBName,check_same_thread = False)
		self.conn.row_factory = helpers.dict_factory
		self.conn.set_progress_handler(self.progressbar,5000)
		self.cursor = self.conn.cursor()
		text_to_search = self.builder.get_object('testo_da_cercare').get_text()
		
		type_search = self.type_search
		if type_search != None:
			if len(type_search) > 8:
				type_search = type_search[0:8]
			type_search = type_search.lower()
		
		####### COMMENTATO	
		#sql = """SELECT tab_rows.id_doc, tab_rows.txt_row, tab_docs.ds_lang, tab_docs.nome_doc_rtf, tab_docs.nome_doc_pdf
		#		FROM tab_rows INNER JOIN tab_docs ON tab_rows.id_doc = tab_docs.id_doc where ds_lang=:lang and txt_row like '%:text_to_search%' """
				
		if language_directory.has_key(self.language):
			lang = language_directory[self.language]
			lang = lang[0:3].lower()
		else:
			lang = 'ita'
			
		#param = {'lang':lang,'text_to_search':text_to_search}
		
		sql = """SELECT d.id_doc,d.ds_lang,d.nome_doc_pdf,t.*
				FROM tab_rows as r INNER JOIN tab_docs as d ON r.id_doc = d.id_doc LEFT JOIN tab_file_av as t ON LOWER(t.nome_doc_rtf)=LOWER(d.nome_doc_rtf)
				where d.ds_lang='""" + lang + "' and r.txt_row like '%" + text_to_search +"%'"
				
		#if type_search != None:		
		#	sql = sql + " and d.nome_doc_pdf like '%" + type_search + "%'"
			#param.append(type_search)
		sql = sql + " group by d.nome_doc_pdf"
		#cursor.execute(sql,param)
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		self.num_progress.set_label(str(len(result)))
		QuickResult(result,text_to_search)
				
	def load_lang_labels(self,lang):
		_ = lang.gettext
		self.window.set_title(_('Ricerca'))
		self.builder.get_object('testo_da_cercare').set_tooltip_text(_('Scrivi qui...'))
		self.builder.get_object('testo_da_cercare').set_text(_('Scrivi qui...'))
		self.builder.get_object('inizia_ricerca').set_tooltip_text(_('inizia ricerca'))
		self.builder.get_object('inizia_ricerca').set_label(_('inizia ricerca'))
		self.builder.get_object('chiudi').set_tooltip_text(_('chiudi'))
		self.builder.get_object('chiudi').set_label(_('chiudi'))
		#self.builder.get_object('pausa').set_tooltip_text(_('pausa'))
		#self.builder.get_object('pausa').set_label(_('pausa'))
		#self.builder.get_object('interrompi').set_tooltip_text(_('interrompi'))
		#self.builder.get_object('interrompi').set_label(_('interrompi'))
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
	#GLib.threads_init()
	Gdk.threads_init()
	Gdk.threads_enter()
	Gtk.main()
	Gdk.threads_leave()

if __name__ == "__main__":
	main()
