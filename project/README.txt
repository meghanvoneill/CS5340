This is my submission for the Question Answering Project in Dr. Riloff's
CS 5340, Natural Language Processing course at the University of Utah.

a)      At the moment I am using libraries that are associated with the Python
    base. I have not begun to successfully implement the methods requiring
    external libraries, but they are in progress.

        I did borrow a prefix-removal method that was fairly straight forward.
    Citation is in the comments, as well as here.
    Credit is given to @Elazar for his prefix removal method:
        https://stackoverflow.com/questions/16891340/remove-a-prefix-from-a-string

b)      I processed all the training files within a minute or two. Since my
    question-identification and answer extraction methods are fairly weak,
    it should not take long to run on any size data set.

c) Solo

d)      I built out the pipeline completely so that I could ensure the program could run.
    My plan is to implement entity recognition so that I can hope to extract the likely
    answer phrase from the text.

        Since I did not have time to complete my implementation, I chose some heuristics
    to decide an answer. First I ran some statistics on the training data set to find the
    most common answers in the set. Next, I was able to implement a rudimentary question-
    identification that would point me in the direction of which common answer to use.

        The implementation's current heuristics are not very strong. With further time,
    I have confidence the accuracy of the system could be dramatically improved.


