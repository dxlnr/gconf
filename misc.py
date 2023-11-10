import argparse


def create_arg_parser():
    r"""Get arguments from command lines."""
    parser = argparse.ArgumentParser(description="Commandline Parser")
    parser.add_argument("--h", type=str, help="help: Prints out help params.")
    parser.add_argument("--conf", type=str, help="Configuration file (path)")

    return parser
