""" Database model
"""
import os
from peewee import *
from fields import *

""" Default database is db/caf.db """
db = SqliteDatabase('db/caf.db')


class BaseModel(Model):
    class Meta:
        database = db


class Listener(BaseModel):
    Name = CharField(max_length=255)


class Run(BaseModel):
    RunNumber = IntegerField()
    EORTime = IntegerField()
    SORTime = IntegerField()
    RecordedEvents = IntegerField()
    EFEvents = IntegerField()
    RunType = CharField(max_length=255)
    GainStrategy = CharField(max_length=255)
    PartitionName = CharField(max_length=255)

    Listeners = ManyToManyField(Listener, related_name='Runs')


class File(BaseModel):
    Name = CharField(max_length=512)
    Run = ForeignKeyField(Run, related_name='Files')


# class RunListener(Model):
#     Run = ForeignKeyField(Run, related_name='Listeners')
#     Listener = ForeignKeyField(Listener, related_name='Runs')
#
#     class Meta:
#         database = db

class Job(BaseModel):
    STATUS_NEW = "NEW"
    STATUS_PREPARED = "PREPARED"
    STATUS_SUBMITED = "SUBMITED"
    STATUS_FAILED = "FAILED"
    STATUS_DONE = "DONE"

    Run = ForeignKeyField(Run, related_name='Jobs')
    Analysis = CharField(max_length=255)
    Start = DateTimeField()
    Status = CharField(max_length=255)


def connect(path=None, recreate=False):
    """ Connect to database
    Args:
        path (string): path to the database
        recreate (bool): recreate database? The old database will be rewritten
                         if this flag is set
    """
    db_path = path
    if not path:
        base_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'db'
        )
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        db_path = os.path.join(base_dir, 'caf.db')

    if os.path.exists(db_path):
        if recreate:
            os.remove(db_path)

    db.database = db_path
    db.connect()
    db.create_tables([Run, Job, Listener, File, Run.Listeners.get_through_model()], not recreate)
