---
title: "How sequence models learn associative recall"
short_title: "Hybrid Transformer Analysis — Associative Recall"
format: blog
byline: Yifan Jing
article_date: 2025-12-22
topic: Sequence models
featured_order: 1
visual:
  image: recall-study-cover
  height: 600
  alt: "The final A points back to an earlier A. B is one step after that A, and C is five steps after it."
excerpt: "What changes when a model knows the key in advance, must wait for the question, or has to remember across a longer gap? A study of Mamba, attention, and their hybrid."
study_archive: https://github.com/Ivann1242/Analysis-AR-problem/blob/d148ad9d87f79df33ed64a0e22cd34d432dda44f
plots:
  task:
    number: 1
    id: recall-task
    stem: task
    title: "One string, two distances"
    alt: "Read A B D E F C G A. The final A asks about the earlier A. At a gap of one the answer is B, and at a gap of five it is C."
    caption: "The final symbol names the key. The gap counts forward from its earlier occurrence to the value. Extra tokens may still arrive between that value and the question."
  learning:
    number: 2
    id: learning-the-fixed-key
    stem: learning
    title: "Who learns the fixed key first?"
    alt: "First completed epoch reaching 90% for gaps of one and five. Mamba 27 and 28, hybrid 54 and 39, RoPE 58 and 24, learned absolute positions 167 and 135. Without positions neither run reached 90%."
    caption: "Each marker is the first completed epoch with at least 90% validation accuracy at length 32. Moving the value changes which model crosses first."
    sources: [["Gap 1 history", "I_1.png"], ["Gap 5 history", "I_3.png"]]
  positions:
    number: 3
    id: fixed-key-delay
    stem: positions
    title: "A position can look like a rule"
    alt: "Fixed-key accuracy in percent. With gap one, learned absolute positions score 14.0, 100, and 39.7 at lengths 31, 32, and 33. At length 96, increasing the gap from one to five moves RoPE from 15.5 to 40.9. Mamba stays at 100."
    caption: "Each cell gives the percentage correct on 990 strings. The column labels are test lengths. Only length 32 appeared in training. Absolute and No positions are the other two Transformer variants."
    sources: [["Gap 1 sweep", "I_2.png"], ["Gap 5 sweep", "I_4.png"]]
  variable_training:
    number: 4
    id: fitting-variable-keys
    stem: variable-training
    title: "Fitting sixteen possible keys"
    alt: "With 16 possible keys at length 32, hybrid ends near 100% at epoch 300, RoPE near 98% at 400, and Mamba near 83% at 1,030. Each line ends with its saved training run."
    caption: "Each line ends at the last recorded epoch for that model. Accuracy was measured on held-out strings of the same length used for training."
    sources: [["Histories for all key sets", "II_1.png"]]
  keys:
    number: 5
    id: query-diversity
    stem: keys
    title: "Short and long recall in one view"
    alt: "Points compare accuracy on 16- and 96-token strings. From four to sixteen possible keys, Mamba moves from about 100/76 to 73/48 percent, while RoPE moves from 72/19 to 91/18. The hybrid runs overlap near 100/100."
    caption: "Read right for higher accuracy at 16 tokens and up for higher accuracy at 96. Numbers beside the points count possible keys. The three hybrid runs overlap near the upper right."
    sources: [["Original length sweeps", "II_2.png"]]
  hybrid:
    number: 6
    id: recall-across-lengths
    stem: hybrid
    title: "Following the same models to 96"
    alt: "With 16 possible keys and an adjacent value, hybrid stays near the ceiling from 16 to 96 tokens. RoPE leads Mamba at the training length, then falls below it as the strings lengthen."
    caption: "The dotted line marks the 32-token training length. Each point in the original sweep used 1,000 test strings. All three models have embedding width 8."
    sources: [["Three-model comparison", "II_2.png"]]
  width:
    number: 7
    id: mamba-at-two-widths
    stem: width
    title: "Who benefits from a wider Mamba?"
    alt: "Change in recall when widening Mamba from 8 to 64. With four keys the change is about one point or less at either length. With eight keys the wider run gains 17 points at length 16 and loses 19 at 96. With sixteen keys it loses about 15 and 30 points."
    caption: "Each bar subtracts width-8 accuracy from width-64 accuracy at the same test length. Right of zero favors the wider run. Differences are approximate percentage points."
    sources: [["Width 8", "II_2.png"], ["Width 64", "II_3.png"]]
  delay:
    number: 8
    id: mamba-width-and-delay
    stem: delay
    title: "A longer gap changes the learning problem"
    alt: "At width 64 with 16 possible keys, the gap-one run is near 100% at length 32. The gap-ten run peaks near 43% there and approaches the 6.25% guessing rate at 96."
    caption: "The horizontal dashed line is uniform guessing among 16 values. The curves begin at 25 tokens, where both traces are visible in the original figures."
    sources: [["One-step gap", "II_3.png"], ["Ten-step gap", "II_4.png"]]
collection: portfolio
date: 2025-12-01
---

If I tell you in advance that I’ll ask what followed the first **A**, you can ignore most of a string. If I wait until the last token to name the letter, you have to decide what to keep before you know what I want. Both are associative recall. They put quite different demands on a model’s memory.

I studied these two versions with Samet Oymak at the University of Michigan in fall 2025. We trained small Transformers, Mamba models, and a hybrid on strings of exactly 32 tokens, drawn from a vocabulary of 16. We varied which symbols could be the key, how far its value lay from it, and how long the model had to wait for the final question.

<nav class="recall-contents" aria-label="In this article"><a href="#fixed-key">Fixed key</a><a href="#variable-keys">Variable keys</a><a href="#hybrid-recall">The hybrid</a><a href="#width-and-delay">Width and delay</a></nav>

{% include recall-plot.html plot=page.plots.task eager=true %}

## When the key is known in advance
{: #fixed-key}

In the first notebook, every string ended with the same key. A reader moving left to right could wait for it, count one or five positions, and hold the value until the end. We compared five two-layer models. Three used causal attention, with learned absolute positions, rotary position embeddings (RoPE), or no explicit positional encoding. The other two used Mamba alone or one Mamba layer followed by attention.

With adjacent values, Mamba reached 90% validation accuracy after 27 epochs. The hybrid took 54, RoPE 58, and learned absolute positions 167. Separating the key and value by five steps barely moved Mamba’s crossing, to epoch 28. RoPE crossed at epoch 24 and the hybrid at 39. The model without explicit positions finished around 48% on the one-step task and 18% on the five-step task.

{% include recall-plot.html plot=page.plots.learning %}

The learned-position Transformer eventually answered all 990 adjacent-value questions correctly at length 32. On 31-token strings it scored **14.0%**. At length 33 it scored **39.7%**. Position 31 had appeared in every training string, but only position 32 had been asked to produce the answer. Across both sweeps, 32 was the only length at which this Transformer got every question right.

{% include recall-plot.html plot=page.plots.positions %}

Mamba got every question right at **all 93 tested lengths** with adjacent values (4–96 tokens) and **all 88** with a five-step gap (9–96). The hybrid finished at 95.7% and 100% at length 96. A larger gap even improved RoPE’s score there, from 15.5% to 40.9%, while the Transformer without explicit positions moved the other way, from 23.7% to 15.7%. Each gap had its own trained models.

## When the last token chooses the question
{: #variable-keys}

In the second notebook we let 4, 8, or all 16 symbols serve as the final query. Each string still contained **one planted key–value pair and one scored answer**. What changed was the set of questions the next string could ask. We put the value immediately after the key and kept embedding width at 8.

Mamba’s four-key run reached nearly perfect validation accuracy within its 300 recorded epochs. With eight keys it approached that level over 1,000 epochs. With sixteen it was still near 83% after 1,030. RoPE reached the ceiling sooner with four or eight keys and finished near 98% with sixteen. The hybrid also learned fastest with four keys, but all three hybrid runs ended near 100%. Some of Mamba’s difficulty was already visible before we lengthened a single string.

{% include recall-plot.html plot=page.plots.variable_training %}

Cutting the test length in half gave us a comparison I hadn’t expected. At 16 tokens, RoPE went from about 72% with four possible keys to 91% with sixteen. Mamba went from nearly 100% to 73% across the same settings. At 96 tokens, RoPE’s three runs were all below 25%. Mamba retained about 76%, 58%, and 48% as the set grew from four keys to eight and then sixteen.

{% include recall-plot.html plot=page.plots.keys %}

## What changes when attention follows Mamba?
{: #hybrid-recall}

Consider the sixteen-key case across the full stretch from 16 to 96 tokens. At length 32, RoPE led Mamba by roughly 15 percentage points. Their curves crossed in the low forties. By 96, Mamba was near 48% and RoPE near 18%. The hybrid stayed close to 100% throughout. Its four- and eight-key runs held up over the same range.

{% include recall-plot.html plot=page.plots.hybrid %}

The order of the hybrid’s layers suggests a reason. By the time its recurrent layer processes a value, it has seen the preceding key. The attention layer can revisit that earlier representation once the final query arrives. The experiments establish that this arrangement handled varying keys and lengths together. Accuracy alone leaves open which representation it actually retrieved.

## How width and delay change the result
{: #width-and-delay}

An obvious explanation for Mamba’s sixteen-key result is that width 8 gave it too little room. We widened the embedding to 64 and trained with each of the three key sets. At the training length, the sixteen-key run went from about 83% to almost 100%. But at 16 tokens it fell from about 73% to 58%, and at 96 from 48% to 18%. The wider model’s advantage was concentrated around the length it had practiced.

{% include recall-plot.html plot=page.plots.width %}

Eight possible keys tell a subtler story. Widening **gained about 17 percentage points at length 16 and lost about 19 at length 96**. With just four keys, changing the width barely moved either score. A single width threshold would miss both the dependence on the question set and the change in direction with length.

Finally, we kept width 64 and sixteen possible keys, and moved the value **ten positions** past the key. Accuracy peaked near 43% even at the 32-token training length. It fell to about 7% at length 96, close to guessing one of sixteen values. The adjacent-value run had learned a lookup that weakened on longer strings. In the ten-step run, learning the lookup was already the bottleneck.

{% include recall-plot.html plot=page.plots.delay %}

What I took away is that the timing of the question matters as much as the length of the string. Mamba could return a known key’s value in 96-token strings. A rotary Transformer learned to choose among many keys at length 32. The hybrid combined those abilities when key and value were adjacent. Whether it can also bridge a long key-to-value gap with an unknown query is the comparison this study leaves open. Only wide Mamba ran the sixteen-key, ten-step condition.

### Reading the figures

The fixed-key percentages come from the 990-example test logs. The learning milestones count completed epochs in the saved validation histories. For variable keys, the notebook saved its length sweeps as plots, with 1,000 examples per condition and length. The lines here reproduce the archived traces, and point and bar values read from them are approximate. Each sweep kept the same checkpoint across lengths, with the pair planted at varying positions. Changes in architecture, key set, gap, or width compare separate training runs whose budgets varied. [Study README]({{ page.study_archive }}/README.md) · [Fixed-key notebook]({{ page.study_archive }}/AR_I.ipynb) · [Variable-key notebook]({{ page.study_archive }}/AR_II.ipynb) · [Original validation history]({{ '/files/recall/training.csv' | relative_url }}) · [Figure source]({{ '/files/recall/archive_figures.py' | relative_url }})
