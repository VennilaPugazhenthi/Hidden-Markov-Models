############################################################
# CMPSC 442: Homework 6
############################################################

student_name = "Vennila Pugazhenthi"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import time


############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
    #create a empty list
    #load each sentence from the file
    #seperate each word by whitespaces put it in the list
    # iterate through each word seperate it put it in tuple put it in new list
    file=open(path,'r')
    top=[]
    for line in file:
        list1=line.split()
        line=[]
        for word in list1:
            newlist=word.split("=")
            tup=tuple(newlist)
            line.append(tup)
        top.append(line)
    return top


class Tagger(object):

    def __init__(self, sentences):
        self.sentences=sentences
        self.tag={"NOUN":0,"VERB":0,"ADJ":0,"ADV":0,"PRON":0,"DET":0,"ADP":0,"NUM":0,"CONJ":0,"PRT":0,".":0,"X":0}
        POS=["NOUN","VERB","ADJ","ADV","PRON","DET","ADP","NUM","CONJ","PRT",".","X"]
        self.POS_trans={}
        for w in POS:
            for w2 in POS:
                item=tuple([w,w2])
                self.POS_trans[item]=0
        self.sample={}
        total=0
        total_trans=0
        laplace_constant=1e-10
        list_of_tag=[]
        pair_num={}
        possibilities=len(self.tag)
        count=0
        pair_num=self.tag.copy()
        for line in self.sentences:
            count+=1
            for tup in line:
                if tup[1] in pair_num:
                    pair_num[tup[1]]+=1
                if tup in self.sample.keys():
                    self.sample[tup]+=1
                else:
                    self.sample[tup]=1
                list_of_tag.append(tup[1])
            if line[0][1] in self.tag:
                self.tag[line[0][1]]+=1
                total+=1

        for word in self.tag:
            num=self.tag[word]
            self.tag[word]= ((num+laplace_constant)/(total+(possibilities*laplace_constant)))
        #print(self.tag)
        for i in range(len(list_of_tag)-1):
            ele=tuple([list_of_tag[i],list_of_tag[i+1]])
            if ele in self.POS_trans:
                self.POS_trans[ele]+=1
                total_trans+=1
        for element in self.POS_trans:
            numerator=self.POS_trans[element]+laplace_constant
            denominator= total_trans+ (len(self.POS_trans)*laplace_constant)
            self.POS_trans[element]=numerator/denominator
        for pair in self.sample.keys():
            if pair[1] in pair_num:
                n=self.sample[pair]+ laplace_constant
                d = pair_num[pair[1]] + (12 * laplace_constant)
                #d=pair_num[pair[1]]+(pair_num[pair[1]]*laplace_constant)
                #d=pair_num[pair[1]]+(len(self.sample)*laplace_constant)
                self.sample[pair]=n/d



    def most_probable_tags(self, tokens):
        l=[]
        result=[]

        for each in tokens:
            small=[]
            for item in self.sample.keys():
                if each == item[0]:
                    a=item
                    b=self.sample[item]
                    small.append([a,b])
            if(len(small)==0):
                a=(each,'X')
                b=0
                small.append([a,b])
            #print("Small")  //TODO: to assign "X" if the item wasn't in self.sample
            #print(small)
            l.append(max(small,key=lambda p:p[1]))
            #l.append(small)
        #print(l)
        for each in l:
            #print(each)
            result.append(each[0][1])
        return (result)

    def viterbi_tags(self, tokens):
        delta={}
        back={}
        for element in self.tag:
            tup=(0,element)
            if (tokens[0],element) in self.sample:
                delta[tup]=self.tag[element]*self.sample[(tokens[0],element)]
            else:
                delta[tup]=1e-10
        for i in range(1,len(tokens)):
            for element in self.tag:
                tup=(i,element)
                bestprob=0
                bestprevtag="X"
                for tag in self.tag:
                    prob=0
                    if (tag,element) in self.POS_trans:
                        prob= delta[(i-1,tag)]*self.POS_trans[(tag,element)]
                    if prob>bestprob:
                        bestprob=prob
                        bestprevtag=tag
                if(tokens[i],element)in self.sample:
                    delta[(i,element)]=bestprob*self.sample[(tokens[i],element)]
                else:
                    delta[(i,element)]=1e-20*bestprob
                back[(i,element)]=bestprevtag
                #print(tokens[i],element,bestprevtag,bestprob,element)
        #besttagprob=[]
        besttag=[]
        for i in range(0,len(tokens)):
            bestprob = 0
            bestprevtag = "X"
            for ele in self.tag:
                prob=delta[(i,ele)]
                if prob > bestprob:
                    bestprob = prob
                    bestprevtag = ele
            #besttagprob.append(bestprob)
            besttag.append(bestprevtag)
            #print(tokens[i], bestprevtag, bestprob)
        for j in range(len(tokens)-1,0,-1):
            #print(j, tokens[j], besttag[j])
            besttag[j-1]=back[(j,besttag[j])]
        return (besttag)








# t1=time.time()
# c=load_corpus("brown-corpus.txt")
# print(c[1402])
# print(c[1799])
# t2=time.time()
# print(t2-t1)
# t3=time.time()
# c=load_corpus("brown-corpus.txt")
# t=Tagger(c)
# t4=time.time()
# print(t4-t3)
# #
# # c=load_corpus("brown-corpus.txt")
# t5=time.time()
# t=Tagger(c)
#
# print(t.most_probable_tags(["The","man","walks","."]))
# print(t.most_probable_tags(["The","blue","bird","sings"]))
# t6=time.time()
# print(t6-t5)
# # t1=time.time()
# # c2=load_corpus("brown-corpus.txt")
# # t=Tagger(c2)
# # s="no evidence that irregularities any The Fulton County Grand Jury said Friday an investigation of Atlanta's recent primary election produced".split()
# # print(t.most_probable_tags(s))
# # print(t.viterbi_tags(s))
# # t2=time.time()
# # print(t2-t1)
# #t1=time.time()
# # # t5=time.time()
# c3=load_corpus("brown-corpus.txt")
# t2=Tagger(c3)
# # # s2="Below is a list of research areas tackled by our faculty".split()
# # #print(t2.most_probable_tags(s2))
# # print(t2.most_probable_tags(s2))
# # print(t2.viterbi_tags(s2))
# #
# # s3="I am waiting to reply".split()
# # print(t2.most_probable_tags(s3))
# # print(t2.viterbi_tags(s3))
# #
# s4="Below is a list of research areas tackled by our faculty".split()
# print(t2.most_probable_tags(s4))
# print(t2.viterbi_tags(s4))
# s3="I am waiting to reply".split()
# print(t2.most_probable_tags(s3))
# print(t2.viterbi_tags(s3))
# s5="I saw the play".split()
# print(t2.most_probable_tags(s5))
# print(t2.viterbi_tags(s5))
# #t2=time.time()
# #t6=time.time()
# #print(t6-t5)

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
I spent 20 hrs on this assignment.
"""

feedback_question_2 = """
I found understanding the initial,transition and emission probability to be challenging.
I also stumbled in implementing the viterbi decoder.
"""

feedback_question_3 = """
I liked the most_propable_tag() because the implementation of it was easy to 
understand. I would have divided the viterbi decoder function into smaller 
problems so its easier to understand and implement it.
"""
