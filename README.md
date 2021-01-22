# Description

AnswerBot is an automated tool that generates answer summary to Developers' Technical Questions

This project is based on the research paper AnswerBot: automated generation of answer summary to developers technical questions

found at [https://dl.acm.org/doi/10.5555/3155562.3155650](https://dl.acm.org/doi/10.5555/3155562.3155650)

[Our project implementation details can be found here](https://pratikpatelx.github.io/AnswerBot/)

# Usage
Note: A Dataset of stackoverflow data dump is required to run this project sucessfully, You can request Swetul Patel, swetulpatel@gmail.com OR Pratik Patel, pratikpatel2369@gmail.com for the dataset. We will be happy to assist you. :)

Extract the Dataset folder to reveal the files needed to run AnswerBot successfully

1. Please set up the Dataset file called pythonsqlite.db under the folder /AnswerBot/"put the DB here"
   it is a sqlite3 database that has all our dataset required for the project
   The database is compressed using 7Z to be able to upload it to UM learn. Inside the dataset Zip folder, there is an installer
   for the 7Z program that can be used to uncompress the database.

2. Navigate to AnswerBot/RelevantQuestionRetrieval directory

   - add the file MainCorpus.txt

3. Then Navigate to AnswerBot/Word2VecModel directory

  - add the file stopWords.txt
   - run the file python build_model.py (NOTE: This can take a while, please be patient for the model to build and may take upto 5-6 GB of storage on disk)

4. Then Navigate to AnswerBot/IDFVocabulary directory

   - add the file IDF_Test.csv

5. Then finally to run the AnswerBot tool:
   Navigate to AnswerBot directory and

   - run the file python user_query.py
   
# Dependencies
- This program uses the basic built-in modules in Python 3.
- Python sqlite3
- gensim==3.4.0 found at [https://radimrehurek.com/gensim/install.html]
- scikit-learn==0.19.1 found at [http://scikit-learn.org/stable/install.html]
- nltk 3.5
