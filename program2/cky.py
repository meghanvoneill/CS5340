import sys
from pprint import pprint

# Author: Meghan V. O'Neill
# For Program 2: CKY Parser with PCFG
# Natural Language Processing, Fall 2020, Professor Riloff, University of Utah

# Test run with: python3 cky.py data/pcfg-tiny.txt data/sentences-tiny.txt
# Test run with: python3 cky.py data/pcfg-example.txt data/sentences-example.txt
def main():

    # Read in arguments.
    args = sys.argv[1:]
    pcfg_file = args[0]
    sentences_file = args[1]

    grammar, words_known = read_pcfg_file(pcfg_file)
    sentences = read_sentences(sentences_file)

    parses = []
    for sentence in sentences:
        parses_found = cky_parse(grammar, sentence, words_known)
        parses.append(parses_found)

    parse_output(parses)

    return


# Read in the grammar file.
def read_pcfg_file(file_name):

    # Build dictionary data set from input file.
    grammar = {}
    words = {}

    # Read in data formatted in Chomsky Normal Form as: A -> B C probability or A -> w probability
    with open(file_name, 'r') as f:
        lines = f.readlines()
        # Build a dictionary using the left half of each rule as the key.
        for line in lines:
            line.strip('\n')
            new_line = line.split()
            lhs = new_line[0]
            if lhs not in grammar.keys():
                grammar[lhs] = {'rules': [], 'terminal': {}, 'non-terminal': {'B': {}, 'C': {}}}
            grammar[lhs]['rules'].append(new_line[2:])

        # Fill in B and C for each A we have found in our grammar rules.
        for line in lines:
            line = line.rstrip()
            new_line = line.split()
            lhs = new_line[0]
            if len(new_line) == 5:
                # Record B with C and its probability.
                if new_line[2] in grammar[lhs]['non-terminal']['B'].keys():
                    grammar[lhs]['non-terminal']['B'][new_line[2]]['C'].append(new_line[3])
                    grammar[lhs]['non-terminal']['B'][new_line[2]]['probabilities'].append(float(new_line[4]))
                else:
                    grammar[lhs]['non-terminal']['B'][new_line[2]] = {'C': [new_line[3]], 'probabilities': [float(new_line[4])]}
                # Record C with B and its probability
                if new_line[3] in grammar[lhs]['non-terminal']['C'].keys():
                    grammar[lhs]['non-terminal']['C'][new_line[3]]['B'].append(new_line[2])
                    grammar[lhs]['non-terminal']['C'][new_line[3]]['probabilities'].append(float(new_line[4]))
                else:
                    grammar[lhs]['non-terminal']['C'][new_line[3]] = {'B': [new_line[2]], 'probabilities': [float(new_line[4])]}
            else:
                grammar[lhs]['terminal'][new_line[2]] = float(new_line[3])
                if new_line[2] not in words.keys():
                    words[new_line[2]] = []
                words[new_line[2]].append(lhs)

    return grammar, words


# Read in sentences file.
def read_sentences(file_name):

    # Build dictionary data set from input file.
    sentences = []

    # Read in data formatted as: sentence \n
    with open(file_name, 'r') as f:
        for line in f.readlines():
            sentence = line.split()
            sentences.append(sentence)

    return sentences


# Perform CKY algorithm parsing.
def cky_parse(grammar, sentence, words_known):

    parses = {'sentence': sentence, 'number of parses': 0, 'table': {}}

    # Iterate over words (columns).
    for column in range(len(sentence)):
        # Add non-terminals for the current word.
        parses['table'][(column, column)] = words_known[sentence[column]]
        # Iterate over rows, from bottom to top.
        for row in range((column - 1), -1, -1):
            for partition in range(row + 1, column + 1):
                if (row, column) in parses['table'].keys():
                    parses['table'][(row, column)] = union_cells(parses['table'][(row, column)], explore_partitioning(grammar, parses, row, column, partition))
                else:
                    parses['table'][(row, column)] = explore_partitioning(grammar, parses, row, column, partition)

    return parses


# Explore partitioning for the given indices of the matrix.
def explore_partitioning(grammar, parses, row, column, partition):

    partitions = []
    Bs = parses['table'][(row, partition - 1)]
    Cs = parses['table'][(partition, column)]

    # B or C are empty, no grammar rules apply.
    if Bs == [] or Cs == []:
        return partitions
    # Both B and C are nonempty. Explore grammar rules with B in Bs, C in Cs.
    else:
        for B in Bs:
            for C in Cs:
                for A in grammar.keys():
                    if len(grammar[A]['non-terminal']['B'].keys()) > 0 and B in grammar[A]['non-terminal']['B'].keys():
                        for c in grammar[A]['non-terminal']['B'][B]['C']:
                            if c == C:
                                partition = A
                                if A == 'S':
                                    parses['number of parses'] += 1
                                partitions.append(partition)

    return partitions


# Print out of report from CKY parsing.
def parse_output(parses):

    for parse in parses:
        s = ''
        for word in parse['sentence']:
            s += word + ' '
        print('PARSING SENTENCE: ' + str(s))
        print('NUMBER OF PARSES FOUND: ' + str(parse['number of parses']))
        print('TABLE:')
        # Print all cells from the table. If the cell is a set, add all entries. If the cell is an array, print the
        # A of all the rules (not as a set).
        for x in range(len(parse['sentence'])):
            for y in range(x, len(parse['sentence'])):
                cell = (x, y)
                item_set = ''
                if len(sorted(parse['table'][cell])) < 1:
                    c = str(x + 1) + ', ' + str(y + 1)
                    print('cell[' + str(c) + ']: ' + '-')
                else:
                    for rule in sorted(parse['table'][cell]):
                        item_set += rule + ' '
                    c = str(x + 1) + ', ' + str(y + 1)
                    print('cell[' + str(c) + ']: ' + item_set)

    return


def union_cells(cell_1, cell_2):

    union = []

    for word in cell_1:
        union.append(word)

    for word in cell_2:
        union.append(word)

    return union


if __name__ == '__main__':
    main()
