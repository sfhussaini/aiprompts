---
# Introduction to Large Language Models (LLMs)
This workshop is designed for absolute beginners to understand the "engine" behind AI. We will demystify how LLMs process text through tokens, how they remember information via the context window, and how we control their "personality" using temperature.

## Stages
1. Stage 1 - The Atomic Unit: Tokens
2. Stage 2 - The AI's Memory: Context Window
3. Stage 3 - The Creativity Knob: Temperature
4. Stage 4 - Putting it All Together

### Stage 1 - The Atomic Unit: Tokens
LLMs don't read words like humans; they read "tokens." Understanding tokens is key to understanding why LLMs struggle with some tasks (like spelling) and how they are billed.

#### Step 1.1 - What is a Token?
The purpose is to understand that tokens are chunks of characters.

Guidance:
1. Analogy: Think of tokens as "LEGO bricks" of language. Some bricks are whole words, some are just prefixes or suffixes.
2. Rule of Thumb: In English, 1,000 tokens is roughly 750 words.
3. Example: The word "apple" might be 1 token, but "applepie" might be 2 tokens ("apple" and "pie").

#### Learning
Tokens are the bridge between human text and machine numbers. Everything in an LLM is calculated based on tokens.

#### DIY Challenge
Take a complex sentence and try to guess where the "splits" happen. Use a free online tokenizer (like OpenAI's Tokenizer) to verify your guess.

#### Test your knowledge
1. Which of the following is true about tokens?
    a. 1 token always equals 1 word.
    b. LLMs process tokens, not characters or words directly.
    c. Tokens are only used for billing, not for processing.
    d. A token is always a single letter.

### Stage 2 - The AI's Memory: Context Window
The context window is the "working memory" of the LLM. If a conversation becomes too long, the AI begins to "forget" the beginning.

#### Step 2.1 - Understanding the Window
The purpose is to learn the limits of LLM memory.

Guidance:
1. Analogy: Think of the context window as a "whiteboard." The AI can only see what is currently written on the board. Once the board is full, it must erase the oldest notes to make room for new ones.
2. Impact: If your prompt is too long, the AI might lose the original instructions (the "Role" or "Rules").

#### Learning
Context window size determines how much documentation or history you can feed the AI before it loses coherence.

#### DIY Challenge
Paste a very long article into an LLM and ask it to summarize the first paragraph. Then, continue the conversation with 20 long messages and ask about the first paragraph again. Observe if the AI still remembers.

#### Test your knowledge
1. What happens when a conversation exceeds the context window?
    a. The AI stops responding.
    b. The AI remembers everything perfectly.
    c. The AI "forgets" the earliest parts of the conversation.
    d. The AI automatically increases its memory.

### Stage 3 - The Creativity Knob: Temperature
Temperature is a hyperparameter that controls the randomness of the AI's output.

#### Step 3.1 - Low vs. High Temperature
The purpose is to learn when to use deterministic vs. creative outputs.

Guidance:
1. **Low Temperature (0.0 - 0.3)**: The AI chooses the most likely token. Result: Predictable, factual, repetitive. (Best for: Coding, Data Extraction).
2. **High Temperature (0.7 - 1.0)**: The AI takes "risks" and chooses less likely tokens. Result: Creative, diverse, but prone to hallucinations. (Best for: Poetry, Brainstorming).
3. Analogy: Low temperature is a "Straight-A Student" who follows the textbook. High temperature is an "Artist" who improvises.

#### Learning
By adjusting temperature, you can switch the LLM from a precise tool to a creative partner.

#### DIY Challenge
Ask an LLM to "Write a 1-sentence story about a cat" three times at Temp 0.1 and three times at Temp 0.9. Compare the consistency of the results.

#### Test your knowledge
1. If you need an LLM to extract data from a PDF with 100% accuracy, what temperature should you use?
    a. 1.0
    b. 0.8
    c. 0.1
    d. 2.0

### Stage 4 - Putting it All Together
Applying the concepts to real-world prompting.

#### Step 4.1 - Optimization
The purpose is to balance tokens, context, and temperature for a specific goal.

Guidance:
1. Goal: a factual summary of a long document.
2. Strategy: Use a model with a large **Context Window**, keep **Tokens** efficient by removing fluff, and set **Temperature** to 0.2.

#### Learning
Prompt engineering is the art of managing these three constraints to get the best result.

#### DIY Challenge
Design a "Fact-Checking Bot." Decide on the ideal temperature and explain why.

#### Test your knowledge
1. To create a creative storytelling bot that remembers a long plot, you need:
    a. Low temperature and small context window.
    b. High temperature and large context window.
    c. Low temperature and large context window.
    d. High temperature and small context window.

## Answers
1. b. LLMs process tokens, not characters or words directly.
2. c. The AI "forgets" the earliest parts of the conversation.
3. c. 0.1
4. b. High temperature and large context window.
