from common import table, table_category

import langid
from datetime import datetime
import dateparser
import unicodecsv
from pprint import pprint

langid.set_languages(['en', 'ar'])


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
    header = None
    table.delete()
    table_category.delete()

    with open('harrassmap.csv', 'r') as fh:
        for row in unicodecsv.reader(fh):
            if header is None:
                header = row
            else:
                data = dict(zip(header, row))
                load_row(data)


def report_phrases():
    with open('phrases.csv', 'w') as fh:
        writer = unicodecsv.writer(fh)
        writer.writerow(['phrase', 'ngram', 'count'])
        phrases = PHRASES.items()
        phrases = sorted(phrases, key=lambda (p, c): len(c), reverse=True)
        for (phrase, plen), cases in phrases[:3000]:
            if len(cases) > 1:
                cases_text = ','.join(cases)
                writer.writerow([phrase, str(plen), str(len(cases)), cases_text])
                print phrase, len(cases)

if __name__ == '__main__':
    load()
    report_phrases()

