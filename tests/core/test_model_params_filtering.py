from autoemulate.core.compare import AutoEmulate


def test_model_params_are_filtered_per_emulator(sample_data_for_ae_compare):
    x, y = sample_data_for_ae_compare

    ae = AutoEmulate(
        x,
        y,
        models=["GaussianProcessRBF", "RandomForest"],
        model_params={"posterior_predictive": True},
        n_bootstraps=1,
        show_progress_bar=False,
    )

    results = {result.model_name: result for result in ae.results}
    assert set(results) == {"GaussianProcessRBF", "RandomForest"}
    assert results["GaussianProcessRBF"].model.model.posterior_predictive is True
    assert "posterior_predictive" not in results["RandomForest"].params
