import sys


def main():

    # Read in arguments.
    # args = sys.argv[1:]
    # train_file = args[0]
    # test_file = args[1]
    # feature_types = args[2:]

    print(check_abbr('C.A.'))

    return


def check_abbr(word):

    arr = list(word)
    print(arr)
    # 1) Must end with a period:
    end = len(word) - 1
    if word[end] is not '.':
        return False
    else:
        # 3) Must have a length <= 4:
        if len(word) > 4:
            return False
        else:
            # 2) Must consist entirely of alphabetic characters [a-z][A-Z] and one or
            #       more periods.
            for char in word:
                if not char.isalpha():
                    if char is '.':
                        continue
                    else:
                        return False

    return True


if __name__ == '__main__':
    main()
