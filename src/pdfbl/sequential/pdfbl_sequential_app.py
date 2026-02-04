import argparse

from pdfbl.sequential import __version__


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
    parser.parse_args()
