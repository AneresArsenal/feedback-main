def import_keywords():
    from sqlalchemy import func, Index, TEXT
    from sqlalchemy.sql.expression import cast
    from sqlalchemy.sql.functions import coalesce
    from domain.keywords import create_tsvector
    from models.content import Content
    from models.review import Review
    from models.tag import Tag
    from models.user import User
    from models.verdict import Verdict

    Content.__ts_vector__ = create_tsvector(
        cast(coalesce(Content.title, ''), TEXT),
        cast(coalesce(Content.summary, ''), TEXT),
    )
    Content.__table_args__ = (
        Index(
            'idx_content_fts',
            Content.__ts_vector__,
            postgresql_using='gin'
        ),
    )

    Review.__ts_vector__ = create_tsvector(
        cast(coalesce(Review.comment, ''), TEXT),
    )
    Review.__table_args__ = (
        Index(
            'idx_review_fts',
            Review.__ts_vector__,
            postgresql_using='gin'
        ),
    )

    Tag.__ts_vector__ = create_tsvector(
        cast(coalesce(Tag.label, ''), TEXT),
    )
    Tag.__table_args__ = (
        Index(
            'idx_tag_fts',
            Tag.__ts_vector__,
            postgresql_using='gin'
        ),
    )

    User.__ts_vector__ = create_tsvector(
        cast(coalesce(User.email, ''), TEXT),
        cast(coalesce(User.firstName, ''), TEXT),
        cast(coalesce(User.lastName, ''), TEXT),
    )
    User.__table_args__ = (
        Index(
            'idx_user_fts',
            User.__ts_vector__,
            postgresql_using='gin'
        ),
    )

    Verdict.__ts_vector__ = create_tsvector(
        cast(coalesce(Verdict.comment, ''), TEXT),
        cast(coalesce(Verdict.title, ''), TEXT),
    )
    Verdict.__table_args__ = (
        Index(
            'idx_verdict_fts',
            Verdict.__ts_vector__,
            postgresql_using='gin'
        ),
    )
