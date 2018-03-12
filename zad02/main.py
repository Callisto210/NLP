#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os import listdir
from os.path import isfile, join

import json

from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import TransportError

def load_json():
    for filename in listdir('data'):
        print(filename)
        if filename.endswith('.json'):
            with open(join('data/', filename), 'r') as open_file:
                yield json.load(open_file)

def main():
    es = Elasticsearch([{'host': '172.17.0.2', 'port':9200}])

    settings = {
        'settings': {
            #'index.mapping.ignore_malformed' : True,
            #'index.mapper.dynamic': False,
            'analysis': {
                'analyzer': {
                    'polish': {
                        'type': 'custom',
                        'tokenizer': 'standard',
                        'filter': ['lowercase', 'morfologik_stem']
                    }
                }
            }
        },
            'mappings': {
                '_default_': {
                    'dynamic_templates': [{
                        'data_errata': {
                            'match_mapping_type': 'date',
                            'path_match': 'items.source.publicationDate',
                            'mapping': {
                                'type':'text',
                              #  'index': False
                            }
                        }
                    }]
                },
                '_doc': {
                    'properties': {
                        'items.textContent': {'type': 'text', 'analyzer': 'polish'},
                        'items.judgmentDate': {'type': 'date'},
                        'items.courtCases.caseNumber': {'type': 'keyword'},
                        'items.judges.name': {'type': 'keyword'}
                    }
                }
            }
      }

    try:
        es.indices.create(index = 'cases', body = settings)
        helpers.bulk(es, load_json(), index='cases', doc_type='_doc')
    except TransportError as e:
        if e.error == 'resource_already_exists_exception':
            pass
        else:
            raise


    count_harm = {
          'query': {
            'match': {
              'items.textContent': 'szkoda'
            }
          }
    }

    res = es.search(index='cases', doc_type='_doc', body=count_harm, size=0)
    print ('Ilość słów szkoda: ' + str(res['hits']['total']))

    phrase = {
        'query': {
            'match_phrase': {
                'items.textContent': 'trwały uszczerbek na zdrowiu'
            }
        }
    }

    res = es.search(index='cases', doc_type='_doc', body=phrase, size=0)
    print ('Ilość uszczerbków na zdrowiu: ' + str(res['hits']['total']))

    phrase2 = {
        'query': {
            'match_phrase': {
                'items.textContent': {
                    'query': 'trwały uszczerbek na zdrowiu',
                    'slop': 4
                }
            }
        }
    }

    res = es.search(index='cases', doc_type='_doc', body=phrase2, size=0)
    print ('Ilośc uszczerbków na zdrowiu (z 2 słowami): ' + str(res['hits']['total']))

    top3 = {
        'aggs': {
            'names': {
                'terms': {'field': 'items.judges.name'}
            }
        }
    }

    res = es.search(index='cases', doc_type='_doc', body=top3, size=0)
    print ('Top3 sędziowie: ' + str(res))

    cnt = {
        'aggs': {
            'monthly': {
                'date_histogram': {
                    'field': 'items.judgmentDate',
                    'interval': 'month'
                }
            }
        }
    }

    res = es.search(index='cases', doc_type='_doc', body=cnt, size=0)
    print ('Orzeczeń miesięcznie: ' + str(res))
if __name__ == '__main__':
    sys.exit(main())
