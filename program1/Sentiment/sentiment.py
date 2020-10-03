import sys
import csv
import json
from pprint import pprint


def main():

    # Read in arguments.
    args = sys.argv[1:]
    train_file = args[0]
    test_file = args[1]
    features_file = args[2]
    k = int(args[3])

    # Training
    features_by_name, features_by_index = read_features_file(features_file, k)
    training_set = read_data_file(train_file)
    training_feature_vectors = make_feature_vectors(training_set['instances'], features_by_name)
    training_sparse_vectors = make_sparse_vectors(training_feature_vectors)
    write_file(train_file + '.vector', training_set['instances'], training_sparse_vectors)

    # Testing
    testing_set = read_data_file(test_file)
    testing_feature_vectors = make_feature_vectors(testing_set['instances'], features_by_name)
    testing_sparse_vectors = make_sparse_vectors(testing_feature_vectors)
    write_file(test_file + '.vector', testing_set['instances'], testing_sparse_vectors)

    return


def read_features_file(file_name, k):

    # Build dictionary data set from input file.
    features_by_name = {}
    features_by_index = [0] * (k + 1)

    # [Read in CSV data formatted as: <label> \n <word1> \n <word2> \n ...]
    with open(file_name, 'r') as f:
        count = 1
        for line in f.readlines():
            if len(line) > 0 and count < k:
                new_row = line.rstrip()
                # If splitting on \n created one new word:
                if len(new_row) > 0:
                    word = str(new_row)
                    # If the feature has not been seen:
                    if word not in features_by_name.keys():
                        features_by_name[word] = count
                        features_by_index[count] = word
                        count += 1

    return features_by_name, features_by_index


def read_data_file(file_name):

    # Build dictionary data set from input file.
    data_set = {'instances': []}

    # [Read in CSV data formatted as: <label> \n <word1> \n <word2> \n ...]
    with open(file_name, 'r') as f:
        new_instance = []
        for line in f.readlines():
            word = line.strip()
            # Non-empty line:
            if len(word) > 0:
                word = word.rstrip('\n')
                # If an integer is found:
                if word.isdigit():
                    # If label found:
                    if int(word) == 1 or int(word) == 0:
                        data_set['instances'].append(new_instance)
                        new_instance = [int(word)]
                    # Not a label, add the word to the previous instance.
                    else:
                        new_instance.append(word)
                # Otherwise, add the word to the previous instance.
                else:
                    new_instance.append(word)

    data_set['instances'] = data_set['instances'][1:]
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


def make_feature_vectors(instances, features):

    feature_vectors = []

    for instance in instances:
        vector = [0] * (len(features.keys()) + 1)
        for word in instance[1:]:
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


if __name__ == '__main__':
    main()
