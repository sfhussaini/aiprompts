With **Oracle Wayflow** as the sole approved library for agentic systems, the architectural lens shifts from general LLM concepts to **Wayflow’s concrete primitives**: **Flows** (structured, predictable pipelines), **Agents** (conversational, tool-using autonomy), and the **composition patterns** that combine them. The revised tree below maps every learning area to the Wayflow designs and patterns you will actually implement.

---

### 1. Architecture & System Design (Wayflow Foundations)

**1.1 LLM Fundamentals for Solution Architects (within Wayflow)**
- **Model providers**: `OCIGenAIModel`, `VllmModel`, `OllamaModel`, `OpenAIModel` — all share a uniform API so architectural choices can be model-agnostic.
- **Tokens / Context windows / Temperature**: Managed through `PromptTemplate` configuration and LLM provider parameters; Wayflow’s `VariableStep` helps centralize shared state across steps to control context footprint.

**1.2 Structured Prompt Design — `PromptTemplate`**
- **Clear / Specific / Well-structured prompting** is expressed through Wayflow’s `PromptTemplate` abstraction: create the template → equip with partial values, tools, or `response_format` → render to a `Prompt` object for the LLM.
- **Structured generation**: Native provider support or custom parsing; `PromptTemplate(strict_output_validation=True)` now validates prompt outputs and forces agents to resubmit invalid `submit_result` calls.

**1.3 Prompting Strategies for Reliable Outputs**
- **Zero-Shot / Few-Shot**: Realized through `PromptTemplate` examples and variable injection.
- **Chain-of-Thought (CoT)**: Embedded in agent reasoning loops; Wayflow’s **ReAct parsing** preserves thought text so CoT traces remain intact.
- **Role Playing**: Configured via `custom_instruction` on `Agent` objects — e.g., a support agent instructed to call `search_memory` before answering.


### 2. Integration & Interoperability (Wayflow Pipelines)

**2.1 Modular AI Pipelines — Wayflow as the Runtime**
- **LangChain is replaced** by Wayflow’s native `Flow` and `Agent` composition. **Agent Spec** is the open specification; **Wayflow is the reference runtime** that natively supports all Agent Spec Agents and Flows.
- **Composability patterns** (the four core agentic patterns):
  - **Calling Agents in Flows** — embed an agent inside a structured flow via `AgentExecutionStep`.
  - **Calling Agents in Agents** — multi-agent collaboration (e.g., `ManagerWorkers`, `Swarm`).
  - **Calling Flows in Agents** — use a structured flow as a tool within a conversational agent.

**2.2 Sequential and Transformation Chains**
- **Sequential chains** → **`Flow`** with linear step connections (`StartStep` → step → … → `CompleteStep`).
- **Transformation chains** → **`PromptExecutionStep`**, `ExtractValueFromJsonStep`, `BranchingStep`, and `VariableStep` for centralized state.
- **`BranchingStep`** enables conditional transitions between steps based on input values or conditions.

**2.3 Model Context Protocol (MCP) — Unified Tool Integration**
- **`MCPTool` / `MCPToolBox`** standardize how applications provide context to LLMs.
- **Transports**: `StdioTransport`, `SSETransport`, `StreamableHTTPTransport`, plus mTLS variants.
- **OAuth support** for MCP clients; session persistence across multiple MCP transports.
- **Tool output streaming** is supported for MCP tools.


### 3. RAG & Knowledge Retrieval (Wayflow Search Stack)

**3.1 Vector Embeddings**
- **`EmbeddingModel`** configured in `VectorConfig`; embedding model can be supplied at the vector config level or deferred to the retriever config.
- **Split/Embed phase**: documents are divided into chunks, vector embeddings are generated for each chunk, and embeddings are stored in a **Vector Store**.
- Supported embedding models include **Cohere, OpenAI, OCI GenAI**, and local models (Ollama/Hugging Face).

**3.2 Semantic Search**
- **`SearchConfig`** with a **`VectorRetrieverConfig`** defines how to retrieve and process entities for search.
- **`VectorConfig`** controls how embeddings/vectors are generated and stored for a collection of entities in a **Datastore**.

**3.3 Distance Metrics**
- **Cosine**, **Euclidean Distance**, and **Dot Product** are all selectable in the vector store configuration.
- **Index types**: **HNSW**, **IVF**, and **HYB** — recorded alongside distance metric for comparative evaluation.

**3.4 End-to-End RAG Architecture (Wayflow Pattern)**
- **Two architectural entry points**:
  1. **OCI Generative AI Agents (`OciAgent`)**: Agents are defined remotely (including tools, prompts, and optional RAG documents) and connected via `OciAgent` from `wayflowcore`.
  2. **Native Wayflow RAG Flow**: `Datastore` + `SearchConfig` + `VectorRetrieverConfig` inside a `Flow`, using `Split/Embed` → Vector Store → Semantic Search → grounded generation.
- **Agent Memory** integration: `search_memory` tool queries Oracle AI Agent Memory for durable facts across sessions, preventing RAG from being limited to the current thread.


### 4. Agent Platforms & Multi-Agent Systems (Wayflow Patterns)

**4.1 ReAct Framework — Native Wayflow Agent Loop**
- Wayflow’s `Agent` autonomously **plans, thinks, acts, and executes tools**.
- **ReAct parsing** is built in; the parser removes only the exact `## Thought:` marker, preserving thought text for downstream traceability.
- **`native_tool_calling`** vs. **custom tool calling**: native mode lets the LLM provider handle tool presentation/parsing; custom mode exposes raw text for manual parsing.

**4.2 Human-in-the-Loop and Supervision**
- **`InputMessageStep`**: The standard flow step to pause execution, request user input, and resume once the response arrives.
- **Tool-confirmation gate**: `ServerTool` with `requires_confirmation=True` raises `ToolExecutionConfirmationStatus` whenever the agent attempts a sensitive tool call, allowing the user to accept or reject.
- **Human Approval Node (Oracle AI Agent Studio)**: A configurable, channel-aware gate (Chat or Email) that pauses workflow agents until a human approves, rejects, or provides feedback; supports iteration limits and timeout handling.
- **Supervision patterns**: Manager-Workers and hierarchical agent structures provide a supervisory agent that coordinates expert agents equipped with tools.


### 5. Technical Demos & Solution Validation (Wayflow Implementation)

**5.1 Prompt Management and Versioning**
- Prompts are centralized in **`PromptTemplate`** objects; templates can be rendered with dynamic partial values, tools, and `response_format` at runtime.
- **Agent Spec** serialization allows assistant configurations (including prompts) to be exported/loaded as JSON/YAML for versioning and portability.

**5.2 Prompt Evaluation**
- **`strict_output_validation=True`** on `PromptTemplate` and `Agent` enforces output schema validation; invalid `submit_result` calls are rejected and the agent is asked to resubmit.
- **ReAct parsing preservation** ensures evaluation can inspect the full reasoning chain, not just the final action.

**5.3 Task-Specific Demo Scenarios**
- **Summarization** → `MessageSummarizationTransform` and `ConversationSummarizationTransform` (with optional summary caching in a `Datastore`).
- **Code Generation** → Demonstrated in the Human-Aware Code Assistant tutorial (Agent Spec + Wayflow); the assistant pauses to ask clarifying questions and resumes after input.
- **Classification** → `PromptExecutionStep` with structured output / `response_format` inside a `Flow`.
- **Writing Assistance** → `AgentExecutionStep` inside a flow for article writing (web browsing + proofreading tools).
- **Knowledge Extraction** → **Ensemble/consensus extraction** using parallel agents orchestrated by Wayflow, improving reliability beyond traditional vector search.

**5.4 AIOps Use Cases**
- **Intelligent Monitoring / Anomaly Detection** → Agents equipped with tools to query monitoring systems; flows enforce predictable diagnosis pipelines.
- **Dynamic Baselines / Event Correlation / Noise Reduction** → Achieved through **multi-agent orchestration** (Manager-Workers) and **flow branching** (`BranchingStep`) to route and consolidate events.
- **AI Operations Assistant** → Tutorial available for building an AIOps assistant with Agent Spec + Wayflow; the agent accesses procedural runbooks and converses with a human operator if required.

**5.5 ChatOps with AI Bots**
- **`OciAgent`** provides a conversational interface; `agent.start_conversation()` → `append_user_message()` → `execute()` returns a `UserMessageRequestStatus` for the assistant reply.
- **A2A protocol** (`A2AServer`) serves Wayflow conversational components to external ChatOps surfaces.


### 6. Responsible AI & Governance (Wayflow Controls)

**6.1 Responsible AI Foundations**
- **Responsible AI Basics / Governance & Compliance** → Enforced through **Human Approval Nodes** and **tool-confirmation gates** that prevent unreviewed AI output from reaching production.
- **Data Privacy & Security** → **MCP OAuth**, **mTLS transports**, and **local embedding models** (Ollama/Hugging Face) keep data within administrative control.
- **Bias Mitigation / Explainability & Interpretability** → **ReAct thought preservation** provides audit trails; **Agent Spec** enables inspectable, versioned configurations.

**6.2 AI Risk Management**
- **Risk Identification** → Map risks to Wayflow constructs: agent autonomy (unbounded tool use), RAG grounding quality, MCP trust boundaries.
- **Risk Assessment** → Evaluate via **`strict_output_validation`**, **tool-confirmation gates**, and **Human Approval Node** decision routing.
- **Risk Controls** → Implement **HITL checkpoints** (`InputMessageStep`, `ServerTool` confirmation), **MCP auth**, and **Agent Memory scoping** (stable `agent_id` / `user_id` so memory is consistently scoped).

**6.3 Customer AI Conversations**
- **`custom_instruction`** on `Agent` defines persona and behavioral guardrails (e.g., “call `search_memory` before answering”).
- **Channel-aware Human Approval** supports both **Chat** (real-time) and **Email** (asynchronous with timeouts) for customer-facing workflows.

**6.4 LLMOps Lifecycle Management (Wayflow)**
- **Build** → Compose `Flow` / `Agent` / `ManagerWorkers` / `Swarm` using Wayflow primitives.
- **Version** → Export/import via **Agent Spec** (`AgentSpecExporter` / `AgentSpecLoader`).
- **Evaluate** → `strict_output_validation`, ReAct trace inspection, and comparative vector-store experiments (chunk size, distance metric, index type).
- **Deploy** → Serve via **`A2AServer`**; connect to **OCI GenAI Agents** (`OciAgent`); integrate with **Oracle AI Agent Memory** for durable context.
- **Monitor** → Agent Memory, MCP session persistence, tool output streaming, and HITL audit trails.


### Architectural Design Principle (Revised)

> **Wayflow replaces the *library layer* entirely.** General concepts (tokens, embeddings, ReAct, HITL) remain the *what*; Wayflow provides the *how* through **Flows** (predictability), **Agents** (adaptability), and **composition patterns** (`AgentExecutionStep`, `ManagerWorkers`, `Swarm`). Every learning topic now has a concrete Wayflow primitive or pattern that a solution architect can design, validate, and govern.
