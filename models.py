import os
from peewee import *

db = SqliteDatabase('db/caf.db')


class Run(Model):
    RunNumber = IntegerField()
    EORTime = IntegerField()
    SORTime = IntegerField()
    RecordedEvents = IntegerField()
    EFEvents = IntegerField()
    RunType = CharField(max_length=255)
    GainStrategy = CharField(max_length=255)
    PartitionName = CharField(max_length=255)
    Listener = CharField(max_length=255)

    class Meta:
        database = db


class Job(Model):
    Run = ForeignKeyField(Run, related_name='Jobs')
    Analysis = CharField(max_length=255)
    Start = DateTimeField()
    Status = CharField(max_length=255)

    class Meta:
        database = db


def connect(path=None, recreate=False):
    db_path = path
    if not path:
        base_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'db'
        )
        if not base_dir:
            os.makedirs(base_dir)
        db_path = os.path.join(base_dir, 'caf.db')

    if os.path.exists(db_path):
        if recreate:
            os.remove(db_path)

    db.database = db_path
    db.connect()
    db.create_tables([Run, Job], not recreate)
