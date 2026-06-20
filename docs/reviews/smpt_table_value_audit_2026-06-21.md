# SMPT 表格数值审计（2026-06-21）

- Total checks: 74
- Issues: 0

## Sources

- artifacts/peak_shaving/20260618/peak_shaving_summary.json
- artifacts/peak_shaving/20260619_smpt/smpt_baselines.csv
- artifacts/peak_shaving/20260619_smpt/smpt_fixed_point_residuals.csv
- artifacts/peak_shaving/20260619_smpt/smpt_ablations.csv
- artifacts/peak_shaving/20260619_smpt/smpt_resolved_sensitivity.csv
- artifacts/peak_shaving/20260619_submission/peak_shaving_mixed_oracle.json

## Result

All audited table values match the artifact values within manuscript rounding tolerance.

## Checked items

- Table4 uniform profit: paper=1193.3, artifact=1193.2649288504072, tolerance=0.05, status=ok
- Table4 uniform peak util: paper=0.213, artifact=0.21297890507561082, tolerance=0.0006, status=ok
- Table4 dynamic profit: paper=1139.4, artifact=1139.4043677649088, tolerance=0.05, status=ok
- Table4 dynamic peak util: paper=0.261, artifact=0.26079119033098214, tolerance=0.0006, status=ok
- optimal_static_qos_routing peak: paper=0.782, artifact=0.7822217827449163, tolerance=0.0006, status=ok
- optimal_static_qos_routing min qos: paper=0.756, artifact=0.756455957358171, tolerance=0.0006, status=ok
- optimal_static_qos_routing profit: paper=1783.0, artifact=1783.239231608924, tolerance=0.6, status=ok
- optimal_static_qos_routing served: paper=2610.0, artifact=2610.105444507793, tolerance=0.6, status=ok
- dynamic_coarse peak: paper=0.706, artifact=0.705901425170401, tolerance=0.0006, status=ok
- dynamic_coarse min qos: paper=0.968, artifact=0.9684143534133162, tolerance=0.0006, status=ok
- dynamic_coarse profit: paper=1949.0, artifact=1948.7877581277107, tolerance=0.6, status=ok
- dynamic_coarse profit gain: paper=9.3, artifact=9.283584814888853, tolerance=0.06, status=ok
- dynamic_coarse served: paper=2865.0, artifact=2865.3796027956846, tolerance=0.6, status=ok
- dynamic_fine peak: paper=0.666, artifact=0.6662669479948348, tolerance=0.0006, status=ok
- dynamic_fine min qos: paper=0.99, artifact=0.9901656568016834, tolerance=0.0006, status=ok
- dynamic_fine profit: paper=1749.0, artifact=1748.7937984034195, tolerance=0.6, status=ok
- dynamic_fine profit gain: paper=-1.9, artifact=-1.931621545496517, tolerance=0.06, status=ok
- dynamic_fine served: paper=3043.0, artifact=3042.987652234993, tolerance=0.6, status=ok
- off_peak_discount_only peak: paper=0.766, artifact=0.7664316142233594, tolerance=0.0006, status=ok
- off_peak_discount_only min qos: paper=0.833, artifact=0.8330016338242416, tolerance=0.0006, status=ok
- off_peak_discount_only profit gain: paper=5.0, artifact=5.028174726358095, tolerance=0.06, status=ok
- off_peak_discount_only served: paper=2849.0, artifact=2849.246827085535, tolerance=0.6, status=ok
- peak_surcharge_only peak: paper=0.738, artifact=0.7382757356710703, tolerance=0.0006, status=ok
- peak_surcharge_only min qos: paper=0.921, artifact=0.9206877193053253, tolerance=0.0006, status=ok
- peak_surcharge_only profit gain: paper=5.8, artifact=5.816141003911496, tolerance=0.06, status=ok
- peak_surcharge_only served: paper=2672.0, artifact=2672.3495273333674, tolerance=0.6, status=ok
- mixed max regret: paper=0.203, artifact=0.20253154148201702, tolerance=0.0006, status=ok
- mixed peak util: paper=0.703, artifact=0.7030252482394335, tolerance=0.0006, status=ok
- mixed min qos: paper=0.97, artifact=0.9698756172771479, tolerance=0.0006, status=ok
- mixed profit: paper=1733.0, artifact=1733.1319878128468, tolerance=0.6, status=ok
- mixed profit gain: paper=-2.8, artifact=-2.809900259477135, tolerance=0.06, status=ok
- optimal_static_qos_routing iterations: paper=52.0, artifact=52.0, tolerance=0.1, status=ok
- optimal_static_qos_routing residual: paper=8.32e-10, artifact=8.320706346154338e-10, tolerance=5e-13, status=ok
- off_peak_discount_only iterations: paper=32.0, artifact=32.0, tolerance=0.1, status=ok
- off_peak_discount_only residual: paper=8.23e-10, artifact=8.225664593908277e-10, tolerance=5e-13, status=ok
- peak_surcharge_only iterations: paper=34.0, artifact=34.0, tolerance=0.1, status=ok
- peak_surcharge_only residual: paper=9.71e-10, artifact=9.71215663447822e-10, tolerance=5e-13, status=ok
- dynamic_coarse iterations: paper=33.0, artifact=33.0, tolerance=0.1, status=ok
- dynamic_coarse residual: paper=8.52e-10, artifact=8.521310324027809e-10, tolerance=5e-13, status=ok
- dynamic_fine iterations: paper=35.0, artifact=35.0, tolerance=0.1, status=ok
- dynamic_fine residual: paper=6.44e-10, artifact=6.441621680508547e-10, tolerance=5e-13, status=ok
- abl baseline qos: paper=0.212, artifact=0.21195839605514522, tolerance=0.0006, status=ok
- abl baseline peak: paper=0.076, artifact=0.07632035757451527, tolerance=0.0006, status=ok
- abl baseline profit: paper=9.3, artifact=9.283584814888854, tolerance=0.06, status=ok
- abl no_outside_option qos: paper=0.307, artifact=0.30677571738176035, tolerance=0.0006, status=ok
- abl no_outside_option peak: paper=0.067, artifact=0.06668983659497862, tolerance=0.0006, status=ok
- abl no_outside_option profit: paper=11.3, artifact=11.323767013163401, tolerance=0.06, status=ok
- abl suppressed_direct_channel qos: paper=0.0, artifact=8.905028238825885e-05, tolerance=0.0006, status=ok
- abl suppressed_direct_channel peak: paper=0.209, artifact=0.20878878777997145, tolerance=0.0006, status=ok
- abl suppressed_direct_channel profit: paper=0.0, artifact=0.0036930243868481868, tolerance=0.06, status=ok
- abl homogeneous_capacity qos: paper=-0.054, artifact=-0.05406323322314144, tolerance=0.0006, status=ok
- abl homogeneous_capacity peak: paper=-0.154, artifact=-0.1541440697317421, tolerance=0.0006, status=ok
- abl homogeneous_capacity profit: paper=-3.6, artifact=-3.6234077389519674, tolerance=0.06, status=ok
- abl no_time_flexible_users qos: paper=0.155, artifact=0.15491028304589638, tolerance=0.0006, status=ok
- abl no_time_flexible_users peak: paper=0.046, artifact=0.04607163346613807, tolerance=0.0006, status=ok
- abl no_time_flexible_users profit: paper=6.1, artifact=6.090082684613335, tolerance=0.06, status=ok
- abl fixed_equal_routing qos: paper=0.125, artifact=0.124862265698375, tolerance=0.0006, status=ok
- abl fixed_equal_routing peak: paper=0.029, artifact=0.02905421602597702, tolerance=0.0006, status=ok
- abl fixed_equal_routing profit: paper=5.9, artifact=5.872454198569913, tolerance=0.06, status=ok
- rs capacity_0.90 qos: paper=0.28, artifact=0.28019384419948345, tolerance=0.0006, status=ok
- rs capacity_0.90 peak: paper=0.06, artifact=0.059719933529423064, tolerance=0.0006, status=ok
- rs capacity_0.90 profit: paper=12.5, artifact=12.530876745147134, tolerance=0.06, status=ok
- rs alpha_1.15 qos: paper=0.241, artifact=0.2414689619437843, tolerance=0.0006, status=ok
- rs alpha_1.15 peak: paper=0.15, artifact=0.14981928252776033, tolerance=0.0006, status=ok
- rs alpha_1.15 profit: paper=-1.4, artifact=-1.4375428803061145, tolerance=0.06, status=ok
- rs flexible_share_0.70 qos: paper=0.242, artifact=0.2419574871260648, tolerance=0.0006, status=ok
- rs flexible_share_0.70 peak: paper=0.136, artifact=0.13586968514929032, tolerance=0.0006, status=ok
- rs flexible_share_0.70 profit: paper=-1.9, artifact=-1.922428317041273, tolerance=0.06, status=ok
- rs qos_threshold_0.78 qos: paper=0.241, artifact=0.24091756712984014, tolerance=0.0006, status=ok
- rs qos_threshold_0.78 peak: paper=0.066, artifact=0.06639404597683995, tolerance=0.0006, status=ok
- rs qos_threshold_0.78 profit: paper=11.0, artifact=11.013893944343591, tolerance=0.06, status=ok
- rs outside_utility_0.50 qos: paper=0.156, artifact=0.1563910446600847, tolerance=0.0006, status=ok
- rs outside_utility_0.50 peak: paper=0.069, artifact=0.06910602813819988, tolerance=0.0006, status=ok
- rs outside_utility_0.50 profit: paper=0.7, artifact=0.7199778472375181, tolerance=0.06, status=ok
