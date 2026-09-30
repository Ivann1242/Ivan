---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

Education
======
* **B.S. in Data Science**, University of Michigan, Ann Arbor — Expected 2027
  * Research Interests: Multimodal Reasoning, LLM Reasoning, AI Scientist Systems, AI Evaluation
* **Visiting Student**, Yale University — 2024 summer
  * Algorithm

Research Experience
======
* **Research Intern** — Z Lab, Princeton University (Jul 2026 – Present)
  * Advisor: Prof. Zhuang Liu
  * Investigating multimodal reasoning through systematic evaluations and controlled ablations; a manuscript is under review at **ICLR 2027** (title withheld).
  * Developing **AI scientist systems** and self-evolving agents that autonomously propose, evaluate, and iteratively improve reasoning strategies and scientific solutions.

* **Contributor** — Terminal-Bench Science (Apr 2026 – Present)
  * Developing mathematical discovery and formal reasoning tasks for evaluating frontier AI agents.
  * **1 task accepted for inclusion**: Cambrian projection in Lean 4, with domain, technical, and final review approved as of **September 22, 2026**.
  * Built a complete reference proof and isolated verifier for Reading's maximality theorem on arbitrary Coxeter systems.
  * [Task and review history — PR #1257](https://github.com/harbor-framework/terminal-bench-science/pull/1257) · [Project]({{ base_path }}/portfolio/2026-terminal-bench-science/)

* **Undergraduate Researcher, SURE 2026** — University of Michigan (May 2026 – Aug 2026)
  * Advisor: Prof. Lei Ying
  * Developed **HintFlow**, training a 4B language-model policy to guide frozen 14B–20B reasoning models through selective supervised fine-tuning and a modified GRPO objective.
  * Built the end-to-end training and inference pipeline using Qwen3, GPT-OSS-20B, LoRA, and vLLM.

* **Contact Sensing Hexapod** — BIRDs Lab, University of Michigan (Jan 2026 – Present)
  * Advisor: Prof. Shai Revzen
  * Developed large-scale MuJoCo simulations for multi-legged locomotion, evaluating modular controllers across varying morphologies and irregular terrain conditions.
  * Developing an efficient control pipeline that uses LLM-guided search to distill a high-capacity neural policy into an interpretable finite-state machine.
  * Simulation contributor to [arXiv:2603.09147](https://arxiv.org/abs/2603.09147).

* **Hybrid Transformer Analysis in Induction Head Problem** — University of Michigan (Sep 2025 – Dec 2025)
  * Mentor: Dr. Samet Oymak
  * Studied generalization of sequence models on the Associative Recall task; proposed hybrid SSM + attention architectures.
  * [GitHub](https://github.com/Ivann1242/Analysis-AR-problem)

* **TITO (Translation-Invariant Total Orders)** — University of Michigan (Sep 2025 – Apr 2026)
  * Advisor: Dr. Grant Barkley
  * Completed the project, formalizing order-comparability through inversion sets and implementing weak order comparison, joins, normalization, and visualization in SageMath.
  * Released a [SageMath package](https://github.com/emmaycl/TITO_Explore_package) and [arXiv preprint](https://arxiv.org/abs/2607.11709); targeting FPSAC 2027.
  * [LoGM project page](https://lsa.umich.edu/math/undergraduates/research-and-career-opportunities/research/LoGM/projects.html)

* **ThinkAct LLM Agent** — University of Michigan (Sep 2025 – Dec 2025)
  * Mentor: Dr. Samet Oymak
  * Improved LLM reasoning via self-reflection and self-consistency within ReAct.
  * [GitHub](https://github.com/Ivann1242/ThinkAct)

Selected Research Result
======
* **General counterexamples to a candidate pure-loss second-order converse** (September 23, 2026)
  * With **Yue Tu** and **six parallel AI agents**, constructed a general family of counterexamples in quantum communication and verified the disproof in **Lean 4**.
  * The candidate formulation arose from a question posed by **Mark M. Wilde, Joseph M. Renes, and Saikat Guha in 2014**, 12 years before this result. QIQCOP credits the result to Yue Tu and Yifan Jing and lists the problem as solved.
  * [Problem and solution](https://qiqc-op.com/problem/op_89fb664ba06ba5de/) · [Project]({{ base_path }}/portfolio/2026-pure-loss-counterexample/)

Teaching Experience
======
<ul>{% for post in site.teaching reversed %}
    {% include archive-single-cv.html %}
{% endfor %}</ul>

Skills
======
* **Languages:** Python (JAX, PyTorch, NumPy), C, C++, Java, HTML, JavaScript, MIPS
* **Engineering:** MuJoCo, Linux
* **Tools:** GitHub Actions, Jupyter Notebook, Colab, Google Cloud Platform, LaTeX, Coding Agents

Publications
======
**Manuscript under review at ICLR 2027** (title withheld).

<ul>{% for post in site.publications reversed %}
    {% include archive-single-cv.html %}
{% endfor %}</ul>

Portfolio
======
<ul>{% assign sorted_portfolio = site.portfolio | sort: 'date' | reverse %}{% for post in sorted_portfolio %}
    {% include archive-single-cv.html %}
{% endfor %}</ul>

Honors & Leadership
======
* **University of Michigan SURE 2026** — Summer Undergraduate Research Experience fellowship
* **University of Pittsburgh NOUR 2025** — Summer Research Scholar, School of Computing and Information
* **Tartanhacks 2026** — Led team of 4; Top 5 grant among 300+ projects. [GitHub](https://github.com/danielryang/spaceoverflow)
* **CAST-USA 33rd Innovation Summit** — Finalist, $1,500 award
* **She Innovations Hackathon** — Led team of 3 to build a 3D runner game in Unity/C#

[Download full CV (PDF)]({{ base_path }}/files/Yifan_Jing_Research_Resume.pdf)
