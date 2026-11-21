---
title: "What a 32-token recall score hides"
short_title: "Hybrid Transformer Analysis — Associative Recall"
format: blog
byline: Yifan Jing
article_date: 2026-11-20
topic: Sequence models
featured_order: 1
visual:
  image: recall-archive-cover
  height: 600
  alt: "At the training length of 32 tokens, RoPE is ahead of Mamba. At 96 tokens, Mamba answers about half of the lookups and RoPE about one in six."
plots:
  models:
    id: recall-across-lengths
    stem: recall-archive-models
    height: 320
    compact_height: 290
    alt: "With 16 possible keys, RoPE starts ahead of Mamba at 32 tokens. Their curves cross in the low forties. At 96 tokens Mamba is near 48% and RoPE below 20%. The hybrid stays near 100%."
    caption: "Any of the 16 symbols can be the query. The answer comes one position after the earlier key. Each point uses 1,000 test strings at that length. All three models have embedding width 8."
  gap:
    id: fixed-key-delay
    stem: recall-archive-gap
    height: 270
    compact_height: 270
    alt: "Fixed-key accuracy at 96 tokens for gaps of one and five positions. Hybrid scores 95.7% and 100%, Mamba 100% and 100%, RoPE 15.5% and 40.9%, learned positions 6.9% and 15.4%, and no explicit positions 23.7% and 15.7%."
    caption: "At 96 tokens, with the same key on every string. A gap of five puts four other tokens between the earlier key and its answer. Each percentage is the fraction of 990 test strings answered correctly."
  width:
    id: mamba-width-and-delay
    stem: recall-archive-width
    height: 320
    compact_height: 290
    alt: "With 16 possible keys and an adjacent answer, Mamba of width 64 leads at 32 tokens, but falls to about 18% by length 96. Width 8 retains about 48%. At width 64 and a gap of ten, accuracy starts near 43% and ends near 7%."
    caption: "Three Mamba checkpoints with 16 possible keys. The embedding width is d. The gap counts positions from the earlier key to the answer. Each curve shows 1,000 test strings per length."
excerpt: "RoPE beats Mamba at 32 tokens. At 96, their ranking reverses. A second reversal appears when we widen Mamba on the same lookup task."
collection: portfolio
date: 2025-12-01
---
{% assign archive = 'https://github.com/Ivann1242/Analysis-AR-problem/blob/d148ad9d87f79df33ed64a0e22cd34d432dda44f' %}

At 32 tokens, a Transformer with rotary position embeddings (RoPE) answered about 98% of our lookups correctly. The state-space model Mamba got about 83%. If I’d had to choose between them, I would have picked the Transformer. Then we gave those same models 96 tokens. Mamba still answered nearly half the questions. RoPE was down to about one in six.

I studied associative recall with Samet Oymak at the University of Michigan in fall 2025. Try reading `P L K R P M L`. The final **L** asks what followed the earlier **L**. The answer is **K**. End the same prefix with **R** and the answer becomes **P**. Our generator planted one key–value pair per string. In the experiment below, any of the 16 symbols could be the query, and every training string was exactly 32 tokens long.

{% include recall-plot.html plot=page.plots.models %}

The line along the top belongs to a hybrid with one Mamba layer followed by one causal attention layer. It stayed close to perfect all the way to 96. To understand why that result surprised me, it helps to start with the version where we knew the question in advance. [Original three-model sweep]({{ archive }}/II_2.png)

## What if the question is always the same?

When every string ends in **L**, a reader can wait for the first **L**, remember the next token, and carry that single answer to the end. Moving the answer five positions past the key adds a counting step. The two-layer Mamba got all 990 length-96 questions right in both versions. [One-position sweep]({{ archive }}/I_2.png) · [Five-position sweep]({{ archive }}/I_4.png)

{% include recall-plot.html plot=page.plots.gap %}

A larger gap even *helped* the rotary Transformer in these runs. Its accuracy at 96 rose from 15.5% to 40.9%. The Transformer without explicit positions went the other way. Their training curves already looked different. RoPE learned the five-position lookup at length 32, while the model without explicit positions stayed below 20% near the end of training. [Training with a gap of one]({{ archive }}/I_1.png) · [Training with a gap of five]({{ archive }}/I_3.png)

The sharpest failure took just one token. With adjacent values and learned absolute positions, the Transformer scored **14.0% at length 31, 100% at 32, and 39.7% at 33**. Position 31 appeared in every training string. It was the *final answer* that the training loss always asked the model to predict at position 32. [Fixed-key notebook and scores]({{ archive }}/AR_I.ipynb)

## More possible questions, even on shorter strings

Once the key can vary, remembering the successor of one familiar symbol no longer solves the task. We trained separate models with 4, 8, or 16 possible keys. One result I nearly missed was on the *short* side of the plot. At length 16, RoPE scored about 72% with four possible keys and 91% with sixteen. Mamba went from nearly 100% to about 73% across those same two settings. [Training curves]({{ archive }}/II_1.png) · [All three key-set sizes]({{ archive }}/II_2.png)

At 96 tokens, all three RoPE runs were below 25%. Mamba still answered roughly three quarters of the four-key questions and half of the sixteen-key questions. The hybrid stayed near 100% across all three sets. Its attention layer can revisit earlier representations after the final question arrives. That makes it a plausible way to handle an unknown key, though these accuracy curves leave open which features it used.

## A wider Mamba loses its lead

If eight dimensions were too few to keep track of sixteen possible keys, widening Mamba ought to help. At the training length, it did. With adjacent values, increasing the embedding width from 8 to 64 brought recall from about 83% to almost 100%. The two curves cross in the mid-forties. By 96 tokens, the wider model was around 18% and the narrower one around 48%. With just four possible keys, both widths finished near 75%. [Original width comparison]({{ archive }}/II_3.png)

{% include recall-plot.html plot=page.plots.width %}

The bottom curve tells a different story. With ten positions from key to value, wide Mamba reached only about 43% **at its own training length**. By 96 it was near 7%, close to the 6.25% accuracy of a uniform guess. The adjacent-value model had learned a lookup that weakened as the string grew. The ten-position model was already struggling before we added any tokens. That last run tested Mamba alone. How well the hybrid handles a delayed answer when any symbol can be the key remains open here. [Ten-position Mamba sweep]({{ archive }}/II_4.png)

The fixed-key notebook logged numerical scores. The variable-key notebook saved its length sweeps as plots, so its percentages here are approximate. I overlaid the original plotted lines on common axes. Each setting used a separately trained checkpoint, with training budgets that varied across runs. [Study README]({{ archive }}/README.md) · [Variable-key notebook]({{ archive }}/AR_II.ipynb) · [Figure source]({{ '/files/recall/archive_figures.py' | relative_url }})
