This is my submission for the Question Answering Project in Dr. Riloff's
CS 5340, Natural Language Processing course at the University of Utah.

a)      At the moment I am using libraries that are associated with the Python
    base. I have made use of two libraries primarily: NLTK and SpaCy. I have
    hybridized answers from both to choose from (while removing duplicates).
    The commands listed in QA-script.txt worked on my home computer and worked
    individually within the IDE on the CADE machine I used. However, the script
    did not seem to run in the same environment that the IDE was configured for,
    so until I right-clicked on the imports that were not compiling, the code
    could not see those libraries were installed elsewhere. The script did not
    fail at any point though, so I am unsure what the issue is. Hopefully you do
    not experience any issues running the code, but please let me know if you do.

        I did borrow a prefix-removal method that was fairly straight forward.
    Citation is in the comments, as well as here.
    Credit is given to @Elazar for his prefix removal method:
        https://stackoverflow.com/questions/16891340/remove-a-prefix-from-a-string

b)      I processed all the training files within a few minutes. Since my
    question-identification and answer extraction methods are not complicated,
    it should not take long to run on any size data set.

c)      Solo

d)      I built out the pipeline completely so that I could ensure the program could run.
    I have successfully run an F-score between 8% - 10%, which is a huge improvement
    compared to my checkpoint progress when my F-score was between 1% - 2%. I played
    with a lot of hyper-parameters with the question-typifying, in order to only use the
    best candidate answers.

        The piece missing from my system at the moment is more complex text extraction for
    the longer-answer questions. 'Why' questions, or 'How' questions, are challenging to
    answer correctly, partly because there is a whole string of text to answer with, but
    also because choosing the wrong string will cost dearly in scoring, so we must not
    choose a large segment arbitrarily.

        To work around the complexity of correctly extracting a string from the text for
    these types of questions, I iterated through the default type for each question label
    I use. The differences were not significant, but one category of question-type yielded
    answers that out-performed the rest: 'When' questions.

        My initial implementation only used NLTK and was an improvement over my simple
    heuristics used previously. Then I started working with SpaCy to fill in the gaps of NLTK.
    There were lots of categories of words to add once I started working with SpaCy,
    but this proved to be a trap too. I added too much data, and the answers were less
    likely to be correct with so many non-answers added to the mix. By choosing which
    data-types fit each question type best, I improved the performance of the system to
    the stage it is at now.


