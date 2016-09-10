from difflib import SequenceMatcher

def gets(s1, s2):
    return getStringSimilarity(s1, s2)

def getStringSimilarity(s1, s2):

    t1 = s1.lower().split(' ')
    t2 = s2.lower().split(' ')
    
    p1 = []
    for i in range(len(t1)):
        p1.append([])
        for j in range(len(t2)):
            a = t1[i]
            b = t2[j]
            p1[-1].append((SequenceMatcher(None, a, b).ratio() * 0.4**(abs(i-j))))

    tp = 0
    tc = 0
    for i in p1:
        tp += max(i)
        tc += 1

    tp2 = 0
    tc2 = 0
    for i in range(len(p1[0])):
        tp2 += max([j[i] for j in p1])
        tc2 += 1
    
    return ((tp/tc) + (tp2/tc2))/2

def getSingleStringSimilarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def getPersonSimilarity(p1, p2):
    sim = 0
    kol = 0
    
    for i in p1.keywords:
        if i in p2.keywords:
            sim += 1
        kol += 1
    
    for i in p1.papers:
        if (i.title in [ppp.strip() for ppp in p2.papers]):
            sim += 1
        kol += 1
    if (p1.photo and p2.photo):
        if (p1.photo == p2.photo):
            sim += 1000
            kol += 1000
    
    if (p1.occupation and p2.occupation):
        kol += 50
        sim += int(50*getStringSimilarity(p1.occupation, p2.occupation))
    return float(sim) / kol

