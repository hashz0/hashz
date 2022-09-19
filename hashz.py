from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.clipboard import Clipboard

import hashlib
import sys
import argparse
import re

from random import randint

Window.size = (270,120)
Window.clearcolor =  (255/255, 186/255, 3/255)

def insert(source_str, insert_str, pos):
	return source_str[:pos]+insert_str+source_str[pos:]

def replace_char(source_str, char, index):
	return source_str[:index] + char + source_str[index+1:]

def hashz(string, key, output_length): # TODO: DRY code
	string = insert(key, string, int(len(key)/2))
	string = hashlib.sha256(string.encode('utf-8')).hexdigest()[:output_length]
	positions = list()

	def hashz_numbers(string):
		pattern = re.compile("[0-9]+")
		string_mod = hashlib.sha256(string.encode('utf-8')).hexdigest()[:output_length]
		if not re.search(pattern, string_mod): return hashz_numbers(string_mod)

		for m in re.finditer(pattern,string_mod):
			position = int(str(m.start())[0])
			string = replace_char(string, m.group()[0], position)
			positions.append(position)
			return string
		return hashz_numbers(string_mod)

	def hashz_capitals(string):
		pattern = re.compile("[a-z]+")

		string_mod = hashlib.sha256(string.encode('utf-8')).hexdigest()[:output_length]
		if not re.search(pattern, string_mod): return hashz_capitals(string_mod)
		for m in re.finditer(pattern,string_mod):
			position = int(str(m.start())[0])
			if position in positions: continue
			string = replace_char(string, m.group()[0].upper(), position)
			positions.append(position)
			return string
		return hashz_capitals(string_mod)

	def hashz_dot(string):
		pattern = re.compile("[a-z]+")
		string_mod = hashlib.sha256(string.encode('utf-8')).hexdigest()[:output_length]
		if not re.search(pattern, string_mod): return hashz_dot(string_mod)
		for m in re.finditer(pattern,string_mod):
			position = int(str(m.start())[0])
			if position in positions: continue
			string = replace_char(string, ".", position)
			positions.append(position)
			return string
		return hashz_dot(string_mod)

	string = hashz_numbers(string)
	string = hashz_capitals(string)
	string = hashz_dot(string)
	return(string)


class MyApp(App):
	

	def __init__(self):
		super().__init__()
		self.key_input = TextInput(hint_text='Master Key', password=True)
		self.outlen_input = TextInput(hint_text='Outlen(default=10)', input_filter = 'int')
		self.input_input = TextInput(hint_text='Input')
		self.output_input = TextInput(hint_text='Output')
		self.btn = Button(text="Copy to Clipboard")
		self.key_input.bind(text=self.on_text)
		self.input_input.bind(text=self.on_text)
		self.outlen_input.bind(text=self.on_text)
		self.btn.bind(on_release=self.btn_pressed)
		self.inner_box = BoxLayout(orientation='horizontal')

	def on_text(self, *args):
		outlen_text = 10	
		if self.outlen_input.text != '': outlen_text = self.outlen_input.text

		if self.key_input.text=='' or self.input_input.text=='': return
		elif len(self.key_input.text)<2:
			self.output_input.text='Master key must be minimum 2 characters long'
			return
		elif int(outlen_text)<3 or int(outlen_text)>33:
			self.output_input.text='Outlen must be between 3 and 33'
			return

		self.output_input.text=hashz(self.input_input.text, self.key_input.text, int(outlen_text))

	def btn_pressed(self, *args ):
		Clipboard.copy(self.output_input.text)

	def build(self):
		self.title = 'hashz'
		box = BoxLayout(orientation='vertical')
		box.add_widget(self.inner_box)
		self.inner_box.add_widget(self.key_input)
		self.inner_box.add_widget(self.outlen_input)
		box.add_widget(self.input_input)
		box.add_widget(self.output_input)
		box.add_widget(self.btn)
		return box

if __name__ == "__main__":
	MyApp().run()
