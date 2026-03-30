import argparse

from pdfbl.sequential import __version__
from pdfbl.sequential.diffpy_interpreter import DiffpyInterpreter


def main():
    """Entry point for the pdfbl-cli.

    Examples
    --------
    >>> pdfbl-cli --version
    """
    parser = argparse.ArgumentParser(
        description=(
            "Scripts for running sequential PDF refinements "
            "using diffpy.cmi automatically"
        )
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"pdfbl.sequential {__version__}",
        help="Show the version of pdfbl.sequential and exit.",
    )
    subparsers = parser.add_subparsers(dest="subcommand")
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("input_file", help="Input .dp-in file.")
    run_parser.set_defaults(func=DiffpyInterpreter().run_app)
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
