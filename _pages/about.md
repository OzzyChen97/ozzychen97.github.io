---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

<span class='anchor' id='about-me'></span>

I am an undergraduate student in **Mathematics & Applied Mathematics** at the [University of Nottingham Ningbo China](https://www.nottingham.edu.cn/). My work sits at the intersection of mathematical foundations and practical machine learning systems.

I am currently a Research Assistant at the Di² Lab, [HKUST(GZ)](https://www.hkust-gz.edu.cn/), under the supervision of **Associate Professor Yutao YUE**. My research focuses on **efficient multimodal reasoning**, **long-context visual understanding**, and algorithms that make large vision-language models more scalable and reliable.

You can find my publications on <a href='https://scholar.google.com/citations?user=x81ITIYAAAAJ'>Google Scholar</a>. Total citations: <span id="total_cit">-</span>.


# 🔥 News
- *2026.06*: &nbsp;🚀 Joined Di² Lab at [HKUST(GZ)](https://www.hkust-gz.edu.cn/) as a Research Assistant, supervised by **Associate Professor Yutao YUE**.
- *2026.06*: &nbsp;🎉🎉 Our paper **TC-SSA: Token Compression via Semantic Slot Aggregation** was accepted to **MICCAI 2026**!
- *2026.06*: &nbsp;📄 **Learnable Token Sparsification for Efficient Gigapixel Whole Slide Image Reasoning** is now available on [arXiv](https://arxiv.org/abs/2606.08641).
- *2026.03*: &nbsp;📄 **TC-SSA: Token Compression via Semantic Slot Aggregation** was released on arXiv.
- *2025.07*: &nbsp;🔬 Joined the Computer Vision and Recognition Center (AI觉-知研究中心) at Shenzhen University of Advanced Technology as a Research Assistant.

# 📝 Publications 

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">MICCAI 2026</div><img src='images/tc_ssa.png' alt="TC-SSA" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

[TC-SSA: Token Compression via Semantic Slot Aggregation for Gigapixel Pathology Reasoning](https://arxiv.org/abs/2603.01143)

**Zhuo Chen**, Xiaoyu Yang, Lijian Xu

<span class="paper_citation" data-arxiv="2603.01143"></span>

- Aggregates all WSI patch features into a fixed budget of 32 semantic slots through sparse Top-2 routing.
- Retains global slide evidence with only **1.7% of the original visual tokens** and **1.72T FLOPs**.
- Achieves **78.34% overall accuracy** and **77.14% diagnosis accuracy** on SlideBench (TCGA).
</div>
</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge badge-arxiv">arXiv</div><img src='images/sparselearn.png' alt="SparseLearn" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

[Learnable Token Sparsification for Efficient Gigapixel Whole Slide Image Reasoning](https://arxiv.org/abs/2606.08641)

Jingzhi Chen, Landi He, **Zhuo Chen**, Shawn Young, Lijian Xu

<span class="paper_citation" data-arxiv="2606.08641"></span>

- Reframes WSI token pruning as an end-to-end learnable sparsification problem with decoupled training and inference.
- Combines a variance-preserving noise gate, differentiable Soft Top-K, and diagonal-attention denoising in **SparseLearn**.
- At inference, deterministic Hard Top-K retains just **32 tokens (0.78%)** and reaches **73.32% overall accuracy** on SlideBench (TCGA).
</div>
</div>

# 💻 Research Experience

<div class="timeline">

  <div class="timeline-item">
    <div class="timeline-info">
      <div class="timeline-date">2024.09 - 2028.06</div>
      <div class="timeline-logo">
        <img src="images/UoN-Logo.jpg" alt="UoN">
      </div>
    </div>
    <div class="timeline-dot"></div>
    <div class="timeline-content">
      <h3>B.Sc. in Mathematics & Applied Mathematics</h3>
      <p class="timeline-institution">University of Nottingham</p>
      <ul>
        <li>Relevant Coursework: Linear Algebra, Machine Learning, Deep Learning, Computer Vision.</li>
      </ul>
    </div>
  </div>

  <div class="timeline-item">
    <div class="timeline-info">
      <div class="timeline-date">2025.07 - Present</div>
      <div class="timeline-logo">
        <img src="images/SUAT-Logo.png" alt="SUAT">
      </div>
    </div>
    <div class="timeline-dot"></div>
    <div class="timeline-content">
      <h3>Research Assistant</h3>
      <p class="timeline-institution">Shenzhen University of Advanced Technology — AI Center (Computer Vision and Recognition Center)</p>
      <p class="timeline-supervisor">Under the supervision of <strong>Associate Professor Lijian Xu</strong></p>
      <ul>
        <li>Conducting research on Large Visual Language Models (LVLMs), studying efficiency optimization.</li>
        <li>Investigating reasoning problems in long-context image understanding.</li>
        <li>Working with models such as Qwen2.5-VL to bridge sensory input with cognitive understanding.</li>
      </ul>
    </div>
  </div>

  <div class="timeline-item">
    <div class="timeline-info">
      <div class="timeline-date">2026.06 - Present</div>
      <div class="timeline-logo hkustgz-logo">
        <img src="images/HKUSTGZ-Logo.png?v=20260617" alt="HKUST(GZ)">
      </div>
    </div>
    <div class="timeline-dot"></div>
    <div class="timeline-content">
      <h3>Research Assistant</h3>
      <p class="timeline-institution">HKUST(GZ) — Di² Lab</p>
      <p class="timeline-supervisor">Under the supervision of <strong>Associate Professor Yutao YUE</strong></p>
      <ul>
        <li>Conducting research on efficient multimodal reasoning and long-context visual understanding.</li>
        <li>Exploring algorithmic approaches for robust and scalable Large Visual Language Models.</li>
      </ul>
    </div>
  </div>

</div>
