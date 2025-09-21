import streamlit as st
import requests
import time

# ... (頁面配置和 API_BASE_URL 保持不變) ...
st.set_page_config(
    page_title="FLUX AI 圖像生成器",
    page_icon="🖼️",
    layout="wide"
)
API_BASE_URL = "https://generate-image-with-user-key-koyy20262733-h775npmi.apn.leapcell.dev/"


st.title("🎨 FLUX 多模型 AI 圖像生成器 (自訂金鑰)")
st.caption("一個由 FastAPI 後端驅動、Streamlit 前端呈現的互動式網頁應用")

# 使用側邊欄來放置 API 金鑰輸入，讓主介面更清爽
st.sidebar.header("🔑 API 設定")
user_api_key = st.sidebar.text_input(
    "輸入您的 API 金鑰",
    type="password",
    help="您的金鑰將被用於圖像生成，我們不會儲存它。"
)

col1, col2 = st.columns([1, 2])

with col1:
    # ... (模型選擇和 Prompt 輸入框保持不變) ...
    st.subheader("⚙️ 設定選項")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        available_models = response.json().get("available_models", []) if response.status_code == 200 else []
    except requests.exceptions.RequestException:
        available_models = []

    if available_models:
        selected_model = st.selectbox("選擇一個圖像生成模型:", options=available_models)
    else:
        st.warning("無法獲取模型列表，請檢查後端連線。")
        selected_model = None

    prompt = st.text_area("輸入您的圖像描述 (Prompt):", "A hyper-realistic, cinematic shot...", height=150)
    submit_button = st.button("✨ 生成圖像", use_container_width=True, type="primary")


with col2:
    st.subheader("🖼️ 生成結果")
    
    if submit_button and selected_model:
        # --- 主要修改點 ---
        if not user_api_key:
            st.error("請在左側的側邊欄輸入您的 API 金鑰！")
        elif not prompt:
            st.warning("請務必輸入圖像描述！")
        else:
            with st.spinner("正在與 AI 溝通，請稍候..."):
                # 準備請求的標頭和內文
                headers = {
                    "Authorization": f"Bearer {user_api_key}"
                }
                payload = {
                    "prompt": prompt,
                    "model": selected_model
                }
                
                try:
                    start_time = time.time()
                    # 向新的後端端點發送請求
                    response = requests.post(
                        f"{API_BASE_URL}/generate-image-with-user-key", 
                        headers=headers, 
                        json=payload
                    )
                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    if response.status_code == 200:
                        data = response.json()
                        st.image(data.get("image_url"), caption=f"模型: {selected_model} | 耗時: {elapsed_time:.2f} 秒")
                    else:
                        error_data = response.json()
                        st.error(f"生成失敗 (狀態碼: {response.status_code}): {error_data.get('detail', '未知錯誤')}")
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"請求後端時發生錯誤: {e}")

