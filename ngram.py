from common import table, table_category

import json
import requests
import unicodecsv
import normality
from collections import defaultdict
from nltk.util import ngrams
from pprint import pprint
from networkx import Graph
from networkx.readwrite import json_graph

CSV = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT1E7UeZieR7j3H_NyT7njT87KMWquL6IhZjIieGNTm02hI77ruZvts8wkWnz3ffNrpse3l_E54Y5i4/pub?gid=0&single=true&output=csv'


def parse_row(phrases, data):
    lang = data['lang']
    if lang != 'en':
        return

    desc = data['description']
    tokens = normality.normalize(desc).split(' ')
    for i in [2, 3, 4, 5, 6, 7]:
        for ngram in ngrams(tokens, i):
            ngram = ' '.join(ngram)
            phrases[(ngram, i)].add(str(data['case_id']))
    # print tokens


def parse():
    print 'parsing ngrams...'
    phrases = defaultdict(set)
    for row in table:
        parse_row(phrases, row)
    # report_phrases(phrases)

    print 'loading mapping...'
    res = requests.get(CSV)
    mapping = {}
    for row in unicodecsv.DictReader(res.iter_lines()):
        phrase = row.pop('phrase')
        mapping[phrase] = row

    print 'generating graph nodes....'
    G = Graph()
    for phrase, mapped in mapping.items():
        map_to = mapped.get('map_to') or None
        group = mapped.get('group') or None
        if not map_to and not group:
            continue
        name = map_to or phrase
        if not G.has_node(name):
            G.add_node(name, label=name, cases=[], type='phrase')
        if group:
            G.node[name]['theme'] = group

        for (p, i), cases in phrases.items():
            if p == phrase:
                for case in cases:
                    if case not in G.node[name]['cases']:
                        G.node[name]['cases'].append(case)

    G.add_node('setting', type='theme')
    G.add_node('incident', type='theme')
    G.add_node('reaction', type='theme')

    print 'generating graph edges....'
    for outer in G.nodes():
        if G.node[outer]['type'] != 'phrase':
            continue
        otheme = G.node[outer].get('theme')
        if otheme is None:
            continue
        ocases = set(G.node[outer].get('cases', []))
        G.add_edge(outer, otheme, type='theme')

        for inner in G.nodes():
            if inner >= outer or G.node[inner]['type'] != 'phrase':
                continue
            icases = set(G.node[inner].get('cases', []))
            ixcases = len(ocases.intersection(icases))
            if ixcases:
                G.add_edge(outer, inner, type='common', weight=ixcases)

    data = json_graph.node_link_data(G)
    with open('web/graph.json', 'w') as fh:
        json.dump(data, fh, indent=2)

    # print 'json data....'
    # nodes = {}
    # for phrase, mapped in mapping.items():
    #     map_to = mapped.get('map_to') or None
    #     group = mapped.get('group') or None
    #     if not map_to and not group:
    #         continue
    #     name = map_to or phrase
    #     if name not in nodes:
    #         nodes[name] = {'name': name, 'cases': []}
    #     if group:
    #         nodes[name]['group'] = group

    #     for (p, i), cases in phrases.items():
    #         if p == phrase:
    #             for case in cases:
    #                 if case not in nodes[name]['cases']:
    #                     nodes[name]['cases'].append(case)

    # with open('web/data.json', 'w') as fh:
    #     json.dump({'nodes': nodes}, fh, indent=2)


def report_phrases(phrases):
    with open('phrases.csv', 'w') as fh:
        writer = unicodecsv.writer(fh)
        writer.writerow(['phrase', 'ngram', 'count', 'cases'])
        phrases = phrases.items()
        phrases = sorted(phrases, key=lambda (p, c): len(c), reverse=True)
        for (phrase, plen), cases in phrases[:3000]:
            if len(cases) > 1:
                cases_text = ','.join(cases)
                writer.writerow([phrase, str(plen), str(len(cases)),
                                 cases_text])


if __name__ == '__main__':
    parse()
