# ATS Lite

ATS Lite was created to automate the fetching of job positings, and to compare job description key words against one's resume.


## Features

- Data Collection
- Natural Language Parsing
- Key Word Comparison


## Installation

Enter folder

```zsh
  cd ~/Developer/folder
```

Create Virual Environment

```zsh
  python3 -m venv venv
```    

Activate Virual Environment
```zsh
  . ./venv/bin/activate
```

Install `requests` library
```zsh
  pip install requests
```

Install `beautifulsoup4` library
```zsh
  pip install beautifulsoup4
```

Install `nltk` library (optional, if you're interested in experimental keyword analysis)
```zsh
  pip install nltk
```


## Settings Results

Setting Search Location

* On the main search page, look at the address bar to confirm the location you have selected, the string comes after `location=`: https://jobs.sample.com/en-us/search?location=`somewhere`

```python
search_parameters = {
    'location': [
        'somewhere'
    ]
}
```

Setting Ignore List

* `Department` refers to `Teams` section when refining search. The only difference I have between internal and external searches is that internal search filters out sample Retail by default.

```python
    ignore = {
        "department": ['sample'],
        "location": ['nowhere']
    }
```

Setting CSV Output Path

* Refers to the name and path of CSV you would like results to write to.

```python
csv_output_path = './assets/sample.csv'
```

Seconds Between Fetching

* By default, the time between fetching data from the web is between 15 and 30 seconds to simulate human browsing.

```python
seconds_range_between_fetch = randint(15, 30)
```

## Settings ATS

Target Part of Speech
* See settings ATS to view examples of part of speech.

```python
target_part_of_speech = ["NN", "NNS", "NNP", "NNPS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "JJ", "JJR", "JJS"]
```

Stop Words
* Stop words are words or characters to remove from consideration during keyword analysis.

```python
user_defined_stop_words = ["'", ')', '#', ';', '—', '(', '’', '!', '/', '+', ',', 'a', '”', ':', '%', '–', '*', '&', '•', '?', '-', '“', '.']
```

Frequency Distribution Count

* Frequency Distribution Count is the top n keywords found in a job description.
```python
fdist_count = 20
```

N Gram Number

* N Gram number is a continguous sequence of n items from a job desription.
```python
ngram_number = 2
```

N Gram Min Count

* N Gram Min Count is the number of occurances minimum wanted for an N Gram to be deemed important.
```python
ngram_min_count = 2
```

Resume Path
* Path of resume txt containing words from resume to compare against job descriptions

```python
resume_txt_path = './assets/resume.txt'
```

## Usage/Examples
---
IMPORTANT: BEFORE RUNNING ANY OF THE FOLLOWING COMMANDS, BE SURE TO HAVE ALREADY `cd ~/Developer/ats_lite` INTO THE ATS_LITE FOLDER AND `. ./venv/bin/activate` TO ACTIVATE THE VIRTUAL ENVIRONMENT.

---
To collection job posts, run:
(This will take come time)
```zsh
python3 main.py
```
---
To run ATS analysis on collected jobs, run the follow:
(HTML doc can be found in ./assets/index.html)

```zsh
python3 create_ats_html.py
```

## Screenshot

ATS html doc will highlight the following:
- Highlight text (grey) - Keyword not found on resume.txt
- Highlight text (green) - Keyword found on resume.txt
- Underline text (grey) - N Gram not found on resume.txt
- Underline text (green) - N Gram structure found on resume.txt

<img src="./assets/images/ats.png" width="800px"/>