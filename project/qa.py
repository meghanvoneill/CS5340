import sys
from project import input_processing, output_processing, question_processing
from pprint import pprint


def main():

    # answers = input_processing.read_answers('test_input.txt')
    # words, counts = input_processing.count_answers(answers)
    # w_c = list(zip(words, counts))
    # sorted_w_c = sorted(w_c, key=lambda x: x[1], reverse=True)
    # print(sorted_w_c)
    # input_processing.write_answer_key('test_input.txt')

    # Read in arguments.
    args = sys.argv[1:]
    input_file = args[0]
    # input_file = 'test_input.txt'

    # Gather story IDs, stories, and questions.
    story_IDs = input_processing.read_story_IDs(input_file)

    # Answer questions.
    # answers = [(1, 'Canada'), (2, 'Betty Jean Aucoin'), (3, ' '), (5, '502')]
    answers = answer_questions(story_IDs)

    # Write response file.
    output_processing.write_response_file(answers, 'test_1.response')

    return


# Returns array of answers to all questions for all given story IDs.
#
#   story_IDs = [story_meta = {'story_ID': '', 'story': {}, 'questions': []}]
#       story = {'headline': '', 'date': '', 'text': ''}
#       questions = [question = {'question_ID': '', 'question': '', 'difficulty': ''}]
def answer_questions(story_IDs):

    answers = []

    # For every story, examine the questions associated.
    for story_meta in story_IDs:
        for question in story_meta['questions']:
            answer = answer_question(story_meta['story'], question['question'])
            answers.append((question['question_ID'], answer))

    return answers


# Returns an answer to a single question, given a story and the question.
def answer_question(story, question, k_possible_answers=1):

    answers = []

    # Classify the question type to determine the entity type we are looking for.
    entity_type = question_type(story, question)

    # TODO: Implement entity recognition and identify elements of story that match the entity type identified.

    # Temporary Implementation: Choose one of the most common labels.
    common_labels = ['Canada', '1997']
    answer_chosen = common_labels[0]
    story_word_arr = story['text'].split()

    # # If the most common label is found, choose that as the answer.
    # for word in story_word_arr:
    #     if word == common_labels[0]:
    #         return common_labels[0]
    #
    # # Otherwise, guess the next most common label.
    # answer_chosen = common_labels[1]

    # Choose most common label for place.
    if entity_type == 0:
        answer_chosen = common_labels[0]
    # Choose most common label for time.
    elif entity_type == 1:
        answer_chosen = common_labels[1]
    # Choose most common label or a number from the story.
    elif entity_type == 2:
        # number = get_most_frequent_number(story['text'])
        # if number is not None:
        #     answer_chosen = str(number)
        # else:
        #     answer_chosen = common_labels[0]
        answer_chosen = common_labels[0]

    return answer_chosen


def question_type(story, question):

    entity_type = 0

    words_in_question = question.split()

    word = words_in_question[0].lower()

    # who: person, organization, or country
    if word == 'who':
        entity_type = 0
    # where: location
    elif word == 'where':
        entity_type = 0
    # when: date or time period
    elif word == 'when':
        entity_type = 1
    # what: person, place, or thing
    elif word == 'what':
        if words_in_question[1].lower() == 'year':
            entity_type = 1
        else:
            entity_type = 0
    # how: [how much] = an amount, [how many] = a number
    elif word == 'how':
        entity_type = 2
    # which: [which city] = a place
    elif word == 'which':
        entity_type = 0

    return entity_type


def get_numbers(text):

    numbers = []
    words = text.split()

    for word in words:
        # Normalize the word to lowercase and remove extra spaces.
        word = word.lower()
        word = word.strip()

        # If the word is a number, add it to the numbers list.
        if word.isnumeric():
            print(word)
            numbers.append(word)

    return numbers


def get_most_frequent_number(text):

    count_of_numbers = {}
    words = text.split()

    for word in words:
        # Normalize the word to lowercase and remove extra spaces.
        word = word.lower()
        word = word.strip()

        # If the word is a number, add it to the numbers list.
        if word.isnumeric():
            # If we have already seen this number, increment its count.
            if word in count_of_numbers.keys():
                count_of_numbers[word] += 1
            # Otherwise, we haven't seen this number before and need to add it.
            else:
                count_of_numbers[word] = 1

    if len(count_of_numbers.keys()) == 0:
        return None

    numbers, counts = zip(*count_of_numbers.items())
    n_c = list(zip(numbers, counts))
    sorted_w_c = sorted(n_c, key=lambda x: x[1], reverse=True)

    return sorted_w_c[0]


if __name__ == '__main__':
    main()
