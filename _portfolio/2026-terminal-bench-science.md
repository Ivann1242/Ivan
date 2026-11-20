---
title: "Terminal Bench Science"
topic: AI evaluation
featured_order: 2
visual:
  image: cambrian
  height: 648
  control: "Project 312"
  result: "6 chambers → 5"
  alt: "A disc is divided into six permutation chambers. The two purple chambers share a dashed wall. Cambrian projection maps 312 to 132, so removing that wall leaves five chambers."
  caption: "Each chamber represents a permutation of three elements. Neighboring dots trace the covers in weak order. With c = s₁s₂, downward projection sends 312 to 132 and fixes the other five permutations. The two purple chambers become one. The Lean task asks for the corresponding theorem in arbitrary Coxeter systems."
  source: https://github.com/harbor-framework/terminal-bench-science/pull/1257
  source_label: "Formalization task"
excerpt: "I turned two problems from combinatorics into tests for AI agents: proving a result about Cambrian projection and comparing translation-invariant total orders."
collection: portfolio
permalink: /portfolio/2026-terminal-bench-science/
date: 2026-09-22
---

I built two tasks for [Terminal Bench Science](https://www.terminal-bench-science.ai/) to test whether AI agents can work from mathematical definitions to a proof or algorithm.

[Cambrian projection](https://github.com/harbor-framework/terminal-bench-science/pull/1257) asks an agent to prove Reading’s maximality theorem for downward Cambrian projection in Lean 4. I wrote the reference proof and an independent verifier. The task was merged into the main benchmark on November 1, 2026.

[TITO weak-order comparison](https://github.com/harbor-framework/terminal-bench-science/pull/268) grew out of our [work on translation-invariant total orders]({{ '/portfolio/2025-tito/' | relative_url }}). It asks an agent to decide whether two orders are comparable. Reviewers designated the task for Lite.
