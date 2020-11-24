from project import input_processing, output_processing, question_processing
from pprint import pprint
from nltk.tree import Tree
import nltk
import random
import sys
import spacy
from spacy import displacy
import en_core_web_sm
nlp = en_core_web_sm.load()


def main():

    random.seed(49)

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
    # output_processing.write_response_standard_output(answers)
    output_processing.write_response_file(answers, 'test_2.response')

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
        # TODO: Implement entity recognition and identify elements of the story.
        ner_results_tree, entities, chunked_entities = ner_on_doc(story_meta['story']['text'])
        numbers = get_numbers(story_meta['story']['text'])
        doc = nlp(story_meta['story']['text'])
        spacy_results = [(X.text, X.label_) for X in doc.ents]
        pprint([(X.text, X.label_) for X in doc.ents])
        print('\n')

        # TODO: Generate the story data once, and reuse it for each question.

        for question in story_meta['questions']:
            answer = answer_question(story_meta['story'], ner_results_tree, chunked_entities, spacy_results, numbers, question['question'])
            answers.append((question['question_ID'], answer))

    return answers


# Returns an answer to a single question, given a story and the question.
def answer_question(story, ner_tree, entities, spacy_results, numbers, question, k_possible_answers=1):

    answers = []

    # Classify the question type to determine the entity type we are looking for.
    entity_type = question_type(question)

    # TODO: Implement entity recognition and identify elements of question that match the entity type identified.
    answer_candidates = choose_answer_candidates(question, entity_type, ner_tree, entities, spacy_results, numbers)
    print(answer_candidates)

    # TODO: Rank answers.


    # TODO: Select answer.
    if len(answer_candidates) == 0:
        chosen_answer = choose_best_guess_common_label(entity_type)
    else:
        chosen_answer = random.choice(answer_candidates)

    return chosen_answer


def question_type(question):

    entity_type = 2

    words_in_question = question.split()

    word = words_in_question[0].lower()

    # who: person, organization, or country
    if word == 'who':
        entity_type = 0
    # where: location
    elif word == 'where':
        entity_type = 1
    # when: date or time period
    elif word == 'when':
        entity_type = 2
    # what: person, place, or thing
    elif word == 'what':
        if words_in_question[1].lower() == 'year' or words_in_question[1].lower() == 'month' or \
                words_in_question[1].lower() == 'day' or words_in_question[1].lower() == 'time':
            entity_type = 2
        else:
            entity_type = 3
    # how: [how much] = an amount, [how many] = a number
    elif word == 'how':
        entity_type = 4
    # which: [which city] = a place
    elif word == 'which':
        entity_type = 5
    # elif word == 'why':
    #     entity_type = 6

    return entity_type


# Entity types will be classified as follows:
#   [who, 0 = person, organization, or country:         'PERSON', 'ORGANIZATION']
#   [where, 1 = location:                               'GPE']
#   [when, what year, 2 = date, or time:                'GPE', number]
#   [what, 3 = person, place, or thing:                 'PERSON', 'ORGANIZATION', non-named object?]
#   [how, 4 = quantity, or amount:                      number]
#   [which, 5 = place:                                  'GPE']
#   [why, 6 = explanation:                              text]
#
def choose_answer_candidates(question, entity_type, ner_tree, entities, spacy_results, numbers):

    candidate_answers = []

    if entity_type == 0:
        candidate_answers.append([word for word, label in spacy_results if label == 'PERSON'])
        candidate_answers.append([word for word, label in spacy_results if label == 'ORG'])
        candidate_answers.append([word for word, label in spacy_results if label == 'NORP'])
        candidate_answers.append(entities['PERSON'])
        candidate_answers.append(entities['ORGANIZATION'])
    elif entity_type == 1:
        candidate_answers.append([word for word, label in spacy_results if label == 'LOC'])
        candidate_answers.append([word for word, label in spacy_results if label == 'GPE'])
        candidate_answers.append([word for word, label in spacy_results if label == 'FAC'])
        candidate_answers.append(entities['GPE'])
    elif entity_type == 2:
        candidate_answers.append([word for word, label in spacy_results if label == 'DATE'])
        candidate_answers.append([word for word, label in spacy_results if label == 'TIME'])
        # candidate_answers.append(entities['GPE'])
        # candidate_answers.append(numbers)
    elif entity_type == 3:
        candidate_answers.append([word for word, label in spacy_results if label == 'PERSON'])
        candidate_answers.append([word for word, label in spacy_results if label == 'ORG'])
        candidate_answers.append([word for word, label in spacy_results if label == 'WORK_OF_ART'])
        candidate_answers.append([word for word, label in spacy_results if label == 'LAW'])
        candidate_answers.append(entities['PERSON'])
        candidate_answers.append(entities['ORGANIZATION'])
    elif entity_type == 4:
        candidate_answers.append(['$' + word for word, label in spacy_results if label == 'MONEY'])
        candidate_answers.append([word for word, label in spacy_results if label == 'QUANTITY'])
        # candidate_answers.append(numbers)
    elif entity_type == 5:
        candidate_answers.append([word for word, label in spacy_results if label == 'LOC'])
        # candidate_answers.append(entities['GPE'])

    candidates = []
    for arr in candidate_answers:
        for word in arr:
            if word not in candidates:
                candidates.append(word)

    # Remove partial duplicates.
    cleaned_candidates = []

    # for word in candidates:
    #     duplicate = False
    #     split_word = word.split()
    #     for w in split_word:
    #         if w in cleaned_candidates:
    #             duplicate = True
    #     if not duplicate:
    #         cleaned_candidates.append(word)

    cleaned_candidates = condense_answer_options(candidates)

    return cleaned_candidates


def condense_answer_options(answers):

    length_sorted_answers = sorted(answers, key=len)
    new_answers = []

    # Grab the words by the shortest first.
    for short_answer in length_sorted_answers:
        # For each answer to compare this to, if we find any that contain this answer already, do not add
        # the short answer.
        add = True
        found_duplicate_component = False
        for answer in length_sorted_answers:
            # Skip if comparing to itself.
            if short_answer == answer:
                continue
            else:
                answer_split = answer.split()
                # If the short answer is contained by the answer, we have found a duplicate.
                if short_answer in answer_split:
                    found_duplicate_component = True
                    continue

        if found_duplicate_component:
            add = False
        if add:
            new_answers.append(short_answer)

    return new_answers


def choose_best_guess_common_label(entity_type):

    if entity_type == 2 or entity_type == 4:
        return '1997'
    else:
        return 'Canada'


def ner_on_doc(document):

    trees = []
    entities = []
    all_chunks = {'GPE': [], 'PERSON': [], 'ORGANIZATION': []}

    tagged_sentences = tag_PoS_doc(document)
    for sentence in tagged_sentences:
        # Create tree.
        bio_tagging, chunked_sentence_tree = chunking_on_sentence(sentence)
        trees.append(chunked_sentence_tree)
        pprint(chunked_sentence_tree)
        gpe_chunks = get_all_chunks(chunked_sentence_tree, 'GPE')
        person_chunks = get_all_chunks(chunked_sentence_tree, 'PERSON')
        org_chunks = get_all_chunks(chunked_sentence_tree, 'ORGANIZATION')

        for chunk in gpe_chunks:
            if len(chunk) > 0 and chunk not in all_chunks['GPE']:
                all_chunks['GPE'].append(chunk)
        for chunk in person_chunks:
            if len(chunk) > 0 and chunk not in all_chunks['PERSON']:
                all_chunks['PERSON'].append(chunk)
        for chunk in org_chunks:
            if len(chunk) > 0 and chunk not in all_chunks['ORGANIZATION']:
                all_chunks['ORGANIZATION'].append(chunk)

        # Classify expected entities based on BIO tagging.
        entities_of_sentence = []
        index = 0
        while index < len(bio_tagging):

            word_tuple = bio_tagging[index]
            bio_tag = word_tuple[2]

            # If this tag is not a 'O', or outside, add it to the sentence's possible entities.
            if bio_tag.startswith('O') == False:
                entities_of_sentence.append(word_tuple)

            index += 1
        # Add the entities for this sentence to the entities list.
        entities.append(entities_of_sentence)

    return trees, entities, all_chunks


def traverse_tree(t):

    try:
        t.label()
    except AttributeError:
        print(t, end=' ')
    # Otherwise, the tree node is defined.
    else:
        print('(', t.label(), end=' ')
        for child in t:
            traverse_tree(child)
        print(')', end=' ')

    return


def tag_PoS_doc(document):

    segmented_sentences = nltk.sent_tokenize(document)
    tokenized_sentences = [nltk.word_tokenize(segmented_s) for segmented_s in segmented_sentences]
    tagged_sentences = [nltk.pos_tag(tokenized_s) for tokenized_s in tokenized_sentences]

    return tagged_sentences


def tag_POS_sentence(sentence):

    tokenized_sentence = nltk.word_tokenize(sentence)
    tagged_sentence = nltk.pos_tag(tokenized_sentence)

    return tagged_sentence


# This processing order using NLTK is suggested by Susan Li, a Sr. Data Science based out of Toronto, Canada.
# Her article can be found here:
#   https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
def chunking_on_sentence(sentence):

    pattern = 'NP: {<DT>?<JJ>*<NN>}'
    parser = nltk.RegexpParser(pattern)
    parsed_sentence = parser.parse(sentence)

    bio_tagged_sentence = nltk.tree2conlltags(parsed_sentence)
    tree = nltk.ne_chunk(bio_tagged_sentence)

    return bio_tagged_sentence, tree


# From Named Entity Recognition with Regular Expression: NLTK.
#   https://stackoverflow.com/questions/48660547/how-can-i-extract-gpelocation-using-nltk-ne-chunk
def get_all_chunks(chunked_tree, label):

    prev = None
    all_chunks = []
    current = []

    for subtree in chunked_tree:
        if type(subtree) == Tree and subtree.label() == label:
            current.append(' '.join([token for token, pos, l in subtree.leaves()]))
        if current:
            named_entity = ' '.join(current)
            if named_entity not in all_chunks:
                all_chunks.append(named_entity)
                current = []
        else:
            continue

    return all_chunks


#######################################################################################################################
def get_numbers(text):

    numbers = []
    words = text.split()

    for word in words:
        # Normalize the word to lowercase and remove extra spaces.
        word = word.lower()
        word = word.strip()

        # If the word is a number, add it to the numbers list.
        if word.isnumeric():
            numbers.append(word)
        elif word.startswith('$'):
            numbers.append(word)
        elif word[0].isnumeric():
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


def generate_answer_key_and_word_counts():

    answers = input_processing.read_answers('test_input.txt')
    words, counts = input_processing.count_answers(answers)
    w_c = list(zip(words, counts))
    sorted_w_c = sorted(w_c, key=lambda x: x[1], reverse=True)
    # print(sorted_w_c)
    input_processing.write_answer_key('test_input.txt')


#######################################################################################################################
if __name__ == '__main__':
    main()
