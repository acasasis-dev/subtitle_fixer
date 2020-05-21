#!/usr/bin/python3

import re
from shutil import copyfile
from os.path import exists
from os import remove
from sys import argv

try:
	sub_file = argv[1]
	fix_option = argv[2]
	desired_time = argv[3]
except Exception:
	print( "syntax: subtitle_fixer.py [subtitle file] [delay/hasten] [desired time in seconds]")
	exit()
time_format_regex = ".*?[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}.*?"
subtitle_format_regex = re.compile( time_format_regex + " --> " + time_format_regex )
sub_file_backup = sub_file + ".bak"
sub_file_handle = sub_file_backup
if not exists( sub_file_backup ):
	copyfile( sub_file, sub_file_backup )
	sub_file_handle = sub_file
sub_file_open = open( sub_file_handle )
sub_file_content = sub_file_open.read().split( "\n" )

def fix_sub( time ):
	sec_ret = to_seconds( time )
	formula = str( sec_ret ) + "-" if fix_option == "delay" else "+" + desired_time
	print( "formula: " + formula )
	correct_time = eval( formula )
	ret = to_original( correct_time )
	return ret

def to_seconds( time ):
	hour, minutes, seconds = map( int, [ x for x in time.split( ":" ) ] )
	total_seconds = ( hour * 3600 ) + ( minutes * 60 ) + seconds
	return str( total_seconds )

def to_original( time ):
	hour = int( time / 3600 )
	time = time - ( hour * 3600 )
	minutes = int( time / 60 )
	time = time - ( minutes * 60 )
	seconds = time

	ret = ( ( "0" if hour < 10 else "" ) + str( hour ) ) + ":" + ( ( "0" if minutes < 10 else "" ) + str( minutes ) ) + ":" + ( ( "0" if seconds < 10 else "" ) + str( seconds ) )
	return ret

splitter1 = " --> "
splitter2 = ","
for sub_duration_index in range( len( sub_file_content ) ):
	if re.match( subtitle_format_regex, sub_file_content[sub_duration_index] ):
		start, end = [ x for x in sub_file_content[sub_duration_index].split( splitter1 ) ]
		start_time, start_milsec = [ x for x in start.split( splitter2 ) ]
		start = splitter2.join( [ fix_sub( start_time ), start_milsec ] )
		end_time, end_milsec = [ x for x in end.split( splitter2 ) ]
		end = splitter2.join( [ fix_sub( end_time ), end_milsec ] )
		sub_duration_fixed = splitter1.join( [ start, end ] )
		sub_file_content[sub_duration_index] = sub_duration_fixed

sub_file_content = "\n".join( sub_file_content )
sub_file_open.close()
sub_file_open = open( sub_file, "w" )
sub_file_open.write( sub_file_content )
sub_file_open.close()