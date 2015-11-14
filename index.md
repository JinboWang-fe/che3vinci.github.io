---
layout: default
title: 日志
---
<section id="archive" class="long-list">
  {%for post in site.posts %}
    {% unless post.next %}
      <h3>{{ post.date | date: '%Y' }}年日志</h3>
      <ul class="this">
    {% else %}
      {% capture year %}{{ post.date | date: '%Y' }}{% endcapture %}
      {% capture nyear %}{{ post.next.date | date: '%Y' }}{% endcapture %}
      {% if year != nyear %}
        </ul>
        <h3>{{ post.date | date: '%Y' }}年日志</h3>
        <ul class="past">
      {% endif %}
    {% endunless %}
      <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
  </ul>
</section>

