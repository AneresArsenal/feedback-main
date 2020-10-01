# Generic single-database configuration

1. Update with migration status

```bash
pc alembic stamp head
```

2. Create a boilerplate file of the new migration

```bash
pc alembic revision -m "revision_name"
```

3. Once the upgrade function has been completed

```bash
pc alembic upgrade <id>
```

## Do

It is possible to perform a migration either by SQL commands :

```SQL
ALTER TABLE "booking" ADD COLUMN amount numeric(10,2);
```

or by the functions provided by the alembic library:


```python
op.add_column('venue_provider', sa.Column('syncWorkerId', sa.VARCHAR(24), nullable=True))
```

## Don't

When you want to modify the schema of several tables at the same time,
do not commit multiple changes in a single commit command.

Avoid doing:

```python
op.add_column('stock', sa.Column('fieldsUpdated', sa.ARRAY(sa.String(100)), nullable=False, server_default="{}"))
op.add_column('offer', sa.Column('fieldsUpdated', sa.ARRAY(sa.String(100)), nullable=False, server_default="{}"))
```

Instead do the following:

```python
op.add_column('stock', sa.Column('fieldsUpdated', sa.ARRAY(sa.String(100)), nullable=False, server_default="{}"))
op.execute("COMMIT")
op.add_column('offer', sa.Column('fieldsUpdated', sa.ARRAY(sa.String(100)), nullable=False, server_default="{}"))
op.execute("COMMIT")
```

If we use execute multiple changes in a single commit, we risk having this kind of errors on Scalingo:
```
sqlalchemy.exc.OperationalError: (psycopg2.extensions.TransactionRollbackError) deadlock detected
```
