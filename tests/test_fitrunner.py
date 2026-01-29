import sys
from pathlib import Path

import numpy
from scipy.optimize import least_squares

from pdfbl.interface import FitDAG, FitRunner, PDFAdapter

sys.path.append(str(Path(__file__).parent / "diffpycmi_scripts.py"))
from diffpycmi_scripts import make_recipe  # noqa: E402


def test_run(fitrunnner_related_instances_dict):
    structure_path = fitrunnner_related_instances_dict["structure_path"]
    profile_path = fitrunnner_related_instances_dict["profile_path"]
    inputs = fitrunnner_related_instances_dict["inputs"]
    payload = fitrunnner_related_instances_dict["payload"]
    # C1: Run the same Fit using diffpy.cmi and FitRunner.
    #  Expect to get similar results.
    diffpycmi_recipe = make_recipe(str(structure_path), str(profile_path))
    diffpycmi_recipe.fithooks[0].verbose = 0
    diffpycmi_recipe.fix("all")
    tags = ["lat", "scale", "adp", "d2", "all"]
    for tag in tags:
        diffpycmi_recipe.free(tag)
        least_squares(
            diffpycmi_recipe.residual,
            diffpycmi_recipe.values,
            x_scale="jac",
        )
    diffpyname_to_runner_name = {
        "fcc_Lat": "a",
        "s1": "scale",
        "fcc_ADP": "Uiso_0",
        "Ni_Delta2": "delta2",
        "Calib_Qdamp": "qdamp",
        "Calib_Qbroad": "qbroad",
        "all": "all",
    }
    diffpy_pv_dict = {}
    for tag, parameter in diffpycmi_recipe._parameters.items():
        pname = diffpyname_to_runner_name[tag]
        diffpy_pv_dict[pname] = parameter.value
    dag = FitDAG()
    dag.from_str("a->scale->qdamp->Uiso_0->delta2->all")
    runner = FitRunner()
    runner._run_dag(dag, PDFAdapter, inputs, payload)
    last_node_id = dag.leaf_nodes[0]
    last_node = dag.nodes[last_node_id]
    runner_pv_dict = {
        pname: last_node["payload"][pname] for pname in diffpy_pv_dict.keys()
    }
    for pname in diffpy_pv_dict.keys():
        numpy.isclose(diffpy_pv_dict[pname], runner_pv_dict[pname], rtol=1e-5)


def test_watch(fitrunner_related_instances_dict):
    # C1: Collect data for parameter "a" at the end of each node
    #  Expect 6 data points collected for parameter "a"
    runner = fitrunner_related_instances_dict["runner"]
    dag = fitrunner_related_instances_dict["dag"]
    inputs = fitrunner_related_instances_dict["inputs"]
    payload = fitrunner_related_instances_dict["payload"]
    runner.watch(
        lambda dag, node_id: True,
        pname="a",
        update_mode="append",
        source="payload",
    )
    runner._run_dag(dag, PDFAdapter, inputs, payload)
    assert list(runner.data_for_plot.values())[0]["ydata"].qsize() == 6


def test_mark(fitrunner_related_instances_dict):
    runner = fitrunner_related_instances_dict["runner"]
    dag = fitrunner_related_instances_dict["dag"]
    # C1: Mark a node "hasAdapter" and "hasPayload"
    #  Expect runner.is_marked(node_id, "initialized") to be True
    node_id = list(dag.nodes.keys())[0]
    runner.mark(node_id, "hasAdapter")
    runner.mark(node_id, "hasPayload")
    assert runner.is_marked(node_id, "initialized")
    # C2: Mark a node "hasAdapter" only
    #  Expect runner.is_marked(node_id, "initialized") to be False
    node_id = list(dag.nodes.keys())[1]
    runner.mark(node_id, "hasAdapter")
    assert not runner.is_marked(node_id, "initialized")
    # C3: Mark a node "hasPayload" only
    #  Expect runner.is_marked(node_id, "initialized") to be False
    node_id = list(dag.nodes.keys())[2]
    runner.mark(node_id, "hasPayload")
    assert not runner.is_marked(node_id, "initialized")
    # C4: Mark a node "hasAdapter", "hasPayload" and "completed"
    #  Expect runner.is_marked(node_id, "initialized") to be False
    #  runner.is_marked(node_id, "initialized") to be True
    node_id = list(dag.nodes.keys())[3]
    runner.mark(node_id, "hasAdapter")
    runner.mark(node_id, "hasPayload")
    runner.mark(node_id, "completed")
    assert not runner.is_marked(node_id, "initialized")
    assert runner.is_marked(node_id, "completed")
