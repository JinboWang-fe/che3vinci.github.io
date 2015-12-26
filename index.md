---
layout: idxlayout
title: Articles
---


<p style="text-align:center;font-size:2em" ><b>Archive</b></p>
<section id="archive" class="long-list">
{% for post in site.posts %}
  {% capture ym %}{{ post.date | date:"%Y 年 %m 月" }}{% endcapture %}
  {% if yearmonth != ym %}
    {% assign yearmonth = ym %}
    <h4>{{ ym }}</h4>
  {% endif %}
  <li id="idxli"><a href="{{ post.url }}" title="{{ post.title }}">{{ post.title }}</a></li>
{% endfor %}

</section>

