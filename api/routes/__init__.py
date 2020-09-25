# pylint: disable=C0415
# pylint: disable=W0611

from utils.config import IS_DEVELOPMENT


def import_routes():
    import routes.appearances
    import routes.author_contents
    import routes.claims
    import routes.contents
    import routes.graphs
    import routes.images
    import routes.jobs
    import routes.organizations
    import routes.password
    import routes.orcid
    import routes.reviews
    import routes.roles
    import routes.scrap
    import routes.sign
    import routes.statistics
    import routes.tags
    import routes.trendings
    import routes.users
    import routes.verdicts
    import routes.verdict_reviewers
    import routes.webhooks
    import routes.wikidata

    import routes.health
    import routes.storage


    import utils.errorhandler

    if IS_DEVELOPMENT:
        import routes.sandboxes
