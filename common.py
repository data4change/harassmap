from ruamel.yaml.error import UnsafeLoaderWarning
import warnings
warnings.simplefilter('ignore', UnsafeLoaderWarning)

import os
import langid
import dataset
from pprint import pprint

langid.set_languages(['en', 'ar'])
engine = dataset.connect('sqlite:///d4c.sqlite')
table = engine['harass']
table_category = engine['harass_category']
table_geo = engine['harass_geo']

google_api_key = os.environ.get('GOOGLE_API_KEY')
