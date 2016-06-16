#!/usr/bin/env python
import os
import sys

import dotenv


if __name__ == "__main__":
    dotenv_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.ENV')
    dotenv.load_dotenv(dotenv_path)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tshape.settings.base")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
