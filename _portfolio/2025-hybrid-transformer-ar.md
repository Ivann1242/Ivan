---
title: "Hybrid Transformer Analysis — Associative Recall"
topic: Sequence models
visual:
  image: recall
  alt: "The Mamba experiment shows three recall-accuracy curves falling at different rates beyond the training length of 32."
  detail_image: recall-results
  detail_height: 291
  detail_alt: "Three original plots compare recall accuracy as context length grows for a Transformer with RoPE, Mamba and a hybrid model. The hybrid curves stay near one across the tested lengths."
  caption: "Trained at a context length of 32, each model was evaluated on longer sequences with three memory sizes. The hybrid model retained high recall accuracy across this experiment."
  source: https://github.com/Ivann1242/Analysis-AR-problem/blob/d148ad9d87f79df33ed64a0e22cd34d432dda44f/II_2.png
  source_label: "Original experiment figure"
excerpt: "Comparing Transformer, Mamba, and hybrid architectures on the Associative Recall generalization problem."
collection: portfolio
date: 2025-12-01
---

Research with Dr. Samet Oymak at the University of Michigan (Sep 2025 – Dec 2025).

**Highlights:**
* Studied generalization behavior of sequence models through the Associative Recall (AR) task.
* Proposed and evaluated hybrid architectures combining state-space models with attention mechanisms.
* Demonstrated improved long-range generalization; designed controlled experiments on convergence dynamics.

**Links:** [GitHub Repository](https://github.com/Ivann1242/Analysis-AR-problem)
