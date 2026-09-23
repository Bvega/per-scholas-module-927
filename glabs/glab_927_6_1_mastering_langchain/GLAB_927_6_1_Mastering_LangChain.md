# GLAB 927.6.1: Mastering LangChain for Advanced Language Model Applications

**Course:** Per Scholas CAX-215, Module 927  
**Student:** Bolivar Vega  
**Correction:** September 23, 2026  
**Canvas assignment:** [GLAB 927.6.1](https://perscholas.instructure.com/courses/3601/assignments/683930)

## Correction after instructor review

The previous lab delegated order lookup to a language model and told it to simulate database results. That produced unsupported status, tracking, dispatch, and delivery claims. The old output also displayed part of the API key. Those examples must not be reused as customer responses or proof of a successful lookup.

The corrected submission is one file: `mastering_langchain.py`. It defines a fixed fictional order database in Python, extracts an explicitly supplied order ID, looks up that ID in the database, and composes a customer reply only from fields found in that record. Missing records and missing fields are described as unverified. A customer's damage report is acknowledged as a report, never described as a confirmed defect or an approved replacement. The fixed records are **lab examples, not live customer data**.

## Tasks and design

| Task | Corrected implementation |
| --- | --- |
| 1. Authentication | Load `GROQ_API_KEY` from a local `.env` beside the script. Check presence without printing any portion of the value. Do not submit `.env`. |
| 2. Basic FAQ prompt chain | `ChatPromptTemplate`, `ChatGroq`, and `StrOutputParser` generate a draft constrained to one approved response. Only the exact approved response is displayed; otherwise the approved response is used. When no FAQ answer is recorded, say it cannot be verified. |
| 3. Multi-stage chain | LangChain `RunnableLambda` stages perform deterministic ID extraction, actual lookup in `MOCK_ORDERS`, and grounded response rendering. No prompt is asked to invent a database row. |
| 4. Optimization and evaluation | Test a known status inquiry, reported damage, a missing order, and a missing ID. Compare the old documented output with the revised design on four criteria. |

The demonstration database has three sample IDs: `12345` (processing), `78901` (mechanical keyboard, in transit), and `44512` (smartphone, delivered). Its tracking, carrier, and delivery-date fields are deliberately unset. The script prints them only when a record actually supplies them. It never claims that damage, a refund, or a replacement was confirmed.

## Running the corrected submission

Install `langchain-core`, `langchain-groq`, and `python-dotenv` in the lab's virtual environment. Save `GROQ_API_KEY` in `.env` in the same directory as `mastering_langchain.py` and keep `.env` out of version control. Do not copy the key into a report, terminal screenshot, or source file.

Run `python mastering_langchain.py --offline` to check every order scenario without Groq or LangChain installed. Run `python mastering_langchain.py` to also exercise the grounded FAQ prompt with ChatGroq and execute the order pipeline through LangChain. The latter requires dependencies, a valid local key, and network access. The local offline checks passed when preparing this correction; a live Groq call has not been verified here.

## Original and optimized results

| Criterion | Original documented workflow | Corrected workflow |
| --- | --- | --- |
| Accuracy | Generated unsupported order facts and treated them as database results. | Uses only explicitly defined sample records; missing information is unverified. |
| Clarity | Said invented tracking and fulfillment details were confirmed. | Labels the database as fictional lab data and states what cannot be verified. |
| Relevance | Answered status and damaged-item requests, but promised an unsupported replacement. | Responds to both requests and directs reported damage to support for review. |
| Hallucination risk | High: the model was instructed to invent order details. | Lower: order facts are read by Python and final order responses are assembled deterministically. The FAQ draft passes an exact-answer gate. |

**Evaluation basis:** The original column describes the output recorded in the earlier version of this lab. The corrected column describes the revised code and its local offline checks. It is not a claim that a live production order system was queried.

## Resubmission

Submit **only `mastering_langchain.py`** in Canvas. Do not submit this notes file, `.env`, screenshots containing secrets, or the former output log.
