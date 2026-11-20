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
  source_label: "Original experiment figure"
excerpt: "Mamba could remember what followed a known key at three times its training length. What happened when any of 16 tokens could be the key?"
collection: portfolio
date: 2025-12-01
---

Read `D A B C E A`. The final `A` asks what came immediately after the earlier `A`. The answer is `B`. Change just the last token to `C` and the answer becomes `E`. If you had to read those first five tokens before you knew the question, what would you remember?

I studied this question with Samet Oymak at the University of Michigan in fall 2025. We trained small sequence models on 32-token examples drawn from a vocabulary of 16 tokens, then tested them on sequences up to 96 tokens long.

## When the key is known in advance

In the first experiment, every sequence ended with the same key. A reader could wait for the first `A`, save the next token, and carry it to the end. Another sixty tokens of filler would make the wait longer, but the reader would still need to remember only one value.

Mamba processes the sequence from left to right, updating a recurrent state at each step. At length 96 it answered **all 990 test examples correctly**. The hybrid, which passes the output of a Mamba layer to a causal attention layer, scored about 96%. A Transformer with rotary positional embeddings (RoPE) scored about 15%. [Fixed-key experiment notebook](https://github.com/Ivann1242/Analysis-AR-problem/blob/d148ad9d87f79df33ed64a0e22cd34d432dda44f/AR_I.ipynb)

## Which key will come last?

In the second experiment we chose the key afresh for each sequence. We trained separate models with 4, 8, or 16 possible keys. Each example still asked just one question. Now, on reaching `E` in our opening example, a reader has a reason to keep both associations, `A → B` and `C → E`. The final token decides which one matters.

{% include project-figure.html visual=page.visual %}

Look at the right edge of each panel, where the sequences are three times as long as those seen in training. Mamba answered about three quarters of the queries correctly with four possible keys and about half with sixteen. The RoPE Transformer scored below 25% in all three runs. The hybrid stayed near 100% for all three. These models used the same embedding width of eight, though their training budgets varied. [Variable-key experiment notebook](https://github.com/Ivann1242/Analysis-AR-problem/blob/d148ad9d87f79df33ed64a0e22cd34d432dda44f/AR_II.ipynb)

## What does the attention layer read?

At the final token, the hybrid’s attention layer can look back at the state Mamba produced at each earlier position. That gives us a specific question for `D A B C E A`. Does the last `A` look back at the state at `B` because it still carries a trace of the preceding `A`? One way to test that idea would be to block attention to the `B` position and measure how often the answer changes compared with blocking an unrelated position.
