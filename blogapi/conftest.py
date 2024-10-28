import os

os.environ["PYTEST_RUNNING"] = "true"

from blogapi.blog.tests.fixtures import *
from blogapi.core.tests.fixtures import *
