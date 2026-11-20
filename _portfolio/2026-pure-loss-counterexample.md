---
title: "Disproving a second-order converse conjecture for pure-loss channels"
format: blog
byline: Yifan Jing
article_date: 2026-11-19
topic: Quantum information
featured_order: 3
visual:
  image: pure-loss
  height: 648
  control: "Transmissivity"
  alt: "Seventeen blue curves show how far the fixed-photon code exceeds the proposed second-order bound. Each curve reaches zero at error probability 0.5. At 50% transmissivity and 10% error, the coefficient gap is +0.74."
  caption: "Each blue curve holds the transmission level fixed and shows how the coefficient gap changes with decoding error, at one photon per mode. The red point marks 10% error on the selected curve."
  source: https://qiqc-op.com/problem/op_89fb664ba06ba5de/
  source_label: "Equations (4) and (5)"
excerpt: "Yue Tu and I determined the exact second-order term under a photon-number cutoff. Our fixed-photon codes beat the conjectured bound at every fixed error probability between zero and one half."
collection: portfolio
permalink: /portfolio/2026-pure-loss-counterexample/
date: 2026-09-23
---

Suppose half the light you send through a fiber reaches the receiver. You have *n* photons for *n* uses of the fiber. How many different messages can the receiver distinguish with 90% success?

The conjecture would subtract about 1.76√n bits from the leading capacity term. Yue Tu and I showed that the optimal second-order penalty is about 1.02√n bits in this example. We achieve it by putting exactly the same number of photons into every message. At the initial setting, the red point marks the 0.74 gap between the two coefficients.

{% include project-figure.html visual=page.visual %}

## Where did the bound come from?

In 2014, Mark Wilde, Joseph Renes, and Saikat Guha studied a Gaussian ensemble of coherent optical states with a budget on the mean photon number. For *M* possible messages, the bit count is log₂ *M*. Their code achieves *n* times capacity to leading order. Its √n correction reflects the photon-number fluctuations of thermal light. Could the same expression serve as a *converse*, an upper bound that every code must obey? [Original paper](https://arxiv.org/abs/1408.5328)

The QIQCOP Zoo posed a precise version with a photon-number cutoff. For a randomly chosen message, the probability that the input exceeds the cutoff must fall at least exponentially fast as *n* grows. Our code uses exactly the allowed photon count in every codeword, so that probability is zero. [Conjecture, equations (2)–(4)](https://qiqc-op.com/problem/op_89fb664ba06ba5de/)

## Put the message in the mode

We encode each message in a different collective optical mode, a pattern of amplitudes and phases spread across all *n* uses of the fiber. All the photons in a codeword occupy its chosen mode. If 47 survive the trip, those 47 still occupy that mode. The count itself has the same distribution for every message. The receiver counts the survivors, then distinguishes the possible patterns within that photon-number sector.

Now take 100 uses of the fiber at one photon per use. Our transmitter sends exactly 100 photons. The arrival count is binomial, with mean 50 and variance 25. The Gaussian ensemble behind the conjecture also delivers 50 photons on average. Its arrival count has variance 75. Fixing the input count leaves only the randomness of which photons survive the trip.

## How photon fluctuations turn into bits

Write η for the fraction of light transmitted and *x* for the mean number of photons received per mode. The variance that sets the √n correction in bits is called the *dispersion*. Under the cutoff, it equals the thermal dispersion multiplied by **(1 − η)/(1 + x)**. In our example η and *x* are both one half, so the factor is one third. At 10% error, the square root of the dispersion is multiplied by the tenth percentile of a standard normal, about −1.28. A smaller dispersion takes fewer bits away. At 50% error the multiplier vanishes and all the curves meet.

At one million uses, keep the same 10% error budget and set the allowed input leakage to 2⁻ⁿ. Our finite-block bounds put the optimal bit count between **1,376,404 and 1,376,443 bits**. The first two terms of the conjecture give about **1,375,685 bits**. A logarithmic correction could absorb the difference at this one block length. The proof rules out every such correction because the gap grows as √n. [Finite-block bounds, equations (5) and (13)](https://github.com/Naixu-Guo/quantum-open-problems/blob/main/database/proofs/pure-loss-second-order.md)

## How close can any code get?

In the manuscript, we combine the dimension of the low-photon output space with the probability of landing outside it. This gives an upper bound for any encoding, including a superposition of different photon counts. It matches our construction through the √n term for every fixed error probability strictly between zero and one. The remainder is O(log n) bits even when the allowed probability of exceeding the input cutoff is as large as a constant times 1/√n.

In Lean 4 we verified the disproof for every transmissivity strictly between zero and one, every positive photon budget per mode, and every fixed error probability between zero and one half. The formal proof constructs codes with zero input leakage. Those codes already satisfy the Zoo’s cutoff and beat the proposed bound. [Lean 4 theorem](https://github.com/Ivann1242/pure-loss-second-order-lean/blob/86d3b5607d19c9de9d4c1698bd9e3c63d247856d/QIQCOP/MainGeneral.lean#L74)

We submitted the proof on September 23, 2026. The next day, Naixu Guo merged it into the QIQCOP Zoo and marked the problem solved. [Zoo submission](https://github.com/Naixu-Guo/quantum-open-problems/pull/99)
