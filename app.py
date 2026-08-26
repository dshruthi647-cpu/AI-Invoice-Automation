import streamlit as st
import re
from pypdf import PdfReader

st.set_page_config(
    page_title="AI Invoice Automation",
    page_icon="🧾"
)

st.title("🧾 AI Invoice Automation")
st.write("Upload your invoice PDF and extract invoice details automatically.")

st.divider()

uploaded_file = st.file_uploader(
    "📤 Upload Invoice PDF",
    type=["pdf"]
)

if uploaded_file:

    st.success("Invoice uploaded successfully! ✅")

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    st.subheader("📄 Invoice Information")

    # Invoice Number
    invoice_number = re.search(
        r"Invoice\s*(?:Number|No\.?|#)?\s*[:\-]?\s*([A-Za-z0-9\-]+)",
        text,
        re.IGNORECASE
    )

    # Date
    invoice_date = re.search(
        r"(?:Date|Invoice Date)\s*[:\-]?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",
        text,
        re.IGNORECASE
    )

    # Email
    email = re.search(
        r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
        text
    )

    # Total
    total = re.search(
        r"(?:Grand Total|Total Amount|Total)\s*[:\-]?\s*(?:₹|Rs\.?|INR|\$|€)?\s*([\d,]+(?:\.\d{1,2})?)",
        text,
        re.IGNORECASE
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Invoice Number**")

        st.text_input(
            "Invoice Number",
            value=invoice_number.group(1) if invoice_number else "Not found",
            key="invoice_number"
        )

        st.write("**Invoice Date**")

        st.text_input(
            "Invoice Date",
            value=invoice_date.group(1) if invoice_date else "Not found",
            key="invoice_date"
        )

    with col2:

        st.write("**Customer Email**")

        st.text_input(
            "Customer Email",
            value=email.group(0) if email else "Not found",
            key="customer_email"
        )

        st.write("**Total Amount**")

        st.text_input(
            "Total Amount",
            value=total.group(1) if total else "Not found",
            key="total_amount"
        )

    st.divider()

    st.subheader("🔍 Extracted Invoice Text")

    st.text_area(
        "Invoice Text",
        text,
        height=250
    )

    if st.button("✅ Process Invoice", use_container_width=True):

        st.success("Invoice processed successfully! 🎉")

else:

    st.info("👆 Upload your invoice PDF to start.")
