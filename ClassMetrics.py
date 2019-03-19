class ClassMetrics:

    def __init__(self):
        self.spam_frequency = 0
        self.spam_probability = 0.0
        self.ham_frequency = 0
        self.ham_probability = 0.0

    def get_spam_frequency(self):
        return self.spam_frequency

    def get_spam_probability(self):
        return self.spam_probability

    def get_ham_frequency(self):
        return self.ham_frequency

    def get_ham_probability(self):
        return self.ham_probability

    def set_spam_frequency(self):
        self.spam_frequency += 1

    def set_spam_probability(self, spam_probability):
        self.spam_probability = spam_probability

    def set_ham_frequency(self):
        self.ham_frequency += 1

    def set_ham_probability(self, ham_probability):
        self.ham_probability = ham_probability
