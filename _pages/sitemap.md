---
layout: profile
title: Sitemap
permalink: /sitemap/
---
<nav class="site-map" aria-label="Site directory">
  <section>
    <h2>Main pages</h2>
    <ul>
      <li><a href="{{ '/' | relative_url }}">Home</a></li>
      {% for link in site.data.navigation.main %}<li><a href="{{ link.url | relative_url }}">{{ link.title }}</a></li>{% endfor %}
    </ul>
  </section>
  {% for link in site.data.navigation.main %}
    {% if link.collection %}
      {% assign entries = site[link.collection] | sort: 'date' | reverse %}
      <section>
        <h2>{{ link.title }}</h2>
        <ul>{% for entry in entries %}<li><a href="{{ entry.url | relative_url }}">{{ entry.short_title | default: entry.title | escape }}</a></li>{% endfor %}</ul>
      </section>
    {% endif %}
  {% endfor %}
</nav>
<details class="citation archive-directory">
  <summary>Other pages and archives</summary>
  <ul>
    {% assign primary_urls = site.data.navigation.main | map: 'url' %}
    {% for entry in site.pages %}
      {% if entry.title and entry.sitemap != false %}
        {% unless primary_urls contains entry.url or entry.url == '/' or entry.url == page.url %}
          <li><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></li>
        {% endunless %}
      {% endif %}
    {% endfor %}
    {% assign posts = site.posts | uniq: 'url' %}
    {% for entry in posts %}<li><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></li>{% endfor %}
    {% for entry in site.talks %}<li><a href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a></li>{% endfor %}
  </ul>
</details>
<a class="text-link" href="{{ '/sitemap.xml' | relative_url }}">XML sitemap <span aria-hidden="true">→</span></a>
