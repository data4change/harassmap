import langid
from datetime import datetime
import dateparser
import unicodecsv
import normality
from collections import defaultdict
from nltk.util import ngrams
from nltk.stem.snowball import SnowballStemmer
from pprint import pprint
from common import table, table_category

langid.set_languages(['en', 'ar'])
PHRASES = defaultdict(int)
stemmer = SnowballStemmer("english")


def load_row(data):
    data['case_id'] = int(data.pop('id'))
    data['latitude'] = float(data['latitude'])
    data['longitude'] = float(data['longitude'])
    data['time_of_submission'] = dateparser.parse(data['time_of_submission'])
    data['date'] = dateparser.parse(data['date'])
    data['date_of_incident'] = dateparser.parse(data['date_of_incident'])

    for k, v in data.items():
        if isinstance(v, datetime):
            v = v.date().isoformat()

    desc = data['description']
    (lang, val) = langid.classify(desc)
    data['lang'] = lang

    if lang == 'en':
        tokens = normality.normalize(desc).split(' ')
        # tokens = [stemmer.stem(t) for t in tokens]
        # for i in [3, 4, 5, 6]:
        for i in [4, 5, 6]:
            for ngram in ngrams(tokens, i):
                ngram = ' '.join(ngram)
                PHRASES[ngram] += 1
        # print tokens

    return
    table.insert(data)
    categories = [c.strip() for c in data['category'].split(',')]
    for cat in categories:
        if cat.lower() in ['none', 'blank']:
            continue
        table_category.insert({
            'case_id': data['case_id'],
            'category': cat
        })


def load():
    # print engine
    header = None
    # table.delete()
    # table_category.delete()

    with open('harrassmap.csv', 'r') as fh:
        for row in unicodecsv.reader(fh):
            if header is None:
                header = row
            else:
                data = dict(zip(header, row))
                load_row(data)


def report_phrases():
    phrases = PHRASES.items()
    phrases = sorted(phrases, key=lambda (p, c): c, reverse=True)
    for phrase, count in phrases[:100]:
        if count > 1:
            print phrase, count

if __name__ == '__main__':
    load()
    report_phrases()

