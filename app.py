import streamlit as st
from datetime import date, timedelta
from dotenv import load_dotenv
import os
import re
from integrations.google_genai_integration import fetch_travel_recommendations
from utils.images_helper import fetch_destination_images

# Load environment variables (Force override)
load_dotenv(override=True)

# Load API keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY", "")
GENAI_API_KEY = os.getenv("GENAI_API_KEY", "")

# Currency Exchange Rate
USD_TO_INR = 83

def convert_prices_to_inr(recommendations):
    """Convert prices in USD to INR."""
    def convert_price(match):
        usd_price = float(match.group(1))
        inr_price = usd_price * USD_TO_INR
        return f"₹{inr_price:.0f} (USD ${usd_price})"

    return re.sub(r"\$(\d+(\.\d+)?)", convert_price, recommendations)

def main():
    st.title("✨ AI Travel Planner – Your Smart Travel Companion! ✈️ 🌍")

    source = st.text_input("📍 Enter Source Location", key="source_location")
    destination = st.text_input("📍 Enter Destination Location", key="destination_location")

    start_date = st.date_input("📅 Start Date", date.today(), key="start_date")
    end_date = st.date_input("📅 End Date", date.today() + timedelta(days=5), key="end_date")

    mode = st.selectbox("✈️🚂🚌🚖 Preferred Transport Mode", ["Flight", "Train", "Bus", "Cab", "Any"], key="mode")
    budget = st.selectbox("💰 Budget Range", ["Budget", "Standard", "Luxury"], key="budget")
    time = st.selectbox("⏰ Preferred Time to Travel", ["Morning", "Afternoon", "Evening", "Night"], key="time")
    travelers = st.number_input("👥 Number of Travelers", min_value=1, key="travelers")
    currency = st.selectbox("💱 Preferred Currency", ["USD ($)", "INR (₹)"], key="currency")

    if st.button("🎒 Plan My Trip"):
        if not source or not destination or not GOOGLE_API_KEY or not UNSPLASH_API_KEY or not GENAI_API_KEY:
            st.error("⚠️ Please fill all fields and set your API keys in `.env` file.")
            return

        st.subheader(f"📸 Stunning Views of {destination}")
        images = fetch_destination_images(destination, UNSPLASH_API_KEY)
        cols = st.columns(3)
        for i, img_url in enumerate(images[:3]):
            with cols[i]:
                st.image(img_url, caption=f"View {i+1}", use_container_width=True)

        date_range = f"{start_date} to {end_date}"

        recommendations = fetch_travel_recommendations(
            source, destination, mode, budget, time, travelers, date_range, GENAI_API_KEY
        )

        if currency == "INR (₹)":
            recommendations = recommendations.replace("$", "USD $")
            recommendations = convert_prices_to_inr(recommendations)

        st.subheader("✨ Travel Recommendations")
        st.markdown(recommendations)

if __name__ == "__main__":
    main()
