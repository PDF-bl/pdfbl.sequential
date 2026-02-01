import numpy


def test_payload(pdfadapter_and_inputs):
    # C1: Use adapter.apply_payload.
    #   Expect the instance to have a new payload.
    expected_payload = {
        "scale": 0.4,
        "a": 3.52,
        "Uiso_0": 0.005,
        "delta2": 2.0,
        "qdamp": 0.04,
        "qbroad": 0.02,
    }
    adapter, _ = pdfadapter_and_inputs
    adapter.apply_payload(expected_payload)
    current_payload = adapter.get_payload()
    current_payload = {key: current_payload[key] for key in expected_payload}
    assert current_payload == expected_payload
    # C2: Use adapter.apply_payload.
    #  Expect the residual to change after applying a new payload
    residual_before = adapter._residual()
    adapter.apply_payload({"scale": 0.5})
    residual_after = adapter._residual()
    assert sum(residual_before) != sum(residual_after)


def test_action(pdfadapter_and_inputs):
    # C1: Use different initial payload values to test the optimization.
    #  Expect the final optimized value to be the same.
    adapter, _ = pdfadapter_and_inputs
    adapter.apply_payload({"scale": 0.4})
    adapter.action_func_factory(["scale"])()
    pv_dict_1 = adapter._get_parameter_values()
    adapter.apply_payload({"scale": 0.6})
    adapter.action_func_factory(["scale"])()
    pv_dict_2 = adapter._get_parameter_values()
    for key in pv_dict_1:
        assert numpy.isclose(pv_dict_1[key], pv_dict_2[key], rtol=1e-5)


def test_clone(pdfadapter_and_inputs):
    # C5: clone the adapter.
    #  Expect the cloned adapter to have the same payload as the original
    adapter, _ = pdfadapter_and_inputs
    new_adapter = adapter.clone()
    assert new_adapter.get_payload() == adapter.get_payload()
