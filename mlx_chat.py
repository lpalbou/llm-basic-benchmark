#!/usr/bin/env python3
"""
MLX Chat Application for Qwen3 Models

A command-line chat interface for running Qwen3 models using Apple's MLX framework.
Supports model selection, configurable context size, and interactive conversations.
"""

import argparse
import sys
import time
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

try:
    from mlx_lm import load, generate, stream_generate
except ImportError:
    print("Error: mlx-lm is not installed. Please install it with: pip install mlx-lm")
    sys.exit(1)


@dataclass
class GenerationStats:
    """Statistics for model generation"""
    
    total_duration: float = 0.0
    load_duration: float = 0.0
    prompt_eval_count: int = 0
    prompt_eval_duration: float = 0.0
    eval_count: int = 0
    eval_duration: float = 0.0
    
    @property
    def prompt_eval_rate(self) -> float:
        """Calculate prompt evaluation rate (tokens/s)"""
        if self.prompt_eval_duration > 0:
            return self.prompt_eval_count / self.prompt_eval_duration
        return 0.0
    
    @property
    def eval_rate(self) -> float:
        """Calculate evaluation rate (tokens/s)"""
        if self.eval_duration > 0:
            return self.eval_count / self.eval_duration
        return 0.0
    
    def format_ollama_style(self) -> str:
        """Format stats in ollama style"""
        return f"""total duration:       {self.total_duration:.9f}s
load duration:        {self.load_duration * 1000:.6f}ms
prompt eval count:    {self.prompt_eval_count} token(s)
prompt eval duration: {self.prompt_eval_duration:.9f}s
prompt eval rate:     {self.prompt_eval_rate:.2f} tokens/s
eval count:           {self.eval_count} token(s)
eval duration:        {self.eval_duration:.9f}s
eval rate:            {self.eval_rate:.2f} tokens/s"""


def check_model_cached(model_name: str) -> bool:
    """Check if model is cached locally in HuggingFace cache"""
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    
    # Convert model name to expected cache format
    # mlx-community/Qwen3-30B-A3B-4bit -> models--mlx-community--Qwen3-30B-A3B-4bit
    cache_model_name = "models--" + model_name.replace("/", "--")
    model_cache_path = cache_dir / cache_model_name
    
    return model_cache_path.exists() and any(model_cache_path.iterdir())


@dataclass
class ModelConfig:
    """Configuration for the MLX model"""
    
    model_name: str = "mlx-community/Qwen3-30B-A3B-4bit"
    max_tokens: int = 12288  # 12k output
    max_kv_size: int = 16384  # 16k context
    temperature: float = 0.7
    top_p: float = 0.9
    enable_thinking: bool = True
    thinking_budget: int = 2048  # 2k tokens for thinking
    verbose: bool = True
    
    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "ModelConfig":
        """Create configuration from command line arguments"""
        return cls(
            model_name=args.model,
            max_tokens=args.max_tokens,
            max_kv_size=args.max_kv_size,
            temperature=args.temperature,
            top_p=args.top_p,
            enable_thinking=args.enable_thinking,
            thinking_budget=args.thinking_budget,
            verbose=args.verbose
        )
    
    def validate(self) -> None:
        """Validate configuration parameters"""
        if self.max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        if self.max_kv_size <= 0:
            raise ValueError("max_kv_size must be positive")
        if not 0 <= self.temperature <= 2:
            raise ValueError("temperature must be between 0 and 2")
        if not 0 <= self.top_p <= 1:
            raise ValueError("top_p must be between 0 and 1")
        if self.thinking_budget < 0:
            raise ValueError("thinking_budget must be non-negative")


class MLXModel:
    """Wrapper for MLX model and tokenizer"""
    
    def __init__(self, config: ModelConfig):
        """Initialize the model wrapper with configuration"""
        self.config = config
        self.model = None
        self.tokenizer = None
        self.conversation_history: List[Dict[str, str]] = []
        self.load_duration = 0.0  # Track model load time
        
    def load_model(self) -> None:
        """Load the MLX model and tokenizer"""
        print(f"Loading model: {self.config.model_name}")
        
        # Check if model is cached
        is_cached = check_model_cached(self.config.model_name)
        if is_cached:
            print("Model found in local cache")
        else:
            print("Model not found in local cache - downloading...")
            print("This may take several minutes depending on model size and connection speed...")
        
        load_start = time.time()
        
        try:
            # Load model with proper tokenizer config for Qwen
            self.model, self.tokenizer = load(
                self.config.model_name,
                tokenizer_config={
                    "eos_token": "<|endoftext|>",
                    "trust_remote_code": True
                }
            )
            self.load_duration = time.time() - load_start
            
            print(f"Model loaded successfully! (took {self.load_duration:.2f}s)")
            print(f"Max output: {self.config.max_tokens} tokens")
            print(f"Note: Advanced parameters (temperature, top_p) not yet implemented")
            print()
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def add_to_history(self, role: str, content: str) -> None:
        """Add a message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
    
    def format_messages(self) -> str:
        """Format messages for model input using chat template"""
        if not self.tokenizer.chat_template:
            # Fallback formatting if no chat template
            formatted = ""
            for msg in self.conversation_history:
                if msg["role"] == "user":
                    formatted += f"User: {msg['content']}\n"
                elif msg["role"] == "assistant":
                    formatted += f"Assistant: {msg['content']}\n"
            return formatted + "Assistant: "
        
        # Use tokenizer's chat template
        try:
            # Try with enable_thinking parameter for Qwen3 models
            return self.tokenizer.apply_chat_template(
                self.conversation_history,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=self.config.enable_thinking
            )
        except TypeError:
            # Fallback without enable_thinking for other models
            return self.tokenizer.apply_chat_template(
                self.conversation_history,
                tokenize=False,
                add_generation_prompt=True
            )
    
    def generate_response(self, prompt: str) -> Tuple[str, GenerationStats]:
        """Generate a response for the given prompt and return stats"""
        generation_start = time.time()
        
        # Add user message to history
        self.add_to_history("user", prompt)
        
        # Format messages and track prompt evaluation
        prompt_eval_start = time.time()
        formatted_prompt = self.format_messages()
        
        # Count prompt tokens
        prompt_tokens = self.tokenizer.encode(formatted_prompt)
        prompt_eval_duration = time.time() - prompt_eval_start
        
        # Generate response using stream_generate with real-time output
        full_response = ""
        thinking_tokens = 0
        in_thinking = False
        thinking_content = ""
        actual_response = ""
        thinking_truncated = False
        output_tokens = 0
        
        eval_start = time.time()
        
        # Use stream_generate which supports max_tokens
        for response in stream_generate(
            self.model,
            self.tokenizer,
            prompt=formatted_prompt,
            max_tokens=self.config.max_tokens
        ):
            if response.text:
                full_response += response.text
                output_tokens += 1  # Approximate token count
                
                # Track thinking state
                if "<think>" in response.text and self.config.enable_thinking:
                    in_thinking = True
                    # Print think tag if we're still under budget
                    if thinking_tokens < self.config.thinking_budget:
                        print(response.text, end="", flush=True)
                elif "</think>" in response.text and self.config.enable_thinking:
                    in_thinking = False
                    # Only print if we haven't exceeded budget
                    if thinking_tokens < self.config.thinking_budget:
                        print(response.text, end="", flush=True)
                    elif not thinking_truncated:
                        print("\n[Thinking truncated - exceeded budget of {} tokens]".format(
                            self.config.thinking_budget), end="", flush=True)
                        thinking_truncated = True
                elif in_thinking:
                    thinking_tokens += 1
                    thinking_content += response.text
                    # Only print thinking content if under budget
                    if thinking_tokens <= self.config.thinking_budget:
                        print(response.text, end="", flush=True)
                    elif thinking_tokens == self.config.thinking_budget + 1:
                        print("\n[... thinking continues but hidden due to token budget ...]", 
                              end="", flush=True)
                else:
                    # Regular response content
                    actual_response += response.text
                    print(response.text, end="", flush=True)
        
        eval_duration = time.time() - eval_start
        total_duration = time.time() - generation_start
        
        # Print newline after generation completes
        print()
        
        # If thinking was enabled, show stats
        if self.config.enable_thinking and thinking_content:
            print(f"\n[Thinking used {thinking_tokens} tokens out of {self.config.thinking_budget} budget]")
        
        # Extract the actual response (remove thinking if present)
        if self.config.enable_thinking and "<think>" in full_response:
            # Remove thinking content
            parts = full_response.split("</think>")
            if len(parts) > 1:
                clean_response = parts[-1].strip()
            else:
                clean_response = actual_response.strip()
        else:
            clean_response = full_response
        
        # Add assistant response to history (without thinking)
        self.add_to_history("assistant", clean_response)
        
        # Create generation stats
        stats = GenerationStats(
            total_duration=total_duration,
            load_duration=self.load_duration,
            prompt_eval_count=len(prompt_tokens),
            prompt_eval_duration=prompt_eval_duration,
            eval_count=output_tokens,
            eval_duration=eval_duration
        )
        
        return clean_response, stats


class ChatInterface:
    """Command-line chat interface"""
    
    def __init__(self, model_wrapper: MLXModel):
        """Initialize chat interface with model wrapper"""
        self.model_wrapper = model_wrapper
        self.running = True
        
    def display_welcome(self) -> None:
        """Display welcome message"""
        print("=" * 60)
        print("MLX Chat - Qwen3 Model Interface")
        print("=" * 60)
        print("Type 'help' for commands, 'quit' to exit")
        print()
    
    def display_help(self) -> None:
        """Display help message"""
        print("\nAvailable commands:")
        print("  help     - Show this help message")
        print("  clear    - Clear conversation history")
        print("  quit, exit, /q, /quit, /exit - Exit the chat")
        print("  info     - Show model information")
        print()
    
    def process_command(self, command: str) -> bool:
        """Process special commands. Returns True if command was processed."""
        command = command.lower().strip()
        
        if command in ["quit", "exit", "/q", "/quit", "/exit"]:
            self.running = False
            return True
        elif command == "help":
            self.display_help()
            return True
        elif command == "clear":
            self.model_wrapper.clear_history()
            print("Conversation history cleared.")
            return True
        elif command == "info":
            print(f"\nModel: {self.model_wrapper.config.model_name}")
            print(f"Max output: {self.model_wrapper.config.max_tokens} tokens")
            print(f"Temperature: {self.model_wrapper.config.temperature} (not yet implemented)")
            print(f"Top-p: {self.model_wrapper.config.top_p} (not yet implemented)")
            print(f"Context size: {self.model_wrapper.config.max_kv_size} tokens (not yet implemented)")
            print(f"Verbose stats: {'Enabled' if self.model_wrapper.config.verbose else 'Disabled'}")
            print(f"Thinking mode: {'Enabled' if self.model_wrapper.config.enable_thinking else 'Disabled'}")
            if self.model_wrapper.config.enable_thinking:
                print(f"Thinking budget: {self.model_wrapper.config.thinking_budget} tokens")
            print()
            return True
        
        return False
    
    def format_response(self, response: str) -> str:
        """Format model response for display"""
        # Simple formatting - can be extended
        return response.strip()
    
    def run(self) -> None:
        """Run the main chat loop"""
        self.display_welcome()
        
        while self.running:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()
                
                # Check for empty input
                if not user_input:
                    continue
                
                # Process commands
                if self.process_command(user_input):
                    continue
                
                # Generate response
                print("\nAssistant: ", end="", flush=True)
                
                # The response will be streamed directly in generate_response
                response, stats = self.model_wrapper.generate_response(user_input)
                
                # Show stats if verbose mode is enabled
                if self.model_wrapper.config.verbose:
                    print(f"\n{stats.format_ollama_style()}")
                
            except KeyboardInterrupt:
                print("\n\nInterrupted. Type 'quit' to exit.")
                continue
            except Exception as e:
                print(f"\nError: {e}")
                continue
        
        print("\nGoodbye!")


class Application:
    """Main application class"""
    
    def __init__(self):
        """Initialize application"""
        self.config: Optional[ModelConfig] = None
        self.model: Optional[MLXModel] = None
        self.interface: Optional[ChatInterface] = None
    
    def setup(self, args: argparse.Namespace) -> None:
        """Setup application components"""
        # Create configuration
        self.config = ModelConfig.from_args(args)
        self.config.validate()
        
        # Create model wrapper
        self.model = MLXModel(self.config)
        self.model.load_model()
        
        # Create chat interface
        self.interface = ChatInterface(self.model)
    
    def run(self) -> None:
        """Run the application"""
        if self.interface:
            self.interface.run()


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="MLX Chat - Interactive chat with Qwen3 models",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="mlx-community/Qwen3-30B-A3B-4bit",
        help="Model to use (e.g., mlx-community/Qwen3-235B-A22B-3bit)"
    )
    
    parser.add_argument(
        "--thinking-budget",
        type=int,
        default=0,
        help="Maximum tokens allowed for thinking mode (default: 0, the strategy is not really working; if you activate, it will think as much as it needs)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Show detailed timing and token statistics after each response (ollama-style)"
    )
    
    parser.add_argument(
        "--quiet",
        dest="verbose",
        action="store_false",
        help="Disable verbose output (opposite of --verbose)"
    )
    
    # These parameters are kept for future implementation
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=12288,
        help="Maximum number of output tokens"
    )
    
    parser.add_argument(
        "--max-kv-size",
        type=int,
        default=16384,
        help="Maximum KV cache size / context length (not yet implemented)"
    )
    
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature 0.0-2.0 (not yet implemented)"
    )
    
    parser.add_argument(
        "--top-p",
        type=float,
        default=0.9,
        help="Top-p sampling parameter 0.0-1.0 (not yet implemented)"
    )
    
    args = parser.parse_args()
    
    # Set enable_thinking based on thinking_budget
    args.enable_thinking = args.thinking_budget > 0
    
    return args


def main():
    """Main entry point"""
    # Parse arguments
    args = parse_arguments()
    
    # Create and run application
    app = Application()
    
    try:
        app.setup(args)
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
