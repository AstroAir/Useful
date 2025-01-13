# Sky-T1: 在450美元内训练你自己的O1预览模型"

我们推出了Sky-T1-32B-Preview，这是一个推理模型，在流行的推理和编码基准测试中表现与o1-preview相当。**值得注意的是，Sky-T1-32B-Preview的训练成本不到450美元，这表明可以以经济高效的方式复制高级推理能力。** 所有[代码](https://github.com/NovaSky-AI/SkyThought)都是开源的。

## 概述

像o1和Gemini 2.0这样的模型在推理方面表现出色，通过产生一长串内部思维链来解决复杂任务，展示了其他进展。然而，技术细节和模型权重无法访问，这给学术界和开源社区的参与带来了障碍。

作为回应，一些值得注意的努力已经出现，以在数学领域训练开放权重的推理模型，例如[Still-2](https://arxiv.org/abs/2412.09413)和[Journey](https://arxiv.org/abs/2411.16489)。同时，我们，加州大学伯克利分校的NovaSky团队，一直在探索各种技术来提升基础和指令调优模型的推理能力。在这项工作中，我们不仅在数学领域，还在编码领域实现了具有竞争力的推理性能。

### 完全开源：共同推动进步

为了确保我们的工作惠及更广泛的社区，我们完全致力于开源合作。我们开源所有细节（即数据、代码、模型权重），以使社区能够轻松复制和改进我们的结果：

- [**基础设施**](https://github.com/NovaSky-AI/SkyThought)：在一个仓库中构建数据、训练和评估模型。
- [**数据**](https://github.com/NovaSky-AI/SkyThought)：用于训练Sky-T1-32B-Preview的17K数据。
- [**技术细节**](https://novasky-ai.github.io/posts/sky-t1)：我们的技术[报告](https://novasky-ai.github.io/posts/sky-t1/)和[wandb日志](https://api.wandb.ai/links/sky-posttraining-uc-berkeley/wjg3sybl)。
- [**模型权重**](https://huggingface.co/NovaSky-AI)：我们的32B模型权重。

| 模型               | Sky-T1-32B-Preview | STILL-2 | Journey | QwQ  | o1   |
|--------------------|--------------------|---------|---------|------|------|
| 数据               | ✅                 | ✅      | ❌      | ❌   | ❌   |
| 代码               | ✅                 | ❌      | ❌      | ❌   | ❌   |
| 报告               | ✅                 | ✅      | ✅      | ❌   | ❌   |
| 数学领域           | ✅                 | ✅      | ✅      | ✅   | ✅   |
| 编码领域           | ✅                 | ❌      | ❌      | ✅   | ✅   |
| 模型权重           | ✅                 | ✅      | ❌      | ✅   | ❌   |

通过分享所有这些资源，我们的目标是使学术界和开源社区能够在我们的工作基础上进行构建，探索新的可能性，并推动推理模型开发的边界。

## 方法

### 数据整理过程

为了生成我们的训练数据，我们使用了QwQ-32B-Preview，这是一个具有与o1-preview相当的推理能力的开源模型。我们整理了数据混合物（见后文部分）以涵盖需要推理的多样化领域，并通过拒绝采样程序来提高数据质量。然后，我们使用GPT-4o-mini将QwQ的跟踪重写为格式良好的版本，灵感来自[Still-2](https://arxiv.org/abs/2412.09413)，以提高数据质量并简化解析。我们特别发现解析的简便性对推理模型有利——它们被训练为以特定格式响应，而结果通常难以解析。例如，在APPs数据集中，如果不重新格式化，我们只能假设代码写在最后一个代码块中，而QwQ的准确率仅为约25%。然而，有时代码可能写在中间，重新格式化后，准确率提高到90%以上。

**拒绝采样：** 如果QwQ样本与数据集中提供的解决方案不符，我们会丢弃这些样本。对于数学问题，我们与真实解决方案进行精确匹配。对于编码问题，我们执行数据集中提供的单元测试。我们的最终数据包含来自APPs和TACO的5k编码数据，以及来自AIME、MATH和NuminaMATH数据集的Olympiads子集的10k数学数据。此外，我们还保留了来自STILL-2的1k科学和谜题数据。

### 训练

我们使用我们的训练数据对Qwen2.5-32B-Instruct进行微调，这是一个没有推理能力的开源模型。模型训练了3个epoch，学习率为1e-5，批量大小为96。模型训练在8个H100上使用DeepSpeed Zero-3卸载完成，耗时19小时（根据Lambda Cloud的定价约为450美元）。我们使用[Llama-Factory](https://github.com/hiyouga/LLaMA-Factory)进行训练。

### 评估和结果

|                    | Sky-T1-32B-Preview | Qwen-2.5-32B-Instruct | QwQ  | o1-preview |
|--------------------|--------------------|-----------------------|------|------------|
| Math500            | 82.4               | 76.2                  | 85.4 | 81.4       |
| AIME2024           | 43.3               | 16.7                  | 50.0 | 40.0       |
| LiveCodeBench-Easy | 86.3               | 84.6                  | 90.7 | 92.9       |
| LiveCodeBench-Medium | 56.8             | 40.8                  | 56.3 | 54.9       |
| LiveCodeBench-Hard | 17.9               | 9.8                   | 17.1 | 16.3       |
| GPQA-Diamond       | 56.8               | 45.5                  | 52.5 | 75.2       |

## 其他发现

**模型大小很重要。** 我们最初尝试在较小的模型（7B和14B）上进行训练，但只观察到了适度的改进。例如，在APPs数据集上训练Qwen2.5-14B-Coder-Instruct，LiveCodeBench的性能从42.6%略微提高到46.3%。然而，在手动检查较小模型（小于32B）的输出时，我们发现它们经常生成重复内容，限制了它们的有效性。

**数据混合物很重要。** 我们最初使用Numina数据集（由STILL-2提供）中的3-4K数学问题训练了一个32B模型，AIME24的准确率从16.7%显著提高到43.3%。然而，当我们将APPs数据集生成的编码数据纳入训练过程时，AIME24的准确率下降到36.7%。我们假设这种下降是由于数学和编码任务所需的推理方法不同。

编码中的推理通常涉及额外的逻辑步骤，例如模拟测试输入或在内部执行生成的代码，而数学问题的推理往往更直接和结构化。为了解决这些差异，我们用NuminaMath数据集中的挑战性数学问题和TACO数据集中的复杂编码任务丰富了训练数据。这种平衡的数据混合物使模型在数学和编码领域都表现出色，恢复了AIME24的43.3%准确率，同时也提高了其编码能力。

## 未来工作

Sky-T1-32B-Preview标志着我们开发具有高级推理能力的开源模型的旅程的开始。未来，我们将专注于开发更高效的模型，以保持强大的推理性能，并探索进一步在测试时提高模型效率和准确性的先进技术。请继续关注我们在这些激动人心的计划中的进展。

## 致谢

这项工作是在[Berkeley Sky Computing Lab](https://sky.cs.berkeley.edu/)完成的，得到了[Lambda Labs](https://lambdalabs.com/service/gpu-cloud?srsltid=AfmBOop5FnmEFTkavVtdZDsLWvHWNg6peXtat-OXJ9MW5GMNsk756PE5)和[Anyscale](https://www.anyscale.com/)的出色计算支持。我们要感谢[Still-2团队](https://arxiv.org/pdf/2412.09413)和[Qwen团队](https://qwenlm.github.io/)的Junyang Lin提供的宝贵学术反馈和支持。

## 引用

```bibtex
@misc{sky_t1_2025,
  author       = {NovaSky Team},
  title        = {Sky-T1: Train your own O1 preview model within $450},
  howpublished = {https://novasky-ai.github.io/posts/sky-t1},
  note         = {Accessed: 2025-01-09},
  year         = {2025}
}
```
