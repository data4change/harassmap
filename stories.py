from common import table, table_category

import json
from pprint import pprint


def generate():
    print 'loading stories...'
    stories = []
    for row in table:
        data = {
            'case': row.get('case_id'),
            'description': row.get('description')
        }
        categories = table_category.find(case_id=data['case'])
        data['categories'] = [c.get('category') for c in categories]

        stories.append(data)

    data = {'stories': stories}
    with open('web/stories.json', 'w') as fh:
        json.dump(data, fh, indent=2)

if __name__ == '__main__':
    generate()
