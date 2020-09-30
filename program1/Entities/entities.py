import sys


def main():

    # Read in arguments.
    args = sys.argv[1:]
    train_file = args[0]
    test_file = args[1]
    feature_types = args[2:]

    # Training
    label_arr = ['O', 'B-PER', 'I-PER', 'B-LOC', 'I-LOC', 'B-ORG', 'I-ORG']
    labels = set(label_arr)
    training_set = read_data_file(train_file, labels)
    arguments = interpret_feature_types(feature_types)
    lexicon, pos = write_training_readable_file(train_file, training_set, arguments)

    # Testing
    testing_set = read_data_file(test_file, labels)
    write_testing_readable_file(test_file, testing_set, arguments, lexicon, pos)

    return


def read_data_file(file_name, labels):

    # Build dictionary data set from input file.
    data_set = {'instances': [], 'labels': [], 'POS': []}

    # [Read in CSV data formatted as: <label> \n <word1> \n <word2> \n ...]
    with open(file_name, 'r') as f:
        new_instance = []
        for line in f.readlines():
            new_line = line.strip()
            # Non-empty line:
            if len(new_line) > 0:
                new_line = new_line.split()
                data_set['labels'].append(new_line[0])
                data_set['POS'].append(new_line[1])
                data_set['instances'].append(new_line[2])
            else:
                data_set['labels'].append('SEN_BRK')
                data_set['POS'].append('SEN_BRK')
                data_set['instances'].append('SEN_BRK')

    return data_set


def write_file(file_name, labels, data_set):

    lines = ''

    with open(file_name, 'w') as f:
        # Loop through labels to build line for instance from data_set.
        for i in range(len(labels)):
            line_to_add = str(labels[i][0])
            line_to_add += ' '
            for key in data_set[i].keys():
                line_to_add += ' ' + str(key)
                line_to_add += ':' + str(data_set[i][key]) + ' '
            line_to_add += ' \n'
            lines += line_to_add

        f.write(lines)


def write_training_readable_file(file_name, data_set, arguments):

    lexicon = set()
    POS = set()

    with open(file_name + '.readable', 'w') as f:

        for i in range(len(data_set['instances'])):
            if data_set['instances'][i] == 'SEN_BRK':
                f.write('\n')
                continue

            lexicon.add(data_set['instances'][i])
            POS.add(data_set['POS'][i])

            if arguments[2] == 1:
                ABBR = check_abbr(data_set['instances'][i])
            else:
                ABBR = 'n/a'
            if arguments[3] == 1:
                CAP = check_cap(data_set['instances'][i])
            else:
                CAP = 'n/a'

            f.write('WORD: ' + str(data_set['instances'][i]) + '\n')
            f.write('POS: ' + str(data_set['POS'][i]) + '\n')
            f.write('ABBR: ' + str(ABBR) + '\n')
            f.write('CAP: ' + str(CAP) + '\n')
            f.write('WORDCON: n/a' + '\n')
            f.write('POSCON: n/a' + '\n')
            f.write('\n')

    return lexicon, POS


def write_testing_readable_file(file_name, data_set, arguments, lexicon, pos):

    with open(file_name + '.readable', 'w') as f:

        for i in range(len(data_set['instances'])):
            if data_set['instances'][i] == 'SEN_BRK':
                f.write('\n')
                continue

            if arguments[2] == 1:
                ABBR = check_abbr(data_set['instances'][i])
            else:
                ABBR = 'n/a'
            if arguments[3] == 1:
                CAP = check_cap(data_set['instances'][i])
            else:
                CAP = 'n/a'

            if data_set['instances'][i] not in lexicon:
                WORD = 'UNK'
            else:
                WORD = data_set['instances'][i]
            if data_set['POS'][i] not in pos:
                POS = 'UNKPOS'
            else:
                POS = data_set['POS'][i]

            f.write('WORD: ' + str(WORD) + '\n')
            f.write('POS: ' + str(POS) + '\n')
            f.write('ABBR: ' + str(ABBR) + '\n')
            f.write('CAP: ' + str(CAP) + '\n')
            f.write('WORDCON: n/a' + '\n')
            f.write('POSCON: n/a' + '\n')
            f.write('\n')


def make_feature_vectors(instances, features):

    feature_vectors = []

    for instance in instances:
        vector = [0] * (len(features.keys()) + 1)
        for word in instance:
            if word in features.keys():
                vector[features[word]] = 1
        feature_vectors.append(vector)

    return feature_vectors


def make_sparse_vectors(vectors):
    sparse_vectors = []

    for vector in vectors:
        sparse_vector = {}
        for i in range(len(vector)):
            if vector[i] == 1:
                sparse_vector[i] = 1
        sparse_vectors.append(sparse_vector)

    return sparse_vectors


# Check if a given word matches definition for abbreviation outlined below:
    # 1) Must end with a period
    # 2) Must consist entirely of alphabetic characters [a-z][A-Z] and one or
    #    more periods
    # 3) Must have a length <= 4
def check_abbr(word):

    arr = list(word)

    # 1) Must end with a period:
    end = len(word) - 1
    if word[end] != '.':
        return 'no'
    else:
        # 3) Must have a length <= 4:
        if len(word) > 4:
            return 'no'
        else:
            # 2) Must consist entirely of alphabetic characters [a-z][A-Z] and one or
            #       more periods.
            for char in word:
                if not char.isalpha():
                    if char == '.':
                        continue
                    else:
                        return 'no'

    return 'yes'


# Check if the first letter of a word is capitalized.
def check_cap(word):

    arr = list(word)

    if len(arr) > 0:
        if str(arr[0]).isupper():
            return 'yes'

    return 'no'


# Returns a binary array indicating which features should be used, given a list of features in any order.
# features = ['WORD', 'POS', 'ABBR', 'CAP', 'WORDCON', 'POSCON']
def interpret_feature_types(feature_types):

    features = [0] * 6

    for f in feature_types:
        if f == 'WORD':
            features[0] = 1
        elif f == 'POS':
            features[1] = 1
        elif f == 'ABBR':
            features[2] = 1
        elif f == 'CAP':
            features[3] = 1
        elif f == 'WORDCON':
            features[4] = 1
        elif f == 'POSCON':
            features[5] = 1

    return features


if __name__ == '__main__':
    main()
