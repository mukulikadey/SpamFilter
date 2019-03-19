import re
import string
from glob import iglob
from ClassMetrics import ClassMetrics

SPAM = "spam"
HAM = "ham"


def parse_corpus():
    training_files = []
    index = dict()
    total_spam_tokens = 0
    total_ham_tokens = 0

    for pathname in iglob('train/train-*.txt'):
        training_files.append(pathname)
    for file in training_files:
        if SPAM in file:
            with open(file, 'r+') as f:
                contents = re.split('\[\^a-zA-Z\]', f.read())  # an array of one item
            words = contents[0].split()
            tokens = preprocess(words)
            total_spam_tokens = len(tokens)
            print("spam:", tokens)
            for token in tokens:
                if token not in index.keys():
                    class_metrics = ClassMetrics()
                    class_metrics.set_spam_frequency()
                    index[token] = class_metrics
                else:
                    obj = index[token]
                    obj.set_spam_frequency()
        elif HAM in file:
            with open(file, 'r+') as f:
                contents = re.split('\[\^a-zA-Z\]', f.read())  # an array of one item
            words = contents[0].split()
            tokens = preprocess(words)
            total_ham_tokens = len(tokens)
            print("ham:", tokens)
            for token in tokens:
                if token not in index.keys():
                    class_metrics = ClassMetrics()
                    class_metrics.set_ham_frequency()
                    index[token] = class_metrics
                else:
                    obj = index[token]
                    obj.set_ham_frequency()


    # for key, value in index.items():
    #     print("IN PARSE: ", key, value.get_ham_frequency(), value.get_spam_frequency())

    compute_probability(index, total_ham_tokens, total_spam_tokens)

    # for key, value in index.items():
    #     print("IN PROB: ", key, value.get_ham_frequency(), value.get_spam_frequency())

    return index


def preprocess(words):
    normalized_tokens = []

    for word in words:
        result = ''.join(c for c in word if c not in string.punctuation)
        result = ''.join([i for i in result if not i.isdigit()])
        result = result.lower()
        if result is not '' and result not in normalized_tokens:
            normalized_tokens.append(result)
    return normalized_tokens


def compute_probability(index, total_ham, total_spam):

    for key, value in index.items():
        spam_freq = value.get_spam_frequency()
        ham_freq = value.get_ham_frequency()

        spam_prob = spam_freq / total_spam
        ham_prob = ham_freq / total_ham

        value.set_spam_probability(spam_prob)
        value.set_ham_probability(ham_prob)


if __name__ == "__main__":
    index = parse_corpus()

    # for key, value in index.items():
    #     print(key, value.get_ham_frequency(), value.get_spam_frequency(), value.get_ham_probability(), value.get_spam_probabilty() )

