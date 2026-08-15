from pathlib import Path

compare_path = Path("autoemulate/core/compare.py")
text = compare_path.read_text()
old = '''                                # Overwrite defaults with user-supplied values
                                best_params_for_this_model = {
                                    **default_params,
                                    **self.model_params,
                                }
'''
new = '''                                # Apply only user parameters accepted by this model.
                                # This lets one shared model_params mapping configure
                                # heterogeneous emulator classes without passing
                                # model-specific arguments to incompatible models.
                                accepts_kwargs = any(
                                    param.kind is inspect.Parameter.VAR_KEYWORD
                                    for param in init_sig.parameters.values()
                                )
                                if accepts_kwargs:
                                    compatible_model_params = self.model_params
                                else:
                                    compatible_model_params = {
                                        name: value
                                        for name, value in self.model_params.items()
                                        if name in init_sig.parameters
                                    }

                                ignored_model_params = (
                                    self.model_params.keys()
                                    - compatible_model_params.keys()
                                )
                                if ignored_model_params:
                                    logger.debug(
                                        'Ignoring unsupported model_params for model "%s": %s',
                                        model_cls.__name__,
                                        sorted(ignored_model_params),
                                    )

                                # Overwrite defaults with compatible user-supplied values.
                                best_params_for_this_model = {
                                    **default_params,
                                    **compatible_model_params,
                                }
'''
if old not in text:
    raise SystemExit("target model_params block not found")
compare_path.write_text(text.replace(old, new, 1))

test_path = Path("tests/core/test_model_params_filtering.py")
test_path.write_text('''from autoemulate.core.compare import AutoEmulate\n\n\ndef test_model_params_are_filtered_per_emulator(sample_data_for_ae_compare):\n    x, y = sample_data_for_ae_compare\n\n    ae = AutoEmulate(\n        x,\n        y,\n        models=["GaussianProcessRBF", "RandomForest"],\n        model_params={"posterior_predictive": True},\n        n_bootstraps=1,\n        show_progress_bar=False,\n    )\n\n    results = {result.model_name: result for result in ae.results}\n    assert set(results) == {"GaussianProcessRBF", "RandomForest"}\n    assert results["GaussianProcessRBF"].model.model.posterior_predictive is True\n    assert "posterior_predictive" not in results["RandomForest"].params\n''')

Path(".github/workflows/apply-921.yml").unlink(missing_ok=True)
Path(__file__).unlink(missing_ok=True)
