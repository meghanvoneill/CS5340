from pathlib import Path


# Reads the given file to gather story ID file names. Returns a dictionary with the story IDs and there collected
# stories and questions.
#
#   story_IDs = [story_meta = {'story_ID': '', 'story': {}, 'questions': []}]
#       story = {'headline': '', 'date': '', 'text': ''}
#       questions = [question = {'question_ID': '', 'question': '', 'difficulty': ''}]
def read_story_IDs(file_name):

    story_IDs = []

    with open(file_name, 'r') as f:
        # Extract the path for the story files.
        path = Path(f.readline().strip())

        # Read in the story ID file names.
        for line in f.readlines():
            story_ID = line.strip()
            story_meta = {'story_ID': story_ID, 'story': {}, 'questions': []}
            story_IDs.append(story_meta)

    f.close()

    for story_meta in story_IDs:
        story_file = story_meta['story_ID'] + '.story'
        story_file_name = path / story_file
        questions_file = story_meta['story_ID'] + '.questions'
        questions_file_name = path / questions_file

        story = read_story(story_file_name)
        questions = read_questions(questions_file_name)

        story_meta['story'] = story
        story_meta['questions'] = questions

    return story_IDs


# Read the story for the given story file.
#
#   story = {'headline': '', 'date': '', 'text': ''}
def read_story(story_file_name):

    # Read the story for the given file name.
    with open(story_file_name, 'r') as s:
        # Read in the headline and date.
        headline = remove_prefix(s.readline().strip(), 'HEADLINE: ')
        date = remove_prefix(s.readline().strip(), 'DATE: ')
        text = ''

        # Skip past blank lines.
        for i in range(4):
            s.readline()

        # Read text lines while removing newline characters.
        for line in s.readlines():
            text += line.replace('\n', ' ')

        story = {'headline': headline, 'date': date, 'text': text.strip()}

    return story


# Read the questions for the given question file.
#
#   questions = [question = {'question_ID': '', 'question': '', 'difficulty': ''}]
def read_questions(questions_file_name):

    questions = []

    # Read the questions for the given file name.
    with open(questions_file_name, 'r') as q:
        lines = q.readlines()
        for index in range(0, len(lines), 4):
            if lines[index].startswith('QuestionID:'):
                question_ID = remove_prefix(lines[index].strip(), 'QuestionID: ')
                question_text = remove_prefix(lines[index + 1].strip(), 'Question: ')
                difficulty = remove_prefix(lines[index + 2].strip(), 'Difficulty: ')

                question = {'question_ID': question_ID, 'question': question_text, 'difficulty': difficulty}
                questions.append(question)

    return questions


def named_entity_tagging(story_IDs):

    return


def format_training_file(file_name):

    new_lines = ''

    with open(file_name, 'r') as f:
        for line in f.readlines():
            arr = line.split()
            file_name = arr[-1]
            name = file_name.split('.')
            new_lines += name[0] + '\n'

    print(new_lines)


def read_answers(file_name):

    file_names = []

    with open(file_name, 'r') as f:
        # Extract the path for the story files.
        path = f.readline().strip()

        # Read in the story ID file names.
        for line in f.readlines():
            story_ID = line.strip()
            file_names.append(path + story_ID + '.answers')

    f.close()

    answers = []

    for answers_file_name in file_names:
        # Read the questions for the given file name.
        with open(answers_file_name, 'r') as a:
            lines = a.readlines()
            for index in range(0, len(lines), 5):
                if lines[index].startswith('QuestionID:'):
                    question_ID = remove_prefix(lines[index].strip(), 'QuestionID: ')
                    question_text = remove_prefix(lines[index + 1].strip(), 'Question: ')
                    answers_for_question = remove_prefix(lines[index + 2].strip(), 'Answer: ').split('|')
                    difficulty = remove_prefix(lines[index + 3].strip(), 'Difficulty: ')

                    answer = {'question_ID': question_ID, 'question': question_text, 'answers': answers_for_question, 'difficulty': difficulty}
                    answers.append(answer)

    return answers


def write_answer_key(file_name):

    file_names = []

    with open(file_name, 'r') as f:
        # Extract the path for the story files.
        path = f.readline().strip()

        # Read in the story ID file names.
        for line in f.readlines():
            story_ID = line.strip()
            file_names.append(path + story_ID + '.answers')

    f.close()

    lines_to_write = []

    for answers_file_name in file_names:
        # Read the questions for the given file name.
        with open(answers_file_name, 'r') as a:
            for line in a.readlines():
                lines_to_write.append(line)
    a.close()

    with open('test_answer_key.txt', 'w') as t:
        for line in lines_to_write:
            t.write(line)

    t.close()

    return


def count_answers(answers):

    count_dictionary = {}

    for answer_obj in answers:
        for answer in answer_obj['answers']:
            answer = answer.strip()
            if answer in count_dictionary.keys():
                count_dictionary[answer] += 1
            else:
                count_dictionary[answer] = 1

    words, counts = zip(*count_dictionary.items())
    return words, counts


# C/O @Elazar for his prefix removal method.
#   https://stackoverflow.com/questions/16891340/remove-a-prefix-from-a-string
def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

