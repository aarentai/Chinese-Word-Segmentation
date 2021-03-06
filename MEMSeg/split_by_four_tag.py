# -*- coding: utf-8 -*-
import codecs
import sys

def split_by_four_tag(input_file, output_file):
    input_text = codecs.open(input_file, 'r', 'utf-8')
    output_text = codecs.open(output_file, 'w', 'utf-8')
    
    for line in input_text.readlines():
        char_tag_list = line.strip().split()
        for char_tag in char_tag_list:
            char_tag_pair = char_tag.split('/')
            char = char_tag_pair[0]
            tag = char_tag_pair[1]
            #如果是开头，则前面加/
            if tag == 'B':
                output_text.write('/' + char)
            elif tag == 'M' or tag == 'E':
                output_text.write(char)
            else: # tag == 'S'
                output_text.write('/' + char)
        output_text.write("\n")
    input_text.close()
    output_text.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "INSTRUCTION FORMAT: python split_by_four_tag.py input output"
        sys.exit()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    split_by_four_tag(input_file, output_file)
