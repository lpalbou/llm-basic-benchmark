# Experiments with various Open Source SLM/LLM (Part 1)

## Notes
- Experiment on M4 Max 128gb memory.
- Ollama 0.9.0, `ollama serve`
- All models in q4_K_M versions
- Warning : effect of context size, huge
- `OLLAMA_CONTEXT_LENGTH=100000 ollama serve`to increase default context size, otherwise API params `n_ctx` and `n_ctx_per_seq` 
- Understanding = clarity = less tokens / words needed to reason/explain ? eg why qwen3:0.6b, while being the fastest generative LLM is not the fastest (lost in too many simplistic reasoning) : check if that's true
- Important insight : the fastest SLM/LLM is not necessarily the fastest GENERATIVE model, but the one who gets the answer right the fastest (issue of evaluating the prompt + context AND how much reasoning is needed to get the answer)
- Note about riddles : larger models already know the answer to similar puzzles; in a way, you could say they have been trained on this, so it's easier to solve.
- Model at Xb parameters : consider if they are multi-modal or not. Eg cogito:8b vs qwen3:8b. Multi-modal = you have to fit more diverse information and scenarios in your network.
- Knowing what you need can help you chose the best model for your use case. Don't be afraid to use SEVERAL models in one application. Multi-agent systems are gonna become the norm.
- Like for humans, you can be very right with a few words or very wrong with a lot of words. The size of the answer (or amount of reasoning) doesn't necessarily correlate with the quality of the answer


## Test sequence

I selected a large number of models and from various sizes. Some are general-purpose (gemma, cogito, qwen), other are supposedly better at reasoning (phi4*-reasoning, deepseek-r1), and others at coding (eg qwen2.5-coder, deepcoder, codestral, etc).

### Cogito architecture
- ollama run cogito:3b --verbose
- ollama run cogito:8b --verbose
- ollama run cogito:14b --verbose
- ollama run cogito:32b --verbose
- ollama run cogito:70b --verbose

### Gemma3 architecture
- ollama run gemma3:1b --verbose
- ollama run gemma3:4b --verbose
- ollama run gemma3:12b --verbose
- ollama run gemma3:27b --verbose

### Granite3.3 architecture
- ollama run granite3.3:2b --verbose
- ollama run granite3.3:8b --verbose

### Qwen3 architecture
- ollama run qwen3:0.6b --verbose
- ollama run qwen3:1.7b --verbose
- ollama run qwen3:8b --verbose
- ollama run qwen3:32b --verbose
- ollama run qwen3:30b-a3b-q4_K_M --verbose

### Llama3&4 architecture
- ollama run llama3.2:1b --verbose
- ollama run llama3.2:3b --verbose
- ollama run llama3.1:8b --verbose
- ollama run llama3.3:70b-instruct-q4_K_M --verbose
- ollama run llama4:17b-scout-16e-instruct-q4_K_M --verbose

### Dedicated coders
- ollama run qwen2.5-coder:0.5b --verbose
- ollama run qwen2.5-coder:3b --verbose
- ollama run qwen2.5-coder:7b --verbose
- ollama run qwen2.5-coder:14b --verbose
- ollama run qwen2.5-coder:32b-instruct-q4_K_M --verbose
- ollama run codegemma:latest --verbose
- ollama run mistral:7b --verbose
- ollama run codestral:22b --verbose
- ollama run devstral:24b --verbose
- ollama run deepcoder:1.5b --verbose
- ollama run deepcoder:14b --verbose

### Deepseek-r1 architecture
- ollama run deepseek-r1:1.5b --verbose
- ollama run deepseek-r1:8b --verbose
- ollama run deepseek-r1:32b-qwen-distill-q4_K_M --verbose
- ollama run deepseek-r1:8b-0528-qwen3-q4_K_M --verbose
- ollama run deepseek-r1:8b-0528-qwen3-q8_0 --verbose

### Phi4 architecture
- ollama run phi4-mini:3.8b --verbose
- ollama run phi4-mini-reasoning:3.8b --verbose
- ollama run phi4-reasoning:14b-q4_K_M --verbose
- ollama run phi4-reasoning:14b-plus-q4_K_M --verbose

### Qwen3-235b-a22b

The 4bit quantization could not run on M4 Max 128gb, so I ran the 3bit quantization (https://huggingface.co/mlx-community/Qwen3-235B-A22B-3bit). The 3bit was not available with Ollama and only available for MLX architecture, so I created a small [mlx_chat.py](mlx_chat.py) capable of reading mlx model. In addition, I had to deactivate the thinking mode as otherwise it generates too many tokens and had some issues with repetitive generations. Qwen models have indeed a tendency to overthink, like deepseek.

A MLX model is optimized for the Apple Silicon, so it is not a 1:1 comparison with other models. The MLX version is expected to run ~20% faster than the same regular version with ollama. Speed should not be interpreted directly but I thought it would be interesting to integrate this model in the benchmark as it is the largest one that could run.

Additional note : if you try it yourself, you need 128gb memory. Be sure to free as much memory as you can.

## Ollama Performance Metrics

| Metric | Description | Example |
|--------|-------------|---------|
| total duration | Total time taken for the entire operation, from start to finish | 5.257125167s |
| load duration | Time required to initialize or load the model into memory | 40.230375ms |
| prompt eval count | Number of tokens in the input prompt sent to the model | 16 token(s) |
| prompt eval duration | Time spent processing the input prompt before generation starts | 693.915875ms |
| prompt eval rate | Speed at which the model processes prompt tokens (tokens per second) | 23.06 tokens/s |
| eval count | Number of tokens generated by the model as output | 104 token(s) |
| eval duration | Time taken to generate the output tokens | 4.522549875s |
| eval rate | Speed of output token generation (tokens per second) | 23.00 tokens/s |


## Evaluation Criteria
- did the model do what it was supposed to do ?
- where the specific details respected (eg X sentences) ?
- did the model answer correctly ?
- did the model fall into some traps ?
- how fast did it get the answer ?
- impact of various parameters (size, architecture, reasoning, quantization - one case only)


## Benchmark Structure

- [Part 1 : Text Generation](benchmark-part1.md)
- [Part 2 : Deceptive Logic Puzzle](benchmark-part2.md)
- [Part 3 : Counterfactual Causality](benchmark-part3.md)
- [Part 4 : Python Programming](benchmark-part4.md)