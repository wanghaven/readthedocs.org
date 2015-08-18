from readthedocs.builds.constants import LATEST
from .indexes import ProjectIndex, PageIndex

from readthedocs.search.signals import before_project_search, before_file_search


def search_project(request, query, language):

    body = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"name": {"query": query, "boost": 10}}},
                    {"match": {"description": {"query": query}}},
                ]
            },
        },
        "facets": {
            "language": {
                "terms": {"field": "lang"},
            },
        },
        "highlight": {
            "fields": {
                "name": {},
                "description": {},
            }
        },
        "fields": ["name", "slug", "description", "lang", "url"],
        "size": 50  # TODO: Support pagination.
    }

    if language:
        body['facets']['language']['facet_filter'] = {"term": {"lang": language}}
        body['filter'] = {"term": {"lang": language}}

    before_project_search.send(request=request, sender=ProjectIndex, body=body)

    return ProjectIndex().search(body)


def search_file(request, query, project=None, version=LATEST, taxonomy=None):

    kwargs = {}
    body = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"title": {"query": query, "boost": 10}}},
                    {"match": {"headers": {"query": query, "boost": 5}}},
                    {"match": {"content": {"query": query}}},
                ]
            }
        },
        "facets": {
            "taxonomy": {
                "terms": {"field": "taxonomy"},
            },
            "project": {
                "terms": {"field": "project"},
            },
            "version": {
                "terms": {"field": "version"},
            },
        },
        "highlight": {
            "fields": {
                "title": {},
                "headers": {},
                "content": {},
            }
        },
        "fields": ["title", "project", "version", "path"],
        "size": 50  # TODO: Support pagination.
    }

    if project or version or taxonomy:
        final_filter = {"and": []}

        if project:
            final_filter['and'].append({'term': {'project': project}})

            # Add routing to optimize search by hitting the right shard.
            kwargs['routing'] = project

        if version:
            final_filter['and'].append({'term': {'version': version}})

        if taxonomy:
            final_filter['and'].append({'term': {'taxonomy': taxonomy}})

        body['filter'] = final_filter
        body['facets']['project']['facet_filter'] = final_filter
        body['facets']['version']['facet_filter'] = final_filter
        body['facets']['taxonomy']['facet_filter'] = final_filter

    before_file_search.send(request=request, sender=PageIndex, body=body)

    results = PageIndex().search(body, **kwargs)
    return results
