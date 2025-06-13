# Open Source Language Model Benchmark

An evaluation of 43 open source language models across four distinct tasks: creative writing, logical reasoning, counterfactual causality, and programming. This benchmark aims to provide practical insights into current open source LLM capabilities and performance characteristics.

## Overview

This benchmark evaluates where we currently stand with open source language models, examining not just raw generative speed (tokens/second) but actual task completion effectiveness. A key insight from this work is that the fastest generative model is not necessarily the fastest at getting correct answers—models that over-reason or are overly verbose can be slower despite higher token generation rates.

## Testing Environment

- **Hardware**: Apple M4 Max with 128GB unified memory
- **Software**: Ollama 0.9.0 (`ollama serve`)
- **Quantization**: All models tested in q4_K_M quantization (4-bit) unless specified
- **Context Length**: Extended context window (`OLLAMA_CONTEXT_LENGTH=100000`) to handle complex reasoning tasks
- **Special Case**: Qwen3-235B-A22B tested with MLX 3-bit quantization due to memory constraints

## Models Tested (44 total)

### General Purpose Models
- **Cogito**: 3B, 8B, 14B, 32B, 70B (5 models)
- **Gemma3**: 1B, 4B, 12B, 27B (4 models)  
- **Granite3.3**: 2B, 8B (2 models)
- **Qwen3**: 0.6B, 1.7B, 8B, 32B, 30B-A3B, 235B-A22B (6 models)
- **Llama3/4**: 3.2:1B, 3.2:3B, 3.1:8B, 3.3:70B, 4:17B-Scout (5 models)

### Specialized Models
- **Coding Models**: Qwen2.5-Coder (0.5B-32B), CodeGemma, Codestral, Devstral, DeepCoder (8 models)
- **Reasoning Models**: DeepSeek-R1 (1.5B, 8B, 32B variants), Phi4 (Mini, Reasoning variants) (9 models)
- **Other**: Mistral 7B (1 model)

## Benchmark Tasks

### 1. Creative Writing ([Part 1](benchmark-part1.md))
**Task**: Generate a 5-sentence short story  
**Evaluation**: Coherence, creativity, adherence to length requirement, narrative structure

### 2. Logic Puzzle ([Part 2](benchmark-part2-light.md))
**Task**: Solve a deceptive riddle requiring careful logical reasoning  
**Evaluation**: Correct answer identification, reasoning quality, avoidance of common logical traps

### 3. Counterfactual Causality ([Part 3](benchmark-part3.md))
**Task**: Analyze a scenario involving counterfactual reasoning about causation  
**Evaluation**: Understanding of causal relationships, ability to reason about hypothetical scenarios

### 4. Python Programming ([Part 4](benchmark-part4-light.md))
**Task**: Generate a complete 3D physics simulation (bouncing ball with gravity)  
**Evaluation**: Code correctness, execution success, physics accuracy, code quality

## Key Performance Metrics

### Ollama Performance Data
Each test captures detailed performance metrics:

| Metric | Description |
|--------|-------------|
| **Total Duration** | Complete operation time (loading + processing + generation) |
| **Load Duration** | Model initialization time |
| **Prompt Eval Count/Rate** | Input processing tokens and speed |
| **Eval Count/Rate** | Output generation tokens and speed |

### Evaluation Criteria
- **Task Completion**: Did the model fulfill the specific requirements?
- **Accuracy**: Was the response factually/logically correct?
- **Efficiency**: How quickly did the model arrive at a correct solution?
- **Quality**: Overall response quality and coherence

## Key Findings

### Performance vs. Size
- Larger models don't always perform better on specific tasks
- Parameter count correlates weakly with task-specific performance
- Specialized models often outperform general-purpose models in their domain

### Speed vs. Effectiveness
- **Token Generation Speed ≠ Task Completion Speed**
- Models with extensive reasoning chains can be slower despite high tok/s rates
- Verbose models may appear productive but take longer to reach conclusions
- Concise, accurate responses often indicate better practical performance

### Architecture Insights
- Multi-modal models may have different performance characteristics due to diverse training data
- Reasoning-specialized models show improved performance on logical tasks but may over-analyze simple problems
- Code-specialized models excel at programming but may struggle with general reasoning

## Practical Implications

### Model Selection Guidelines
- **Task-Specific Performance** matters more than general benchmarks
- **Multi-Agent Systems** using different specialized models may be optimal
- **Context Requirements** significantly impact performance and should be considered
- **Resource Constraints** (memory, inference time) are practical limiting factors

### Real-World Considerations
- Quality doesn't always correlate with response length
- Different architectures excel at different task types
- Quantization impacts should be evaluated per use case
- Local deployment considerations (hardware, memory) affect model choice

## Repository Structure

```
├── README.md                      # This file
├── LICENSE                        # MIT License
├── benchmark.md                   # Summary and methodology
├── benchmark-part1.md             # Creative writing results
├── benchmark-part2-light.md       # Logic puzzle results  
├── benchmark-part3.md             # Counterfactual reasoning results
├── benchmark-part4-light.md       # Programming task results
├── mlx_chat.py                    # MLX model testing utility
└── codes/                         # Generated code samples
    ├── [model-name].py            # Programming task outputs
    └── performance_data.py        # Performance analysis
```

## Testing Tools

### MLX Chat Utility (`mlx_chat.py`)

For models that couldn't run with Ollama due to memory constraints (specifically Qwen3-235B-A22B), I provide a specialized MLX testing utility. This Python script enables testing of MLX-optimized models on Apple Silicon:

**Features:**
- Interactive chat interface for MLX models
- Configurable thinking mode and token budgets
- Support for large models (tested with 235B parameters)
- Real-time response streaming
- Conversation history management

**Usage:**
```bash
# Test with default Qwen3-30B-A3B model
python mlx_chat.py

# Test with larger model (requires ~128GB RAM)
python mlx_chat.py --model mlx-community/Qwen3-235B-A22B-3bit

# Disable thinking mode for direct responses
python mlx_chat.py --thinking-budget 0
```

**Requirements:**
- Apple Silicon Mac with sufficient memory
- MLX framework: `pip install mlx-lm`
- For 235B model: 128GB unified memory recommended

**Note:** MLX models are optimized for Apple Silicon and run ~20% faster than equivalent Ollama models, but results should be interpreted within this context when comparing performance metrics.

## Important Notes

- **Context Window Size**: Critical for complex reasoning tasks—many models perform significantly better with extended context
- **Quantization Effects**: 4-bit quantization used throughout for consistency, but performance may vary with different quantization levels
- **Hardware Specificity**: Results obtained on Apple Silicon; performance may differ on other architectures
- **Model Versions**: Specific model versions and quantizations tested—results may not generalize to other versions

## Acknowledgments

This benchmark was made possible by the incredible work of the open source community:

### Model Developers
I extend my gratitude to all the organizations and researchers who have made their language models freely available:
- **Alibaba** (Qwen series)
- **Google** (Gemma series)
- **Meta** (Llama series)
- **Microsoft** (Phi series)
- **IBM** (Granite series)
- **Mistral AI** (Mistral, Codestral, Devstral)
- **DeepSeek** (DeepSeek-R1 series)
- **DeepCogito** (Cogito series)
- **And all other contributors** to the open source LLM ecosystem

### Infrastructure and Tools
- **[Ollama](https://ollama.ai/)** - For providing an excellent local LLM serving platform that made testing 40+ models seamless
- **[Apple MLX](https://github.com/ml-explore/mlx)** - For the MLX framework enabling efficient inference on Apple Silicon
- **[MLX-LM](https://github.com/ml-explore/mlx-examples/tree/main/llms)** - For the high-level MLX interface used in our custom testing utility
- **[Hugging Face](https://huggingface.co/)** - For hosting and distributing the quantized models

### Hardware
- **Apple** - For the M4 Max chip and unified memory architecture that enabled testing of large models locally

### Analysis and Documentation
- The open source AI community's collaborative spirit makes research like this possible. These benchmarks aim to contribute back to the community by providing practical performance insights.

- Claude 4 Sonnet, for its valuable assistance in analyzing benchmark results, identifying data inconsistencies, and helping to structure comprehensive documentation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this benchmark in your research or analysis, please reference this repository and note the specific testing conditions (hardware, software versions, quantization levels) as they significantly impact results.

---

*This benchmark provides a snapshot of open source LLM capabilities as of the testing date. The rapidly evolving nature of this field means results should be interpreted within their temporal and technical context.* 
