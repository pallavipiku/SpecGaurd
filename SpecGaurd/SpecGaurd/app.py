from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

from specsense.data_loader import load_products
from specsense.recommendation import generate_recommendations

DATA_PATH = Path(__file__).resolve().parent / "data" / "sample_products.csv"


def render_app() -> None:
    st.set_page_config(page_title="SpecSense AI", page_icon="✨", layout="wide")
    st.title("SpecSense AI")
    st.caption("AI-powered product matching for personalized recommendations")

    query = st.text_area(
        "Describe the product you need",
        value="Looking for a lightweight laptop under ₹30,000 for coding and long battery life.",
        height=150,
    )

    if st.button("Recommend products"):
        products = load_products(DATA_PATH)
        result = generate_recommendations(query, products=products, top_n=5)
        recommendations = result["recommendations"]

        if not recommendations:
            st.warning("No product matches the provided criteria. Try adjusting the budget or preference list.")
        else:
            for item in recommendations:
                with st.container():
                    st.markdown(f"### {item['product_name']} — ₹{item['price']:.0f}")
                    st.write(f"Category: {item['category']}")
                    st.write(f"Match score: {item['score']}")
                    st.write(f"Recommendation reason: {item['recommendation_reason']}")
                    st.write(
                        f"Matched hard constraints: {', '.join(item['matched_hard_constraints']) if item['matched_hard_constraints'] else 'None'}"
                    )
                    st.write(f"Soft matches: {', '.join(item['soft_matches']) if item['soft_matches'] else 'None'}")
                    if item["unmet_requirements"]:
                        st.write(f"Unmet requirements: {', '.join(item['unmet_requirements'])}")
                    if item["trade_offs"]:
                        st.write(f"Trade-offs: {', '.join(item['trade_offs'])}")
                    st.markdown("---")


def main() -> None:
    """Launch the Streamlit app in the correct runtime mode."""
    if sys.argv and "streamlit" not in sys.modules:
        try:
            from streamlit.web import bootstrap

            bootstrap.run(str(Path(__file__).resolve()), "", [], {})
            return
        except Exception:
            pass

    render_app()


if __name__ == "__main__":
    main()
