import sys
from project import input_processing, output_processing


def main():

    # Read in arguments.
    # args = sys.argv[1:]
    # input_file = args[0]
    input_file = 'test_input.txt'

    story_IDs = input_processing.read_story_IDs(input_file)

    print(story_IDs)

    return


if __name__ == '__main__':
    main()
