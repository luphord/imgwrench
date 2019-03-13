# -*- coding: utf-8 -*-

'''Console script for imgwrench.'''

import sys

from .cli import cli_imgwrench

if __name__ == '__main__':
    sys.exit(cli_imgwrench())
