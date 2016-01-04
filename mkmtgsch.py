# I really prefer atpy to astropy.Tables, but you know, whatever floats your boat
# you'll have to adapt accordingly, atpy tables are just so easy to update and manipulate 

import atpy

# previously, VU227.csv would have been a trimmed down version of the schedule... 
# however, now the code does the querying of the full schedule, easy peasy, covergirl!
a = atpy.Table('VU227.csv',type='ascii',delimiter=',')

# get columns
col = a.columns.keys 
# print columns to find columns and ids of note (useful for customization): 
for i,ci in enumerate(col): 
	print i,ci 
	
# search title and abstract for keywords (my choices follow): 
keywords = ['PN','planetary nebula', 'PNe','AGB','asymptotic giant branch','red giant', 
			'white dwarf','close binary','red supergiant',' nova ', 'VY CMa']
# set up a dummy boolean array set to False, could probably be smarter ;): 
kwkey = asarray(['Fitbit' in ai for ai in a[col[10]]])
# loop and update truthiness
for ki in keywords: 
	kwkey_titleupdate =  asarray([ki in ai for ai in a[col[10]]])
	kwkey_absupdate = asarray([ki in ai for ai in a[col[18]]])
	for i in range(len(kwkey)): 
		kwkey[i] = kwkey[i] | kwkey_titleupdate[i] | kwkey_absupdate[i]

# add Keyword flag 
a.add_column('Keyword',kwkey)

# add VU flag: 
a.add_column('VU',['Vanderbilt' in ai for ai in a[col[17]]])

# add poster or talk flag
ctype = ['Poster' if x.split(' ')[0] == 'Poster' else 'Talk' for x in a[col[2]]]
a.add_column('conf_type',ctype)

# add day dict:
days  = { '03-Jan-2016': 'Sun','04-Jan-2016': 'Mon', '05-Jan-2016': 'Tue', '06-Jan-2016': 'Wed', '07-Jan-2016': 'Thu', '08-Jan-2016': 'Fri' }
day = [days[x] for x in a[col[4]]]
a.add_column("conf_day",day)

# filter the table based on truth column of choice
#a = a.where(a.VU) # <== Vanderbilt Query 
a = a.where(a.Keyword)

# formatting (first two aren't used... I think...)     
fmt = '<div class="entry {0}">\n<h4>{1} {2}-{3}</h4>\n<h2>{4}</h2>\n<h3>{5}</h3>\n<span>{6}</span>\n<blockquote>{7}</blockquote>\n</div>\n'
fmt = '<div class="entry {0}">\n<h4>{1} {2}-{3}</h4>\n<h2>{6} &mdash; {4}</h2>\n<h3>{5}</h3>\n</div>\n'
fmt1 = '<div class="entry {0}">\n<h4>{1} {2}-{3}</h4>\n<div class="head-circle">{6}</div>\n<h2>{4}</h2>\n<h3>{5}</h3>\n<h2>({7})</h2>\n</div>\n'
fmt2 = '<div class="entry {0}">\n<h4>{1} {2}</h4>\n<div class="head-circle">{6}</div>\n<h2>{4}</h2>\n<h3>{5}</h3>\n</div>\n'
dayfmt = '<a name="{0}"></a><div class="clear"></div><hr class="head-hr"><div class="head-day">{0}</div>\n'

# set up output file for writing and header file for reading
o = open('newlist.html','w') 

# read/write the header (CSS, menu, etc.): 
h = open('header.html','r') 
for li in h: 
	o.write(li + '\n') 

# write title of choosing: 
o.write('<div class="head"><h2>#{0} @ #AAS{1}</h2>\n'.format('PNe','227'))

# make navigation: 
daynav = '<div class="days"> | '
udays = unique(a[col[4]]) 
for udi in udays: 
	daynav = daynav + '<a href="#{0}">{0}</a> | '.format(days[udi])
daynav = daynav + '</div></div>\n<div class="container">\n'

# write day navigation
o.write(daynav)

# set day before first day... 
thisday = 'Sun'

# loop through the table and write out the days:
for t,d,t1,t2,title,author,affil,comm,loc in zip(a.conf_type,a.conf_day,a[col[12]],a[col[13]],a[col[10]],a[col[14]],a[col[17]],a[col[11]],a[col[7]]): 
	if (d!= thisday): 
		# first new day, add header, update thisday: 
		thisday = d
		o.write(dayfmt.format(d))
	if (t1!='5:30 PM'): 
		# new to AAS 227, the posters have a time slot, they start at 5:30pm
    	# if not 5:30pm, then it is a a talk with a specified time range 
    	# so use format code fmt1, accordingly:  
		o.write(fmt1.format(t.lower(),d,t1,t2,title,author.replace('*',''),comm,loc.split('(')[0].strip()))
	else: 
		# this is a poster, so use format code fmt2, accordingly: 
		o.write(fmt2.format(t.lower(),d,'Poster Session','',title,author.replace('*',''),comm))
    
# close up the html and close the file: 
o.write('</div></body></html>') 
o.close()