#!/usr/bin/env python
"""The main entry point. Invoke as `https' or `python -m httpies'.

"""
import sys


def main():
    try:
        from .core import main
        exit_status = main()
    except KeyboardInterrupt:
        exit_status = -1

    sys.exit(exit_status.value)


if __name__ == '__main__':
    main()
