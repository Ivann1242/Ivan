---
title: "AI-Assisted Discovery — Pure-Loss Converse Counterexample"
short_title: "A counterexample in quantum communication"
topic: Quantum information
featured: true
visual:
  image: pure-loss
  height: 648
  control: "Transmissivity"
  alt: "Seventeen blue curves show how far the fixed-photon code exceeds the proposed second-order bound. Each curve reaches zero at error probability 0.5. At 50% transmissivity and 10% error, the coefficient gap is +0.74."
  caption: "Each curve fixes a transmissivity and shows the gap between the two √n coefficients at one photon per mode. At 10% error and 50% transmissivity, the fixed-photon code’s coefficient exceeds the proposed bound’s by 0.74."
  source: https://qiqc-op.com/problem/op_89fb664ba06ba5de/
  source_label: "Equations (4) and (5)"
excerpt: "Yue Tu and I worked with six AI agents to disprove a [candidate pure-loss converse](https://qiqc-op.com/problem/op_89fb664ba06ba5de/) arising from a 2014 question. We verified the counterexamples in Lean 4."
collection: portfolio
permalink: /portfolio/2026-pure-loss-counterexample/
date: 2026-09-23
---

On **September 23, 2026**, working with **Yue Tu** and **six parallel AI agents**, I constructed a **general family of counterexamples** to the **candidate pure-loss second-order converse** in quantum communication.

Following review by QIQCOP Zoo maintainer **[Naixu Guo](https://github.com/Naixu-Guo/quantum-open-problems/pull/99)**, our solution was **included in [QIQCOP Zoo](https://qiqc-op.com/problem/op_89fb664ba06ba5de/)** on **September 24, 2026**. The entry credits the result to **Yue Tu and Yifan Jing** and marks the problem as **Solved**.

The candidate is a precise formulation arising from an open question raised by **Mark M. Wilde, Joseph M. Renes, and Saikat Guha in 2014**, **12 years** before this result.

**Highlights:**
* Developed a general counterexample construction, rather than a single numerical instance.
* Disproved the candidate upper bound under its stated exponential photon-number-tail condition.
* Verified the disproof in **Lean 4**; the counterexample uses fixed-photon condensate codes satisfying the photon-number constraint with zero leakage.

This project forms part of my research on **AI scientist systems**: coordinating parallel agents to explore mathematical ideas and turn promising constructions into verifiable results.

**Links:** [Problem statement, solution, and attribution](https://qiqc-op.com/problem/op_89fb664ba06ba5de/) · [Lean 4 proof](https://github.com/Ivann1242/pure-loss-second-order-lean) · [Original 2014 paper](https://arxiv.org/abs/1408.5328)
