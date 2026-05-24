---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% if site.google_scholar_stats_use_cdn %}
{% assign gsDataBaseUrl = "https://cdn.jsdelivr.net/gh/" | append: site.repository | append: "@" %}
{% else %}
{% assign gsDataBaseUrl = "https://raw.githubusercontent.com/" | append: site.repository | append: "/" %}
{% endif %}
{% assign url = gsDataBaseUrl | append: "google-scholar-stats/gs_data_shieldsio.json" %}

<span class='anchor' id='about-me'></span>

I am an undergraduate student majoring in **Mathematics & Applied Mathematics** at the [University of Nottingham](https://www.nottingham.edu.cn/). My passion lies in the intersection of rigorous mathematical theory and practical algorithmic implementation.

My research interest includes **Large Visual Language Models (LVLMs)**, **Algorithm Design**, and **Mathematical Modeling**. I am currently working as a Research Assistant at the [AI Center, Shenzhen University of Advanced Technology](https://www.suat-sz.edu.cn/), focusing on efficiency optimization and reasoning problems in long-context image understanding.

You can find my publications on [Google Scholar](https://scholar.google.com/citations?user=x81ITIYAAAAJ).


# 🔥 News
- *2026.03*: &nbsp;🎉🎉 Our paper **TC-SSA: Token Compression via Semantic Slot Aggregation** is now available on arXiv!
- *2026.05*: &nbsp;🎉🎉 Our paper **PathoSelect: Capacity-Constrained Token Budgeting for Gigapixel Pathology Inference** is now available on arXiv!
- *2025.07*: &nbsp;🔬 Joined the Computer Vision and Recognition Center (AI觉-知研究中心) at Shenzhen University of Advanced Technology as a Research Assistant.

# 📝 Publications 

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">arXiv 2026</div><img src='images/tc_ssa.png' alt="TC-SSA" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

[TC-SSA: Token Compression via Semantic Slot Aggregation](https://arxiv.org/pdf/2603.01143v1)

**Ozzy Chen**, et al.

- Proposed a learnable token-budgeting mechanism for Gigapixel Whole-Slide Images.
- Reframed spatial reasoning as aggregation-based compression via gated assignment (Top-2 routing).
- Achieved **76.78% accuracy** on SlideChat and **120× efficiency gain**.
</div>
</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">arXiv 2026</div><img src='images/pathoselect.png' alt="PathoSelect" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

[PathoSelect: Capacity-Constrained Token Budgeting for Gigapixel Pathology Inference](https://arxiv.org/)

Jingzhi Chen, Landi He, **Zhuo Chen**, Xiaoyu Yang, Lijian Xu

- Proposed a capacity-constrained token budgeting framework for efficient gigapixel pathology image inference.
</div>
</div>

# 📖 Educations
- *2024.09 - 2028.06 (expected)*, B.Sc. in Mathematics & Applied Mathematics, **University of Nottingham**. 
  - Relevant Coursework: Linear Algebra, Machine Learning, Deep Learning, Computer Vision.

# 💻 Research Experience
- *2025.07 - Present*, Research Assistant, **Shenzhen University of Advanced Technology**, AI Center (Computer Vision and Recognition Center).
  - Conducting research on Large Visual Language Models (LVLMs), studying efficiency optimization.
  - Investigating reasoning problems in long-context image understanding.
  - Working with models such as Qwen2.5-VL to bridge sensory input with cognitive understanding.