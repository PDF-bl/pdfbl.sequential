from pathlib import Path

import pytest

from pdfbl.interface import FitDAG, FitRunner


@pytest.fixture
def fitrunnner_related_instances_dict():
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
        "remove_vars": ["delta1"],
    }
    payload = {
        "scale": 0.4,
        "a": 3.52,
        "Uiso_0": 0.005,
        "delta2": 2.0,
        "qdamp": 0.04,
        "qbroad": 0.02,
    }
    dag = FitDAG()
    dag.from_str("a->scale->qdamp->Uiso_0->delta2->all")
    runner = FitRunner()
    yield {
        "runner": runner,
        "dag": dag,
        "payload": payload,
        "inputs": inputs,
        "structure_path": structure_path,
        "profile_path": profile_path,
    }
