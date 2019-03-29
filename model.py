import math
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
                contents = re.split('[^a-zA-Z]', f.read())  # an array of one item
            words = contents
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
                    index[token] = obj
        elif HAM in file:
            with open(file, 'r+', encoding="latin-1") as f:
                contents = re.split('[^a-zA-Z]', f.read())  # an array of one item

            words = contents
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
                    index[token] = obj

    compute_probability(index, total_ham_tokens, total_spam_tokens)

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
    smoothing = 0.5
    vocab_size = len(index.keys())
    for key, value in index.items():
        spam_freq = value.get_spam_frequency()
        ham_freq = value.get_ham_frequency()

        spam_prob = (spam_freq + smoothing)/ (total_spam + vocab_size*smoothing)
        ham_prob = (ham_freq + smoothing)/ (total_ham + vocab_size*smoothing)

        value.set_spam_probability(spam_prob)
        value.set_ham_probability(ham_prob)


def probability_classes():
    spam_files = 997
    ham_files = 1000

    ham_probability = ham_files / (ham_files + spam_files)
    spam_probability = spam_files / (ham_files + spam_files)

    return ham_probability, spam_probability


def output_index_to_file(index):
    f = open("model.txt", "w+", encoding="latin-1")
    count = 0
    for key, value in sorted(index.items()):
        count += 1
        f.write(str(count)+"  "+key+"  "+str(value.get_ham_frequency())+"  "+str(value.get_ham_probability())+"  "+
                str(value.get_spam_frequency())+"  "+str(value.get_spam_probability())+"\r")


def classifier(index, type):
    training_files = []
    ham_prob_total = probability_classes()[0]
    spam_prob_total = probability_classes()[1]
    ham_score = 0
    spam_score = 0
    count = 0

    for pathname in iglob('test/test-*.txt'):
        training_files.append(pathname)
    for file in training_files:
        with open(file, 'r+', encoding="latin-1") as f:
            contents = re.split('[^a-zA-Z]', f.read())  # an array of one item
        words = contents
        tokens = preprocess(words)
        ham_prob = 0
        spam_prob = 0

        for token in tokens:
            for key, value in index.items():
                if token == key:
                    ham_prob += math.log10(value.get_ham_probability())
                    spam_prob += math.log10(value.get_spam_probability())
        ham_score = math.log10(ham_prob_total) + ham_prob
        spam_score = math.log10(spam_prob_total) + spam_prob

        count = count + 1
        write_baseline_text(file, ham_score, spam_score, count, type)
        print("wrote to file", count)


def write_baseline_text(file, ham_score, spam_score, count, type):
    if type == "stop":
        f = open("stopword-result.txt", "a")
    elif type == "word":
        f = open("wordlength-result.txt", "a")
    else:
        f = open("baseline-result.txt", "a")

    class_name = ''
    correct_class = ''
    check = ''

    if HAM in file:
        class_name = "ham"
    elif SPAM in file:
        class_name = "spam"

    if ham_score > spam_score:
        correct_class = "ham"
    else:
        correct_class = "spam"

    if class_name == correct_class:
        check = "right"
    else:
        check = "wrong"

    f.write(str(count) + "  " + file + "  " + class_name + "  " + str(ham_score) + "  " +
            str(spam_score) + "  " + correct_class + "  " + check + "\r")


def remove_stopwords():
    stop_words_list = []
    with open('English-Stop-Words.txt', 'r+') as f:
        for line in f:
            stop_words_list.append(line.rstrip())
    return stop_words_list


def output_index_to_file_stop_words(index):
    list_sw = remove_stopwords()

    for word in list_sw:
        for key in list(index.keys()):
            if word == key:
                index.pop(key)

    f = open("stopword-model.txt", "w+", encoding="latin-1")
    count = 0
    for key, value in sorted(index.items()):
        count += 1
        f.write(str(count)+"  "+key+"  "+str(value.get_ham_frequency())+"  "+str(value.get_ham_probability())+"  "+
                str(value.get_spam_frequency())+"  "+str(value.get_spam_probability())+"\r")


def output_index_to_file_word_length(index):
        for key in list(index.keys()):
            if len(key) <= 2 or len(key) >= 9:
                index.pop(key)

        f = open("wordlength-model.txt", "w+", encoding="latin-1")
        count = 0
        for key, value in sorted(index.items()):
            count += 1
            f.write(str(count) + "  " + key + "  " + str(value.get_ham_frequency()) + "  " + str(
                value.get_ham_probability()) + "  " +
                    str(value.get_spam_frequency()) + "  " + str(value.get_spam_probability()) + "\r")


if __name__ == "__main__":
    index = parse_corpus()

    # REGULAR CLASSIFIER
    # output_index_to_file(index)
    # classifier(index)

    # STOP-WORD REMOVER CLASSIFIER
    # output_index_to_file_stop_words(index)
    # classifier(index, "stop")

    # WORD-LENGTH CLASSIFIER
    # output_index_to_file_word_length(index)
    # classifier(index, "word")