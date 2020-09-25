from models.content import Content
from models.verdict import Verdict


def get_global_statistics():
    return [
        {
            'collectionName': 'contents',
            'count': Content.query.filter(Content.type == None).count(),
        },
        {
            'collectionName': 'verdicts',
            'count': Verdict.query.count(),
        }
    ]
