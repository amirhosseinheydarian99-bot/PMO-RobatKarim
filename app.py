import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# ۱. تنظیمات صفحه و استایل RTL فارسی
# ==========================================
st.set_page_config(
    page_title="داشبورد مدیریتی PMO | نهضت ملی مسکن رباط کریم",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/webfonts/font-face.css');
    
    html, body, [class*="css"], .stMarkdown, .stText, h1, h2, h3, h4, h5, h6 {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    .metric-box {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stMetric label {
        font-size: 14px !important;
        color: #6c757d !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        font-size: 24px !important;
        font-weight: bold !important;
    }
    div[data-testid="stSidebarNav"] {
        direction: rtl;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# ۲. پایگاه داده نمونه پروژه‌ها
# ==========================================
@st.cache_data
def load_data():
    projects = [
        {"سایت / زون": "زون A (شمالی)", "پیمانکار": "عمران سازه آریا", "تعداد واحد": 650, "پیشرفت برنامه‌ای (%)": 78.0, "پیشرفت واقعی (%)": 71.5, "ارزش وزنی (%)": 25.0, "وضعیت": "تاخیر مجاز", "شاخص SPI": 0.92, "ریسک اصلی": "تأمین میلگرد و اسکلت"},
        {"سایت / زون": "زون B (مرکزی)", "پیمانکار": "بنیان پویا بتن", "تعداد واحد": 820, "پیشرفت برنامه‌ای (%)": 65.0, "پیشرفت واقعی (%)": 66.2, "ارزش وزنی (%)": 30.0, "وضعیت": "مطابق برنامه", "شاخص SPI": 1.02, "ریسک اصلی": "انشعابات آب و گاز"},
        {"سایت / زون": "زون C (جنوبی)", "پیمانکار": "توسعه ابنیه نوین", "تعداد واحد": 540, "پیشرفت برنامه‌ای (%)": 85.0, "پیشرفت واقعی (%)": 69.0, "ارزش وزنی (%)": 20.0, "وضعیت": "تاخیر بحرانی", "شاخص SPI": 0.81, "ریسک اصلی": "نقدینگی و صورت وضعیت"},
        {"سایت / زون": "زون D (شرقی)", "پیمانکار": "مسکن‌سازان پارس", "تعداد واحد": 400, "پیشرفت برنامه‌ای (%)": 45.0, "پیشرفت واقعی (%)": 43.0, "ارزش وزنی (%)": 15.0, "وضعیت": "تاخیر جزئی", "شاخص SPI": 0.95, "ریسک اصلی": "تأمین آسانسور و موتورخانه"},
        {"سایت / زون": "زون تجاری و خدماتی", "پیمانکار": "پیمان‌کاران مهر", "تعداد واحد": 120, "پیشرفت برنامه‌ای (%)": 30.0, "پیشرفت واقعی (%)": 22.0, "ارزش وزنی (%)": 10.0, "وضعیت": "تاخیر بحرانی", "شاخص SPI": 0.73, "ریسک اصلی": "تغییر نقشه‌های معماری"},
    ]
    df_proj = pd.DataFrame(projects)
    
    # داده‌های منحنی S (S-Curve)
    scurve_data = {
        "ماه": ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر (فعلی)", "آبان", "آذر", "دی"],
        "برنامه‌ای تجمیعی (%)": [10.0, 18.5, 29.0, 42.0, 56.0, 68.0, 78.5, 87.0, 94.0, 100.0],
        "واقعی تجمیعی (%)": [9.5, 17.0, 26.5, 37.5, 49.0, 59.5, 68.4, None, None, None]
    }
    df_scurve = pd.DataFrame(scurve_data)
    
    return df_proj, df_scurve

df_proj, df_scurve = load_data()

# ==========================================
# ۳. نوار کناری (Sidebar) - فیلترها و اطلاعات
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=70)
    st.title("پنل نظارت و راهبری PMO")
    st.markdown("**کارفرما:** اداره کل راه و شهرسازی")
    st.markdown("**مشاور و نظارت عالیه:** مهندسین مشاور")
    st.markdown("---")
    
    # فیلتر زون / پیمانکار
    selected_status = st.multiselect(
        "وضعیت پیشرفت:",
        options=df_proj["وضعیت"].unique(),
        default=df_proj["وضعیت"].unique()
    )
    
    filtered_df = df_proj[df_proj["وضعیت"].isin(selected_status)]

# ==========================================
# ۴. هدر و شاخص‌های کلیدی عملکرد (KPIs)
# ==========================================
st.title("🏗️ داشبورد پایش پروژه نهضت ملی مسکن رباط کریم")
st.caption("گزارش دوره‌ای پیشرفت فیزیکی، وضعیت زون‌ها و تحلیل تاخیرات نظارت عالیه")

total_units = int(filtered_df["تعداد واحد"].sum())
weighted_plan = (filtered_df["پیشرفت برنامه‌ای (%)"] * filtered_df["ارزش وزنی (%)"]).sum() / filtered_df["ارزش وزنی (%)"].sum()
weighted_actual = (filtered_df["پیشرفت واقعی (%)"] * filtered_df["ارزش وزنی (%)"]).sum() / filtered_df["ارزش وزنی (%)"].sum()
variance = weighted_actual - weighted_plan
avg_spi = weighted_actual / weighted_plan if weighted_plan > 0 else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("کل واحدهای تحت پایش", f"{total_units:,} واحد")
c2.metric("پیشرفت کل برنامه‌ای", f"{weighted_plan:.1f}%")
c3.metric("پیشرفت کل واقعی", f"{weighted_actual:.1f}%")
c4.metric("انحراف از برنامه (SV)", f"{variance:+.1f}%", delta=f"{variance:.1f}%", delta_color="normal")
c5.metric("شاخص عملکرد زمانی (SPI)", f"{avg_spi:.2f}", delta="مطلوب" if avg_spi >= 1 else "نیازمند اقدام اصلاحی", delta_color="normal" if avg_spi >= 1 else "inverse")

st.markdown("---")

# ==========================================
# ۵. نمودارهای تحلیلی (منحنی S و مقایسه زون‌ها)
# ==========================================
col_left, col_right = st.columns([6, 4])

with col_left:
    st.subheader("📈 منحنی S پیشرفت پروژه (S-Curve)")
    fig_s = go.Figure()
    fig_s.add_trace(go.Scatter(
        x=df_scurve["ماه"], 
        y=df_scurve["برنامه‌ای تجمیعی (%)"], 
        mode='lines+markers', 
        name='برنامه‌ای (Planned)',
        line=dict(color='#2b5c8f', width=3, dash='dash')
    ))
    fig_s.add_trace(go.Scatter(
        x=df_scurve["ماه"], 
        y=df_scurve["واقعی تجمیعی (%)"], 
        mode='lines+markers', 
        name='واقعی (Actual)',
        line=dict(color='#28a745', width=4)
    ))
    fig_s.update_layout(
        hovermode="x unified",
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(title="درصد پیشرفت تجمیعی", range=[0, 105]),
        xaxis=dict(title="دوره‌های گزارش‌دهی")
    )
    st.plotly_chart(fig_s, use_container_width=True)

with col_right:
    st.subheader("📊 مقایسه پیشرفت به تفکیک زون‌ها")
    fig_bar = go.Figure(data=[
        go.Bar(name='برنامه‌ای', x=filtered_df["سایت / زون"], y=filtered_df["پیشرفت برنامه‌ای (%)"], marker_color='#90caf9'),
        go.Bar(name='واقعی', x=filtered_df["سایت / زون"], y=filtered_df["پیشرفت واقعی (%)"], marker_color='#1e88e5')
    ])
    fig_bar.update_layout(
        barmode='group',
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(title="درصد (%)", range=[0, 100])
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================
# ۶. جدول جامع وضعیت پیمانکاران و ریسک‌های نظارتی
# ==========================================
st.subheader("📋 ماتریس پایش کارگاهی و ریسک‌های بحرانی (نظارت عالیه)")

st.dataframe(
    filtered_df.style.format({
        "پیشرفت برنامه‌ای (%)": "{:.1f}%",
        "پیشرفت واقعی (%)": "{:.1f}%",
        "ارزش وزنی (%)": "{:.1f}%",
        "شاخص SPI": "{:.2f}"
    }),
    use_container_width=True
)

# ==========================================
# ۷. ثبت و خروجی داده‌ها
# ==========================================
col_exp1, col_exp2 = st.columns(2)
with col_exp1:
    csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 دانلود گزارش اکسل (CSV) برای کارفرما",
        data=csv,
        file_name='PMO_Report_RobatKarim.csv',
        mime='text/csv',
    )
with col_exp2:
    st.info("💡 **نکته نظارت:** جهت جبران عقب‌ماندگی در زون C، برنامه جبرانی (Catch-up Schedule) از پیمانکار اخذ و در دست بررسی است.")
