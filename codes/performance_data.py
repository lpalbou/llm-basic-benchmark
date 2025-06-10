"""
Performance data extracted from the benchmark results
"""

# Performance metrics from the benchmarks
# Format: model_name: {test_name: {metric: value}}

performance_data = {
    # Part 1: Text Generation (5-sentence short story)
    "cogito:3b": {
        "text_generation": {
            "eval_rate": 129.92,  # tokens/s
            "total_duration": 2.37,  # seconds
            "quality": "good",
            "word_count": 180,
            "success": True
        }
    },
    "cogito:8b": {
        "text_generation": {
            "eval_rate": 71.76,
            "total_duration": 4.24,
            "quality": "good",
            "word_count": 159,
            "success": True
        }
    },
    "cogito:14b": {
        "text_generation": {
            "eval_rate": 40.96,
            "total_duration": 3.88,
            "quality": "good",
            "word_count": 141,
            "success": True
        }
    },
    "cogito:32b": {
        "text_generation": {
            "eval_rate": 20.31,
            "total_duration": 14.05,
            "quality": "good",
            "word_count": 120,
            "success": True
        }
    },
    "cogito:70b": {
        "text_generation": {
            "eval_rate": 9.01,
            "total_duration": 38.45,
            "quality": "good",
            "word_count": 197,
            "success": True
        }
    },
    "gemma3:1b": {
        "text_generation": {
            "eval_rate": 192.72,
            "total_duration": 0.69,
            "quality": "good",
            "word_count": 112,
            "success": True
        }
    },
    "gemma3:4b": {
        "text_generation": {
            "eval_rate": 99.54,
            "total_duration": 1.42,
            "quality": "good",
            "word_count": 110,
            "success": True
        }
    },
    "gemma3:12b": {
        "text_generation": {
            "eval_rate": 45.25,
            "total_duration": 2.27,
            "quality": "good",
            "word_count": 86,
            "success": True
        }
    },
    "gemma3:27b": {
        "text_generation": {
            "eval_rate": 23.00,
            "total_duration": 5.26,
            "quality": "good",
            "word_count": 104,
            "success": True
        }
    },
    "granite3.3:2b": {
        "text_generation": {
            "eval_rate": 133.35,
            "total_duration": 2.60,
            "quality": "good",
            "word_count": 187,
            "success": True
        }
    },
    "granite3.3:8b": {
        "text_generation": {
            "eval_rate": 65.70,
            "total_duration": 5.94,
            "quality": "good",
            "word_count": 125,
            "success": True
        }
    },
    "qwen3:0.6b": {
        "text_generation": {
            "eval_rate": 267.72,
            "total_duration": 1.30,
            "quality": "good with thinking",
            "word_count": 257,
            "success": True
        }
    },
    "qwen3:1.7b": {
        "text_generation": {
            "eval_rate": 168.73,
            "total_duration": 3.58,
            "quality": "good with thinking",
            "word_count": 500,
            "success": True
        }
    },
    "qwen3:8b": {
        "text_generation": {
            "eval_rate": 65.93,
            "total_duration": 5.84,
            "quality": "good with thinking",
            "word_count": 240,
            "success": True
        }
    },
    "qwen3:32b": {
        "text_generation": {
            "eval_rate": 18.12,
            "total_duration": 31.69,
            "quality": "good with thinking",
            "word_count": 430,
            "success": True
        }
    },
    "qwen3:30b-a3b": {
        "text_generation": {
            "eval_rate": 78.41,
            "total_duration": 4.44,
            "quality": "good with thinking",
            "word_count": 306,
            "success": True
        }
    },
    "qwen3-235b-a22b-3bit": {
        "text_generation": {
            "eval_rate": 32.317,
            "total_duration": 2.87,  # calculated from tokens
            "quality": "good",
            "word_count": 93,
            "success": True
        }
    },
    "llama3.2:1b": {
        "text_generation": {
            "eval_rate": 218.92,
            "total_duration": 0.68,
            "quality": "good",
            "word_count": 127,
            "success": True
        }
    },
    "llama3.2:3b": {
        "text_generation": {
            "eval_rate": 131.95,
            "total_duration": 1.84,
            "quality": "good",
            "word_count": 120,
            "success": True
        }
    },
    "llama3.1:8b": {
        "text_generation": {
            "eval_rate": 73.10,
            "total_duration": 2.01,
            "quality": "good",
            "word_count": 128,
            "success": True
        }
    },
    "llama3.3:70b": {
        "text_generation": {
            "eval_rate": 9.63,
            "total_duration": 15.36,
            "quality": "good",
            "word_count": 136,
            "success": True
        }
    },
    "llama4:17b-scout": {
        "text_generation": {
            "eval_rate": 31.20,
            "total_duration": 12.21,
            "quality": "good",
            "word_count": 125,
            "success": True
        }
    },
    "qwen2.5-coder:0.5b": {
        "text_generation": {
            "eval_rate": 282.90,
            "total_duration": 0.64,
            "quality": "poor",
            "word_count": 152,
            "success": False  # Not coherent
        }
    },
    "qwen2.5-coder:3b": {
        "text_generation": {
            "eval_rate": 124.59,
            "total_duration": 0.78,
            "quality": "fair",
            "word_count": 79,
            "success": True
        }
    },
    "qwen2.5-coder:7b": {
        "text_generation": {
            "eval_rate": 77.24,
            "total_duration": 1.45,
            "quality": "good",
            "word_count": 92,
            "success": True
        }
    },
    "qwen2.5-coder:14b": {
        "text_generation": {
            "eval_rate": 40.85,
            "total_duration": 3.84,
            "quality": "good",
            "word_count": 136,
            "success": True
        }
    },
    "qwen2.5-coder:32b": {
        "text_generation": {
            "eval_rate": 20.19,
            "total_duration": 12.45,
            "quality": "good",
            "word_count": 93,
            "success": True
        }
    },
    "codegemma": {
        "text_generation": {
            "eval_rate": 74.48,
            "total_duration": 2.95,
            "quality": "good",
            "word_count": 65,
            "success": True
        }
    },
    "mistral:7b": {
        "text_generation": {
            "eval_rate": 87.65,
            "total_duration": 1.69,
            "quality": "good",
            "word_count": 127,
            "success": True
        }
    },
    "codestral:22b": {
        "text_generation": {
            "eval_rate": 31.38,
            "total_duration": 12.09,
            "quality": "verbose",
            "word_count": 226,
            "success": True
        }
    },
    "devstral:24b": {
        "text_generation": {
            "eval_rate": 22.49,
            "total_duration": 15.80,
            "quality": "good",
            "word_count": 129,
            "success": True
        }
    },
    "deepcoder:1.5b": {
        "text_generation": {
            "eval_rate": 189.25,
            "total_duration": 1.31,
            "quality": "good with thinking",
            "word_count": 226,
            "success": True
        }
    },
    "deepcoder:14b": {
        "text_generation": {
            "eval_rate": 40.18,
            "total_duration": 13.60,
            "quality": "good with thinking",
            "word_count": 402,
            "success": True
        }
    },
    "deepseek-r1:1.5b": {
        "text_generation": {
            "eval_rate": 184.34,
            "total_duration": 2.22,
            "quality": "good with thinking",
            "word_count": 390,
            "success": True
        }
    },
    "deepseek-r1:8b": {
        "text_generation": {
            "eval_rate": 65.02,
            "total_duration": 4.68,
            "quality": "good with thinking",
            "word_count": 283,
            "success": True
        }
    },
    "deepseek-r1:32b": {
        "text_generation": {
            "eval_rate": 16.81,
            "total_duration": 68.08,
            "quality": "good with long thinking",
            "word_count": 1132,
            "success": True
        }
    },
    "deepseek-r1:8b-0528-qwen3-q4": {
        "text_generation": {
            "eval_rate": 65.17,
            "total_duration": 7.04,
            "quality": "good with thinking",
            "word_count": 322,
            "success": True
        }
    },
    "deepseek-r1:8b-0528-qwen3-q8": {
        "text_generation": {
            "eval_rate": 46.96,
            "total_duration": 8.76,
            "quality": "good with thinking",
            "word_count": 395,
            "success": True
        }
    },
    "phi4-mini:3.8b": {
        "text_generation": {
            "eval_rate": 102.33,
            "total_duration": 2.14,
            "quality": "good",
            "word_count": 200,
            "success": True
        }
    },
    "phi4-mini-reasoning:3.8b": {
        "text_generation": {
            "eval_rate": 88.57,
            "total_duration": 4.85,
            "quality": "good with thinking",
            "word_count": 410,
            "success": True
        }
    },
    "phi4-reasoning:14b": {
        "text_generation": {
            "eval_rate": 30.66,
            "total_duration": 45.20,
            "quality": "good with long thinking",
            "word_count": 1347,
            "success": True
        }
    },
    "phi4-reasoning:14b-plus": {
        "text_generation": {
            "eval_rate": 29.64,
            "total_duration": 68.52,
            "quality": "good with long thinking",
            "word_count": 1881,
            "success": True
        }
    }
}

# Part 2: Logic Puzzle Results (Two Guards)
logic_puzzle_results = {
    "cogito:3b": {"correct": False, "reasoning": "complex but incorrect"},
    "cogito:8b": {"correct": True, "reasoning": "clear and correct"},
    "cogito:14b": {"correct": True, "reasoning": "clear and correct"},
    "cogito:32b": {"correct": True, "reasoning": "clear and correct"},
    "cogito:70b": {"correct": True, "reasoning": "clear and correct"},
    "gemma3:1b": {"correct": True, "reasoning": "correct but explanation issues"},
    "gemma3:4b": {"correct": True, "reasoning": "clear and correct"},
    "gemma3:12b": {"correct": True, "reasoning": "detailed and correct"},
    "gemma3:27b": {"correct": True, "reasoning": "clear and correct"},
    "granite3.3:2b": {"correct": False, "reasoning": "incorrect approach"},
    "granite3.3:8b": {"correct": True, "reasoning": "correct"},
    "qwen3:0.6b": {"correct": False, "reasoning": "infinite loop/incorrect"},
    "qwen3:1.7b": {"correct": True, "reasoning": "correct with long thinking"},
    "qwen3:8b": {"correct": True, "reasoning": "detailed correct"},
    "qwen3:32b": {"correct": True, "reasoning": "very detailed correct"},
    "qwen3:30b-a3b": {"correct": True, "reasoning": "detailed correct"},
    "qwen3-235b-a22b-3bit": {"correct": True, "reasoning": "clear and correct"},
    "llama3.2:1b": {"correct": False, "reasoning": "confused"},
    "llama3.2:3b": {"correct": False, "reasoning": "incorrect approach"},
    "llama3.1:8b": {"correct": False, "reasoning": "incorrect logic"},
    "llama3.3:70b": {"correct": True, "reasoning": "correct"},
    "llama4:17b-scout": {"correct": True, "reasoning": "correct"},
    "qwen2.5-coder:0.5b": {"correct": False, "reasoning": "very confused"},
    "qwen2.5-coder:3b": {"correct": False, "reasoning": "incorrect"},
    "qwen2.5-coder:7b": {"correct": True, "reasoning": "correct"},
    "qwen2.5-coder:14b": {"correct": True, "reasoning": "correct"},
    "qwen2.5-coder:32b": {"correct": True, "reasoning": "correct"},
    "deepcoder:1.5b": {"correct": False, "reasoning": "incorrect with long thinking"},
    "deepcoder:14b": {"correct": True, "reasoning": "correct but verbose"},
    "deepseek-r1:1.5b": {"correct": True, "reasoning": "correct with thinking"},
    "deepseek-r1:8b": {"correct": False, "reasoning": "gibberish output"},
    "deepseek-r1:32b": {"correct": True, "reasoning": "correct with long thinking"},
    "deepseek-r1:8b-0528-qwen3-q4": {"correct": False, "reasoning": "long thinking incomplete"},
    "deepseek-r1:8b-0528-qwen3-q8": {"correct": False, "reasoning": "long thinking incomplete"},
    "phi4-mini:3.8b": {"correct": True, "reasoning": "correct"},
    "phi4-mini-reasoning:3.8b": {"correct": True, "reasoning": "correct with thinking"},
    "phi4-reasoning:14b": {"correct": True, "reasoning": "correct with long thinking"},
    "phi4-reasoning:14b-plus": {"correct": True, "reasoning": "correct with long thinking"}
}

# Part 3: Counterfactual Causality Results
counterfactual_results = {
    "cogito:3b": {"correct": True, "reasoning": "identifies alternative causes"},
    "cogito:8b": {"correct": True, "reasoning": "identifies false dilemma"},
    "cogito:14b": {"correct": False, "reasoning": "uses contrapositive incorrectly"},
    "cogito:32b": {"correct": True, "reasoning": "explains uncertainty well"},
    "cogito:70b": {"correct": True, "reasoning": "good logical analysis"},
    "gemma3:1b": {"correct": False, "reasoning": "falls for the trap"},
    "gemma3:4b": {"correct": False, "reasoning": "modus tollens misapplied"},
    "gemma3:12b": {"correct": False, "reasoning": "modus tollens misapplied"},
    "gemma3:27b": {"correct": False, "reasoning": "modus tollens misapplied"},
    "granite3.3:2b": {"correct": False, "reasoning": "too simple"},
    "granite3.3:8b": {"correct": True, "reasoning": "good analysis"},
    "qwen3:0.6b": {"correct": False, "reasoning": "incorrect with thinking"},
    "qwen3:1.7b": {"correct": False, "reasoning": "falls for contrapositive"},
    "qwen3:8b": {"correct": False, "reasoning": "detailed but wrong"},
    "qwen3:32b": {"correct": False, "reasoning": "very detailed but wrong"},
    "qwen3:30b-a3b": {"correct": False, "reasoning": "detailed contrapositive error"},
    "qwen3-235b-a22b-3bit": {"correct": False, "reasoning": "uses contrapositive incorrectly"},
    "llama3.2:1b": {"correct": True, "reasoning": "surprisingly nuanced"},
    "llama3.2:3b": {"correct": False, "reasoning": "too simple"},
    "llama3.1:8b": {"correct": True, "reasoning": "identifies other factors"},
    "llama3.3:70b": {"correct": True, "reasoning": "good analysis"},
    "llama4:17b-scout": {"correct": True, "reasoning": "identical to llama3.3"},
    "qwen2.5-coder:0.5b": {"correct": False, "reasoning": "confused"},
    "qwen2.5-coder:3b": {"correct": False, "reasoning": "too simple"},
    "qwen2.5-coder:7b": {"correct": False, "reasoning": "modus ponens error"},
    "qwen2.5-coder:14b": {"correct": False, "reasoning": "modus ponens error"},
    "qwen2.5-coder:32b": {"correct": True, "reasoning": "identifies other factors"},
    "codegemma": {"correct": True, "reasoning": "brief but correct"},
    "mistral:7b": {"correct": False, "reasoning": "hedges but leans wrong"},
    "codestral:22b": {"correct": True, "reasoning": "first yes then correctly no"},
    "devstral:24b": {"correct": True, "reasoning": "clear and correct"},
    "deepcoder:1.5b": {"correct": False, "reasoning": "long thinking but wrong"},
    "deepcoder:14b": {"correct": False, "reasoning": "very long but wrong"},
    "deepseek-r1:1.5b": {"correct": False, "reasoning": "thinking but wrong"},
    "deepseek-r1:8b": {"correct": False, "reasoning": "interrupted/incomplete"},
    "deepseek-r1:32b": {"correct": False, "reasoning": "long thinking wrong"},
    "phi4-mini:3.8b": {"correct": True, "reasoning": "mentions rainfall"},
    "phi4-mini-reasoning:3.8b": {"correct": False, "reasoning": "extremely long wrong"},
    "phi4-reasoning:14b": {"correct": True, "reasoning": "careful analysis"},
    "phi4-reasoning:14b-plus": {"correct": True, "reasoning": "very detailed correct"}
}

# Part 4: Programming Task Results
programming_results = {
    "cogito:3b": {"success": False, "issues": "syntax errors, didn't work after fix"},
    "cogito:8b": {"success": False, "issues": "triangle explodes, ball flies away"},
    "cogito:14b": {"success": False, "issues": "triangle morphs, ball bounces off screen"},
    "cogito:32b": {"success": True, "issues": "partial - ball escapes sometimes", "attempts": 3},
    "cogito:70b": {"success": False, "issues": "ball stuck on edge", "attempts": 3},
    "gemma3:1b": {"success": False, "issues": "didn't work"},
    "gemma3:4b": {"success": False, "issues": "didn't work"},
    "gemma3:12b": {"success": False, "issues": "triangle rotates wrong, ball escapes"},
    "gemma3:27b": {"success": False, "issues": "ball bounces wrong axis"},
    "granite3.3:2b": {"success": False, "issues": "crashed"},
    "granite3.3:8b": {"success": False, "issues": "didn't work"},
    "qwen3:32b": {"success": False, "issues": "only provided collision code, not full program"},
    "qwen3:30b-a3b": {"success": False, "issues": "ball stuck on edge"},
    "qwen3-235b-a22b-3bit": {"success": True, "issues": "partial - ball escapes after time", "attempts": 3},
    "llama3.3:70b": {"success": True, "issues": "works correctly", "attempts": 3},
    "llama4:17b-scout": {"success": True, "issues": "partial - ball escapes sometimes"},
    "qwen2.5-coder:32b": {"success": False, "issues": "incomplete code"}
}