from bs4 import BeautifulSoup
import mechanize, HTMLParser, os, re

br = mechanize.Browser()
br.set_handle_robots(False)

f=open('dizi.txt','r')
st = f.read()
f.close()
#with open('output.txt', 'w') as f: f.write(st)
ar = st.split('\n')
st_out = ''
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
					True:
					os.system("open "+magnet)
					inenler.append(epn)
	
	for i in xrange(len(ar)):
		if isim in ar[i]: 
			ar[i] = isim + ';' + str(max(inenler))
with open('dizi.txt','w') as f: f.write('\n'.join(ar))

