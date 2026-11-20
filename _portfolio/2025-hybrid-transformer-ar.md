---
title: "Hybrid Transformer Analysis — Associative Recall"
format: blog
byline: Yifan Jing
article_date: 2026-11-20
topic: Sequence models
visual:
  image: recall
  alt: "Mamba’s recall accuracy at 96 tokens falls from about three quarters with four possible keys to about one half with sixteen."
  detail_image: recall-results
  detail_height: 291
  detail_alt: "Three panels plot recall accuracy against sequence length. Beyond 32 tokens, accuracy falls for the rotary Transformer and for Mamba. The hybrid stays near 100% through 96 tokens for all three sets of possible keys."
  caption: "Each point measures accuracy on 1,000 sequences. The dotted line marks the training length of 32 tokens. The colors show how many different tokens could be the final key across examples (M = 4, 8, or 16)."
  source: https://github.com/Ivann1242/Analysis-AR-problem/blob/d148ad9d87f79df33ed64a0e22cd34d432dda44f/II_2.png
  source_label: "Open the full-resolution figure"
plots:
  positions:
    id: position-sweep
    stem: recall-positions
    height: 325
    compact_height: 300
    alt: "With a fixed query and adjacent answer, learned positional embeddings jump from 14% accuracy at length 31 to 100% at 32 and fall to 40% at 33. Rotary embeddings change more gradually. The model without explicit positions stays below 50% near length 32."
    caption: "Three two-layer Transformers trained on 32-token sequences. Each point is the fraction correct on 990 test examples at that length. The dotted vertical line marks the training length. The orange dot is the learned-position model’s perfect score there."
  readout:
    id: readout-probe
    stem: recall-readout
    height: 290
    compact_height: 285
    alt: "At length 96, the hybrid answers 1,023 out of 1,024 correctly with all positions visible or the earlier key blocked, 70 with the value blocked, and 1,024 with a distractor blocked."
    caption: "Four reads of the same 1,024 examples at length 96, using the 16-key hybrid. Whiskers are 95% Wilson intervals for each accuracy. The dashed line is the 6.25% accuracy expected from a uniform guess among 16 tokens."
excerpt: "A hybrid trained on 32 tokens answered 1,023 of 1,024 lookups at length 96. Blocking its final attention read at one earlier position reduced that to 70. Explore where it looked."
collection: portfolio
date: 2025-12-01
---

A Transformer trained to answer a lookup question on 32 tokens got all 990 test questions right at that length. On 31-token examples it got just 139 right. What had it learned that worked so well at exactly 32?

In fall 2025 I studied associative recall with Samet Oymak at the University of Michigan. The task fits in one line. Read `D A B C E A`. The last `A` asks what came immediately after the earlier `A`, so the answer is `B`. Change the last token to `C` and the answer becomes `E`. The prefix stays the same. A model has to decide what to keep before it knows which question it will get.

Here is an actual read from our trained hybrid, a Mamba layer followed by a causal attention layer. Switch the final query between `A` and `C` and watch where the attention goes. Then block the value position and see which token the model predicts instead.

{% include recall-demo.html %}

## Why did one fewer token hurt?

In the first experiment every sequence ended with the same key. The vocabulary had 16 tokens, the embedding width was eight, and the model received a loss only on its final answer. A reader could solve this version by waiting for one familiar symbol and holding on to its successor.

{% include recall-plot.html plot=page.plots.positions %}

The orange point explains the opening puzzle. The Transformer with learned absolute positions scored **14.0%, 100%, and 39.7%** at lengths 31, 32, and 33. It had seen position 31 during training on every sequence. It had only ever answered the question at position 32. The dip on the *shorter* side is what makes simple lack of exposure to longer positions an incomplete explanation. Rotary positional embeddings (RoPE) produced a smoother curve around 32, although their accuracy eventually fell to 15.5% at 96. Mamba got all 990 right there. [Fixed-key experiment and all five models](https://github.com/Ivann1242/Analysis-AR-problem/blob/d148ad9d87f79df33ed64a0e22cd34d432dda44f/AR_I.ipynb)

The order in which the models learned also depended on the task. With the value one position after the key, Mamba first reached 90% validation accuracy at epoch 27, the hybrid at 54, RoPE at 58, and learned positions at 167. The model without explicit positions stayed below 90% through epoch 250. With the value five positions after the key, RoPE overtook Mamba, crossing 90% at epoch 24 to Mamba’s 28. Yet at length 96 in that five-position sweep, RoPE answered 40.9% correctly and Mamba answered all 990. [Saved training histories]({{ '/files/recall/training.csv' | relative_url }}) · [Five-position length sweep](https://github.com/Ivann1242/Analysis-AR-problem/blob/d148ad9d87f79df33ed64a0e22cd34d432dda44f/I_4.png)

## What if the reader doesn’t know the key yet?

Next we chose a key separately for each example, planted it and its value in the prefix, and repeated the key at the end. We trained separate checkpoints with 4, 8, or 16 eligible keys. That number counts which symbols *could* be asked about across examples. Each sequence still has one planted association and one scored answer. This is a narrower question than the multi-query associative recall task studied in *Zoology*. [Variable-key notebook](https://github.com/Ivann1242/Analysis-AR-problem/blob/d148ad9d87f79df33ed64a0e22cd34d432dda44f/AR_II.ipynb) · [Zoology](https://arxiv.org/abs/2312.04927)

At length 96, Mamba’s accuracy in a fresh checkpoint evaluation went from **72.7%** with four possible keys to **54.9%** with eight and **50.7%** with sixteen. With sixteen keys, RoPE scored 16.4% and the hybrid scored 99.9%. A recurrent model can carry one known answer a long way. Asking for an association whose identity arrives at the end changes what the model needs to retain.

<details class="recall-archive">
  <summary>See the original length sweeps for all nine models</summary>
  {% include project-figure.html visual=page.visual %}
</details>

## Does widening Mamba help it remember?

We increased Mamba’s embedding width from 8 to 64 and kept all 16 keys eligible. The table shows a replay of the saved checkpoints on 1,024 fresh examples per column and condition. The two width settings at offset one saw identical test sequences.

{% include recall-width.html %}

At the training length, the wider run answered **157 more questions** correctly. At length 96 it answered **341 fewer**. A larger model fit the training-length task better and still lost more as the sequence grew. Training budgets differed across these checkpoints, so the crossover is an observation about the saved runs. It also shows why embedding width alone is a poor proxy for how many associations a model can retrieve.

The last row changes a different distance. An offset of ten puts the value ten positions after the key, wherever the pair appears in the sequence. This wide checkpoint answered only 477 of 1,024 questions even at length 32. Some of its difficulty was already present before we asked it to read a longer sequence. [Original width experiment](https://github.com/Ivann1242/Analysis-AR-problem/blob/d148ad9d87f79df33ed64a0e22cd34d432dda44f/II_3.png) · [Ten-position offset](https://github.com/Ivann1242/Analysis-AR-problem/blob/d148ad9d87f79df33ed64a0e22cd34d432dda44f/II_4.png)

## Which earlier position does the hybrid need?

The hybrid gives us a place to intervene. Mamba reads the prefix from left to right. Its output at `B` has already seen the preceding `A`. The attention layer can later revisit that output. For this post I tested which position the final attention read actually depends on. I kept every input and every Mamba output fixed, removed one position from the final attention scores, and renormalized the remaining weights.

{% include recall-plot.html plot=page.plots.readout %}

On the 96-token examples, the largest attention weight landed on the planted **value** 994 times out of 1,024. The intervention tells us more than the weight alone. Blocking the earlier **key** left every prediction unchanged. Blocking a random unrelated prefix position left 1,024 correct. Blocking the **value** took accuracy from **1,023 correct to 70**, close to uniform guessing. At the training length the same intervention took the hybrid from 1,024 correct to 59. [Paired predictions for all nine hybrid test conditions]({{ '/files/recall/paired-predictions.csv.gz' | relative_url }})

In the opening example, the final `A` can read from `B`, one position *after* its earlier match. Blocking the earlier `A` at the final layer still lets Mamba use it while forming the state at `B`. The experiment locates a necessary read for most of these predictions. How Mamba makes that state recognizable to the final query is the question I’d test next.

## Replaying the experiments

The fixed-key curves come from the saved notebook outputs. The replay uses 11 variable-key checkpoints at lengths 32, 64, and 96, with seed 202511. Within each task setting, all architectures see the same inputs and all masks reuse the same examples. Each configuration represents one training run. The results file records the checkpoint hashes, completed epochs, software versions, and raw correct counts. The evaluation script accepts weights produced by the original notebook and checks its unmasked readout against the model’s own forward pass. [Training notebooks](https://github.com/Ivann1242/Analysis-AR-problem/tree/d148ad9d87f79df33ed64a0e22cd34d432dda44f) · [Evaluation code]({{ '/files/recall/evaluate.py' | relative_url }}) · [Results and example attention weights]({{ '/files/recall/results.json' | relative_url }}) · [Plotting code]({{ '/files/recall/figures.py' | relative_url }})

To replay the measurements with your own copy of the checkpoints, keep their notebook filenames in a directory called `weights`. With PyTorch, NumPy, and einops installed, run `python evaluate.py --notebook AR_II.ipynb --checkpoints weights --out replay`.
