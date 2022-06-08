import os
import glob
import re
import csv
from datetime import datetime
import re

def parse_transcripts():
    # transcript directories
    src_dire1 = './data/mooc_data/transcripts_srt/mooc1_textretrieval_srt/'
    src_dire2 = './data/mooc_data/transcripts_srt/mooc2_textanalytics_srt/'
    tgt_dire1 = './data/parsed/transcripts/mooc1_textretrieval_srt/'
    tgt_dire2 = './data/parsed/transcripts/mooc2_textanalytics_srt/'

    # process each transcript file in both directories
    for src_dire, tgt_dire in zip([src_dire1, src_dire2], [tgt_dire1, tgt_dire2]):
        for fname in sorted(glob.glob(src_dire+'*.srt')):

            # construct csv tuples
            basename = os.path.splitext(os.path.basename(fname))[0]
            with open(fname, 'r') as f:
                csv_data = []
                cur_row = [basename+'.srt', 0, 0.0, 0.0, ''] # 5 entries for each tuple
                state = 0 # 0 for nothing, 1 for id, 2 for time, 3 for text
                lines = [line.strip() for line in f.readlines()]
                for line in lines:
                    if line == '' and cur_row:
                        csv_data.append(cur_row)
                        cur_row = [basename+'.srt', 0, 0.0, 0.0, '']
                        state = 0
                    elif line.isnumeric():
                        state = 1
                    elif '-->' in line:
                        state = 2
                    else:
                        state = 3
                    
                    if state == 0:
                        continue
                    elif state == 1:
                        cur_row[1] = int(line)
                    elif state == 2:
                        line = line.replace(' ', '')
                        start, end = line.split('-->')
                        start_pt = datetime.strptime(start,'%H:%M:%S,%f')
                        start_time = start_pt.microsecond/1000000 + start_pt.second + start_pt.minute*60 + start_pt.hour*3600
                        end_pt = datetime.strptime(end,'%H:%M:%S,%f')
                        end_time = end_pt.microsecond/1000000 + end_pt.second + end_pt.minute*60 + end_pt.hour*3600
                        cur_row[2], cur_row[3] = start_time, end_time
                        print(start, end, start_pt.microsecond, end_pt.microsecond, start_time, end_time)
                    else:
                        cur_row[4] += line
                        cur_row[4] += ' '

            # save as csv file
            with open(os.path.join(tgt_dire, basename+'.csv'), 'w') as f:
                writer = csv.writer(f, quotechar='_')
                writer.writerow(['name', 'id', 'from', 'to', 'text']) # fieldnames
                writer.writerows(csv_data)



week1_question_lecture_map = {
    "1.1": "2 - 1 - 1.1 Natural Language Content Analysis (00-21-05).csv",
    "1.2": "2 - 2 - 1.2 Text Access (00-09-24).csv",
    "1.3": "2 - 3 - 1.3 Text Retrieval Problem (00-26-18).csv",
    "1.4": "2 - 4 - 1.4 Overview of Text Retrieval Methods (00-10-10).csv",
    "1.5": "2 - 5 - 1.5 Vector Space Model- Basic Idea (00-09-44).csv",
    "1.6": "2 - 6 - 1.6 Vector Space Model- Simplest Instantiation (00-17-30).csv"
}

week2_question_lecture_map = {
    "2.1": "2 - 7 - 1.7 Vector Space Model- Improved Instantiation (00-16-52).csv",
    "2.2": "2 - 8 - 1.8 TF Transformation (00-09-31).csv",
    "2.3": "2 - 9 - 1.9 Doc Length Normalization (00-18-56).csv",
    "2.4": "3 - 1 - 2.1 Implementation of TR Systems (00-21-27).csv",
    "2.5": "3 - 2 - 2.2 System Implementation- Inverted Index Construction (00-18-21).csv",
    "2.6": "3 - 3 - 2.3 System Implementation- Fast Search (00-17-11).csv"
}

week3_question_lecture_map = {
    "3.1": "3 - 4 - 2.4 Evaluation of TR Systems (00-10-10).csv",
    "3.2": "3 - 5 - 2.5 Evaluation of TR Systems- Basic Measures (00-12-54).csv",
    "3.3": "3 - 6 - 2.6 Evaluation of TR Systems- Evaluating Ranked Lists Part 1 (00-12-51).csv",
    "3.4": "3 - 7 - 2.6 Evaluation of TR Systems- Evaluating Ranked Lists Part 2 (00-10-01) .csv",
    "3.5": "3 - 8 - 2.7 Evaluation of TR Systems- Multi-Level Judgements (00-10-48).csv",
    "3.6": "3 - 9 - 2.8 Evaluation of TR Systems- Practical Issues (00-15-14).csv"
}

week4_question_lecture_map = {
    "4.1": "4 - 1 - 3.1 Probabilistic Retrieval Model- Basic Idea (00-12-44).csv",
    "4.2": "4 - 2 - 3.2 Statistical Language Models (00-17-53).csv",
    "4.3": "4 - 3 - 3.3 Query Likelihood Retrieval Function (00-12-07).csv",
    "4.4": "4 - 4 - 3.4 Smoothing of Language Model - Part 1 (00-12-15).csv",
    "4.5": "4 - 5 - 3.4 Smoothing of Language Model - Part 2 (00-09-36).csv",
    "4.6": "4 - 6 - 3.5 Smoothing Methods Part - 1 (00-09-54).csv",
    "4.7": "4 - 7 - 3.5 Smoothing Methods Part - 2 (00-13-17).csv"
}

week5_question_lecture_map = {
    "5.1": "4 - 8 - 3.6 Feedback in Text Retrieval (00-06-49).csv",
    "5.2": "4 - 9 - 3.7 Feedback in Vector Space Model- Rocchio (00-12-05).csv",
    "5.3": "4 - 10 - 3.8 Feedback in Text Retrieval- Feedback in LM (00-19-11).csv",
    "5.4": "5 - 1 - 4.1 Web Search- Introduction & Web Crawler (00-11-05).csv",
    "5.5": "5 - 2 - 4.2 Web Indexing (00-17-19).csv",
    "5.6": "5 - 3 - 4.3 Link Analysis - Part 1 (00-09-16).csv",
    "5.7": "5 - 4 - 4.3 Link Analysis - Part 2 (00-17-30).csv",
    "5.8": "5 - 5 - 4.3 Link Analysis - Part 3 (00-05-59).csv"
}

week6_question_lecture_map = {
    "6.1": "5 - 6 - 4.4 Learning to Rank Part 1 (00-13-09).csv",
    "6.2": "5 - 7 - 4.4 Learning to Rank - Part 2 (00-05-54).csv",
    "6.3": "5 - 8 - 4.4 Learning to Rank - Part 3 (00-04-58).csv",
    "6.4": "5 - 9 - 4.5 Future of Web Search (00-13-09).csv",
    "6.5": "5 - 10 - 4.6 Recommender Systems- Content-based Filtering - Part 1 (00-12-55).csv",
    "6.6": "5 - 11 - 4.6 Recommender Systems- Content-based Filtering - Part 2 (00-10-42).csv",
    "6.7": "5 - 12 - 4.7 Recommender Systems- Collaborative Filtering - Part 1 (00-06-20).csv",
    "6.8": "5 - 13 - 4.7 Recommender Systems- Collaborative Filtering - Part 2 (00-12-09).csv",
    "6.9": "5 - 14 - 4.7 Recommender Systems- Collaborative Filtering - Part 3 (00-04-45).csv"
}

week7_question_lecture_map = {
    "7.1": "2 - 1 - 1.1 Overview Text Mining and Analytics- Part 1 (00-11-43).csv",
    "7.2": "2 - 2 - 1.2 Overview Text Mining and Analytics- Part 2 (00-11-44).csv",
    "7.3": "2 - 3 - 1.3 Natural Language Content Analysis- Part 1 (00-12-48).csv",
    "7.4": "2 - 4 - 1.4 Natural Language Content Analysis- Part 2 (00-04-25).csv",
    "7.5": "2 - 5 - 1.5 Text Representation- Part 1 (00-10-46).csv",
    "7.6": "2 - 6 - 1.6 Text Representation- Part 2 (00-09-29).csv",
    "7.7": "2 - 7 - 1.7 Word Association Mining and Analysis (00-15-39).csv",
    "7.8": "2 - 8 - 1.8 Paradigmatic Relation Discovery Part 1 (00-14-31).csv",
    "7.9": "2 - 9 - 1.9 Paradigmatic Relation Discovery Part 2 (00-17-53).csv"
}

week8_question_lecture_map = {
    "8.1": "2 - 10 - 1.10 Syntagmatic Relation Discovery- Entropy (00-11-00).csv",
    "8.2": "2 - 11 - 1.11 Syntagmatic Relation Discovery- Conditional Entropy (00-11-57).csv",
    "8.3": "2 - 12 - 1.12 Syntagmatic Relation Discovery- Mutual Information- Part 1 (00-13-55).csv",
    "8.4": "2 - 13 - 1.13 Syntagmatic Relation Discovery- Mutual Information- Part 2 (00-09-42).csv",
    "8.5": "3 - 1 - 2.1 Topic Mining and Analysis- Motivation and Task Definition (00-07-36).csv",
    "8.6": "3 - 2 - 2.2 Topic Mining and Analysis- Term as Topic (00-11-31).csv",
    "8.7": "3 - 3 - 2.3 Topic Mining and Analysis- Probabilistic Topic Models (00-14-17).csv",
    "8.8": "3 - 4 - 2.4 Probabilistic Topic Models- Overview of Statistical Language Models- Part 1 (00-10-25).csv",
    "8.9": "3 - 5 - 2.5 Probabilistic Topic Models- Overview of Statistical Language Models- Part 2 (00-13-11).csv",
    "8.10": "3 - 6 - 2.6 Probabilistic Topic Models- Mining One Topic (00-12-21).csv"
}

week9_question_lecture_map = {
    "9.1": "3 - 7 - 2.7 Probabilistic Topic Models- Mixture of Unigram Language Models (00-12-39).csv",
    "9.2": "3 - 8 - 2.8 Probabilistic Topic Models- Mixture Model Estimation- Part 1 (00-10-16).csv",
    "9.3": "3 - 9 - 2.9 Probabilistic Topic Models- Mixture Model Estimation- Part 2 (00-08-15).csv",
    "9.4": "3 - 10 - 2.10 Probabilistic Topic Models- Expectation-Maximization Algorithm- Part 1 (00-11-05).csv",
    "9.5": "3 - 11 - 2.11 Probabilistic Topic Models- Expectation-Maximization Algorithm- Part 2 (00-10-39).csv",
    "9.6": "3 - 12 - 2.12 Probabilistic Topic Models- Expectation-Maximization Algorithm- Part 3 (00-06-25).csv",
    "9.7": "3 - 13 - 2.13 Probabilistic Latent Semantic Analysis (PLSA)- Part 1 (00-10-38).csv",
    "9.8": "3 - 14 - 2.14 Probabilistic Latent Semantic Analysis (PLSA)- Part 2 (00-10-15).csv",
    "9.9": "3 - 15 - 2.15 Latent Dirichlet Allocation (LDA)- Part 1 (00-10-20).csv",
    "9.10": "3 - 16 - 2.16 Latent Dirichlet Allocation (LDA)- Part 2 (00-12-03).csv"
}

week10_question_lecture_map = {
    "10.1": "4 - 1 - 3.1 Text Clustering- Motivation (00-15-52).csv",
    "10.2": "4 - 2 - 3.2 Text Clustering- Generative Probabilistic Models Part 1 (00-16-18).csv",
    "10.3": "4 - 3 - 3.3 Text Clustering- Generative Probabilistic Models Part 2 (00-08-37).csv",
    "10.4": "4 - 4 - 3.4 Text Clustering- Generative Probabilistic Models Part 3 (00-14-55).csv",
    "10.5": "4 - 5 - 3.5 Text Clustering- Similarity-based Approaches (00-17-48).csv",
    "10.6": "4 - 6 - 3.6 Text Clustering- Evaluation (00-10-11).csv",
    "10.7": "4 - 7 - 3.7 Text Categorization- Motivation (00-14-37).csv",
    "10.8": "4 - 8 - 3.8 Text Categorization- Methods (00-11-50).csv",
    "10.9": "4 - 9 - 3.9 Text Categorization- Generative Probabilistic Models (00-31-18).csv"
}

week11_question_lecture_map = {
    "11.1": "4 - 10 - 3.10 Text Categorization- Discriminative Classifier Part 1 (00-20-34).csv",
    "11.2": "4 - 11 - 3.11 Text Categorization- Discriminative Classifier Part 2 (00-31-46).csv",
    "11.3": "4 - 12 - 3.12 Text Categorization- Evaluation Part 1 (00-14-12).csv",
    "11.4": "4 - 13 - 3.13 Text Categorization- Evaluation Part 2 (00-10-51).csv",
    "11.5": "5 - 1 - 4.1 Opinion Mining and Sentiment Analysis- Motivation (00-17-51).csv",
    "11.6": "5 - 2 - 4.2 Opinion Mining and Sentiment Analysis- Sentiment Classification (00-11-47).csv",
    "11.7": "5 - 3 - 4.3 Opinion Mining and Sentiment Analysis- Ordinal Logistic Regression (00-13-43).csv"
}

week12_question_lecture_map = {
    "12.1": "5 - 4 - 4.4 Opinion Mining and Sentiment Analysis- Latent Aspect Rating Analysis Part 1 (00-15-17).csv",
    "12.2": "5 - 5 - 4.5 Opinion Mining and Sentiment Analysis- Latent Aspect Rating Analysis Part 2 (00-14-43).csv",
    "12.3": "5 - 6 - 4.6 Text-Based Prediction (00-12-08).csv",
    "12.4": "5 - 7 - 4.7 Contextual Text Mining- Motivation (00-06-47).csv",
    "12.5": "5 - 8 - 4.8 Contextual Text Mining- Contextual Probabilistic Latent Semantic Analysis (00-17-59).csv",
    "12.6": "5 - 9 - 4.9 Contextual Text Mining- Mining Topics with Social Network Context (00-14-43).csv",
    "12.7": "5 - 10 - 4.10 Contextual Text Mining- Mining Casual Topics with Time Series Supervision (00-19-37).csv",
    "12.8": "5 - 11 - 4.11 Course Summary (00-18-36).csv"
}


meta_ql_map = {
    '1': week1_question_lecture_map,
    '2': week2_question_lecture_map,
    '3': week3_question_lecture_map,
    '4': week4_question_lecture_map,
    '5': week5_question_lecture_map,
    '6': week6_question_lecture_map,
    '7': week7_question_lecture_map,
    '8': week8_question_lecture_map,
    '9': week9_question_lecture_map,
    '10': week10_question_lecture_map,
    '11': week11_question_lecture_map,
    '12': week12_question_lecture_map
}

def qtime_to_seconds(qtime):
    qtime = re.sub(' ', '', qtime) # remove all spaces
    qtime = re.sub('[^0-9]',' ', qtime).split() 
    if len(qtime) == 2:
        return 60 * int(qtime[0]) + int(qtime[1])
    else:
        return int(qtime[0])


assert qtime_to_seconds("3'30\"") == 210
assert qtime_to_seconds("30") == 30
        


        
def parse_questions():
    # question directories
    src_dire = './data/questions-cleaned/'
    tgt_dire = './data/parsed/questions/'
    messy_data = []

    # process each question file
    #for fname in sorted(glob.glob(src_dire+'week*.txt')):
    for i in range(1,13):
        fname = src_dire + 'week' + str(i) + "_allquestions.txt"
        # construct csv tuples
        basename = os.path.splitext(os.path.basename(fname))[0]

        ql_map = meta_ql_map[str(i)] # get the week number, and match it to the correct map

        with open(fname, 'r', errors='ignore') as f:
            csv_data = []
            lines = [line.strip() for line in f.readlines()]
            for i, line in enumerate(lines):
                if line == '':
                    continue
                else:
                    line_split = line.split(':')
                    if len(line_split) < 3: # must be at least 3 elements, otherwise the format is invalid
                        messy_data.append([basename+'.txt', i])
                        continue
                    elif len(line_split) >= 3:
                        filename = basename

                        question_lecture = line_split[0][2:] # remove question mark and 'L'
                        transcript_lecture = ql_map.get(question_lecture, 'MISSING')
                        raw_time = line_split[1]
                        raw_from, raw_to = raw_time.split('-')

                        text = ':'.join(line_split[2:]) # in case the question contains colons

                        sec_from = qtime_to_seconds(raw_from)
                        sec_to = qtime_to_seconds(raw_to)

                        csv_data.append([filename, question_lecture, transcript_lecture, raw_from, raw_to, sec_from, sec_to, text])


        # save as csv file
        with open(os.path.join(tgt_dire, basename+'.csv'), 'w') as f:
            writer = csv.writer(f, quotechar='$')
            writer.writerow(['filename', 'lecture in question', 'lecture', 'raw from', 'raw to', 'from', 'to', 'text']) # fieldnames
            writer.writerows(csv_data)

    # save messy data as well for future cleanup
    with open('./data/parsed/questions/messy_data.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'line']) # fieldnames
        writer.writerows(messy_data)

if __name__ == '__main__':
    parse_transcripts()
    parse_questions()