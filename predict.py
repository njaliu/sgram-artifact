import sys
import os
import json
#import numpy as np
import kenlm
import operator

report_dir = '/home/aliu/Research/Projects/sgram-artifact/report/'

def predict(dump_file, model):
	rank = {}
	K = 10
	with open(dump_file) as f:
		for line in f:
			print line
			pyjson = json.loads(line)
			#print pyjson['position'] + " !!!!"
			score = model.score(pyjson['sequence'])
			rank[line] = score
			print rank[line]
		sorted_rank = dict(sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[:K])
		base = os.path.basename(dump_file).split('.')[0]
		json_file = report_dir + base + '.json'
		hit = check(json_file, sorted_rank)
		if hit > 0:
			print 'hit: ' + hit
		else:
			print 'no hit'

def check(json_file, rank):
	count = 0
	with open(json_file) as f:
		report = json.load(f)
		vulns = getVulnPos(report)
		for key in rank:
			pos = key['position']
			if pos in vulns:
				count = count + 1
	return count


def getVulnPos(data):
	out = []
	out = out + data['vulnerabilities']['parity_multisig_bug_2']
	out = out + data['vulnerabilities']['reentrancy']
	out = out + data['vulnerabilities']['integer_underflow']
	out = out + data['vulnerabilities']['money_concurrency']
	out = out + data['vulnerabilities']['integer_overflow']
	out = out + data['vulnerabilities']['assertion_failure']
	out = out + data['vulnerabilities']['callstack']
	out = out + data['vulnerabilities']['time_dependency']
	return out

def main(dump_file):
	model = kenlm.LanguageModel('/home/aliu/Research/Projects/sgram/model/n3-2018-4-27-new.klm')
	predict(dump_file, model)

if __name__ == '__main__':
    main(sys.argv[1])
