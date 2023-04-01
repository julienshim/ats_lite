# nltk
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.util import ngrams

## built-in libraries
from csv import reader
from re import IGNORECASE, findall
from json import dump

## settings
from src.settings_ats import target_part_of_speech, fdist_count, ngram_number, ngram_min_count, user_defined_stop_words, resume_txt_path
from src.settings_results import csv_output_path
from src.functions import generate_html_doc

def findNgrams(text, n):
    ngs = []
    text = sent_tokenize(text)
    for line in text:
        token = nltk.word_tokenize(line)
        ng = list(ngrams(token, n))
        ngs.extend(ng)
    return ngs

def filter_ngrams(tup):
    for el in tup[0]:
        if el in stop_words:
            return False
    if tup[1] < ngram_min_count:
        return False
    return True

def reduce_n_gram_range_matches(n_gram_range_matches, substring):
    results = []
    for match in n_gram_range_matches:
        r_index = match.lower().rindex(substring)
        if r_index == 0:
            results.append(match)
        else:
            results.append(match[r_index:])
    return list(set(results))


json_to_write = {
    'results': []
}

with open(resume_txt_path) as txt_path:
    resume = txt_path.read().strip()

with open(csv_output_path) as csv_output:
    data = [r for r in reader(csv_output)]
    data_header = data[0]
    data_body = data[1:]
    for item_index, item in enumerate(data_body):
        print(f'Analyzing job description {item_index + 1} of {len(data_body)}')
        [import_date, job_reference_no, job_title, department, location, summary, key_qualifications, description, education_experience, base_pay_lower, base_pay_upper, base_pay_type, job_posting_url] = item

        # tokenize job_description
        job_description = '\n'.join([summary, key_qualifications, description])
        job_description_tokenized = word_tokenize(job_description)
        
        # define and filter stop words from job description
        stop_words = set(stopwords.words('english'))
        stop_words.update(user_defined_stop_words)

        filtered_tokens = []

        for word in job_description_tokenized:
            if word.lower() not in stop_words:
                filtered_tokens.append(word)

        # tag parts of speech and filter out unwanted pos
        tagged_tokens = nltk.pos_tag(filtered_tokens)

        filtered_pos = []

        for tuple in tagged_tokens:
            if tuple[1] in target_part_of_speech: # token, pos
                filtered_pos.append(tuple)

        # frequency distribution
        fdist_pos = FreqDist((list(map(lambda x: x[0], filtered_pos))))
        top_n_words = fdist_pos.most_common(fdist_count)
        top_n_words = { k: {'count': v, 'has_resume_match': k in resume }for (k,v) in top_n_words }
        job_description_filtered = [x.lower() for x in job_description.split(' ') if x.lower() not in stop_words]
        job_description_ngrams = findNgrams(' '.join(job_description_filtered), n=ngram_number)

        ngrams_freq = {}

        for ngram_tuple in job_description_ngrams:
            if ngram_tuple not in ngrams_freq:
                ngrams_freq[ngram_tuple] = 1
            else:
                ngrams_freq[ngram_tuple] += 1

        ngrams_freq_filtered = list(filter(filter_ngrams, ngrams_freq.items()))
        ngrams_freq_sorted = sorted(ngrams_freq_filtered, key=lambda x: x[1], reverse=True)
        n_gram_matches = []

        for item in ngrams_freq_sorted:
            n_gram_range = '_'.join(item[0])
            n_gram_range_count = item[1]
            n_gram_range_match = reduce_n_gram_range_matches(list(set(findall(rf"{item[0][0]}.*?{item[0][1]}", job_description, IGNORECASE))), str(item[0][0]))
            n_gram_resume_match = bool(reduce_n_gram_range_matches(list(set(findall(rf"{item[0][0]}.*?{item[0][1]}", resume, IGNORECASE))), str(item[0][0])))
            n_gram_dict = {
                'range': n_gram_range,
                'range_count': ngram_min_count,
                'range_match': n_gram_range_match,
                'has_resume_match': n_gram_resume_match
            }
            n_gram_matches.append(n_gram_dict)

        tmp = {
            'import_date': import_date,
            'job_reference_no': job_reference_no,
            'job_title': job_title,
            'department': department,
            'location': location, 
            'summary': summary.replace('\n', '\\n'), 
            'key_qualifications': key_qualifications.replace('\n', '\\n'), 
            'description': description.replace('\n', '\\n'), 
            'education_experience': education_experience, 
            'base_pay_lower': base_pay_lower, 
            'base_pay_upper': base_pay_upper, 
            'base_pay_type': base_pay_type, 
            'job_posting_url': job_posting_url,
            'top_n_words': top_n_words,
            'n_gram_matches': n_gram_matches
        }

        json_to_write['results'].append(tmp)

    print('Done!')


generate_html_doc(json_to_write['results'])