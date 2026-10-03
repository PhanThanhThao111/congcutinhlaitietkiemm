
import streamlit as st
st.image("logo.jpg")
import pandas as pd

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm - Phan Thanh Thảo",
    page_icon="🏦",
    layout="centered"
)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_vnd(amount):
    return f"{amount:,.0f}".replace(",", ".") + " VNĐ"


# =========================
# TIÊU ĐỀ ỨNG DỤNG
# =========================
st.title("🏦 TÍNH LÃI GỬI TIẾT KIỆM - Phan Thanh Thảo")
st.write(
    "Tính toán tiền lãi dự kiến dựa trên số tiền gửi, "
    "kỳ hạn, lãi suất và hình thức nhận lãi."
)

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin tiền gửi")

with st.form("savings_form"):
    principal = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=1_000_000,
        value=100_000_000,
        step=1_000_000,
        format="%d"
    )

    col1, col2 = st.columns(2)

    with col1:
        term_months = st.selectbox(
            "Kỳ hạn gửi",
            options=[1, 2, 3, 6, 9, 12, 18, 24, 36],
            index=6,
            format_func=lambda x: f"{x} tháng"
        )

    with col2:
        annual_rate = st.number_input(
            "Lãi suất (%/năm)",
            min_value=0.0,
            max_value=30.0,
            value=5.0,
            step=0.1,
            format="%.2f"
        )

    interest_method = st.selectbox(
        "Hình thức nhận lãi",
        options=[
            "Cuối kỳ",
            "Hàng tháng",
            "Hàng quý"
        ]
    )

    submitted = st.form_submit_button(
        "🧮 TÍNH TIỀN LÃI",
        use_container_width=True
    )


# =========================
# TÍNH TOÁN VÀ HIỂN THỊ
# =========================
if submitted:
    # Quy đổi lãi suất năm sang lãi suất theo tháng
    monthly_rate = annual_rate / 100 / 12

    # Xác định số kỳ nhận lãi
    if interest_method == "Cuối kỳ":
        periods = 1
        months_per_period = term_months
    elif interest_method == "Hàng tháng":
        periods = term_months
        months_per_period = 1
    else:
        # Nhận lãi hàng quý: mỗi kỳ gồm 3 tháng
        periods = term_months // 3
        months_per_period = 3

    # Lãi suất tính theo thời gian của mỗi kỳ
    periodic_interest = (
        principal * monthly_rate * months_per_period
    )

    # Tổng lãi đơn, không nhập lãi vào gốc
    total_interest = periodic_interest * periods

    # Tổng tiền gốc và lãi
    total_amount = principal + total_interest

    st.divider()
    st.subheader("💰 Kết quả tính toán")

    # Ba ô kết quả
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Tổng tiền lãi",
            value=format_vnd(total_interest)
        )

    with col2:
        st.metric(
            label="Tổng gốc + lãi",
            value=format_vnd(total_amount)
        )

    st.info(
        f"**Tiền lãi mỗi kỳ nhận:** "
        f"{format_vnd(periodic_interest)}"
    )

    # =========================
    # BẢNG LỊCH NHẬN LÃI
    # =========================
    st.subheader("📅 Lịch nhận lãi dự kiến")

    if interest_method == "Cuối kỳ":
        schedule = [{
            "Kỳ nhận lãi": "Cuối kỳ",
            "Thời điểm": f"Tháng thứ {term_months}",
            "Tiền lãi (VNĐ)": round(total_interest),
            "Gốc nhận lại (VNĐ)": principal
        }]
    else:
        schedule = []

        for i in range(1, periods + 1):
            month = i * months_per_period

            schedule.append({
                "Kỳ nhận lãi": f"Kỳ {i}",
                "Thời điểm": f"Tháng thứ {month}",
                "Tiền lãi (VNĐ)": round(periodic_interest),
                "Gốc nhận lại (VNĐ)": (
                    principal if i == periods else 0
                )
            })

    df = pd.DataFrame(schedule)

    # Định dạng số tiền để dễ đọc
    df["Tiền lãi (VNĐ)"] = df["Tiền lãi (VNĐ)"].apply(
        lambda x: f"{x:,.0f}".replace(",", ".")
    )
    df["Gốc nhận lại (VNĐ)"] = df["Gốc nhận lại (VNĐ)"].apply(
        lambda x: f"{x:,.0f}".replace(",", ".")
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # =========================
    # LƯU Ý
    # =========================
    st.caption(
        "Lưu ý: Kết quả mang tính tham khảo, áp dụng lãi đơn "
        "trên số tiền gốc ban đầu. Lãi suất thực tế, cách tính "
        "ngày gửi và điều kiện nhận lãi phụ thuộc vào ngân hàng. "
        "Với hình thức hàng quý, kỳ hạn nên chia hết cho 3 tháng."
    )

else:
    st.caption(
        "Nhập thông tin tiền gửi và nhấn "
        "'TÍNH TIỀN LÃI' để xem kết quả."
    )
