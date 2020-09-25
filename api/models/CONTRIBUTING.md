# Package `models`

The modules in this package mainly contain classes that implement the relational data model for the backend. These classes are represented as follows:

- SQL tables (inheritance from `ApiHandler` and` Model`);
- columns of SQL tables (we call class `*Mixin`).

This system is entirely based on the ORM SQL `Alchemy`.

## Do

The modifications made to the data model must be imperatively and systematically scripted in a relational schema migration with `Alembic`. Both modifications (ORM classes and `Alembic` migration) must be merged simultaneously in the master branch. It is imperative to be ISO between an ORM class and the `Alembic` revision because the production only plays the` Alembic` revisions and does not take care about the `Model`. 

It is important to know that a foreign key is not a default index in `Postgres`, so you have to add it according to your context.

So when we have:

```python
fooId = Column(BigInteger,
    ForeignKey('foo.id'),
    index=True)
```

In the `Alembic` revision, you need:

```python
ALTER TABLE ONLY bar_foo ADD CONSTRAINT "bar_foo_fooId_fkey" FOREIGN KEY ("fooId") REFERENCES foo(id);
CREATE INDEX "idx_bar_foo_fooId" ON offer_foo ("fooId");
```

## Testing

The classes present in this package are not testable since they are designed, in their simplest form, to comprised only of declaration of fields. However, if we want to give them behaviors or logic (e.g. via instance methods or _properties_), it is possible to test them individually.

## For more information

- https://fr.wikipedia.org/wiki/Mapping_objet-relationnel
- https://www.sqlalchemy.org/features.html
- https://alembic.sqlalchemy.org/en/latest/index.html