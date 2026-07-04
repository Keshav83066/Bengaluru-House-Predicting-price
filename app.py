import pickle
import pandas as pd
import streamlit as st


def load_model():
    with open("bangalore_house_price_model.pkl", 'rb') as f:
        return pickle.load(f)


model = load_model()

st.set_page_config(page_title='Bengaluru Real Estate Portal', layout='wide')
st.title('Bengaluru Real Estate Portal')
st.subheader("Browse listed properties or estimate your custom home value")

st.write('---')
st.header("Featured Properties Available to Buy")

properties = [
    {"location": "Whitefield", "total_sqft": 1200, "bath": 2, "bedroom": 2, "image": "https://via.placeholder.com/150"},
    {"location": "Electronic City Phase II", "total_sqft": 1056, "bath": 2, "bedroom": 2, "image": "https://via.placeholder.com/150"},
    {"location": "Uttarahalli", "total_sqft": 1440, "bath": 2, "bedroom": 3, "image": "https://via.placeholder.com/150"}
]

cols = st.columns(3)

for idx, prop in enumerate(properties):
    with cols[idx]:
        st.image(prop['image'], use_container_width=True)
        st.subheader(f"{prop['bedroom']} BHK in {prop['location']}")
        st.write(f"Size: {prop['total_sqft']} sqft | Baths: {prop['bath']}")

        input_df = pd.DataFrame([prop]).drop(columns=['image'])
        estimated_price = model.predict(input_df)[0]
        st.metric(label="Asking Price", value=f"{estimated_price:.2f} Lakhs")

        if st.button("Buy/Inquire Now", key=f"buy_{idx}"):
            st.success(f"Thank you for your interest in the property at {prop['location']}! Our agent will contact you shortly.")

st.write("---")
st.header("Custom Property Valuation Tool")
st.write("Can't find what you are looking for? Enter custom dimensions to estimate the market price:")

col1, col2 = st.columns(2)

with col1:
    location = st.selectbox("Select Location", ['Whitefield', 'Electronic City Phase II', 'Uttarahalli', 'Kothanpur', 'other'])
    total_sqft = st.number_input("Total Square Feet", min_value=300, max_value=5000, value=1200)

with col2:
    bedroom = st.slider("Number of Bedrooms (BHK)", min_value=1, max_value=12, value=2)
    bath = st.slider("Number of Bathrooms", min_value=1, max_value=12, value=2)

if st.button("Calculate Estimated Value"):
    user_input = {
        'location': location,
        'total_sqft': total_sqft,
        'bath': bath,
        'bedroom': bedroom
    }
    prediction = model.predict(pd.DataFrame([user_input]))[0]
    st.balloons()
    st.success(f"The estimated market price for this configuration is **{prediction:.2f} lakhs**")
