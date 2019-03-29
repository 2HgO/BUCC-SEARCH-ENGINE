# packages to be used in the program
import re
import cgi, cgitb
import os
import json

# cgitb.enable() is used to catch ang display python errors in a human readable web format
cgitb.enable()

# search_item is gotten from form field in 'update.py' on every keystroke the user makes
form = cgi.FieldStorage()
item=form.getvalue('search_item').strip()

# the mat function is used to match the item pattern at the start of a string in the dataset 
def mat(don):
	if re.match(r'(\s|^)%s' % item, don ,re.I):
		return don
	return

# The dataset is loaded into a list from json files where properties such as 'title' and 'keywords' partaining to the resources are stored
db=[]
for i in os.listdir("Data"):
	da=json.load(open("Data/%s" % i,"r"))
	db+=da["keywords"]
	db+=da["title"]

# the resources that match the search_item are stored in a set
find = [x for x in list(map(mat,db)) if x != None]
find=list(set(find))
find.sort()

# header string for the html program
print("Content-Type: text/html\n\n")

# search results are returned to 'index.py'
print(",".join(find[:min(5,len(find))]))
