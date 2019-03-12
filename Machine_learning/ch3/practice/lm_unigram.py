import math, collections

corpus = [
    'I am Sam',
    'Sam I am',
    'I do not like green'
]

# Counting
unigram_counts = collections.defaultdict(int)
for sentence in corpus:
    words = sentence.split()
    for word in words:
        unigram_counts[word] += 1

# Printing unigram counts
print('- Unigram counts -')
for word in unigram_counts:
    print(('unigram_count[%s] = %d'%(word, unigram_counts[word])))

# Unigram function
def unigram(word):
    return float(unigram_counts[word]) / sum(unigram_counts.values())
        
# Printing results
print('\n- Unigram probabilities - ')
print(('P(Sam) = %f'%unigram('Sam')))
print(('P(I) = %f'%unigram('I')))
print(('P(green) = %f'%unigram('green')))