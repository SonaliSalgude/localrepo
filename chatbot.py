import os
import re
import json
from typing import List, Dict
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer

# Ensure required libraries are installed
try:
    import torch
except ImportError:
    raise ImportError("PyTorch is required for this script. Please install it from https://pytorch.org/get-started/locally/ and restart the script.")

# Suppress symlink warnings
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Load pre-trained model and tokenizer for question answering
model_name = "deepset/roberta-base-squad2"
try:
    qa_model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    qa_pipeline = pipeline("question-answering", model=qa_model, tokenizer=tokenizer)
except Exception as e:
    raise RuntimeError(f"Failed to load model or tokenizer: {e}")

# Define the paths to the documentation files
documentation_paths = {
    "Segment": "docs/segment.txt",
    "mParticle": "docs/mparticle.txt",
    "Lytics": "docs/lytics.txt",
    "Zeotap": "docs/zeotap.txt"
}

# Load the documentation into memory
def load_documentation(paths: Dict[str, str]) -> Dict[str, str]:
    docs = {}
    for platform, path in paths.items():
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as file:
                    docs[platform] = file.read()
            except Exception as e:
                print(f"Error reading documentation for {platform}: {e}")
        else:
            print(f"Warning: Documentation for {platform} not found at {path}")
    return docs

documentation = load_documentation(documentation_paths)

# Answer a question using the documentation
def answer_question(question: str, docs: Dict[str, str]) -> str:
    platform_detected = None
    for platform in docs:
        if platform.lower() in question.lower():
            platform_detected = platform
            break

    if not platform_detected:
        return "I couldn't determine the platform you're asking about. Please specify Segment, mParticle, Lytics, or Zeotap."

    context = docs.get(platform_detected, "")
    
    try:
        result = qa_pipeline({"question": question, "context": context})
        answer = result.get('answer', "No answer found.")
        return f"Here is what I found for your question: {answer}"
    except Exception as e:
        return f"I'm sorry, I couldn't process your question due to an error: {e}"

# Cross-CDP comparison
def compare_cdps(question: str, docs: Dict[str, str]) -> str:
    platforms = [platform for platform in docs if platform.lower() in question.lower()]
    if len(platforms) < 2:
        return "Please specify at least two platforms for comparison."

    comparisons = {}
    for platform in platforms:
        try:
            result = qa_pipeline({"question": question, "context": docs[platform]})
            comparisons[platform] = result.get('answer', "No answer found.")
        except Exception as e:
            comparisons[platform] = f"Error processing information for {platform}: {e}"

    comparison_result = "\n\n".join([f"{platform}: {answer}" for platform, answer in comparisons.items()])
    return f"Here is the comparison:\n{comparison_result}"

# Handle irrelevant questions
def is_irrelevant_question(question: str) -> bool:
    irrelevant_keywords = ["movie", "weather", "sports", "game"]
    return any(keyword in question.lower() for keyword in irrelevant_keywords)

# Advanced "how-to" questions handling
def advanced_how_to(question: str, docs: Dict[str, str]) -> str:
    try:
        results = []
        for platform, context in docs.items():
            result = qa_pipeline({"question": question, "context": context})
            results.append((platform, result.get('answer', "No answer found.")))

        advanced_results = "\n\n".join([f"{platform}: {answer}" for platform, answer in results if answer])
        return f"Here is the advanced guidance:\n{advanced_results}"
    except Exception as e:
        return f"I'm sorry, I couldn't process your question due to an error: {e}"

# Main chatbot function
def chatbot():
    print("Welcome to the CDP Support Agent Chatbot! Ask your 'how-to' questions about Segment, mParticle, Lytics, or Zeotap.")
    print("You can also ask for comparisons or advanced guidance. Type 'exit' to quit.")

    while True:
        question = input("You: ").strip()
        if question.lower() == "exit":
            print("Goodbye!")
            break

        if is_irrelevant_question(question):
            print("Chatbot: I am here to answer questions about Segment, mParticle, Lytics, or Zeotap. Please ask relevant questions.")
        elif "compare" in question.lower():
            answer = compare_cdps(question, documentation)
            print(f"Chatbot: {answer}")
        elif "advanced" in question.lower():
            answer = advanced_how_to(question, documentation)
            print(f"Chatbot: {answer}")
        else:
            answer = answer_question(question, documentation)
            print(f"Chatbot: {answer}")

# Run the chatbot
if __name__ == "__main__":
    chatbot()
