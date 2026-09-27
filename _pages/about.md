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

My primary research affiliation is with the Di² Lab at [HKUST(GZ)](https://www.hkust-gz.edu.cn/), where I work on **text-to-motion generation** and **embodied AI** under the supervision of **Associate Professor Yutao YUE**. I also work remotely on **QuantVLA**, quantization for efficient Vision-Language-Action models, jointly supervised by [Assistant Professor Xiao Luo](https://luoxiao12.github.io/) at the [University of Wisconsin–Madison](https://www.wisc.edu/) and [Assistant Professor Yiyang Gu](https://www.bza.edu.cn/teacher/j9n3khin72s1jan0vp9gbehuyivdvcxr) at the [Beijing Zhongguancun Academy](https://www.bza.edu.cn/). Previously, at the Shenzhen University of Advanced Technology, I worked on token-efficient gigapixel pathology reasoning and developed **TC-SSA**.

You can find my publications on <a href='https://scholar.google.com/citations?user=x81ITIYAAAAJ'>Google Scholar</a>. Total citations: <span id="total_cit">-</span>.


# 🔥 News
- *2026.08*: &nbsp;📦 Released the [TC-SSA dataset](https://huggingface.co/datasets/OzzyChen97/TC-SSA) on Hugging Face.
- *2026.08*: &nbsp;🌐 Started working on QuantVLA as a Remote Research Assistant, jointly supervised by [Assistant Professor Xiao Luo](https://luoxiao12.github.io/) ([University of Wisconsin–Madison](https://www.wisc.edu/)) and [Assistant Professor Yiyang Gu](https://www.bza.edu.cn/teacher/j9n3khin72s1jan0vp9gbehuyivdvcxr) ([Beijing Zhongguancun Academy](https://www.bza.edu.cn/)).
- *2026.06*: &nbsp;🚀 Joined Di² Lab at [HKUST(GZ)](https://www.hkust-gz.edu.cn/) as a Research Assistant, supervised by **Associate Professor Yutao YUE**.
- *2026.06*: &nbsp;🎉🎉 Our paper **TC-SSA: Token Compression via Semantic Slot Aggregation** was accepted to **MICCAI 2026**!
- *2026.06*: &nbsp;📄 **SparseLearn: Learnable Token Pruning with Continuous Noise Gating for Gigapixel Whole-Slide Images** is now available on [arXiv](https://arxiv.org/abs/2606.08641) and is under review at WACV.
- *2026.03*: &nbsp;📄 **TC-SSA: Token Compression via Semantic Slot Aggregation** was released on arXiv.
- *2025.07*: &nbsp;🔬 Joined the Computer Vision and Recognition Center (AI觉-知研究中心) at Shenzhen University of Advanced Technology as a Research Assistant.

# 📝 Publications 

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">MICCAI 2026</div><img src='images/tc_ssa.png' alt="TC-SSA" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

[TC-SSA: Token Compression via Semantic Slot Aggregation for Gigapixel Pathology Reasoning](https://arxiv.org/abs/2603.01143)

**Zhuo Chen**, Xiaoyu Yang, Lijian Xu

<span class="paper_citation" data-arxiv="2603.01143"></span>

<span class="dataset-stat">📦 <a href="https://huggingface.co/datasets/OzzyChen97/TC-SSA">Dataset</a> · Total downloads: <strong id="tc_ssa_total_downloads">-</strong></span>

- Aggregates all WSI patch features into a fixed budget of 32 semantic slots through sparse Top-2 routing.
- Retains global slide evidence with only **1.7% of the original visual tokens** and **1.72T FLOPs**.
- Achieves **78.34% overall accuracy** and **77.14% diagnosis accuracy** on SlideBench (TCGA).
</div>
</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">WACV (under review)</div><img src='images/sparselearn.png' alt="SparseLearn" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

[SparseLearn: Learnable Token Pruning with Continuous Noise Gating for Gigapixel Whole-Slide Images](https://openreview.net/pdf?id=HS1DodAT88)

Jingzhi Chen, Landi He, **Zhuo Chen**, Shawn Young, Lijian Xu

<span class="paper_citation" data-arxiv="2606.08641"></span>

- Reformulates token reduction for gigapixel whole-slide images as a trainable sparsification problem instead of fixed downsampling or heuristic pruning.
- Trains a decoupled router with **SparseLearn**: a variance-preserving continuous noise gate, a differentiable Soft Top-K operator, and a diagonal-attention denoiser that keeps gradients flowing through pruning.
- At inference the gate is discarded and a deterministic Hard Top-K keeps only **32 tokens (0.78%)**, reaching **73.32% overall accuracy** on SlideBench (TCGA) with strong zero-shot transfer to SlideBench (BCNB) and WSI-VQA*.
- Preprint: [arXiv:2606.08641](https://arxiv.org/abs/2606.08641).
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
      <div class="timeline-date">2025.07 - 2026.08</div>
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
        <li>Developed <a href="https://arxiv.org/abs/2603.01143">TC-SSA</a>, a semantic-slot token compression framework for efficient gigapixel whole-slide image reasoning.</li>
        <li>Compressed thousands of pathology patch tokens into 32 semantic slots while preserving global slide-level evidence.</li>
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
        <li>Conducting research on text-to-motion generation and human motion synthesis from natural-language instructions.</li>
        <li>Exploring embodied AI systems that connect multimodal perception, language understanding, and action generation.</li>
      </ul>
    </div>
  </div>

  <div class="timeline-item">
    <div class="timeline-info">
      <div class="timeline-date">2026.08 - Present</div>
      <div class="timeline-logo uwmadison-logo">
        <img src="images/UWMadison-Logo.png" alt="University of Wisconsin–Madison">
      </div>
    </div>
    <div class="timeline-dot"></div>
    <div class="timeline-content">
      <h3>Remote Research Assistant</h3>
      <p class="timeline-institution"><a href="https://www.wisc.edu/">University of Wisconsin–Madison</a> — Department of Statistics &amp; <a href="https://www.bza.edu.cn/">Beijing Zhongguancun Academy</a></p>
      <p class="timeline-supervisor">Jointly supervised by <strong><a href="https://luoxiao12.github.io/">Assistant Professor Xiao Luo</a></strong> (UW–Madison) and <strong><a href="https://www.bza.edu.cn/teacher/j9n3khin72s1jan0vp9gbehuyivdvcxr">Assistant Professor Yiyang Gu</a></strong> (Beijing Zhongguancun Academy)</p>
      <ul>
        <li>Working on QuantVLA: quantization of Vision-Language-Action models for efficient robot policies.</li>
        <li>Investigating post-training quantization and memory-efficient deployment for embodied AI systems.</li>
      </ul>
    </div>
  </div>

</div>
