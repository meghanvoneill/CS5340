/usr/local/bin/python3 entities.py data/trainE.txt data/testE.txt WORD POS ABBR CAP
./liblinear-1.93/train -q -s 0 -e 0.0001 trainE.txt.vector classifier
./liblinear-1.93/predict testE.txt.vector classifier predictions.txt > accuracyE.txt
DIFF=$(diff accuracyE.txt data/accuracyE.5340.txt)
if [ "$DIFF" ] 
then
    echo "Your code didn't pass the sample test!"
else
    echo "Congratulations, your code passed the sample test!"
fi

rm *.readable
rm *.vector
rm classifier
rm predictions.txt
