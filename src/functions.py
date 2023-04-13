from re import match, sub, search
from requests import get
from bs4 import BeautifulSoup

from datetime import datetime, timedelta
from src.settings_results import no_of_weeks_limit

from src.settings_results import search_parameters

def get_soup(url):
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def compress_text(text):
    return sub('\n{1,}', '\n', text.get_text(separator='\n'))

def get_job_posting_details(internal_job_posting_url):
    job_posting_url_reg = r''
    base_pay_reg = r'(\$[\d,.]{1,} and \$[\d,.]{1,})'

    if bool(match(job_posting_url_reg, internal_job_posting_url)):
        public_job_posting_url = internal_job_posting_url.replace('', '')
        soup = get_soup(public_job_posting_url)

    tmp = {
        'job-summary': None,
        'key-qualifications': None,
        'description': None,
        'education-experience': None,
        'posting-supplement-footer-0': None,
        'base_pay_lower': None,
        'base_pay_upper': None,
        'base_pay_type': None
    }

    for key in list(tmp.keys())[0:5]:
        results = soup.find('div', {'id': f'jd-{key}'})
        if results is not None:
            tmp[key] = compress_text(results)
    
    if tmp['posting-supplement-footer-0'] is not None:
        results = search(base_pay_reg, tmp['posting-supplement-footer-0'])
        if results is not None:
            base_pay = search(base_pay_reg, tmp['posting-supplement-footer-0']).group()
            [base_pay_lower, base_pay_upper] = base_pay.split(' and ') 
            tmp['base_pay_lower'] = base_pay_lower
            tmp['base_pay_upper'] = base_pay_upper[:-1] if base_pay_upper.endswith(',') else base_pay_upper
            tmp['base_pay_type'] = 'hourly' if '.' in base_pay else 'salary'
        
    values = list(tmp.values())
    del values[4]
    return values

def get_target_locations():
    locations = search_parameters['location']
    return '+'.join(locations)

def get_date_n_weeks_ago():
    today = datetime.now()
    delta = timedelta(weeks=no_of_weeks_limit)
    two_weeks_ago = today - delta
    return two_weeks_ago

def generate_html_doc(jtrw):
    html_template = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ATS Report</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css">
    <style>
        body {
            color: #333333;
        }

        .top-word {
            background-color: lightgrey;
        }

        .n-match {
            border-bottom: 5px solid;
        }

        .job-reference {
            color: grey;
        }

        .department {
            color: black;
            border-radius: 25px;
            border: 1px solid lightgrey;
            background-color: darkgrey;
            padding: 6px 12px;
            margin-right: 12px;
        }

        .accordion-button:not(.collapsed) {
            background-color: lightgrey;
        }

        .accordion-button-container {
            display: flex;
            width: 100%;
            justify-content: space-between;
            align-items: center;
        }

        .reference-container {
            display:flex;
            justify-content: space-between;
            margin: 0 12px 48px 0;
            padding: 3px 6px;
            border: 1px solid lightgrey;
        }

        .jd-text {
            padding: 6px 24px;
        }

        .jd-text div {
            margin-bottom: 48px;
        }

        .job-title {
            font-weight: 700;
        }


    </style>
</head>

<body>

    <div class="accordion" id="accordionResults">
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
    <script>

        const results = $$jtwr$$

        const generateAccordionItem = (result, resultIndex) => {
            const {
                import_date,
                job_reference_no,
                job_title,
                department,
                location,
                summary,
                key_qualifications,
                description,
                education_experience,
                base_pay_lower,
                base_pay_upper,
                base_pay_type,
                job_posting_url,
                top_n_words,
                n_gram_matches
            } = result;

            const highlightWord = (word) => {
                for (let top_word of Object.keys(top_n_words)) {
                    if (word.includes(top_word)) {
                        return ([top_word, top_n_words[top_word].has_resume_match])
                    }
                }
                return false
            }

            const highlightNGram = (sentence) => {
                for(let n_gram of n_gram_matches) {
                    for (let match of n_gram['range_match']) {
                        if (sentence.includes(match)) {
                            const underlineColor = n_gram.has_resume_match ? 'lightgreen': 'lightgrey' 
                            return sentence.replace(match, `<span class="n-match" style="border-bottom-color:${underlineColor}">${match}</span>`)
                        }
                    }
                }
                return sentence
            }

            const highlightSentence = (sentence) => {
                const higlightedWordsArr = [];
                const wordArr = sentence.split(' ');
                for (let word of wordArr) {
                    if (highlightWord(word)) {
                        const [top_word, has_resume_match] = highlightWord(word);
                        const highlightColor = has_resume_match ? 'lightgreen': 'lightgrey';
                        higlightedWordsArr.push(word.replace(top_word, `<span class="top-word" style="background-color:${highlightColor};">${top_word}</span>`))
                    } else {
                        higlightedWordsArr.push(word)
                    }
                }
                const highlightedSentence = highlightNGram(higlightedWordsArr.join(' '));
                return highlightedSentence
            }

            const highlighter = (str) => {
                const strArr = str.split(/\\n/g);
                const highlightedStrArr = strArr.map(highlightSentence);
                return highlightedStrArr.map(str => `<p>${str}</p>`).join('')
            }

            return `<div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button collapse show" type="button" data-bs-toggle="collapse"
                        data-bs-target="#collapse${resultIndex}" aria-expanded="true" aria-controls="collapse${resultIndex}">
                        <div class="accordion-button-container">
                            <span class="job-title"><a href='${job_posting_url}' target="_blank"/>${job_title}</a></span><span class="department">${department}</span>
                        </div>
                    </button>
                </h2>
                <div id="collapse${resultIndex}" class="accordion-collapse collapse show" data-bs-parent="#accordionExample">
                    <div class="accordion-body">
                        <div class="accordion-content-container">
                            <div class="reference-container">
                                <span>Role Number: ${job_reference_no}</span>
                                <span>Date Posted: ${import_date}</span>
                            </div>
                            <div class="jd-text">
                                <h5>Summary</h5>
                                <div>${highlighter(summary)}</div>
                                <h5>Key Qualifications</h5>
                                <div>${highlighter(key_qualifications)}</div>
                                <h5>Description</h5>
                                <div>${highlighter(description)}</div>
                                <h5>Salary Band</h5>
                                <div>${base_pay_lower}-${base_pay_upper} (${base_pay_type})</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>`;
        }

        const generateResults = (results) => {
            const resultsAccordionInnerHTML = results.map(generateAccordionItem);
            const accordion = document.getElementById('accordionResults');
            accordion.innerHTML = resultsAccordionInnerHTML.join('');
        };

        generateResults(results)
    </script>
</body>

</html>"""

    with open('./assets/ats.html', 'w') as output_html_doc:

        def javascriptify(template):
            template = template.replace('$$jtwr$$', str(jtrw))
            reference = {
                ': False': ': false',
                ': True': ': true'
            }
            for item in reference.keys():
                template = sub(item, reference[item], template)
            
            return template
        
        html_template = javascriptify(html_template)
        output_html_doc.write(html_template)