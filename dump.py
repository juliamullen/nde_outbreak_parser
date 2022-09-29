import os
import datetime

import biothings, config
biothings.config_for_app(config)
from config import DATA_ARCHIVE_ROOT

import biothings.hub.dataload.dumper

class NDEDumper(biothings.hub.dataload.dumper.DummyDumper):
    SRC_NAME = "nde"
    SRC_ROOT_FOLDER = os.path.join(DATA_ARCHIVE_ROOT, SRC_NAME)

    SCHEDULE = "40 4 * * *"

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_release()

    def set_release(self):
        self.release = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M')
