import string
import re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

lemma = WordNetLemmatizer()
stop = set(stopwords.words('english'))

## list for storing postive and negative reviews
pos_rev = []
neg_rev = []
train_file = []
test_file = []
valid_file = []
training_file = open('1599165963_0346937_train_file.txt', 'r', encoding="utf-8")
test_file = open('1599165963_120247_test_file.txt', 'r', encoding="utf-8")

# append positive and negative reviews depending on their status
for ele in training_file:
    if ele[0] == '1':
        pos_rev.append(ele)
    else:
        neg_rev.append(ele)


# filtering out list for positive and negative reviews by passing list in the parameter
def preProcess(text_file):
    for element in range(len(text_file)):
        text_file[element] = text_file[element].lower()
        text_file[element] = re.sub('[%s]' % re.escape(string.punctuation), '', text_file[element])
        text_file[element] = re.sub('\w*\d\w*', '', text_file[element])
        tokenizers = text_file[element].split()
        text_file[element] = tokenizers
        text_file[element] = [eachWord for eachWord in text_file[element] if eachWord not in stop]
        for subEle in range(len(text_file[element])):
            text_file[element][subEle] = lemma.lemmatize(text_file[element][subEle])

    return text_file


# filtering out test file by passing test file as a parameter
def preProcessForTestFile(text_file):
    text_file = text_file.lower()
    text_file = re.sub('[%s]' % re.escape(string.punctuation), '', text_file)
    text_file = re.sub('\w*\d\w*', '', text_file)
    tokenizers = text_file.split()
    text_file = tokenizers
    text_file = [eachWord for eachWord in text_file if eachWord not in stop]
    for subEle in range(len(text_file)):
        text_file[subEle] = lemma.lemmatize(text_file[subEle])
    return text_file


# using knn. Passing list of positive and negative reviews and word test file
def knn(listType, word):
    score = 0
    for i in range(len(listType)):
        if score < 10:
            for wording in listType[i]:
                if (wording == word):
                    score = score + 1

        else:
            break

    return score


preProcess(pos_rev)
preProcess(neg_rev)

# create a list to store 1 and -1
score = []
testFile = []
counter = 0

# appends test file into list name testFile
with test_file as FILE:
    for LINE in FILE:
        testFile.append(LINE)

for line in testFile:

    clean_testFile = preProcessForTestFile(line)

    positive_score = 0
    negative_score = 0
    # appends the score and finds its difference
    for word in clean_testFile:
        negative_score = negative_score + knn(neg_rev, word)
        positive_score = positive_score + knn(pos_rev, word)

    K_score = positive_score - negative_score

    if K_score >= 0:
        score.append('1')
    else:
        score.append('-1')

# writes from list to text file named formatedFile
with open('formatedFile.txt', 'w', encoding="utf-8") as finalFile:
    finalFile.writelines("%s\n" % place for place in score)
