import json
import requests
import time


def reorganize_publication_datum(crossref_record, extra_datum):
    raw_publication = crossref_record['message']

    title = str()
    if raw_publication['title']:
        title = raw_publication['title'][0]

    journal_name = str()
    if raw_publication['container-title']:
        journal_name = raw_publication['container-title'][0]

    publication_year = str()
    if raw_publication['issued']:
        publication_year = raw_publication['issued']['date-parts'][0][0]

    author_list = list()
    if raw_publication['author']:
        for author_index in range(len(raw_publication['author'])):
            # First test that 'given' and 'family' are both valid keys for this author dictionary:
            if all(x in raw_publication['author'][author_index] for x in ['given', 'family']):
                author_list.append(raw_publication['author'][author_index]['given'] + ' ' +
                                   raw_publication['author'][author_index]['family'])

    url = str()
    if raw_publication['URL']:
        url = raw_publication['URL']

    publication = {
        'author_list':      author_list,
        'is_valid':         False,
        'journal_name':     journal_name,
        'publication_year': publication_year,
        'title':            title,
        'url':              url,
        **extra_datum
    }

    return publication


def find_if_date_is_valid(publication_year):
    today_year = int(time.strftime("%Y,%m,%d,%H,%M,%S").split(',')[0])
    return (publication_year >= today_year - 5)


def find_author_in_list_and_where(author_list, first_name, last_name):

    first_name = first_name.strip().split()[0]
    last_name = last_name.strip().split()[-1]

    for index, author in enumerate(author_list):
        if (first_name == author.strip().split()[0]) & (last_name == author.strip().split()[-1]):
            return(True, index + 1)

    return(False, 0)


def find_author_good_position(author_position, length_list):
    if (author_position == 1) | (length_list == 2):
        return True
    return False


def get_publication_from_doi(doi):
    url_crossref = 'https://api.crossref.org/works/{}'.format(doi)
    response = requests.get(url_crossref)

    if response.status_code != 200:
        return None

    crossref_record = json.loads(response.content.decode('utf-8'))
    publication = reorganize_publication_datum(
        crossref_record,
        {'doi': doi, 'is_doi_valid': True}
    )
    return publication


def is_publication_valid_for(user, publication):
    is_date_valid = is_author_in_list = is_author_good_position = False

    is_date_valid = find_if_date_is_valid(publication['publication_year'])
    is_author_in_list, author_position = find_author_in_list_and_where(
        publication['author_list'], user['first_name'], user['last_name'])
    if is_author_in_list:
        is_author_good_position = find_author_good_position(
            author_position,
            len(publication['author_list'])
        )

    if publication.get('is_doi_valid') \
                and is_date_valid \
                and is_author_in_list \
                and is_author_good_position:
        return True

    return False
