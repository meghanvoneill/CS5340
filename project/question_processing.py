#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.linear_model import SGDClassifier
#import tensorflow as tf
#import numpy
from project import input_processing


def main():

    # question_type_words = ['who', 'where', 'when', 'how', 'which', 'what']
    # all_labels = []
    # input_file = 'test_input.txt'
    # story_IDs = input_processing.read_story_IDs(input_file)
    # classifiers = []
    #
    # # Generate labeled data for each question type word.
    # for word in question_type_words:
    #     questions, labels = generate_labeled_question_data(word, story_IDs)
    #     print(labels)
    #     all_labels.append(labels)
    #
    #     # Vectorize questions.
    #     vectorizer = CountVectorizer()
    #     vectors = vectorizer.fit_transform(questions)
    #
    #     # Stochastic gradient descent optimizer.
    #     classifier = SGDClassifier(max_iter=1000, tol=1e-3)
    #     acc = classifier.fit(vectors, labels).score(vectors, labels)
    #     classifiers.append(classifier)
    #     print(acc)

    return


# Labels questions that do or do not contain the given target word for each question in each story.
def generate_labeled_question_data(word, story_IDs):

    questions = []
    labels = []

    for story_meta in story_IDs:
        for question in story_meta['questions']:
            questions.append(question['question'])
            q_array = question['question'].split()
            target_found = False
            for w in q_array:
                # Normalize the word.
                w = normalize_word(w, True)

                # If the target word is in our question, stop looking for it.
                if w == word:
                    target_found = True
                    break

            # If the target word was found in our question, label = 1.
            if target_found:
                labels.append(1)
            # Otherwise, label = 0.
            else:
                labels.append(0)

    return questions, labels


# Normalizes a word to given conditions.
def normalize_word(word, lower_case=True):

    new_word = word

    if lower_case:
        new_word = word.lower()

    return new_word


if __name__ == '__main__':
    main()
