#! /usr/bin/env python
"""
What this will do

Based on the Python script template at
https://github.com/BrianGallew/script_templates/blob/master/template.py
"""

import logging
import logging.handlers
logger = logging.getLogger(__name__)
# Requires Python 2.7 or better
import argparse


def setup_logging(option_group):
    """Sets up logging in a syslog format by log level
    :param option_group: options as returned by the OptionParser
    """
    stderr_log_format = "%(levelname) -8s %(asctime)s %(funcName)s line:%(lineno)d: %(message)s"
    file_log_format = "%(asctime)s - %(levelname)s - %(message)s"
    if option_group.debug:
        logger.setLevel(level=logging.DEBUG)
    elif option_group.verbose:
        logger.setLevel(level=logging.INFO)
    else:
        logger.setLevel(level=logging.WARNING)

    handlers = []
    if option_group.syslog:
        handlers.append(
            logging.handlers.SysLogHandler(facility=option_group.syslog))
        # Use standard format here because timestamp and level will be added by
        # syslogd.
    if option_group.logfile:
        handlers.append(logging.FileHandler(option_group.logfile))
        handlers[0].setFormatter(logging.Formatter(file_log_format))
    if not handlers:
        handlers.append(logging.StreamHandler())
        handlers[0].setFormatter(logging.Formatter(stderr_log_format))
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    for handler in handlers:
        logger.addHandler(handler)
    return


def main():
    """Primary entry point."""
    parser = argparse.ArgumentParser()
    # Standard logging options.
    parser.add_argument("-v", "--verbose", dest="verbose", action='store_true',
                        default=False, help="Verbose output")
    parser.add_argument("-d", "--debug", dest="debug", action='store_true',
                        default=False, help="Debugging output")
    parser.add_argument("--syslog", dest="syslog", metavar="FACILITY",
                        help="Send log messages to the syslog")
    parser.add_argument("--logfile", dest="logfile", metavar="FILENAME",
                        help="Send log messages to a file")
    # script-specific options here

    options = parser.parse_args()
    setup_logging(options)

    # Your code here.

    return


if __name__ == '__main__':
    main()
