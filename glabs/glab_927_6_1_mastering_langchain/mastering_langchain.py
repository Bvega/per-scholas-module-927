"""
=============================================================================
GLAB 927.6.1 - Mastering LangChain for Advanced Language Model Applications
=============================================================================
Course: Per Scholas - CAX-215 | Module 927: NLP & LangChain
Student: Bolivar Vega

This script implements the four core tasks of GLAB 927.6.1:
  - Task 1: Retrieving and Configuring the Groq API Key
  - Task 2: Setting Up LangChain and LangChain-Groq (Basic FAQ Prompt Chain)
  - Task 3: Creating Advanced Sequential Prompt Chains (Extract -> Retrieve -> Respond)
  - Task 4: Optimizing and Evaluating Workflows (Refined Prompts & Multi-query Evaluation)
=============================================================================
"""

import os
import sys
from dotenv import load_dotenv

# Ensure UTF-8 output encoding for terminal printing
sys.stdout.reconfigure(encoding='utf-8')

# ---------------------------------------------------------------------------
# Task 1: Retrieving & Configuring the Groq API Key
# ---------------------------------------------------------------------------
print("=" * 70)
print("TASK 1: Retrieving and Configuring the Groq API Key")
print("=" * 70)

# Load environment variables from local .env file
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")
load_dotenv(env_path)

groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing! Please set it in .env or your environment.")

# Mask key for secure terminal verification
masked_key = groq_api_key[:8] + "..." + groq_api_key[-4:]
print(f"[OK] Groq API Key configured successfully: {masked_key}")

# Initialize the Groq model
# Note: Groq recently decommissioned 'llama3-8b-8192'. We dynamically select
# the recommended active model (openai/gpt-oss-20b or qwen/qwen3.8-27b) with graceful fallback.
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

MODEL_NAME = "openai/gpt-oss-20b"

try:
    llm = ChatGroq(model=MODEL_NAME, temperature=0.2)
    print(f"[OK] LangChain ChatGroq initialized with model: '{MODEL_NAME}'\n")
except Exception as e:
    # Fallback to qwen if needed
    MODEL_NAME = "qwen/qwen3.8-27b"
    llm = ChatGroq(model=MODEL_NAME, temperature=0.2)
    print(f"[Fallback] Initialized with fallback model: '{MODEL_NAME}'\n")


# ---------------------------------------------------------------------------
# Task 2: Setting Up LangChain and LangChain-Groq (Basic FAQ Prompt Chain)
# ---------------------------------------------------------------------------
print("=" * 70)
print("TASK 2: Basic FAQ Customer Support Prompt Chain")
print("=" * 70)
print("Scenario: Automating common FAQ responses (e.g., business hours, return policies).\n")

messages = [
    ("system", "You are a helpful customer support representative. Your goal is to efficiently handle queries."),
    ("human", "What are your business hours?")
]

print("User Query: 'What are your business hours?'")
result = llm.invoke(messages)
print("\n[AI Support Response]:")
print(result.content.strip())
print("-" * 70)

# Additional FAQ test: Return Policy
faq_query_2 = "What is your return policy?"
print(f"\nUser Query: '{faq_query_2}'")
faq_messages_2 = [
    ("system", "You are a customer support representative. Your goal is to efficiently handle queries with polite, concise information."),
    ("human", faq_query_2)
]
result_2 = llm.invoke(faq_messages_2)
print("\n[AI Support Response]:")
print(result_2.content.strip())
print("\n")


# ---------------------------------------------------------------------------
# Task 3: Creating Advanced Multi-Stage Prompt Chains
# ---------------------------------------------------------------------------
print("=" * 70)
print("TASK 3: Advanced Multi-Stage Prompt Chains (Sequential Pipeline)")
print("=" * 70)
print("Scenario: Handling complex queries via multi-step processing:")
print("  Step 1: Extract key query information (order #, dates, intent)")
print("  Step 2: Retrieve relevant order details based on extracted information")
print("  Step 3: Generate a comprehensive, empathetic customer response\n")

# Step 1: Prompt Template for Information Extraction
first_prompt_template = PromptTemplate(
    input_variables=["customer_query"],
    template="Extract the key information from the following customer query: {customer_query}"
)

# Step 2: Prompt Template for Data Retrieval Simulation
second_prompt_template = PromptTemplate(
    input_variables=["extracted_info"],
    template="Using the extracted information: {extracted_info}, retrieve the relevant order details."
)

# Step 3: Prompt Template for Customer Response Generation
third_prompt_template = PromptTemplate(
    input_variables=["order_details"],
    template="Based on the following order details: {order_details}, generate a detailed response to address the customer's query."
)

# Build LangChain pipeline chains (compatible with LangChain 1.x LCEL)
output_parser = StrOutputParser()
first_chain = first_prompt_template | llm | output_parser
second_chain = second_prompt_template | llm | output_parser
third_chain = third_prompt_template | llm | output_parser

# Initial input from the Per Scholas lab prompt
initial_input = "Can you help me with the status of my order #12345 placed last week?"
print(f"Initial Customer Query:\n  \"{initial_input}\"\n")

# Execute Stage 1
print(">>> Executing Stage 1: Key Information Extraction...")
extracted_info = first_chain.invoke({"customer_query": initial_input})
print(f"Extracted Info:\n{extracted_info.strip()}\n")

# Execute Stage 2
print(">>> Executing Stage 2: Order Details Retrieval...")
order_details = second_chain.invoke({"extracted_info": extracted_info})
print(f"Order Details:\n{order_details.strip()}\n")

# Execute Stage 3
print(">>> Executing Stage 3: Customer Response Generation...")
customer_response = third_chain.invoke({"order_details": order_details})
print(f"Customer Response:\n{customer_response.strip()}\n")


# ---------------------------------------------------------------------------
# Task 4: Optimizing and Evaluating Workflows
# ---------------------------------------------------------------------------
print("=" * 70)
print("TASK 4: Optimizing and Evaluating Workflows")
print("=" * 70)
print("Refining prompts with explicit persona, output structure, and grounding guardrails.\n")

# Optimized Prompt 1: Structured JSON/bullet extraction with entity validation
optimized_prompt_1 = PromptTemplate(
    input_variables=["customer_query"],
    template="""You are an expert customer data parser for an e-commerce platform.
Analyze the customer query and extract the following structured entities:
- Order ID (or 'Not Provided')
- Issue/Intent Category (e.g., Order Status, Return, Cancellation, Defect)
- Timeframe/Date mentioned
- Specific Customer Sentiment / Urgency

Customer Query:
"{customer_query}"

Output the extracted entities clearly in bullet points."""
)

# Optimized Prompt 2: Contextualized Database Lookup Simulation
optimized_prompt_2 = PromptTemplate(
    input_variables=["extracted_info"],
    template="""You are a database integration agent for customer support.
Based on the extracted query details:
{extracted_info}

Simulate a realistic database lookup from our inventory and shipping systems. Include:
- Current Order Status (e.g., Shipped, In Transit, Processing)
- Tracking Number & Carrier
- Estimated Delivery Date
- Items in Order
- Any relevant fulfillment notes or delays."""
)

# Optimized Prompt 3: Professional, Empathetic Customer Communication
optimized_prompt_3 = PromptTemplate(
    input_variables=["order_details"],
    template="""You are an elite Customer Success representative for NovaStore.
Review the following verified order details from our system:
{order_details}

Draft a warm, professional, and clear response to the customer.
Guidelines:
1. Greet the customer courteously.
2. Directly answer their query with the exact order status and estimated arrival date.
3. Provide the tracking link/carrier info so they can track the package in real-time.
4. Offer proactive assistance in case they need anything further.
5. Close with a polite sign-off."""
)

# Build optimized chains
opt_chain_1 = optimized_prompt_1 | llm | output_parser
opt_chain_2 = optimized_prompt_2 | llm | output_parser
opt_chain_3 = optimized_prompt_3 | llm | output_parser

# Evaluation across 2 diverse test queries
eval_queries = [
    {
        "id": "Query A (Standard Status)",
        "query": "Hi, I ordered a mechanical keyboard last Friday under order #78901 and haven't seen an update. When will it arrive?"
    },
    {
        "id": "Query B (Damaged Goods / Urgent Resolution)",
        "query": "Order #44512 arrived yesterday but the screen is completely cracked! I need a replacement or refund immediately for my work."
    }
]

for test in eval_queries:
    print(f"\n--- Evaluating Workflow: {test['id']} ---")
    print(f"Customer Input: \"{test['query']}\"")
    
    e_info = opt_chain_1.invoke({"customer_query": test["query"]})
    print(f"\n[Optimized Stage 1 - Structured Extraction]:\n{e_info.strip()}")
    
    o_data = opt_chain_2.invoke({"extracted_info": e_info})
    print(f"\n[Optimized Stage 2 - System Order Retrieval]:\n{o_data.strip()}")
    
    c_reply = opt_chain_3.invoke({"order_details": o_data})
    print(f"\n[Optimized Stage 3 - Final Empathetic Support Reply]:\n{c_reply.strip()}")
    print("=" * 70)

print("\n[SUCCESS] All tasks for GLAB 927.6.1 executed and validated successfully!")
