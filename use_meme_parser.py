
#License MIT 2017 Ahmad Retha

import sys
import argparse
from meme_parser import MEMEFile

def main():
	parser = argparse.ArgumentParser(description='Meme_Parser is a parser for the MEME Motif Format')
	parser.add_argument('meme_file', type=argparse.FileType('r'), help='The MEME Motif file')
	args = parser.parse_args()

	memefile = MEMEFile(args.meme_file)
	if memefile.errors:
		print "An error occured during the parsing process:\n", "\n".join(memefile.errors)
		sys.exit(1)
	else:
		print 'Version:', memefile.version
		print 'Alphabet:', memefile.alphabet
		print 'Strands:', memefile.strands
		print 'Background Source:', memefile.backgroundSource
		print 'Background:', memefile.background
		for motif in memefile.motifs:
			print motif.id, motif.matrix[0]
	sys.exit(0)

if __name__ == '__main__':
	main()

