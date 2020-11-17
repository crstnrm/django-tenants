import os

from multi_tenant.migration_executors.base import MigrationExecutor
from multi_tenant.migration_executors.parallel import ParallelExecutor
from multi_tenant.migration_executors.standard import StandardExecutor


def get_executor(codename=None):
    codename = codename or os.environ.get('EXECUTOR', StandardExecutor.codename)

    for klass in MigrationExecutor.__subclasses__():
        if klass.codename == codename:
            return klass

    raise NotImplementedError('No executor with codename %s' % codename)