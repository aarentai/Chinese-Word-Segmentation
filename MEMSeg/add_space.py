import codecs
import sys

def add_space(input_file, output_file):
    input_text = codecs.open(input_file, 'r', 'utf-8')
    output_text = codecs.open(output_file, 'w', 'utf-8')
    for line in input_text.readlines():
        for word in line.strip():
            output_text.write(word + " ")
        output_text.write("\n")
    input_text.close()
    output_text.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "INSTRUCTION FORMAT: python add_space.py input output"
        sys.exit()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    add_space(input_file, output_file)
