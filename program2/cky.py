import sys
from pprint import pprint


# Test run with: python3 cky.py data/pcfg-tiny.txt data/sentences-tiny.txt

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

        for line in lines:
            line = line.rstrip()
            new_line = line.split()
            lhs = new_line[0]
            if len(new_line) == 5:
                grammar[lhs]['non-terminal']['B'][new_line[2]] = {new_line[3]: float(new_line[4])}
                grammar[lhs]['non-terminal']['C'][new_line[3]] = {new_line[2]: float(new_line[4])}

            else:
                grammar[lhs]['terminal'][new_line[2]] = float(new_line[3])
                if new_line[2] not in words.keys():
                    words[new_line[2]] = set()
                words[new_line[2]].add(lhs)

    return grammar, words


def read_sentences(file_name):

    # Build dictionary data set from input file.
    sentences = []

    # Read in data formatted as: sentence \n
    with open(file_name, 'r') as f:
        for line in f.readlines():
            sentence = line.split()
            sentences.append(sentence)

    return sentences


def cky_parse(grammar, sentence, words_known):

    parses = {'sentence': sentence, 'number of parses': 0, 'table': {}}

    # Iterate over words (columns).
    for column in range(len(sentence)):
        # Add non-terminals for the current word.
        parses['table'][column, column] = words_known[sentence[column]]
        # Iterate over rows, from bottom to top.
        for row in range((column - 1), -1, -1):
            for partition in range(row + 1, column + 1):
                if (row, column) in parses['table'].keys():
                    parses['table'][row, column] = parses['table'][row, column].union(
                        explore_partitioning(grammar, parses, row, column, partition))
                else:
                    parses['table'][row, column] = explore_partitioning(grammar, parses, row, column, partition)

    return parses


def explore_partitioning(grammar, parses, row, column, partition):

    pprint(parses['table'])
    partitions = []
    Bs = set(parses['table'][row, partition - 1])
    Cs = set(parses['table'][partition, column])

    # B or C are empty, no grammar rules apply.
    if Bs == {} or Cs == {}:
        return partitions
    # Both B and C are nonempty. Explore grammar rules with B in Bs, C in Cs.
    else:
        for B in Bs:
            for C in Cs:
                for A in grammar.keys():
                    if B in grammar[A]['non-terminal']['B'].keys():
                        if C in grammar[A]['non-terminal']['B'][B].keys():
                            partition = [A, B, C]
                            parses['number of parses'] += 1
                            partitions.append(partition)

    return partitions


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
                # Print set from dictionary.
                item_set = ''
                if isinstance(parse['table'][cell], set):
                    for item in parse['table'][cell]:
                        item_set += item + ' '
                elif isinstance(parse['table'][cell], list):
                    for rule in parse['table'][cell]:
                        item_set += rule[0] + ' '
                c = str(x + 1) + ', ' + str(y + 1)
                print('cell[' + str(c) + ']: ' + item_set)

    return


if __name__ == '__main__':
    main()
