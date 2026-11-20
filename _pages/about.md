---
layout: profile
permalink: /
title: "Yifan Jing（敬益凡）"
redirect_from:
  - /about/
  - /about.html
---
<section class="intro" aria-labelledby="profile-name">
  <div class="intro-name">
    <h1 id="profile-name">Yifan <em>Jing</em></h1>
    <p class="name-alias"><span lang="zh-Hans">敬益凡</span><span class="alias-divider" aria-hidden="true">/</span>Ivan Jing</p>
  </div>
  <div class="intro-copy">
    <p class="intro-lead">{{ site.author.bio }}</p>
    <p>I’m a data science undergraduate at the <a href="https://umich.edu/">University of Michigan</a> and a research intern with <a href="https://liuzhuang13.github.io/">Zhuang Liu</a> at Princeton’s Z Lab.</p>
    <nav id="contact" class="contact-links" aria-label="Contact and profiles">
      <a href="mailto:{{ site.author.email }}">Email</a>
      {% if site.author.googlescholar %}<a href="{{ site.author.googlescholar | escape }}">Google Scholar</a>{% endif %}
      {% if site.author.github %}<a href="https://github.com/{{ site.author.github }}">GitHub</a>{% endif %}
      {% if site.author.linkedin %}<a href="https://www.linkedin.com/in/{{ site.author.linkedin }}">LinkedIn</a>{% endif %}
      <a href="{{ '/files/Yifan_Jing_Research_Resume.pdf' | relative_url }}">CV <span class="file-type">(PDF)</span></a>
    </nav>
  </div>
  <figure class="portrait">
    <picture>
      <source srcset="{{ '/images/profile.webp' | relative_url }}" type="image/webp">
      <img src="{{ site.author.avatar | prepend: '/images/' | relative_url }}" alt="Yifan Jing in front of a research poster" width="478" height="738" fetchpriority="high">
    </picture>
    <figcaption>Based in {{ site.author.location }}</figcaption>
  </figure>
</section>

<section class="home-section" id="research-highlights" aria-labelledby="news">
  <header class="section-heading">
    <h2 id="news">Selected research</h2>
    <a class="text-link" href="{{ '/portfolio/' | relative_url }}">All projects <span aria-hidden="true">→</span></a>
  </header>
  {% assign featured = site.portfolio | where: 'featured', true | sort: 'date' | reverse %}
  {% include work-list.html entries=featured level=3 gallery=true featured=true %}
</section>

<div class="home-notes">
  <section id="my-current-research" aria-labelledby="collaborations-title">
    <h2 id="collaborations-title">Research experience</h2>
    <p>At Princeton, I test when generated images help a vision-language model reason. At Michigan, I developed HintFlow with <a href="https://leiying.engin.umich.edu/post-docs-students/">Lei Ying</a> to train a small model to give useful hints to a larger one.</p>
    <p><a href="https://lsa.umich.edu/math/people/postdoc-faculty/gbarkley.html">Grant Barkley</a>, a postdoctoral assistant professor at Michigan, advised our work on translation-invariant total orders (TITOs). We built a SageMath package, and our <a href="https://arxiv.org/abs/2607.11709">paper</a> is under review at FPSAC 2027.</p>
    <p>In Shai Revzen’s <a href="https://www.birds.eecs.umich.edu/">BIRDs Lab</a>, I ran long MuJoCo simulations for <a href="https://iopscience.iop.org/article/10.1088/1748-3190/ae9261/pdf"><i>Contact Sensing Hexapod</i></a>.</p>
    <a class="text-link" href="{{ '/files/Yifan_Jing_Research_Resume.pdf' | relative_url }}">Full CV (PDF) <span aria-hidden="true">→</span></a>
  </section>
  <section id="selected-honors" aria-labelledby="honors-title">
    <h2 id="honors-title">Selected honors</h2>
    <dl class="honors">
      <div><dt>2026</dt><dd>SURE Fellowship, University of Michigan</dd></div>
      <div><dt>2026</dt><dd>Top 5 grant, <a href="https://github.com/danielryang/spaceoverflow">TartanHacks</a>, among 300+ projects</dd></div>
      <div><dt>2025</dt><dd>Finalist, CAST-USA 33rd Innovation Summit. Award presented by Avi Wigderson.</dd></div>
      <div><dt>2025</dt><dd>NOUR Summer Research Scholar, University of Pittsburgh</dd></div>
    </dl>
  </section>
</div>
