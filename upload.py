import os
import biothings.hub.dataload.uploader

import requests
import biothings
import config
import requests
biothings.config_for_app(config)

MAP_URL = "https://raw.githubusercontent.com/outbreak-info/outbreak.info-resources/master/outbreak_resources_es_mapping_v3.json"
MAP_VARS = ["@type", "abstract", "date", "author", "citedBy", "curatedBy", "dateModified", "datePublished", "doi", "funding", "identifier", "isBasedOn", "issueNumber", "journalName", "journalNameAbbrev", "keywords", "license", "name", "pmid", "publicationType", "isRelatedTo", "url", "volumeNumber","correction"]

# when code is exported, import becomes relative
try:
    from litcovid.parser import load_annotations as parser_func
except ImportError:
    from .parser import load_annotations as parser_func


class NDEUploader(biothings.hub.dataload.uploader.BaseSourceUploader):

    name = "nde"
    __metadata__ = {
        "src_meta": {
            "author":{
                "name": "Julia Mullen",
                "url": "https://github.com/juliamullen"
            },
            "code":{
                "branch": "master",
                "repo": "https://github.com/outbreak-info/nde_outbreak_parser.git"
            },
            "url": "",
            "license": ""
        }
    }
    idconverter = None
    storage_class = biothings.hub.dataload.storage.BasicStorage

    def load_data(self, data_folder):
        self.logger.info("Load data from directory: '%s'" % data_folder)
        return parser_func(data_folder)

    @classmethod
    def get_mapping(klass):
        r = requests.get(MAP_URL)
        if(r.status_code == 200):
            mapping = r.json()
            mapping_dict = { key: mapping[key] for key in MAP_VARS }
            return mapping_dict
