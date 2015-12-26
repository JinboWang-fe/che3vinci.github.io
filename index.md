---
layout: idxlayout
title: archive
---
<p style="text-align:center;font-size:2em" ><b>Archive</b></p>
<section id="archive" class="long-list">
  {%for post in site.posts %}
    {% unless post.next %}
      <h3>{{ post.date | date: '%Y' }}年 {{post.date|date:'%M'}}月</h3>
      <ul class="this">
    {% else %}
      {% capture year %}{{ post.date | date: '%Y' }}{% endcapture %}
      {% capture nyear %}{{ post.next.date | date: '%Y' }}{% endcapture %}
      {% if year != nyear %}
        </ul>
        <h3>{{ post.date | date: '%Y' }}年</h3>
        <ul class="past">
      {% endif %}
    {% endunless %}
      <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
  </ul>
</section>

