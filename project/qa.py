import sys
from project import input_processing, output_processing
from pprint import pprint


def main():

    # Read in arguments.
    # args = sys.argv[1:]
    # input_file = args[0]
    input_file = 'test_input.txt'

    # Gather story IDs, stories, and questions.
    story_IDs = input_processing.read_story_IDs(input_file)

    # Answer questions.
    # answers = [(1, 'Canada'), (2, 'Betty Jean Aucoin'), (3, ' '), (5, '502')]
    answers = answer_questions(story_IDs)

    # Write response file.
    output_processing.write_response_file(answers, 'test.response')

    return


# Returns array of answers to all questions for all given story IDs.
#
#   story_IDs = {story_ID: {'story': {}, 'questions': {}}}
#       story = {'headline': '', 'date': '', 'text': ''}
#       questions = {'question_ID': {'question': '', 'difficulty': ''}}
def answer_questions(story_IDs):

    answers = []

    # For every story, examine the questions associated.
    for story_ID in story_IDs.keys():
        for question_ID in story_IDs[story_ID]['questions'].keys():
            answer = answer_question(story_IDs[story_ID]['story'], story_IDs[story_ID]['questions'][question_ID])
            answers.append((question_ID, answer))

    return answers


# Returns an answer to a single question, given a story and the question.
def answer_question(story, question):

    answer = ''


    return answer


if __name__ == '__main__':
    main()
