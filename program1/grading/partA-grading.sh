/usr/local/bin/python3 sentiment.py data/trainS.txt data/testS.txt data/words.txt 100
./liblinear-1.93/train -q -s 0 -e 0.0001 trainS.txt.vector classifier
./liblinear-1.93/predict testS.txt.vector classifier predictions.txt > accuracyS.txt
DIFF=$(diff accuracyS.txt data/accuracyS.100.txt)
if [ "$DIFF" ] 
then
    echo "Your code didn't pass the sample test!"
else
    echo "Congratulations, your code passed the sample test!"
fi

rm classifier
rm predictions.txt
