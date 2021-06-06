import re
import copy


global lambda3, lambda2, lambda1, epsilon

ferdowsiUnigram = dict()
ferdowsiBigram = dict()

hafezUnigram = dict()
hafezBigram = dict()

molaviUnigram = dict()
molaviBigram = dict()

SENTENCE_START = "<s>"
SENTENCE_END = "</s>"


"""global htotalWords
global ftotalWords
global mtotalWords
"""
ftotalWords = 0
htotalWords = 0
mtotalWords = 0

# array = [re.split("\s+", line.rstrip('\n')) for line in files]
def generateUniTokens(fileName):
    global htotalWords
    global ftotalWords
    global mtotalWords
    dir = "train_set/" + fileName
    with open(dir, "r", encoding="utf-8") as files:
        array = []
        with open(dir, "r", encoding="utf-8") as files:
            for line in files:
                sntnc = re.split("\s+", line.rstrip('\n'))
                sntnc.insert(0, SENTENCE_START)
                sntnc.append(SENTENCE_END)
                array.append(sntnc)
    for element in array:
        for word in element:
            if fileName == "hafez_train.txt":
                htotalWords += 1
                if word in hafezUnigram.keys():
                    hafezUnigram[word] = hafezUnigram[word] + 1
                else:
                    hafezUnigram[word] = 1
            if fileName == "ferdowsi_train.txt":
                ftotalWords += 1
                if word in ferdowsiUnigram.keys():
                    ferdowsiUnigram[word] = ferdowsiUnigram[word] + 1
                else:
                    ferdowsiUnigram[word] = 1
            if fileName == "molavi_train.txt":
                mtotalWords += 1
                if word in molaviUnigram.keys():
                    molaviUnigram[word] = molaviUnigram[word] + 1
                else:
                    molaviUnigram[word] = 1



def unigramProbs(data):
    data2 = copy.deepcopy(data)
    if data2 == ferdowsiUnigram:
        for key in data2.keys():
            data2[key] = data2[key] / ftotalWords
    if data2 == hafezUnigram:
        for key in data2.keys():
            data2[key] = data2[key] / htotalWords
    if data2 == molaviUnigram:
        for key in data2.keys():
            data2[key] = data2[key] / mtotalWords
    return data2


generateUniTokens("ferdowsi_train.txt")
generateUniTokens("hafez_train.txt")
generateUniTokens("molavi_train.txt")
for key, val in list(ferdowsiUnigram.items()):
    if val < 2:
        del ferdowsiUnigram[key]
for key, val in list(hafezUnigram.items()):
    if val < 2:
        del hafezUnigram[key]
for key, val in list(molaviUnigram.items()):
    if val < 2:
        del molaviUnigram[key]
fer = unigramProbs(ferdowsiUnigram)
haf = unigramProbs(hafezUnigram)
mol = unigramProbs(molaviUnigram)

#print(ferdowsiUnigram)


def generateBiTokens(fileName):
    dir = "train_set/" + fileName
    sentences = []
    with open(dir, "r", encoding="utf-8") as files:
        for line in files:
            sntnc = re.split("\s+", line.rstrip('\n'))
            sntnc.insert(0, SENTENCE_START)
            sntnc.append(SENTENCE_END)
            sentences.append(sntnc)
    for sentence in sentences:
        previous_word = None
        for word in sentence:
            if fileName == "ferdowsi_train.txt":
                if previous_word != None:
                    ferdowsiBigram[(previous_word, word)] = ferdowsiBigram.get((previous_word, word), 0) + 1
                previous_word = word
            if fileName == "hafez_train.txt":
                if previous_word != None:
                    hafezBigram[(previous_word, word)] = hafezBigram.get((previous_word, word), 0) + 1
                previous_word = word
            if fileName == "molavi_train.txt":
                if previous_word != None:
                    molaviBigram[(previous_word, word)] = molaviBigram.get((previous_word, word), 0) + 1
                previous_word = word


#generateBiTokens("hafez_train.txt")
#print(hafezBigram)

def bigramProbs(data):
    for key in data.keys():
        if data == ferdowsiBigram:
            if key[0] in ferdowsiUnigram.keys():
                data[key] = data[key] / ferdowsiUnigram.get(key[0])
            else:
                data[key] = data[key] / 1
            # print(ferdowsiUnigram[key[0]])
        if data == hafezBigram:
            if key[0] in hafezUnigram.keys():
                data[key] = data[key] / hafezUnigram.get(key[0])
            else:
                data[key] = data[key] / 1
        if data == molaviBigram:
            if key[0] in molaviUnigram.keys():
                data[key] = data[key] / molaviUnigram.get(key[0])
            else:
                data[key] = data[key] / 1


generateBiTokens("ferdowsi_train.txt")
generateBiTokens("hafez_train.txt")
generateBiTokens("molavi_train.txt")

for key, val in list(ferdowsiBigram.items()):
    if val < 2:
        del ferdowsiBigram[key]
for key, val in list(hafezBigram.items()):
    if val < 2:
        del hafezBigram[key]
for key, val in list(molaviBigram.items()):
    if val < 2:
        del molaviBigram[key]
#print("done")
bigramProbs(ferdowsiBigram)
bigramProbs(hafezBigram)
bigramProbs(molaviBigram)
#print("done")

def ferdowsiCalculator(array):
    total = 1
    for set in array:
        bigram = 0
        unigram = 0
        if set in ferdowsiBigram.keys():
            bigram = ferdowsiBigram[set]
        if set[0] in fer.keys():
            unigram = fer[set[0]]
        part1 = lambda3 * float(bigram) + lambda2 * float(unigram) + lambda1 * epsilon
        total = total * part1
    return total


def hafezCalculator(array):
    total = 1
    for set in array:
        bigram = 0
        unigram = 0
        if set in hafezBigram.keys():
            bigram = hafezBigram[set]
        if set[0] in haf.keys():
            unigram = haf[set[0]]
        part1 = lambda3 * float(bigram) + lambda2 * float(unigram) + lambda1 * epsilon
        total = total * part1
    return total

def molaviCalculator(array):
    total = 1
    for set in array:
        bigram = 0
        unigram = 0
        if set in molaviBigram.keys():
            bigram = molaviBigram[set]
        if set[0] in mol.keys():
            unigram = mol[set[0]]
        part1 = lambda3 * float(bigram) + lambda2 * float(unigram) + lambda1 * epsilon
        total = total * part1
    return total


def backOffModel():
    dir = "test_set/test case - 3.txt"
    oneRights = 0
    twoRights = 0
    threeRights = 0
    totalOnes = 0
    totalTwos = 0
    totalThrees = 0
    totalRights = 0
    sentences = []
    with open(dir, "r", encoding="utf-8") as files:
        for line in files:
            sntnc = re.split("\s+", line.rstrip('\n'))
            sntnc.insert(0, SENTENCE_START)
            sntnc.append(SENTENCE_END)
            a = sntnc.pop(1)
            sntnc.append(a)
            sentences.append(sntnc)
    for sentence in sentences:
        previous_word = None
        candidate = []
        for word in sentence:
            if previous_word != None:
                candidate.append((previous_word, word))
            previous_word = word
        model1 = ferdowsiCalculator(candidate)
        model2 = hafezCalculator(candidate)
        model3 = molaviCalculator(candidate)
        maximum = max(model1, model2, model3)
        if maximum == model1:
            returned = 1
        if maximum == model2:
            returned = 2
        if maximum == model3:
            returned = 3

        if returned == int(sentence[-1]) and returned == 1:
            oneRights += 1
        if returned == int(sentence[-1]) and returned == 2:
            twoRights += 1
        if returned == int(sentence[-1]) and returned == 3:
            threeRights += 1
        if int(sentence[-1]) == 1:
            totalOnes += 1
        if int(sentence[-1]) == 2:
            totalTwos += 1
        if int(sentence[-1]) == 3:
            totalThrees += 1
        if returned == int(sentence[-1]):
            totalRights += 1

    print("total percentage: "+ str(float(totalRights/len(sentences))))
    print("ferdowsi percentage: " + str(float((oneRights/totalOnes)*100)))
    print("hafez percentage: " + str(float((twoRights / totalTwos) * 100)))
    print("molavi percentage: " + str(float((threeRights / totalThrees) * 100)))



lambda3 = 0.9
lambda2 = 0.99
lambda1 = 0.01
epsilon = 0.001


backOffModel()



# part1 = 0.9 * float(bigram) + 0.99 * float(unigram) + 0.01 * 0.001