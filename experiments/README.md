# Experiment Entrypoints

Run commands from the project root so relative artifact paths stay consistent.

```bash
python experiments/run_experiment.py --smoke
python experiments/run_reproducibility_bundle.py --smoke
python experiments/run_intermediary_experiment.py --full
python experiments/run_review_strengthening_experiments.py
python experiments/run_calibration_uncertainty_experiments.py
```

The reusable simulation code stays in `pricing_sim/`. This directory only holds
CLI entrypoints and plotting helpers.
