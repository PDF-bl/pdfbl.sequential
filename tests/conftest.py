from pathlib import Path

import pytest

from pdfbl.interface import PDFAdapter


@pytest.fixture
def pdfadapter_and_inputs():
    profile_path = Path("tests/data/Ni.gr")
    structure_path = Path("tests/data/Ni.cif")
    inputs = {
        "profile_string": profile_path.read_text(),
        "structure_string": structure_path.read_text(),
        "xmin": 1.5,
        "xmax": 50,
        "dx": 0.01,
        "qmax": 25.0,
        "qmin": 0.1,
    }
    adapter = PDFAdapter()
    adapter.load_inputs(inputs)
    yield adapter, inputs
