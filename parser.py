import json
import gzip
import os

from biothings import config

logger = config.logger

def load_annotations(data_folder):
    with open('/opt/home/outbreak/outbreak.api/plugins/nde/nde.jsonl') as data:
        for line in data:
            datum = json.loads(line)
            yield datum
