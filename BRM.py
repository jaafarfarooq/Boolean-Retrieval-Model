import string
from collections import defaultdict
from nltk.stem import PorterStemmer
from nltk import word_tokenize
import re
import time

start_time=time.time()
ps=PorterStemmer()
InvertedIndex=defaultdict(list)
PositionalIndex=dict()

# Function to remove Punctuations from the text

def remove_Stopwords_Punctuations(input_string):
    punctuations = ['.', '!', '(', ')', ':','?',';','#','&','*','@','[',']','-','"', "'", ",",'“','”',"‘"]
    newstring=""
    #remove punctuations
    input_string=input_string.lower()
    for c in input_string:
        if c in punctuations:
            if c==",":
                c+=" "
            continue
        else:
            newstring += c
        
    return newstring

# Function to remove Stop Words

def remove_Stopwords(newstring,stop_words):
    newstring=newstring.split()
    result=""
    for word in newstring:
        if word not in stop_words:
            result += (word + " ")

    return result

# Function to create Inverted Index

def createInvertedIndex(input_string,doc_id):
    
    input_string=word_tokenize(input_string)
    for words in input_string:
       # words=ps.stem(words)
        if (doc_id not in InvertedIndex[words]) and (len(words)>1) :
            InvertedIndex[words].append(doc_id)
    
# Function to create Positional Index

def createpositionalIndex(word_list,doc_id,stop_words):
    i=0
    
    for word in word_list:
        if word not in stop_words:
            if not word in PositionalIndex :
                PositionalIndex[word]=[(doc_id,i)]      # Dictionary contains list of tuples 
                #PositionalIndex[word][doc_id]=[i]
            else:
                PositionalIndex[word].append((doc_id,i))
                #PositionalIndex[word][doc_id].append([i])
        i+=1
    #print(PositionalIndex)

#Function to store Inverted Index
def storeInvertedIndex():
    f = open("InvertedIndex.txt", "w")
    for word,value in InvertedIndex.items():
        f.write(word)
        for i in value:
            f.write(" " + str(i)+ " ")
        f.write("\n")
    f.close()

#Function to store positional index
def storePositionalIndex():
    f = open("PositionalIndex.txt", "w")
    for word,value in PositionalIndex.items():
        f.write(word)
        for i in value:
            f.write(" ( " + str(i[0]) + "," + str(i[1])+ " ) ")
        f.write("\n")
    f.close()


#Function to get Posting List 

def getposting_list(term):
    posting_list=[]
    for word,value in InvertedIndex.items():
        if word==term:
            posting_list=value
            return posting_list

# Function to handle simple queries

def simplequeryHandler(q):
    #BooleanOperations=["AND","OR","NOT","and","or","not"]

    query=q.split()
    #query=[]
    #for words in q:
    #    query.append(ps.stem(words))
    #print(query)
    # if query contains 1 or 2 terms 
    if len(query) < 3:
        if len(query)==1:
            return getposting_list(query[0])
        elif len(query)==2:
            temp=[]
            for i in range(1,51):
                temp.append(i)
            #print(getposting_list(query[1]))
            #a=getposting_list(query[1])
            #return temp.remove(a)
            temp2=getposting_list(query[1])
            if temp2 is not None:
                return (set(temp)-set(temp2))
            else:
                return set(temp)
    # if query contains more then 3 terms
    else:
        temp=set()
        if query[0]=="NOT" or query[0]=="not":               # Query Not * * * 
            
            for i in range(1,51):
                temp.add(i)
            #print(temp)
            temp2=getposting_list(query[1])
            #print(set(temp2))
            if temp2 :
                temp.difference_update(set(temp2))


            for i in range(2,len(query)):
                docs=set()
                for j in range(1,51):
                    docs.add(j)

                if(query[i]=="AND" or query[i]=="and"):
                    
                    if (query[i+1]=="NOT" or query[i+1]=="not"):
                        temp2=getposting_list(query[i+2])
                        if len(temp2) !=0:

                            temp=temp & (docs - (set(temp2)))
                        else:
                            temp=temp & docs
                        i+=2
                    else:
                        temp=temp & set(getposting_list(query[i+1]))
                        i+=1 
                if(query[i]=="OR" or query[i]=="or"):
                    if (query[i+1]=="NOT" or query[i+1]=="not"):
                        temp2=getposting_list(query[i+2])
                        if len(temp2)==0 :
                            temp=temp.union(docs - (set(temp2)))
                        else:
                            temp=temp.union(docs)
                        i+=2
                    else:
                        temp=temp.union(set(getposting_list(query[i+1])))
                        i+=1 

        else:
            temp=set()
            temp.update(set(getposting_list(query[0])))

            for i in range(1,len(query)):
                docs=set()
                for j in range(1,51):
                    docs.add(j)
                if(query[i]=="AND" or query[i]=="and"):
                    if (query[i+1]=="NOT" or query[i+1]=="not"):
                        temp2=getposting_list(query[i+2])
                        if len(temp2)==0:
                            temp=temp & (docs - (set(temp2)))
                        else:
                            temp=temp & docs
                        i+=2
                    else:
                        temp2=getposting_list(query[i+1])
                        temp=temp & set(temp2)
                        i+=1 
                if(query[i]=="OR" or query[i]=="or"):
                    if (query[i+1]=="NOT" or query[i+1]=="not"):

                        temp2=getposting_list(query[i+2])
                        if len(temp2)==0:
                            temp=temp.union(docs - set(temp2))
                        else:
                            temp=temp.union(docs)
                        i+=2
                    else:
                        temp=temp.union(set(getposting_list(query[i+1])))
                        i+=1

        return temp 
                    

def getpositionpostinglists(term):
    posting_list=[]
    for word,value in PositionalIndex.items():
        if word == term:
            #posting_list=PositionalIndex[word]
            return value
    #print(posting_list)

def positionalintersection(term1,term2,k):
    answer=[]
    p1=getpositionpostinglists(term1)
    p2=getpositionpostinglists(term2)
    print(p1)
    print(p2)
    #print(len(p1))
    #print(len(p2))
    i=0
    j=0
    doc_list_p1=[a_tuple[0] for a_tuple in p1]
    doc_list_p2=[a_tuple[0] for a_tuple in p2]
    
    pos_doc_list_p1=[a_tuple[1] for a_tuple in p1]
    pos_doc_list_p2=[a_tuple[1] for a_tuple in p2]

    


    while(i < (len(doc_list_p1)) and j < (len(doc_list_p2))):
        if((doc_list_p1[i] - doc_list_p2[j])==0):
            if((pos_doc_list_p2[j] - pos_doc_list_p1[i]) ==(k+1) ):
                answer.append(doc_list_p1[i])
                if(doc_list_p2[j+1]==doc_list_p1[i]):
                    j+=1
            else:
                j+=1
        
        elif( doc_list_p1[i] > doc_list_p2[j] ):
            j+=1
        elif( doc_list_p1[i] < doc_list_p2[j] ):
            i+=1
    return answer


def proximityQueryHandler(query):
    query=re.sub("AND","",query)
    query=re.sub("and","",query)
    query=query.split()

    term1=query[0]
    term2=query[1]

    #print(query[2])
    k=query[2].split("/")
    

    result=positionalintersection(term1,term2,int(k[1]))

    print(result)




def main():
    stopwords=[]
    fi=open("Stopword-List.txt",encoding='utf8')
    for lines in fi:
        for word in lines.split():
            stopwords.append(word)
    #print(stopwords)
    name=".txt"
    for i in range(1,51):
        file_list=[]
        f=open(str(i)+name,encoding='utf8')
        for li in f:
            new=remove_Stopwords_Punctuations(li)
            file_list+=new.split()
            new1=remove_Stopwords(new,stopwords)
            createInvertedIndex(new1,i)
            
            #print(new)
        createpositionalIndex(file_list,i,stopwords)
    f.close()
    fi.close()
main()
#print(InvertedIndex)
#print(PositionalIndex)
#getposting_list("powder")
storeInvertedIndex()
storePositionalIndex()
q=""
print("Line 264 contains path for stopword list  (Change Accordingly)")
print("Line 272 contains path for Shortstories list (Change Accordingly)")

while(q!="4"):
    print("Enter 1 to run queries mentioned :")
    print("Enter 2 to run your own boolean queries  :")
    print("Enter 3 to run your own proximity queries  :")
    print("Enter 4 to exit  :\n")
    q=input()
    print("\n")
    
    if(q=="1"):
        print("beard:  ",simplequeryHandler("beard"))
        print("passenger: ",simplequeryHandler("passenger"))
        print("permission and possible: ",simplequeryHandler("permission and possible"))
        print("power and play: ",simplequeryHandler("power and play "))
        print("ladies and gentleman: ",simplequeryHandler("ladies and gentleman"))
        print("strange and land and play: ",simplequeryHandler("strange and land and play"))
        print("god and man and love: ",simplequeryHandler("god and man and love"))
        print("not pleaser and not fever: ",simplequeryHandler("not pleaser and not fever"))
        print("smiling AND face /3: ")
        proximityQueryHandler("smiling AND face /3")
        print("filling room /1: ")
        proximityQueryHandler("filling room /1")
    elif (q=="2"):
        s=input("Enter Boolean Query(i.e smiling and face): ")
        print(simplequeryHandler(s))
        print("\n")
    elif (q=="3"):
        s=input("Enter Proximity Query(i.e. filling room /1): ")
        proximityQueryHandler(s)
        print("\n")


print("Total Time in seconds: ",(time.time()-start_time))

print(len(InvertedIndex))




