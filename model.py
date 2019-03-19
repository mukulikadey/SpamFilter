import re
import string
from collections import OrderedDict
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
            with open(file, 'r+', encoding="latin-1") as f:
                contents = re.split('\[\^a-zA-Z\]', f.read())  # an array of one item
            words = contents[0]
            words = clean_words(words)
            tokens = preprocess(words)

            total_spam_tokens += len(tokens)

            for token in tokens:
                if token not in index.keys():
                    class_metrics = ClassMetrics()
                    class_metrics.set_spam_frequency()
                    index[token] = class_metrics
                else:
                    obj = index[token]
                    obj.set_spam_frequency()
        elif HAM in file:
            with open(file, 'r+', encoding="latin-1") as f:
                contents = re.split('\[\^a-zA-Z\]', f.read())  # an array of one item
            words = contents[0]
            words = clean_words(words)
            tokens = preprocess(words)
            total_ham_tokens += len(tokens)

            for token in tokens:
                if token not in index.keys():
                    class_metrics = ClassMetrics()
                    class_metrics.set_ham_frequency()
                    index[token] = class_metrics
                else:
                    obj = index[token]
                    obj.set_ham_frequency()

    compute_probability(index, total_ham_tokens, total_spam_tokens)

    return index


def clean_words(words):
    split_words = words.replace('<', ' ') \
        .replace('>', ' ') \
        .replace('/', ' ') \
        .replace('=', ' ') \
        .replace('%', ' ') \
        .replace('_', ' ') \
        .replace('#', ' ') \
        .replace('(', ' ') \
        .replace(')', ' ') \
        .replace(':', ' ') \
        .replace(':', ' ') \
        .replace('-', ' ') \
        .replace('@', ' ') \
        .replace('.', ' ') \
        .replace('+', ' ') \
        .replace('?', ' ') \
        .replace('!', ' ') \
        .replace('&', ' ') \
        .replace('$', ' ') \
        .replace('[', ' ') \
        .replace(']', ' ') \
        .split()

    return split_words


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
    smoothing = 0.5
    vocab_size = len(index.keys())
    for key, value in index.items():
        spam_freq = value.get_spam_frequency()
        ham_freq = value.get_ham_frequency()

        spam_prob = (spam_freq + smoothing)/ (total_spam + vocab_size)
        ham_prob = (ham_freq + smoothing)/ (total_ham + vocab_size)

        value.set_spam_probability(spam_prob)
        value.set_ham_probability(ham_prob)


def output_index_to_file(index):
    f = open("model.txt", "w+", encoding="latin-1")
    counter = 0
    for key, value in sorted(index.items()):
        counter += 1
        f.write(str(counter)+"  "+key+"  "+str(value.get_ham_frequency())+"  "+str(value.get_ham_probability())+"  "+
                str(value.get_spam_frequency())+"  "+str(value.get_spam_probability())+"\r")


if __name__ == "__main__":
    index = parse_corpus()
    output_index_to_file(index)
