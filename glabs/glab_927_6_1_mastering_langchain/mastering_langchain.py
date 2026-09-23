"""GLAB 927.6.1: grounded customer-support chains.

Submit this single file. Install langchain-core, langchain-groq, python-dotenv,
then place GROQ_API_KEY in a local .env beside this script. Never submit .env.
Run `python mastering_langchain.py --offline` to inspect the mock workflow
without an API key or model call; run without the flag to exercise ChatGroq.

All records below are fictional, fixed lab examples. A match verifies only
that the value occurs in this sample database, not in a real order system.
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


# Task 1: sample source of truth. Unknown fields stay unknown.
MOCK_ORDERS = {
    "12345": {
        "item": None,
        "status": "Processing",
        "carrier": None,
        "tracking_number": None,
        "delivery_date": None,
    },
    "78901": {
        "item": "Mechanical keyboard",
        "status": "In transit",
        "carrier": None,
        "tracking_number": None,
        "delivery_date": None,
    },
    "44512": {
        "item": "Smartphone",
        "status": "Delivered",
        "carrier": None,
        "tracking_number": None,
        "delivery_date": None,
    },
}

FAQ_ANSWERS = {
    "HOURS": "Business hours are not available in the sample data. Please contact a support representative to confirm them.",
    "RETURNS": "The return policy is not available in the sample data. Please contact a support representative to confirm it.",
}

ORDER_ID = re.compile(r"\b(?:order\s*(?:number|no\.?|id)?\s*#?\s*|#)(\d{5})\b", re.I)
DAMAGE = re.compile(r"\b(damag\w*|crack\w*|broken|defective)\b", re.I)


def extract_request(query: str) -> dict[str, object]:
    """Stage 1: extract an explicit order ID without asking a model to guess."""
    match = ORDER_ID.search(query)
    return {"order_id": match.group(1) if match else None,
            "damage_reported": bool(DAMAGE.search(query))}


def lookup_order(request: dict[str, object]) -> dict[str, object]:
    """Stage 2: retrieve a real row from the fixed mock database."""
    order_id = request["order_id"]
    return {**request, "record": MOCK_ORDERS.get(order_id) if order_id else None}


def render_response(result: dict[str, object]) -> str:
    """Stage 3: assemble the customer reply from recorded facts only."""
    order_id = result["order_id"]
    record = result["record"]
    if order_id is None:
        return "Please provide your order number so I can check the sample records."
    if record is None:
        return (f"I cannot verify order #{order_id} in the sample records. "
                "Please contact a support representative to check the order system.")

    lines = [f"Sample record for order #{order_id}: status is {record['status']}."]
    if record["item"]:
        lines.append(f"Item: {record['item']}.")
    if record["carrier"]:
        lines.append(f"Carrier: {record['carrier']}.")
    if record["tracking_number"]:
        lines.append(f"Tracking number: {record['tracking_number']}.")
    if record["delivery_date"]:
        lines.append(f"Recorded delivery date: {record['delivery_date']}.")
    if result["damage_reported"]:
        lines.append("I understand you reported damage. The sample record does not confirm damage, a refund, or a replacement. Please contact support for review.")
    if record["delivery_date"] is None:
        lines.append("A delivery date cannot be verified from the sample record.")
    return " ".join(lines)


def respond_to_order(query: str) -> str:
    """Standard-library path for reproducible offline validation."""
    return render_response(lookup_order(extract_request(query)))


def faq_label(question: str) -> str | None:
    """Conservative routing; an unfamiliar question has no approved answer."""
    q = question.lower()
    if "hour" in q and "return" not in q:
        return "HOURS"
    if "return" in q and "hour" not in q:
        return "RETURNS"
    return None


def run_faq_chain(question: str, llm: object) -> str:
    """Task 2: prompt -> ChatGroq -> parser, gated by an approved answer."""
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate

    label = faq_label(question)
    if label is None:
        return "I cannot verify an answer from the sample data. Please contact support."
    approved = FAQ_ANSWERS[label]
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Return precisely the supplied approved response, with no additions or changes: {approved}"),
        ("human", "Customer question: {question}"),
    ])
    faq_chain = prompt | llm | StrOutputParser()
    draft = faq_chain.invoke({"approved": approved, "question": question})
    # Only the exact approved text can reach the customer. The fallback is safe.
    return draft if draft.strip() == approved else approved


def run_order_chain(query: str) -> str:
    """Tasks 3-4: LangChain LCEL extraction -> lookup -> grounded response."""
    from langchain_core.runnables import RunnableLambda

    chain = (RunnableLambda(extract_request) | RunnableLambda(lookup_order)
             | RunnableLambda(render_response))
    return chain.invoke(query)


def validate_offline() -> None:
    """Check known, unknown, and reported-damage cases without a model."""
    status = respond_to_order("Status of order #78901? When will it arrive?")
    damage = respond_to_order("Order #44512 arrived with a cracked screen; refund?")
    missing = respond_to_order("Where is order #99999? Is it arriving tomorrow?")
    no_id = respond_to_order("Where is my order?")
    assert "In transit" in status and "delivery date cannot be verified" in status
    assert "tracking number:" not in status.lower()
    assert "reported damage" in damage and "does not confirm damage" in damage
    assert "cannot verify order #99999" in missing
    assert "provide your order number" in no_id
    print("Offline checks passed: known order, reported damage, missing order, missing ID.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="run without Groq or LangChain")
    args = parser.parse_args()
    validate_offline()

    if not args.offline:
        try:
            from dotenv import load_dotenv
            from langchain_groq import ChatGroq
            from langchain_core.runnables import RunnableLambda  # noqa: F401
        except ImportError as exc:
            parser.error(f"Install langchain-core langchain-groq python-dotenv ({exc.name} missing).")
        load_dotenv(Path(__file__).with_name(".env"))
        if not os.getenv("GROQ_API_KEY"):
            parser.error("Set GROQ_API_KEY in a local .env next to this file.")
        llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
        print("Groq API key loaded; key value is never displayed.")
        print("FAQ:", run_faq_chain("What are your business hours?", llm))

    print("\nOrder scenarios (fictional sample records):")
    for query in (
        "Can you check my order #12345?",
        "I ordered a mechanical keyboard under order #78901. When will it arrive?",
        "Order #44512 arrived with a cracked screen. I need a replacement or refund.",
        "What is the status of order #99999?",
        "Where is my order?",
    ):
        reply = respond_to_order(query) if args.offline else run_order_chain(query)
        print(f"Customer: {query}\nSupport: {reply}\n")

    print("Original vs optimized (original findings are from the prior lab record):")
    print("Accuracy: original invented order fields; optimized reads only fixed sample records.")
    print("Clarity: original said fabricated values were verified; optimized labels sample data and uncertainty.")
    print("Relevance: both address status and damage; optimized requests support review for unconfirmed damage.")
    print("Hallucination risk: original model generated order facts; optimized code never lets model output supply order facts.")


if __name__ == "__main__":
    main()
