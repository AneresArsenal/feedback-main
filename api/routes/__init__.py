from utils.config import IS_DEV

def install_routes():
    import routes.articles
    import routes.evaluations
    import routes.images
    import routes.password
    import routes.reviews
    import routes.roles
    import routes.scrap
    import routes.sign
    import routes.tags
    import routes.trendings
    import routes.users
    import routes.verdicts
    import routes.verdict_users

    import routes.health_check
    import routes.storage

    import routes.error_handlers

    if IS_DEV:
        import routes.sandboxes
