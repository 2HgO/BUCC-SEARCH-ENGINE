# Packages to be used in the program
import re
import cgi, cgitb
import nltk
from nltk import ngrams
import os, sys
from pdfrw import PdfReader
from textblob import TextBlob
import json
import pickle


# cgitb.enable() is used to catch ang display python errors in a human readable web format
cgitb.enable()

# header string for the html program
print("Content-Type: text/html\n\n")


# function match searches for the search_item in a given string from the dataset by searching for the pattern using the regular expression "(\s|^){data}" 
def mat(c):
	a,b=c
	if re.search(r'(\s|^)%s' % item, b ,re.I):
		return (a,b)
	return

# search_item is gotten from form field in 'update.py' after submission and then converted to a textblob
form = cgi.FieldStorage()
item_raw=form.getvalue('search_item').strip()
item=TextBlob(item_raw)
item_sum=" ".join([x for x,t in item.tags if t not in ['TO','SYM','DT','CC','EX']])
item_lem=" ".join(map(lambda x: x.lemmatize(),TextBlob(item_sum).words))
data=TextBlob(item_sum).words + TextBlob(item_lem).words + item.words

# the search history, stored in a pickle file is loaded into a list
d=pickle.load(open("Data/searchHistory.pickle","rb"))

# if search_item is in search history, the stored result is returned back to 'update.py'
if item in d.keys():
	print("|".join(d[item_raw]))
	exit()

# The dataset is loaded into a list from json files where properties such as 'title' and 'keywords' partaining to the resources are stored
db=[]
for i in os.listdir("Data"):
	if i[-5:] == ".json":
		da=json.load(open("Data/%s" % i,"r"))
		db+=map(lambda x: (da["path"],x),da["keywords"])
		db+=map(lambda x: (da["path"],x),da["title"])

# the resources that match the search_item are stored in a set
fin=list(map(lambda x: "{}:{}".format(x,PdfReader("/opt/lampp/htdocs/AI_PROJECT/%s" % x).Info.Title.strip(' ()')),list(set([l for l,m in [x for x in list(map(mat,db)) if x != None]]))))
fin.sort()

# search results are returned to 'index.py'
print("|".join(fin))

if len(fin):
	try:
		if item not in d.keys():
			d[item_raw]=fin
	except:
		d={}
		d[item_raw] = fin
	# search results are written to search history
	with open("Data/searchHistory.pickle","wb") as pp:
		pp.write(pickle.dumps(d))
		pp.close()
