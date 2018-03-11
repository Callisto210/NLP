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
                    'morfilogik_based_analyzer': {
                        'type': 'custom',
                        'tokenizer': 'standard',
                        'filter': ['morfologik_stem']
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
                'judgement': {
                    'properties': {
                        'items': {'type': 'object',
                                  'properties': {
                                    'textContent': {'type': 'text'},
                                    'judgmentDate': {'type': 'date'},
                                    'courtCases': {'type': 'object',
                                                   'properties': {'caseNumber': {'type': 'keyword'}}},
                                    'judges': {'type': 'object',
                                                'properties': {'name': {'type': 'text'}}}
                                  }
                        }
                    }
                }
            }
      }

    try:
        es.indices.create(index = 'cases', body = settings)
    except TransportError as e:
        if e.error == 'resource_already_exists_exception':
            pass
        else:
            raise

    helpers.bulk(es, load_json(), index='cases', doc_type='judgement')

    count_harm = {
          'query': {
            'query_string': {
              'fields': [
                'textContent'
              ],
              'query': '\'szkoda\''
            }
          },  
          'aggs' : {
            'my-terms' : {
                'terms' : {
                    'field' : 'textContent'
                }
            }
        }
    }
    res = es.search(index='cases', doc_type='judgement', body=count_harm, size=100)
    print (res)

if __name__ == '__main__':
    sys.exit(main())
