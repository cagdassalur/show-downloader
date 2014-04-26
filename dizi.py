# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import mechanize, HTMLParser, os, re, sys

br = mechanize.Browser()
br.set_handle_robots(False)

if len(sys.argv) < 2: fn = 'dizi.txt'
else: fn = sys.argv[1]

f=open(fn,'r')
st = f.read()
f.close()
#with open('output.txt', 'w') as f: f.write(st)
ar = st.split('\n')
st_out = ''

foundCount = 0
for line in ar:
	line = line.split(';')
	isim = line[0].replace(' ', '%20')
	ep = int(line[1])
	url = "http://194.71.107.80/search/{0}/0/7/0".format(isim)
	reg = re.compile(r"([sS]\d+[eE]\d+)")
	inenler = [ep]
	
	soup = BeautifulSoup(br.open(url).read())
	isim = isim.replace('%20',' ')
	magnets = [a.get('href') for a in soup.find_all('a') if 'magnet' in a.get('href')]
	
	for magnet in magnets:
		found = reg.search(magnet)
		if found: 
			epn = int(found.group()[1:].lower().replace('e', ''))
			if epn > ep:
				if( (epn not in inenler) and
					#raw_input(isim + '/' + str(epn) + ' bulundu. indir? [y-n]').lower() == 'y'):
					True):
					os.system("open "+magnet)
					inenler.append(epn)
					foundCount += 1

	for i in xrange(len(ar)):
		if isim in ar[i]: 
			ar[i] = isim + ';' + str(max(inenler))
if foundCount == 0:
	print 'No new episodes.'
	os.system("""osascript -e 'display notification "Yeni Bölüm bulunamadı." with title "Dizi-indir"'""")
else:
	print str(foundCount) + ' new episodes downloaded.'
	os.system("""osascript -e 'display notification " """+str(foundCount)+""" Bölüm indiriliyor.."with title "Dizi-indir"'""")
	with open('dizi.txt','w') as f: f.write('\n'.join(ar))
	raw_input()

