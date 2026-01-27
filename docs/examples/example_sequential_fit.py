from pathlib import Path

from pdfbl.interface import FitDAG
from pdfbl.sequential.pdf_sequential_fit import PDFSequentialFit

sq_fit = PDFSequentialFit()
template_dag = FitDAG()
template_dag.from_str("a->scale->qdamp->Uiso_0->delta2->all")
sq_fit.set_meta_inputs(
    profile_folder=Path("example/data/Ni-Tdep"),
    structure_file=Path("tests/data/Ni.cif"),
    initial_payload={
        "scale": 0.4,
        "a": 3.52,
        "Uiso_0": 0.005,
        "delta2": 2.0,
        "qdamp": 0.04,
        "qbroad": 0.02,
    },
    dump_folder=Path("example/results"),
    dump_filename="fit_results",
    template_dag=template_dag,
    filename_pattern=r"(\d+)K\.gr",
    xmin=1.5,
    xmax=50,
    dx=0.01,
    qmax=25.0,
    qmin=0.1,
    remove_vars=["delta1"],
)
sq_fit.watch("a", when="dag end")
sq_fit.watch("ycalc_0", when="all", update_mode="replace")
# uncomment if the previous fit result files are generated
# sq_fit.set_start_profile("Ni_PDF_20250922-234708_04f3a7_60K.gr")
sq_fit.launch(mode="batch")
