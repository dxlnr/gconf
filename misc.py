import argparse
import os


def create_arg_parser():
    r"""Get arguments from command lines."""
    parser = argparse.ArgumentParser(
        description="Parser for KI-Wissen object detection."
    )
    parser.add_argument("--cfg", type=str, help="Configuration file (path)")

    return parser
