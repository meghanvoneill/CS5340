from pprint import pprint
import sys
import operator
import string

# Author: Meghan V. O'Neill
# For Program 3: Part 1 - Lesk Algorithm
# Natural Language Processing, Fall 2020, Professor Riloff, University of Utah


# Tested with: python3 lesk.py test.txt definitions.txt stopwords.txt
def main():

    # Read in arguments.
    args = sys.argv[1:]
    test_sentences_file = args[0]
    sense_definitions_file = args[1]
    stopwords_file = args[2]
    output_file_name = test_sentences_file + '.lesk'

    # Read in data from given files.
    test_sentences = read_test_sentences_file(test_sentences_file)
    stopwords = read_stopwords_file(stopwords_file)
    sense_definitions = read_sense_definitions_file(sense_definitions_file)

    # Create filtered sentences from the stopwords file.
    filtered_test_sentences = filter_stopwords(test_sentences, stopwords)

    # Run the Lesk algorithm on the filtered test sentences and write the output to the output file.
    lesk_output = run_lesk(filtered_test_sentences, sense_definitions, stopwords)
    write_lesk_ordered(output_file_name, lesk_output)

    return


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


# Read in sense definitions file.
def read_sense_definitions_file(file_name):

    sense_definitions = {}

    with open(file_name, 'r') as f:
        for line in f.readlines():
            line = line.split('\t')

            # Read in sense, the sense definition, and the example sentence.
            sense = line[0]
            original_definition = line[1].split('\n')
            original_example = line[2].split('\n')

            # If there are '\n' characters in the definition, remove them and concatenate.
            if len(original_definition) > 1:
                definition = ''
                for piece in original_definition:
                    definition += piece
            else:
                definition = original_definition[0]

            # If there are '\n' characters in the example, remove them and concatenate.
            if len(original_example) > 1:
                example = ''
                for piece in original_example:
                    example += piece
            else:
                example = original_example[0]

            # Add the definition and example to the sense in the sense definitions dictionary.
            sense_definitions[sense] = {'definition': definition, 'example': example}

    return sense_definitions


# Write the output file for the lesk ordered output.
def write_lesk_ordered(file_name, lesk_ordered_outputs):

    with open(file_name, 'w') as f:
        for lesk_ordered in lesk_ordered_outputs:
            line = ''
            for pair in lesk_ordered:
                sense = operator.getitem(pair, 1)
                overlap = operator.getitem(pair, 0)
                line += str(sense) + '(' + str(overlap) + ') '
            line = line.strip()
            line += '\n'
            f.write(line)

    return


# Returns the given sentences array with a new filtered sentence array of words for each sentence.
def filter_stopwords(sentences, stopwords, remove_punctuation=True):

    punctuation = set(string.punctuation)

    # Loop through each sentence.
    for sentence in sentences:
        # Create a filtered words array for each sentence.
        sentence['filtered_words'] = []
        for word in sentence['words']:
            # If this is not a stopword, add it to our filtered words array.
            if word not in stopwords:
                # If punctuation is being removed, check if the word is a punctuation character.
                if remove_punctuation:
                    if word not in punctuation:
                        sentence['filtered_words'].append(word)
                # Otherwise, we are not worried about checking punctuation and can add the word to our filtered
                #   words array.
                else:
                    sentence['filtered_words'].append(word)

    return sentences


def run_lesk(sentences, sense_definitions, stopwords):

    lesk_output = []

    for sentence in sentences:
        lesk_result = ordered_lesk(sentence['target'], sentence, sentences, sense_definitions, stopwords)
        lesk_output.append(lesk_result)

    return lesk_output


# Takes a word and a sentence and returns the senses of the word in descending order by most likely sense.
def ordered_lesk(word, sentence, sentences, senses, stopwords):

    signatures = []
    overlap_of_senses = []
    context = sentence

    for sense in senses.keys():
        signature = get_signature(sense, senses, stopwords, word)
        overlap = compute_overlap(signature, context)

        signatures.append(sense)
        overlap_of_senses.append(overlap)

    zipped = zip(overlap_of_senses, signatures)
    zipped = list(zipped)
    ordered = sorted(zipped, key=lambda pair: (-pair[0], pair[1]))

    return ordered


# Returns a dictionary with the set of words in the gloss and examples of the word in that sense.
def get_signature(sense, senses, stopwords, target):

    signature = {'gloss': set(senses[sense]['definition'].split()), 'examples': set(senses[sense]['example'].split()),
                 'signature': set()}

    # Add the normalized (lowercase) words from both the gloss and the examples to the signature.
    for word in signature['gloss']:
        word = word.lower()
        if word not in stopwords and word is not target:
            signature['signature'].add(word)
    for word in signature['examples']:
        word = word.lower()
        if word not in stopwords and word is not target:
            signature['signature'].add(word)

    return signature


# Returns the number of distinct words in common between two sets, case insensitively.
#   signature = {'gloss': set(), 'examples': set(), 'signature': set(gloss + examples}
#   sentence = {'target': '', 'words': [], 'filtered_words': []}
def compute_overlap(signature, context):

    overlap = 0
    found_words = set()

    # For each word in the sentence context's filtered words, check if it matches the signature.
    for word in context['filtered_words']:
        # Normalize the word to lowercase.
        word = word.lower()
        if word in signature['signature'] and word not in found_words:
            overlap += 1
            found_words.add(word)

    return overlap


if __name__ == '__main__':
    main()
