
# Write the QuestionID and Answer for each answer to the given output file name.
#
#   e.g. answers = [(1, 'Canada'), (2, 'Betty Jean Aucoin'), (3, ' '), (5, '502')]
def write_response_file(answers, output_file_name):

    with open(output_file_name, 'w') as a:

        for (QID, answer) in answers:
            a.write('QuestionID: ' + str(QID) + '\n')
            a.write('Answer: ' + str(answer) + '\n')
            a.write('\n')

    return


# Write the QuestionID and Answer for each answer to standard output.
#
#   e.g. answers = [(1, 'Canada'), (2, 'Betty Jean Aucoin'), (3, ' '), (5, '502')]
def write_response_standard_output(answers):

    for (QID, answer) in answers:
        print('QuestionID: ' + str(QID) + '\n')
        print('Answer: ' + str(answer) + '\n')
        print('\n')

    return

