# Verified source log (raw)
## Apple
- ICLR2024 Large-scale Training of FMs for Wearable Biosignals. Abbaspourazad, Elachqar, Miller, Emrani, Nallasamy, Shapiro. arXiv 2312.05409 (2023-12-08; v2 2024-03-06 camera ready). OpenReview pC3WJHf51j published 16 Jan 2024 ICLR 2024 poster. AHMS ~141K PPG, 106K ECG, ~3 years; participant-level positive pairs, regularized contrastive (KoLeo), momentum. "first ... large-scale PPG/ECG via consumer wearables". URLs: https://machinelearning.apple.com/research/large-scale-training ; https://openreview.net/forum?id=pC3WJHf51j ; https://proceedings.iclr.cc/paper_files/paper/2024/hash/0d99a8c048befb6dd6e17d7684adacac-Abstract-Conference.html
- Subject-Aware Contrastive Learning for Biosignals. Cheng, Goh, Dogrusoz, Tuzel, Azemi. Apple page Aug 2021 (arXiv 2007.04871?). EEG/ECG, subject-specific contrastive. -> precursor
- Learning Insulin-Glucose Dynamics in the Wild. Miller, Foti, Fox. Aug 2020 (MLHC 2020). hybrid biomedical model + seq model -> world model precursor
- Modeling Heart Rate Response to Exercise with Wearable Data. Nazaret, Tonekaboni, Darnell, Ren, Sapiro, Miller. Dec 2022 NeurIPS TS4H workshop. -> world model
- Latent Temporal Flows (Oct 2022)
- Frequency-Aware MAE multimodal biosignals (bioFAME) Apr 2024 ICLR workshop
- Promoting Cross-Modal Representations ... Physiological Signals, Oct 2024 (PhysioNet2018, MAE)
- Wearable Accelerometer FMs via Knowledge Distillation. Abbaspourazad, Mishra, Futoma, Miller, Shapiro. Feb 2025 page. distill PPG->accel, 172K AHMS, 99.2% retrieval
- RelCon ICLR 2025 motion FM. 87,376 participants, 1B segments
- Beyond Sensor Data (WBM) ICML 2025, arXiv 2507.00191; Erturk, Kamran, Abbaspourazad... Futoma. 2.5B hours 162K, 27 HealthKit metrics, Mamba-2, 57 tasks; complementary with PPG FM
- Hypertension Notifications validation paper Sept 2025 PDF: step1 PPG feature extractor = DL via self-supervised on unlabeled AHMS; linear risk models; 30-day; FDA-cleared. (paper not explicitly cited)
- Speech FMs generalize to wearable TS (NeurIPS 2025 TS4H) ; LLMs for late multimodal sensor fusion (NeurIPS 2025 TS4H)
- CPEP (Oct 2025 NeurIPS BrainBody ws), EMBridge (Mar 2026)
- Device Passport ICML 2026 (July 2026) channel embedding cross-layout
- Emergent Symbolic Structure in Health FMs, ICML 2026 MechInterp ws, arXiv 2605.07407: independently trained FMs converge to common physiology representation
- MS-ECG-FM arXiv 2610.07662 (Oct 2026) Apple
- Apple Health app redesign, Apple Intelligence at core; Insights, For You, Longevity tab, Health Age; iOS 27.3 beta; newsroom 2026-11-03 (language expansion update)
- AI health coach: reports scaled back (9to5mac 2026-02-05) -> treat as reported only
## OPPO
- HiPPT arXiv 2610.14489 (2026-10-10) Southeast U / OPPO / SZTU / PKU; PPG-Text 4M recordings 202K users; multi-scope text alignment
- Smartwatch PPG Heart Age via ECG-guided cross-modal pretraining arXiv 2608.01620 (2026-08-03) PKU + OPPO Health Lab; 581,804 participants, 7.45M recordings, OPPO cohorts; PPG-only inference
- AnyPPG arXiv 2511.01747 PKU (KDD 2026) - academic, not OPPO
## Samsung
- HiMAE ICLR 2026 (Samsung Research page date 2026.01.26) on-watch sub-ms
- xMAE arXiv 2605.00973 ECG->PPG cross-modal MAE
- MMR wavelet PPG FM arXiv 2601.12215 (Samsung smartwatch data 17M segments 32K users)
- Samsung newsroom 2026-08-14 health foundation models article
## Google
- LSM ICLR 2025 (165K, 40M hours, minute-level features); LSM-2 AIM arXiv 2506.05321, blog 2025-07-22; SensorFM blog 2026-07-09 (5M people, 1T minutes, 34 features, grounding tool for PHA)
## Oura
- Women's health LLM in Advisor (blog) ; AHA 2025 "CVD detection with a large-scale foundation model" abstract; job ads "Large Physiology Models"
## Whoop
- Foundation AI team job posts (2026)
