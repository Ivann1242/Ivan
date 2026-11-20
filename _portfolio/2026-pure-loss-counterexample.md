---
title: "Disproving a second-order converse conjecture for pure-loss channels"
format: blog
byline: Yifan Jing
article_date: 2026-11-19
topic: Quantum information
featured: true
visual:
  image: pure-loss
  height: 648
  control: "Transmissivity"
  alt: "Seventeen blue curves show how far the fixed-photon code exceeds the proposed second-order bound. Each curve reaches zero at error probability 0.5. At 50% transmissivity and 10% error, the coefficient gap is +0.74."
  caption: "Each blue curve holds the transmission level fixed and shows how the coefficient gap changes with decoding error, at one photon per mode. The red point marks 10% error on the selected curve."
  source: https://qiqc-op.com/problem/op_89fb664ba06ba5de/
  source_label: "Equations (4) and (5)"
excerpt: "Yue Tu and I showed that a code with a fixed photon count can transmit more classical information than the proposed bound allows. We verified the disproof in Lean 4."
collection: portfolio
permalink: /portfolio/2026-pure-loss-counterexample/
date: 2026-09-23
---

Suppose half the light you send through a fiber reaches the receiver. You have *n* photons for *n* uses of the fiber. How many different messages can the receiver distinguish with 90% success?

Yue Tu and I built a code that beats the conjectured limit. At this setting the conjecture subtracts about 1.76√n bits from the capacity term. Our code gives up only 1.02√n bits at the same order. The red point marks the 0.74 gap between the two coefficients.

{% include project-figure.html visual=page.visual %}

## Where did the bound come from?

In 2014, Mark Wilde, Joseph Renes, and Saikat Guha analyzed a code for sending classical messages through a pure-loss bosonic channel. A choice among *M* messages carries log₂ *M* bits. Capacity determines the leading term in that bit count, proportional to *n*. Their calculation also gave a correction of order √n for a finite block. They asked whether the same expression could serve as a *converse*, an upper bound that every code must obey. [Original paper](https://arxiv.org/abs/1408.5328)

The version in the QIQCOP Zoo made the photon budget precise. It requires the probability of exceeding the budget to fall at least exponentially fast as *n* grows. Our code has zero probability of exceeding it because every message uses exactly the allowed number of photons. [Conjecture, equations (2)–(4)](https://qiqc-op.com/problem/op_89fb664ba06ba5de/)

## Put the message in the mode

With the photon count fixed, we still get to choose the optical mode the photons occupy. Think of a mode as a pattern spread across the *n* uses of the fiber. We choose a different pattern for each message and put all its photons into that pattern.

If we send 100 photons through the half-transmitting fiber, the number that arrive follows a binomial distribution centered on 50. If 47 arrive, all 47 still occupy the mode we chose. The receiver counts the survivors, then uses a measurement designed for that count to distinguish the possible patterns.

## Why the gap grows with block length

The variance that controls the √n correction is called the *dispersion*. In our half-transmitting example, the fixed-photon code has one third of the dispersion used in the conjecture. At 10% error, the correction multiplies the square root of that dispersion by the tenth percentile of a standard normal, about −1.28. A smaller dispersion takes fewer bits away. That accounts for the 0.74√n-bit gain in the opening example.

The same sign argument works for every fixed error probability between zero and one half, every positive photon budget per mode, and every transmissivity strictly between zero and one. As the block grows, the √n gain eventually outgrows the logarithmic remainder allowed by the conjecture.

We verified the disproof in Lean 4 using the standard Fock-basis model of pure loss. In our written proof we also derive a matching upper bound, which pins down the dispersion with an O(log n) remainder in the bit count. [Lean 4 theorem](https://github.com/Ivann1242/pure-loss-second-order-lean/blob/af47f65fba5bd3c81d5e8f0bec45c8ce331e1d83/QIQCOP/MainGeneral.lean#L74) · [Full proof note](https://github.com/Naixu-Guo/quantum-open-problems/blob/main/database/proofs/pure-loss-second-order.md)

We submitted the proof on September 23, 2026. The next day, Naixu Guo merged it into the QIQCOP Zoo and marked the problem solved. [Zoo submission](https://github.com/Naixu-Guo/quantum-open-problems/pull/99)
