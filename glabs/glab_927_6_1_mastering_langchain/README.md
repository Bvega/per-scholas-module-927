# GLAB 927.6.1: Mastering LangChain for Advanced Language Model Applications

**Course:** Per Scholas - CAX-215 | Module 927: Natural Language Processing (NLP) & LangChain  
**Student:** Bolivar Vega  
**Version:** 01 | **Date:** 09/12/2024  
**Canvas Assignment:** [GLAB 927.6.1 - Canvas Submission](https://perscholas.instructure.com/courses/3601/assignments/683930)  
**Curriculum Presentation:** [Canva Slide Deck Embed](https://www.canva.com/design/DAGQkhxGUnc/_-beRp_hhjBKCY0bJPKL4w/view?embed)

---

## 🎯 Executive Summary & Learning Objectives

LangChain provides modular, composable abstractions to design, parameterize, and chain interactions with Large Language Models (LLMs). This guided laboratory demonstrates how to move from direct LLM invocations to production-ready customer support pipelines that perform automated question answering, multi-stage information extraction, simulated database retrieval, and contextualized response generation.

By the end of this lab, learners will be able to:
- **Configure & Authenticate:** Set up LangChain with high-speed inference providers using `ChatGroq`.
- **Implement Basic Chains:** Automate FAQ responses using chat prompt structures and system/human messages.
- **Build Multi-Stage Chains:** Create sequential prompt pipelines that decompose complex business queries into discrete stages (Extraction $\rightarrow$ Retrieval $\rightarrow$ Response).
- **Optimize & Evaluate:** Apply prompt engineering principles (context injection, role prompting, structured formatting guardrails) to elevate response reliability across diverse customer scenarios.

---

## 🛠️ Equipment & Environment Setup

- **Python Environment:** Python 3.13 virtual environment (`Module 927\.venv`)
- **Key Libraries Installed:**
  - `langchain>=1.4.1`
  - `langchain-core>=1.6.3`
  - `langchain-groq>=1.1.3`
  - `groq>=0.37.1`
  - `python-dotenv>=1.2.3`
- **Inference Engine:** Groq Cloud LPU (`openai/gpt-oss-20b` / `qwen/qwen3.8-27b`)

### Terminal Installation Commands
```bash
pip install langchain
pip install -U langchain-groq python-dotenv
```

---

## 📸 Comprehensive Slide Capture & Educational Notes

### 📖 Slide 1: Introduction & Prerequisites
* **Definition/Overview:** LangChain is an open-source orchestration framework designed to simplify the development of applications driven by Large Language Models.
* **Key Details:** Integrates foundational components including prompt templates, language models, output parsers, and multi-stage chains. In this lab, LangChain couples with Groq's high-speed inference engine for ultra-low latency customer interactions.
* **Practical Application:** Serves as the backbone for automated customer support hubs, interactive conversational assistants, and knowledge retrieval agents.

---

### 📖 Slide 2 (Task 1): Retrieving & Configuring the Groq API Key
* **Definition/Overview:** Authenticating client applications against Groq Cloud via API keys.
* **Key Details:**
  1. Navigate to [Groq Console](https://console.groq.com).
  2. Sign up or log into the developer dashboard.
  3. Navigate to **API Keys** on the navigation pane.
  4. Create a new key named `FirstName + "Groq_API"` (e.g., `Bolivar_Groq_API`).
  5. Store the key securely in a local `.env` file (`GROQ_API_KEY=gsk_...`) and add `.env` to `.gitignore` to prevent secret leaks.
* **Practical Application:** Prevents hardcoding production secrets in public source repositories while ensuring dynamic runtime loading.

---

### 📖 Slide 3 (Task 2): Basic FAQ Customer Support Prompt Chain
* **Definition/Overview:** Deploying `ChatGroq` to resolve recurring Frequently Asked Questions (FAQs) such as business hours and return policies.
* **Key Details:**
  - Configures a system message establishing the agent's identity: `"You customer support representative. Your goal is to efficiently handle queries."`
  - Feeds customer inquiries as human messages.
  - Model generates concise, professional answers tailored to business operating parameters.
* **Practical Application:** Deflects Tier-1 repetitive inquiries (e.g., store hours, return policies, shipping schedules) from human agents to automated AI responders.

```python
import os
from langchain_groq import ChatGroq

# Initialize LangChain with Groq Chat Model
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.2)

# Create a prompt template for FAQs
messages = [
    ("system", "You are a customer support representative. Your goal is to efficiently handle queries."),
    ("human", "What are your business hours?")
]

result = llm.invoke(messages)
print(result.content)
```

---

### 📖 Slide 4 (Task 3): Creating Advanced Multi-Stage Prompt Chains
* **Definition/Overview:** Decomposing complex customer requests into a sequential pipeline where the output of each prompt stage acts as the input to the subsequent stage.
* **Key Details:**
  - **Stage 1 (Extraction):** Takes the raw query (`customer_query`) and parses key entities (order number, dates, intent).
  - **Stage 2 (Retrieval):** Uses `extracted_info` to simulate or execute a database lookup for shipment tracking, carrier, and package status.
  - **Stage 3 (Customer Response):** Takes `order_details` and synthesizes an empathetic, customer-facing notification.
* **Practical Application:** End-to-end customer order tracking and automated resolution workflows without human intervention.

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Step 1: Prompt Template to extract key information
first_prompt_template = PromptTemplate(
    input_variables=["customer_query"],
    template="Extract the key information from the following customer query: {customer_query}"
)

# Step 2: Prompt Template to retrieve order details based on extracted information
second_prompt_template = PromptTemplate(
    input_variables=["extracted_info"],
    template="Using the extracted information: {extracted_info}, retrieve the relevant order details."
)

# Step 3: Prompt Template to generate detailed response for the customer
third_prompt_template = PromptTemplate(
    input_variables=["order_details"],
    template="Based on the following order details: {order_details}, generate a detailed response to address the customer's query."
)

# Build sequential execution pipeline
output_parser = StrOutputParser()
first_chain = first_prompt_template | llm | output_parser
second_chain = second_prompt_template | llm | output_parser
third_chain = third_prompt_template | llm | output_parser

# Execution
query = "Can you help me with the status of my order #12345 placed last week?"
info = first_chain.invoke({"customer_query": query})
details = second_chain.invoke({"extracted_info": info})
reply = third_chain.invoke({"order_details": details})
```

---

### 📖 Slide 5 (Task 4): Optimizing & Evaluating Workflows
* **Definition/Overview:** Refining prompts with explicit persona constraints, structured output specifications (Markdown tables/bullet points), and data-grounding guardrails, followed by multi-case validation.
* **Key Details:**
  - **Prompt 1 Optimization:** Enforces entity extraction (Order ID, Issue Category, Timeframe, Sentiment/Urgency).
  - **Prompt 2 Optimization:** Enforces systematic database lookup attributes (Status, Carrier, Tracking #, Item breakdown, Fulfillment notes).
  - **Prompt 3 Optimization:** Adds customer empathy, actionable tracking hyperlinks, contact channels, and professional sign-offs.
  - **Evaluation Cases:** Tested against two distinct user intents:
    1. *Query A:* Standard status check for in-transit mechanical keyboard.
    2. *Query B:* Urgent damaged-goods replacement request (cracked smartphone screen).
* **Practical Application:** Enterprise prompt hardening to prevent hallucinations, maintain brand consistency, and handle edge-case customer sentiments.

---

## 💻 Complete Python Implementation (`mastering_langchain.py`)

The full script is stored in [`mastering_langchain.py`](file:///C:/Users/boliv/Desktop/06_trainings/per_scholas/2026-cax-215/Module%20927/glabs/glab_927_6_1_mastering_langchain/mastering_langchain.py). Below is the code structure:

```python
import os
import sys
from dotenv import load_dotenv

# Ensure UTF-8 output encoding for terminal printing
sys.stdout.reconfigure(encoding='utf-8')

# Task 1: Environment & API Authentication
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env"))

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Model Initialization
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.2)
output_parser = StrOutputParser()

# Task 2: Basic FAQ Prompt Chain
messages = [
    ("system", "You are a helpful customer support representative. Your goal is to efficiently handle queries."),
    ("human", "What are your business hours?")
]
faq_result = llm.invoke(messages)

# Task 3: Advanced Sequential Pipeline
first_prompt = PromptTemplate(
    input_variables=["customer_query"],
    template="Extract the key information from the following customer query: {customer_query}"
)
second_prompt = PromptTemplate(
    input_variables=["extracted_info"],
    template="Using the extracted information: {extracted_info}, retrieve the relevant order details."
)
third_prompt = PromptTemplate(
    input_variables=["order_details"],
    template="Based on the following order details: {order_details}, generate a detailed response to address the customer's query."
)

first_chain = first_prompt | llm | output_parser
second_chain = second_prompt | llm | output_parser
third_chain = third_prompt | llm | output_parser

# Task 4: Optimized Prompts & Multi-query Evaluation
# (Includes structured entity parsing, simulated DB lookup, and empathetic customer resolution)
```

---

## 📋 Live Terminal Execution & Verification Record

Executed in the active `.venv` environment on **Monday, September 21, 2026**:

```text
======================================================================
TASK 1: Retrieving and Configuring the Groq API Key
======================================================================
[OK] Groq API Key configured successfully: gsk_GGLl...O5oV
[OK] LangChain ChatGroq initialized with model: 'openai/gpt-oss-20b'

======================================================================
TASK 2: Basic FAQ Customer Support Prompt Chain
======================================================================
Scenario: Automating common FAQ responses (e.g., business hours, return policies).

User Query: 'What are your business hours?'

[AI Support Response]:
I’d be happy to help! Could you let me know which location or department you’re referring to? That way I can give you the most accurate business hours.
----------------------------------------------------------------------

User Query: 'What is your return policy?'

[AI Support Response]:
Return Policy:
- Timeframe: You may return most items within 30 days of receipt.
- Condition: Items must be unused, in original packaging, and with all tags attached.
- Refunds & Exchanges: Refund issued to original payment method once inspected.
- Defective or wrong items: We cover return shipping with a prepaid label.

======================================================================
TASK 3: Advanced Multi-Stage Prompt Chains (Sequential Pipeline)
======================================================================
Scenario: Handling complex queries via multi-step processing:
  Step 1: Extract key query information (order #, dates, intent)
  Step 2: Retrieve relevant order details based on extracted information
  Step 3: Generate a comprehensive, empathetic customer response

Initial Customer Query:
  "Can you help me with the status of my order #12345 placed last week?"

>>> Executing Stage 1: Key Information Extraction...
Extracted Info:
| Field | Value |
|-------|-------|
| Order ID | 12345 |
| Request | Status update for the order |
| Order Placement Time | Last week |
| Customer Intent | Seeking assistance with order status |

>>> Executing Stage 2: Order Details Retrieval...
Order Details:
Status: Processing (Packaging deadline: 12 PM tomorrow)
Items: Product A (x2), Product B (x1)
Shipping: Carrier handoff pending (UPS/FedEx)
ETA: 3-5 business days after shipment

>>> Executing Stage 3: Customer Response Generation...
Customer Response:
Hi there! Thank you for reaching out about Order #12345. Both Product A and Product B 
are currently in the 'Processing' stage and will be fully packaged by 12 pm tomorrow. 
Once packaged, your order will be dispatched via UPS/FedEx with real-time tracking provided.

======================================================================
TASK 4: Optimizing and Evaluating Workflows
======================================================================

--- Evaluating Workflow: Query A (Standard Status) ---
Customer Input: "Hi, I ordered a mechanical keyboard last Friday under order #78901 and haven't seen an update. When will it arrive?"

[Optimized Stage 1 - Structured Extraction]:
- Order ID: 78901
- Issue/Intent Category: Order Status / Tracking
- Timeframe/Date mentioned: Last Friday
- Specific Customer Sentiment / Urgency: Mild urgency

[Optimized Stage 2 - System Order Retrieval]:
Order #78901 Status: In Transit | Carrier: UPS Ground | Tracking: 1Z9Y4X3B5C6D7E8F9 | ETA: Thursday, Sept 27

[Optimized Stage 3 - Final Empathetic Support Reply]:
Hi there! Your order #78901 is currently In Transit with UPS Ground and expected by Thursday, September 27. 
Track your package here: https://www.ups.com/track?loc=en_US&tracknum=1Z9Y4X3B5C6D7E8F9

--- Evaluating Workflow: Query B (Damaged Goods / Urgent Resolution) ---
Customer Input: "Order #44512 arrived yesterday but the screen is completely cracked! I need a replacement or refund immediately for my work."

[Optimized Stage 1 - Structured Extraction]:
- Order ID: 44512
- Issue/Intent Category: Defect (cracked screen) - replacement/refund request
- Urgency: High / Immediate

[Optimized Stage 2 - System Order Retrieval]:
Order #44512: Delivered damaged. 5 replacement units in stock.
Next Dispatch: FedEx Overnight (Tracking: 999999999999), ETA: Next Business Day.

[Optimized Stage 3 - Final Empathetic Support Reply]:
Subject: Your NovaStore Order #44512 – Replacement in Transit
Hi [Customer Name], I am so sorry to hear about the damaged screen. We have already dispatched an overnight replacement unit via FedEx (Tracking #999999999999) arriving tomorrow. If you prefer an immediate refund instead, please reply and we will issue it within 48 hours.

[SUCCESS] All tasks for GLAB 927.6.1 executed and validated successfully!
```

---

## 📦 Canvas Submission Checklist

- [x] **File to Submit:** [`mastering_langchain.py`](file:///C:/Users/boliv/Desktop/06_trainings/per_scholas/2026-cax-215/Module%20927/glabs/glab_927_6_1_mastering_langchain/mastering_langchain.py)
- [x] **Educational Record File:** [`GLAB_927_6_1_Mastering_LangChain.md`](file:///C:/Users/boliv/Desktop/06_trainings/per_scholas/2026-cax-215/Module%20927/glabs/glab_927_6_1_mastering_langchain/GLAB_927_6_1_Mastering_LangChain.md)
- [x] **All 4 Tasks Implemented & Tested:**
  - Task 1: Groq API Key Setup & Authentication verified
  - Task 2: FAQ Prompt Chain implemented and verified
  - Task 3: 3-stage sequential chain implemented and verified
  - Task 4: Optimized prompts evaluated across standard and urgent customer queries
- [x] **Security Verified:** API keys kept in `.env`, excluded from git via `.gitignore`.
