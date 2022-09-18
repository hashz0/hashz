#!/usr/bin/env python

import hashlib
import sys
import argparse
import re

def insert(source_str, insert_str, pos):
	return source_str[:pos]+insert_str+source_str[pos:]

def replace_char(source_str, char, index):
	return source_str[:index] + char + source_str[index+1:]

def hashz(string, key, output_length): 
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


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-key', dest='key', type=str, help='your master key')
	parser.add_argument('-outlen', dest='outlen', type=int, help='output string length (default is 10)')
	args = parser.parse_args()
	key = args.key
	outlen = args.outlen
	if not outlen: outlen = 10

	if not key or len(key)<2:
		print("Key is not provided or not valid (Minimum 2 symbols in length)", file=sys.stderr)
		sys.exit(1)

	while True:
		for string in sys.stdin.readline().splitlines():
			print(hashz(string, key, outlen),file=sys.stdout)


if __name__ == "__main__":
    main()
