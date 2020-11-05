from pathlib import Path


# Reads the given file to gather story ID file names. Returns a dictionary with the story IDs and there collected
# stories and questions.
#
#   story_IDs = {story_ID: {'story': {}, 'questions': {}}}
#       story = {'headline': '', 'date': '', 'text': ''}
#       questions = {'question_ID': {'question': '', 'difficulty': ''}}
def read_story_IDs(file_name):

    story_IDs = {}

    # [Read in CSV data formatted as: <label> \n <word1> \n <word2> \n ...]
    with open(file_name, 'r') as f:
        # Extract the path for the story files.
        path = Path(f.readline().strip())
        print('path: ' + str(path))

        # Read in the story ID file names.
        for line in f.readlines():
            story_ID = line.strip()
            print('story_ID: ' + str(story_ID))
            story_IDs[story_ID] = {'story': {}, 'questions': {}}

    f.close()

    for story_ID in story_IDs.keys():
        story_file = story_ID + '.story'
        story_file_name = path / story_file
        questions_file = story_ID + '.questions'
        questions_file_name = path / questions_file

        story = read_story(story_file_name)
        questions = read_questions(questions_file_name)

        story_IDs[story_ID]['story'] = story
        story_IDs[story_ID]['questions'] = questions

    return story_IDs


# Read the story for the given story file.
#
#   story = {'headline': '', 'date': '', 'text': ''}
def read_story(story_file_name):

    # Read the story for the given file name.
    with open(story_file_name, 'r') as s:
        headline = s.readline().strip()
        date = s.readline().strip()
        text = ''
        s.readline()
        s.readline()

        # TODO: Clean up text.
        for line in s.readlines():
            text += line

        story = {'headline': headline.split()[1:], 'date': date.split()[1:], 'text': text}

    return story


# Read the questions for the given question file.
#
#   questions = {'question_ID': {'question': '', 'difficulty': ''}}
def read_questions(questions_file_name):

    questions = {}

    # Read the questions for the given file name.
    with open(questions_file_name, 'r') as q:
        lines = q.readlines()
        for index in range(0, len(lines), 4):
            if lines[index].startswith('QuestionID:'):
                question_ID = lines[index].strip()
                question_text = lines[index + 1].strip()
                difficulty = lines[index + 2]

                questions[question_ID] = {'question': question_text, 'difficulty': difficulty}

    return questions


# C/O @Elazar for his prefix removal method.
#   https://stackoverflow.com/questions/16891340/remove-a-prefix-from-a-string
def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

