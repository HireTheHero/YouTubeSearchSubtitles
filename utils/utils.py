"""
# Summary
Utility functions
# Details
## Reference
- https://qiita.com/FukuharaYohei/items/92795107032c8c0bfd19
"""
import argparse
import json
from logging import getLogger, Formatter, StreamHandler, DEBUG, INFO
import os
import re


def args_generator():
    """
    Add arguments to main function
    """
    formatter_class = argparse.RawTextHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=formatter_class)
    parser.add_argument("-k", "--key", help="YouTube Data API key", required=True)
    parser.add_argument("-q", "--query", help="YouTube query", required=True)
    parser.add_argument("-s", "--suffix", help="Suffix for query")
    parser.add_argument(
        "-t",
        "--search_type",
        help="YouTube search type",
        choices=["video", "playlist"],
        default="video",
    )
    parser.add_argument(
        "-m",
        "--max",
        help="Max # of items in query result",
        default=5,
        type=int,
    )
    parser.add_argument(
        "-n",
        "--next_count",
        help="Max count of searching next result",
        default=1,
        type=int,
    )
    parser.add_argument("-e", "--export_path", help="Export path", default="export")
    args = parser.parse_args()
    return args


def get_module_logger(verbose: bool = False, level=DEBUG):
    """
    Create logger
    """
    logger = getLogger(__name__)
    logger = _set_handler(logger, StreamHandler(), False)
    logger.setLevel(level)
    logger.propagate = False
    return logger


def _set_handler(logger, handler, verbose: bool):
    """
    Prep handler
    """
    if verbose:
        handler.setLevel(DEBUG)
    else:
        handler.setLevel(INFO)
    formatter = Formatter(
        "%(asctime)s %(name)s:%(lineno)s [%(levelname)s]: %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def export_json(args, videos):
    """
    Export result as json file
    """
    os.makedirs(args.export_path, exist_ok=True)
    suffix = re.sub("[^A-Za-z0-9]+", "_", args.suffix)
    with open(os.path.join(args.export_path, f"{args.query}{suffix}.json"), "w") as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)
    return
