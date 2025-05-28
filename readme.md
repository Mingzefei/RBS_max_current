# 可重构电池系统最大许用电流计算

[English Version](readme_en.md)

本项目专注于为任意可重构电池系统 (RBS) 提出一种最大许用电流 (MAC) 的计算方法。该方法结合了有向图模型和贪心算法，旨在自动化计算过程，以指导 RBS 的设计、优化，并评估其在实际运行中的电流过载风险。

## 项目概述

可重构电池系统因其灵活的拓扑结构在储能领域展现出巨大潜力。然而，确定其在不同配置下的最大许用电流对于确保系统安全和高效运行至关重要。本项目提出的方法旨在解决手动计算 MAC 耗时且易出错的问题。

核心贡献包括：
*   基于有向图的 RBS 电路拓扑建模方法。
*   一种结合贪心策略的 MAC 求解算法。

相关研究成果已整理成学术论文（见 `paper/` 目录）和专利申请（见 `patent/` 目录）。

## 目录结构

```
.
├── code/                     # 实现 MAC 计算算法的 MATLAB 代码
│   └── main.m                # 主要的 MATLAB 计算脚本
├── paper/                    # 学术论文相关 LaTeX 文稿和手稿
│   ├── main.tex              # 论文主文件
│   └── SST/                  # 论文提交 (Space: Science & Technology) 相关文件
├── patent/                   # 专利申请相关 Markdown 文档
│   └── main.md               # 专利说明书和权利要求书
├── topology-design-from-Xu/  # 徐同学关于拓扑设计的研究 (Python 实现)
│   ├── README.md             # 该子项目的说明
│   └── LICENSE               # 该子项目的许可证 (MIT)
├── attachments/              # 论文和专利中使用的图片附件
└── ...                       # 其他配置文件和辅助文件
```

## 主要组件

*   **有向图建模**: 将 RBS 的电池、开关和连接关系抽象为有向图模型，其中边属性包含电压和电阻信息（详见 [patent/main.md](patent/main.md) 中“发明内容”部分）。
*   **MAC 计算算法**:
    *   在 [patent/main.md](patent/main.md) 的“发明内容”和“具体实施方式”部分有详细描述。
    *   算法实现位于 [code/main.m](code/main.m)。
    *   论文 [paper/main.tex](paper/main.tex) 中也对算法进行了阐述。

## 相关工作

本项目与 `topology-design-from-Xu/` 目录下的工作相关，该工作专注于 RBS 的拓扑设计和评估。详细信息请参阅 [topology-design-from-Xu/README.md](topology-design-from-Xu/README.md)。

## 使用

相关的计算和算法实现主要在 `code/` 目录下的 MATLAB 脚本中。运行 [code/main.m](code/main.m) 文件可以执行 MAC 的计算。

## 许可证

`topology-design-from-Xu/` 目录下的代码使用 MIT 许可证，详情请见 [topology-design-from-Xu/LICENSE](topology-design-from-Xu/LICENSE)。本项目其他部分的许可证未指定。