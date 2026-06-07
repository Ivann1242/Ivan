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
* **B.S. in Data Science**, University of Michigan, Ann Arbor — Expected Winter 2028
  * Research Interests: Reinforcement Learning, Language Models, Group Theory
* **Visiting Student**, Yale University — 2024 summer
  * Algorithm

Research Experience
======
* **Terminal-Bench Science** — Co-author & Contributor (Apr 2026 – Present)
  * Developed the Structure2Discover task series to evaluate AI agents on inferring hidden structures from computational evidence.
  * [Project announcement](https://www.tbench.ai/news/tb-science-announcement)

* **Hybrid Transformer Analysis in Induction Head Problem** — University of Michigan (Sep 2025 – Dec 2025)
  * Mentor: Dr. Samet Oymak
  * Studied generalization of sequence models on the Associative Recall task; proposed hybrid SSM + attention architectures.
  * [GitHub](https://github.com/Ivann1242/Analysis-AR-problem)

* **Contact Sensing Hexapod** — BIRDs Lab, University of Michigan (Jan 2026 – Present)
  * Mentor: Shai Revzen
  * Large-scale MuJoCo simulation for multi-legged robotic locomotion across varying leg counts and terrains.

* **TITO (Translation-Invariant Total Orders)** — University of Michigan (Sep 2025 – Apr 2026)
  * Advisor: Dr. Grant Barkley
  * Formalized order-comparability through inversion sets; built Python package for weak order comparison and visualization.
  * [LoGM project page](https://lsa.umich.edu/math/undergraduates/research-and-career-opportunities/research/LoGM/projects.html)

* **ThinkAct LLM Agent** — University of Michigan (Sep 2025 – Dec 2025)
  * Mentor: Dr. Samet Oymak
  * Improved LLM reasoning via self-reflection and self-consistency within ReAct.
  * [GitHub](https://github.com/Ivann1242/ThinkAct)

Teaching Experience
======
  <ul>{% for post in site.teaching reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>

Skills
======
* **Languages:** Python, C, C++, Java, JavaScript, MIPS
* **Tools:** GitHub Actions, Jupyter Notebook, Colab, Google Cloud Platform, LaTeX

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
