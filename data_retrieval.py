import json

from outbreak_parser_tools.addendum import Addendum


from outbreak_parser_tools import safe_request as requests
from outbreak_parser_tools.logger import get_logger
logger = get_logger('nde')

def get_annotations():
   urls = [  
           # biotools, dockstore and zenodo
           'http://api-staging.data.niaid.nih.gov/v1/query?&q=topicCategory.name:%22COVID-19%22',
           # immport
           'http://api-staging.data.niaid.nih.gov/v1/query?&q=healthCondition.name:%22covid-19%22%20AND%20includedInDataCatalog.name:%20ImmPort'
   ]
   for url in urls:
       logger.debug(url)
       url = f'{url}&fetch_all'
       response = requests.get(url).json()
       max_length = response['total']
       hits = response['hits']
       logger.debug(f'first request {len(hits)} out of {max_length}')

       while len(hits) < max_length:
           logger.debug('extending')
           res = requests.get(f'{url}&scroll_id={response["_scroll_id"]}').json()
           hits.extend(res['hits'])

       yield from hits

def load_annotations():
    pubs = [i for i in get_annotations()]
    Addendum.biorxiv_corrector().update(pubs)
    Addendum.topic_adder().update(pubs)
    Addendum.altmetric_adder().update(pubs)
    return pubs

if __name__ == '__main__':
    with open('nde.jsonl', 'w') as json_output:
        for doc in load_annotations():
            json.dump(doc, json_output)
            json_output.write('\n')
