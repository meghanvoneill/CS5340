from pprint import pprint
import sys
import string
import math
import operator


# Author: Meghan V. O'Neill
# For Program 3: Part 2 - Nearest-Neighbor Algorithm
# Natural Language Processing, Fall 2020, Professor Riloff, University of Utah

# Tested with: python3 distsim.py data/train.txt data/test.txt data/stopwords.txt 2
def main():

    # Read in arguments.
    args = sys.argv[1:]
    training_sentences_file = args[0]
    test_sentences_file = args[1]
    stopwords_file = args[2]
    k = int(args[3])
    output_file_name = test_sentences_file + '.distsim'

    # Read in data from given files.
    training_sentences, training_frequencies, sense_inventory = read_training_sentences_file(training_sentences_file)
    test_sentences = read_test_sentences_file(test_sentences_file)
    stopwords = read_stopwords_file(stopwords_file)

    # Build vocabulary.
    vocab, vocab_frequencies = build_vocabulary(training_sentences, k, stopwords, training_frequencies)

    # Build signature vectors.
    signature_vectors = create_signature_vectors(training_sentences, sense_inventory, k, vocab, vocab_frequencies)

    # Test on test sentences.
    output = test(test_sentences, signature_vectors, vocab, vocab_frequencies, k)

    # Write output to file.
    write_output(output_file_name, output, len(training_sentences), len(test_sentences), len(sense_inventory), len(vocab))

    return


# Read in training sentences file.
#
#   training_sentences = [sentences]
#   sentences = [sentence = {'goldsense': goldsense, 'target': '', 'target index': 0, 'words': []}]
#
#   frequencies = {'words': [], 'frequencies': [], 'frequencies, index by word': {}}
#   frequencies['frequencies by word'][word] = {'index': len(frequencies['words']) - 1, 'frequency': 1}
def read_training_sentences_file(file_name):

    training_sentences = []
    frequencies = {'words': [], 'frequencies': [], 'frequencies, index by word': {}}
    sense_inventory = set()

    with open(file_name, 'r') as f:
        for line in f.readlines():
            line = line.split('\t')
            # If there is data in the line.
            if len(line) > 0:
                # Separate the goldsense label from the sentence.
                goldsense_and_product = line[0]
                tagged_sentence = line[1].split()

                # Isolate the label for goldsense.
                g_and_p = goldsense_and_product.split(':')
                goldsense = g_and_p[1]
                sentence = {'goldsense': goldsense, 'words': []}
                sense_inventory.add(goldsense)

                # Add words in the sentence and find the target occurrence word.
                for word in tagged_sentence:
                    word = word.lower()
                    # Found occurrence word. Strip off tagging and add as target to sentence.
                    if word.startswith('<occurrence>'):
                        divided_word_array = word.split('>')
                        divided_word_array = divided_word_array[1].split('<')
                        word = divided_word_array[0]
                        sentence['target'] = word
                        sentence['target index'] = int(len(sentence['words']))
                    # Otherwise, this isn't the occurrence word, so add it to the sentence array.
                    else:
                        sentence['words'].append(word)

                        # If the word is already in our frequencies dictionary, increment it's count at it's
                        #   index position.
                        if word in frequencies['frequencies, index by word'].keys():
                            index = frequencies['frequencies, index by word'][word]['index']
                            frequencies['frequencies'][index] += 1
                            frequencies['frequencies, index by word'][word]['frequency'] += 1
                        # Otherwise, the word needs to be added to our frequencies dictionary.
                        else:
                            frequencies['words'].append(word)
                            frequencies['frequencies'].append(1)
                            frequencies['frequencies, index by word'][word] = \
                                {'index': int(len(frequencies['words']) - 1), 'frequency': 1}
                training_sentences.append(sentence)

    return training_sentences, frequencies, sense_inventory


# Read in test sentences file.
def read_test_sentences_file(file_name):

    test_sentences = []

    with open(file_name, 'r') as f:
        for line in f.readlines():
            line = line.split()
            # If there is data in the line.
            if len(line) > 0:
                # Trim newline character.
                tagged_sentence = line
                sentence = {'words': []}
                # Add words in the sentence and find the target occurrence word.
                for word in tagged_sentence:
                    # Found occurrence word. Strip off tagging and add as target to sentence.
                    if word.startswith('<occurrence>'):
                        divided_word_array = word.split('>')
                        divided_word_array = divided_word_array[1].split('<')
                        word = divided_word_array[0]
                        sentence['target'] = word
                        sentence['target index'] = int(len(sentence['words']))
                    # Otherwise, this isn't the occurrence word, so add it to the sentence array.
                    else:
                        sentence['words'].append(word)
                test_sentences.append(sentence)

    return test_sentences


# Read in stopwords file.
def read_stopwords_file(file_name):

    stopwords = set()

    with open(file_name, 'r') as f:
        for line in f.readlines():
            line = line.split()
            if len(line) > 0:
                word = line[0]
                stopwords.add(word)

    return stopwords


def write_output(file_name, output, training_number, test_number, goldsense_number, vocabulary_number):

    with open(file_name, 'w') as f:
        # Write statistics.
        f.write('Number of Training Sentences = ' + str(training_number) + '\n')
        f.write('Number of Test Sentences = ' + str(test_number) + '\n')
        f.write('Number of Gold Senses = ' + str(goldsense_number) + '\n')
        f.write('Vocabulary Size = ' + str(vocabulary_number) + '\n')

        # Write ouput data.
        for sentence_result in output:
            line = ''
            for pair in sentence_result:
                sense = operator.getitem(pair, 1)
                prob = operator.getitem(pair, 0)
                line += str(sense) + '(' + str(prob) + ') '
            line = line.strip()
            line += '\n'
            f.write(line)

    return


# Build a vocabulary from the given training sentences, within the context window size, excluding punctuation,
# normalizing to lowercase, and excluding frequency counts of 1.
#
#   sentences = [sentence = {'goldsense': goldsense, 'target': '', 'target index': 0, 'words': []}]
#   frequencies['frequencies by word'][word] = {'index': len(frequencies['words']) - 1, 'frequency': 1}
def build_vocabulary(training_sentences, context_window_size, stopwords, frequencies):

    vocabulary = set()
    vocab_frequencies = {'words': [], 'frequencies': [], 'frequencies, index by word': {}}
    punctuation = set(string.punctuation)

    for sentence in training_sentences:

        min_index, max_index = get_context_indices(sentence, context_window_size)

        # Gather all the words within the context window of the target.
        for i in range(min_index, max_index):
            # Grab the next word and convert to lowercase.
            word = sentence['words'][i]
            word = word.lower()

            # If word is a stopword, has no alphabetical letters, or has a frequency count of 1, do not add it.
            frequency = frequencies['frequencies, index by word'][word]['frequency']
            if word not in stopwords and word not in punctuation and frequency > 1:
                # If we can remove punctuation from the word and still have characters, the word must contain
                #   alphanumeric characters.
                punc_removed_word = word.translate(str.maketrans('', '', string.punctuation))
                if len(punc_removed_word) > 0:
                    # If we can remove digits from the word and still have characters, the word must be valid.
                    digits_removed_word = punc_removed_word.translate(str.maketrans('', '', string.digits))
                    if len(digits_removed_word) > 0:
                        vocabulary.add(word)

                        # If the word is already in our frequencies dictionary, increment it's count at it's
                        #   index position.
                        if word in vocab_frequencies['frequencies, index by word'].keys():
                            index = vocab_frequencies['frequencies, index by word'][word]['index']
                            vocab_frequencies['frequencies'][index] += 1
                            vocab_frequencies['frequencies, index by word'][word]['frequency'] += 1
                        # Otherwise, the word needs to be added to our frequencies dictionary.
                        else:
                            vocab_frequencies['words'].append(word)
                            vocab_frequencies['frequencies'].append(1)
                            vocab_frequencies['frequencies, index by word'][word] = \
                                {'index': int(len(vocab_frequencies['words']) - 1), 'frequency': 1}

    return vocabulary, vocab_frequencies


# Create a signature vector for each sense.
#
#   sentences = [sentence = {'goldsense': goldsense, 'target': '', 'target index': 0, 'words': []}]
#   frequencies = {'words': [], 'frequencies': [], 'frequencies, index by word': {}}
#   frequencies['frequencies by word'][word] = {'index': len(frequencies['words']) - 1, 'frequency': 1}
def create_signature_vectors(training_sentences, sense_inventory, context_window_size, vocabulary, vocab_frequencies):

    signature_vectors = {}

    # Create a signature vector for each sense.
    for sense in sense_inventory:
        # Add the sense to our signature vectors.
        signature_vectors[sense] = [0] * len(vocabulary)

        # Collect all sentences that contain the instances of the target word labelled sense, and extract the context.
        for sentence in training_sentences:
            if sentence['goldsense'] == sense:
                vector = create_context_vector(sentence, vocabulary, vocab_frequencies, context_window_size)
                signature_vectors[sense] = [sum(x) for x in zip(signature_vectors[sense], vector)]

    return signature_vectors


def create_context_vector(sentence, vocabulary, vocab_frequencies, context_window_size):

    # Find the context indices for the sentence.
    context = []
    min_index, max_index = get_context_indices(sentence, context_window_size)

    # Gather all the words within the context window of the target.
    for i in range(min_index, max_index):
        # Grab the next word and convert to lowercase.
        word = sentence['words'][i]
        word = word.lower()
        context.append(word)

    # Create a vector of size |V| where each position of the vector represents a word in the vocabulary.
    vector = [0] * len(vocabulary)

    for word in context:
        # If the word is in our vocabulary, increment the vector at that word's position.
        if word in vocab_frequencies['frequencies, index by word'].keys():
            index = vocab_frequencies['frequencies, index by word'][word]['index']
            vector[index] += 1
        # Otherwise, the word is not in our vocabulary and is not a part of the context vector.

    return vector


def get_context_indices(sentence, context_window_size):

    # If the context window size is 0, include the entire sentence.
    if context_window_size == 0:
        min_index = 0
        max_index = len(sentence['words'])
    # Otherwise, calculate the index range for the context window around the target word.
    else:
        min_index = sentence['target index'] - context_window_size
        if min_index < 0:
            min_index = 0
        max_index = sentence['target index'] + context_window_size
        if max_index > len(sentence['words']):
            max_index = len(sentence['words'])

    return min_index, max_index


def test(test_sentences, signature_vectors, vocabulary, vocab_frequencies, context_window_size):

    test_predictions = []

    # Evaluate each test sentence.
    for sentence in test_sentences:
        # Create a context vector for the sentence.
        context_vector = create_context_vector(sentence, vocabulary, vocab_frequencies, context_window_size)

        # Compute the cosign similarity between the context vector and each signature vector.
        predicted_sense = []
        predicted_sim = []
        for v in signature_vectors.keys():
            sim = cosign_similarity(context_vector, signature_vectors[v])
            predicted_sense.append(v)
            predicted_sim.append(sim)

        zipped = zip(predicted_sim, predicted_sense)
        zipped = list(zipped)
        ordered = sorted(zipped, key=lambda pair: (-pair[0], pair[1]))
        test_predictions.append(ordered)

    return test_predictions


def cosign_similarity(test_sentence_vector, signature_vector):

    numerator = .0
    x = .0
    y = .0

    for i in range(len(test_sentence_vector)):
        # Calculate numerator.
        numerator += test_sentence_vector[i] * signature_vector[i]

        # Calculate denominator.
        x += math.pow(test_sentence_vector[i], 2)
        y += math.pow(signature_vector[i], 2)

    denominator = math.sqrt(x) * math.sqrt(y)

    if denominator == 0:
        return 0

    sim = numerator / denominator

    return sim


if __name__ == '__main__':
    main()
