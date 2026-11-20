---
layout: profile
title: "Curriculum vitae"
permalink: /cv/
redirect_to: /files/Yifan_Jing_Research_Resume.pdf
prose: true
redirect_from:
  - /resume
---

[Download CV (PDF)]({{ '/files/Yifan_Jing_Research_Resume.pdf' | relative_url }}){: .text-link }

{{ site.author.bio }}

Education
---------

* **University of Michigan, Ann Arbor** — B.S. in Data Science, expected 2027.
* **Yale University** — Visiting student in algorithms, summer 2024.

Research Experience
-------------------

* **Princeton University, Z Lab** — Research intern with [Zhuang Liu](https://liuzhuang13.github.io/) (Jul 2026 – present).
  * Compare vision-language models’ answers with and without generated images to identify when image generation helps visual reasoning.

* **University of Michigan, SURE** — Undergraduate researcher with [Lei Ying](https://leiying.engin.umich.edu/post-docs-students/) (May – Aug 2026).
  * Developed HintFlow, training a 4B model to guide frozen 14B–20B reasoning models with short hints. Evaluated the collaboration on math, ARC, and coding tasks.

* **University of Michigan, Mathematics (LoGM)** — Translation-invariant total orders (TITOs), advised by [Grant Barkley](https://lsa.umich.edu/math/people/postdoc-faculty/gbarkley.html), Postdoctoral Assistant Professor of Mathematics (Sep 2025 – Apr 2026).
  * Developed algorithms to compare TITOs through their inversion sets and compute joins using weighted paths. Released them with my coauthors in [TITO_Explore](https://github.com/emmaycl/TITO_Explore_package).

* **Terminal-Bench Science** — Benchmark contributor (Apr 2026 – present).
  * Built two tasks from combinatorics research. [Cambrian projection in Lean 4](https://github.com/harbor-framework/terminal-bench-science/pull/1257) was merged into the main benchmark. Reviewers designated [TITO weak-order comparison](https://github.com/harbor-framework/terminal-bench-science/pull/268) for Lite.

* **University of Michigan, BIRDs Lab** — Undergraduate researcher with Shai Revzen (Jan 2026 – present).
  * Ran long MuJoCo simulations for [Contact Sensing Hexapod](https://iopscience.iop.org/article/10.1088/1748-3190/ae9261/pdf). I now study how neural networks and finite-state controllers can guide six-legged robots over rough terrain.

* **University of Michigan, hybrid sequence models** — Research project with Samet Oymak (Sep – Dec 2025).
  * Compared Transformer, Mamba, and hybrid architectures on [associative recall](https://github.com/Ivann1242/Analysis-AR-problem) to study long-range generalization.

Publications
------------

* Joint first author on a study of image generation for visual reasoning. Under review at ICLR 2027.
{% for paper in site.publications reversed %}* {{ paper.authors | join: ', ' }}. [*{{ paper.title }}*]({{ paper.paperurl | default: paper.url | relative_url }}). {{ paper.venue }}, {{ paper.date | date: '%Y' }}.{% if paper.review_status %} {{ paper.review_status }}.{% endif %}
{% endfor %}

Selected Research Result
------------------------

* Disproved a [second-order converse conjecture for pure-loss channels](https://qiqc-op.com/problem/op_89fb664ba06ba5de/) with Yue Tu and [verified the disproof in Lean 4](https://github.com/Ivann1242/pure-loss-second-order-lean) (Sep 2026).

Teaching Experience
-------------------

{% for course in site.teaching reversed %}* **[{{ course.title }}]({{ course.url | relative_url }})** — {{ course.type }}, {{ course.venue }}, {{ course.date | date: '%Y' }}. {{ course.excerpt }}
{% endfor %}

Honors & Leadership
-------------------

* **SURE Fellowship**, University of Michigan, 2026.
* **TartanHacks**, 2026. Led a team of four to a top-five grant among 300+ projects with [SpaceOverflow](https://github.com/danielryang/spaceoverflow).
* **NOUR Summer Research Scholar**, University of Pittsburgh, 2025.
* **CAST-USA 33rd Innovation Summit**, 2025. Finalist, $1,500 award presented by Avi Wigderson.
* **She Innovations Hackathon**. Led a team of three building a 3D runner in Unity and C#.

Skills
------

* Python (PyTorch, JAX, NumPy), C, C++, Java, JavaScript, HTML, MIPS.
* SageMath, Lean 4, MuJoCo, Linux, GitHub Actions, Jupyter, Colab, Google Cloud Platform, LaTeX.
