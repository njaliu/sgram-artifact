import sys
import json
#import numpy as np
import kenlm
import operator

def predict(dump_file, model):
	rank = {}
	with open(dump_file) as f:
		for line in f:
			print line
			pyjson = json.loads(line)
			#print pyjson['position'] + " !!!!"
			score = model.score(pyjson['sequence'])
			rank[line] = score
			print rank[line]
		#sorted_rank = sorted(rank.items(), key=operator.itemgetter(1))

def main(dump_file):
	model = kenlm.LanguageModel('/home/aliu/Research/Projects/sgram/model/n3-2018-4-27-new.klm')
	predict(dump_file, model)

if __name__ == '__main__':
    main(sys.argv[1])
