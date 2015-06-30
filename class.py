import nltk, os, json

raw1=raw_input('Hi ! How can I help you ?\n')
raw2=raw1.replace('.','').replace(',','').replace('?','').replace('!','')
tokenized=nltk.word_tokenize(raw2)
length=len(tokenized)

direc=os.getcwd()
f=open((direc+'/class.json'), 'r')
data=json.loads(f.read())
f.close()
ff=open((direc+'/newclass.json'), 'r')
newdata=json.loads(ff.read())
ff.close()

score={}
flag={}
occurrence={}
stop=0

def confirm(mp, oldcat, occ):
	x=input('Right? 1 - Ya, 2 - No\t')
	if x==1:
		newdata["confirm"][oldcat+' @ '+mp]=occ
		fw=open(direc+'/newclass.json','w')
		fw.write(json.dumps(newdata,indent=4))
		fw.close()
		print 'Thank you! Your order has been taken.'
	elif x==2:
		cat=raw_input('Sorry! Which category you meant?\t').lower()
		newdata["confusion"]['old- '+oldcat+', new- '+cat+' @ '+mp]=occ
		fw=open(direc+'/newclass.json','w')
		fw.write(json.dumps(newdata,indent=4))
		fw.close()
		print 'Thanks for the new info. Your order has been taken.'
	else:
		print 'Invalid option'
		
def confusion(sent, occ):
	x=raw_input('Please mention in which category your request falls - ')
	newdata["confusion"][x+' @ '+sent]=occ			#new data entry in dictionary - entire sentence for recheck by admin
	fw=open(direc+'/newclass.json','w')
	fw.write(json.dumps(newdata,indent=4))
	fw.close()
	print 'Thanks for the new info. Your order has been taken.'

for a in data.keys():
	score[a]=0
	flag[a]=0
	occurrence[a]={}
	
for i in range(length):
	if stop==1:
		break
	phrases=nltk.ngrams(tokenized, length-i) #reverse order of length of n-grams : 3-grams first then 2-grams followed by 1-grams
	for each in phrases: #each possible tuple of n-gram
		each_phrase=''
		if stop==1:
			break						
		for j in range(length-i):
			each_phrase=each_phrase+' '+each[j] #making n-gram phrases from tuples
		match_phrase=each_phrase[1:].lower()
		for k in data.keys():					#loop for each category (e.g. movie, food, travel, grocery etc.)
			if match_phrase in data[k].keys():
				if (length-i)==1:
					score[k]=score[k]+1
					occurrence[k][match_phrase]=1
				else:
					score[k]=score[k]+2		#giving more weightage to multiword matching
					occurrence[k][match_phrase]=2
				flag[k]=1
				
				
		#priority block for matching a phrase  with only one category -- clearly goes out of the program
		if (length-i) != 1 and sum(flag.values()) == 1:
			for out in flag.keys():
				if flag[out] ==1:
					category=out
			print 'Your request is about '+ category
			confirm(match_phrase, category, occurrence)
			stop=1
			break
		
		
		
	#score counting in the last lap
	if (length-i)==1:
		flag2=0
		#sorting the categories in ascending order formign a list of tuples containing category name and score
		l=sorted(score.items(), key= lambda x:x[1], reverse=True)
		#l[0] will contain the highest score - l[0][0]:category and l[0][1]:score
		
		
		if l[0][1]==0:			#unable to get any category, all scores are zeroe
			confusion(raw2, occurrence)
			
			
		else:					#many non-zero scores, finding big ones
			for cat in range(len(score.keys())):
				if (l[0][1]/2)>=l[cat][1]:
					flag2=cat
				else:
					break
			if flag2==0:					#category confirmed, only one big score
				print 'The category is ', l[0][0]
				confirm(raw2, l[0][0], occurrence)
				
			else:							#category needed to be confirmed
				print 'We think your request falls in one of the following -'
				for m in range(flag2):
					print l[m][0]
				print 'but we are not sure!'
				confusion(raw2, occurrence)
						
	
	
