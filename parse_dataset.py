import glob
import csv
import json
import pickle

def load_questions(path_to_parsed_questions):
    """
    Loads all question csv files (starting with 'week')
    args:
        path_to_parsed_questions: str path to dir containing questions in csv
    returns:
        all_questions: dict structured like
            {lecture_name: [
                {from: <int>, to: <int>, text: <str>}
                ...
            ]
            ...}
    """
    all_questions = {}
    for fname in glob.glob(path_to_parsed_questions + 'week*'):
        with open(fname, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='$', restkey='textmore')
            for row in reader:
                if row and row['lecture'] != 'MISSING':
                    if row['lecture'] not in all_questions:
                        all_questions[row['lecture']] = []
                    row_text = row['text']
                    if 'textmore' in row:
                        row_text = ','.join([row_text, *row['textmore']])
                    all_questions[row['lecture']].append({'from': int(row['from']), 'to': int(row['to']), 'text': row_text})

    return all_questions

def load_transcripts(path_to_parsed_transcripts):
    """
    Loads all transcripts from csv file
    args:
        path_to_parsed_transcripts: str path to dir containing transcript srt csvs
    returns:
        all_transcripts: dict structured like
            {lecture_name: [
                {from: <int>, to: <int>, text: <str>}
                ...
            ]
            ...}
    """
    all_transcripts = {}
    for fname in glob.glob(path_to_parsed_transcripts + '*'):
        if fname not in all_transcripts:
            #  need to split because fname has full path 
            # might need to change on non-window machines?
            try:
                fname_short = fname.split('\\')[1]
            except:
                fname_short = fname.split('/')[-1]
            all_transcripts[fname_short] = []
        with open(fname) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='_')
            for row in reader:
                # same split as above
                all_transcripts[fname_short].append({'from': int(float(row['from'])), 'to': int(float(row['to'])), 'text': row['text']})
    return all_transcripts

def contains(qfrom, qto, lfrom, lto):
    return (qfrom <= lfrom) and (qto >= lto)


if __name__ == "__main__":
    path_to_parsed_questions = 'data/parsed/questions/'
    path_to_parsed_mooc1 = 'data/parsed/transcripts/mooc1_textretrieval_srt/'
    path_to_parsed_mooc2 = 'data/parsed/transcripts/mooc2_textanalytics_srt/'

    questions = load_questions(path_to_parsed_questions)
    mooc1 = load_transcripts(path_to_parsed_mooc1)
    mooc2 = load_transcripts(path_to_parsed_mooc2)

    # remove lectures in questions that are not in the moocs
    for lec in list(questions.keys()):
        if lec in mooc1:
            total_time = max([x['to'] for x in mooc1[lec]])
        elif lec in mooc2:
            total_time = max([x['to'] for x in mooc2[lec]])
        else:
            print('does not appear in moocs: ' + lec)
            del questions[lec]
            continue
            
        # remove any question that doesn't fit into a lecture
        cleaned_questions = []
        for question in questions[lec]:
            if question['to'] <= total_time:
                cleaned_questions.append(question)
            else:
                print('timestamp does not match lecture :', question, lec)
                
        # update with cleaned questions
        questions[lec] = cleaned_questions
    print('Total number of questions: ', sum([len(questions[lec]) for lec in questions]))
    print('Total number of lectures: ', len(list(questions.keys())))

    # Extract corresponding lecture text
    #   Condition: include lecture text segment [a,b] in question window [A,B] iff A <= a, b <= B
    questions_wlec = {}
    for lec in questions:
        qs = questions[lec]
        new_qs = []
        for q in qs:
            new_q = {}
            qfrom, qto = q['from'], q['to']
            lec_text = ''
            mooc = mooc1 if lec in mooc1 else mooc2
            for line in mooc[lec]:
                if contains(qfrom, qto, line['from'], line['to']):
                    lec_text = ' '.join([lec_text, line['text']])
            for k,v in q.items():
                new_q[k] = v
            new_q['lecture_text'] = lec_text.strip().replace('  ', ' ')

            if lec_text:
                new_qs.append(new_q)
            else:
                # print('Empty lecture content!')
                pass
        questions_wlec[lec] = new_qs
    
    print('Lecture count + valid question count:')
    print(len(questions_wlec))
    print(sum([len(questions_wlec[lec]) for lec in questions_wlec]))
    with open('data/text_pairs.pkl', 'wb') as handle:
        pickle.dump(questions_wlec, handle)