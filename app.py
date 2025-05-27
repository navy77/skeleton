import streamlit as st
import os
import dotenv
import pandas as pd
import time
from datetime import datetime
import redis
from pathlib import Path

# TXT_DIR = './txt'
TXT_DIR = "/app/txt"
# session clear
if "clear_fields" in st.session_state and st.session_state.clear_fields:
    st.session_state.emp_id = ""
    st.session_state.part_no = ""
    st.session_state.mc_no = ""
    st.session_state.clear_fields = False

def input_data():
    col1, col2, col3 = st.columns(3)
    with col2:
        emp_id = st.text_input("Employee ID",type="default",key="emp_id")
        part_no = st.text_input("Part no.",type="default",key="part_no")
        mc_no = st.text_input("MC no.",type="default",key="mc_no")

        submit_button = st.button("Submit",key='submit_button',use_container_width=True)

        if submit_button:
            if all(val != "" for val in [emp_id, part_no, mc_no]):
                txt_value = f'{emp_id}_{part_no}_{mc_no}'
                r.rpush('data_queue', txt_value)
                st.success('SUCCESS', icon="✅")
            else:
                st.error('DATA NCOMPLETE', icon="🚨")

            st.session_state.clear_fields = True
            time.sleep(0.5)
            st.rerun()
            

def verify_data():
    col1, col2, col3 = st.columns(3)
    with col1:
        txt_path = Path("/app/txt")
        txt_files = [f.name for f in txt_path.glob("*.txt")]

        
        selected_file = st.selectbox("select file", txt_files)
        preview_button = st.button("Preview",key='preview_button')

        if preview_button:
            file_path = f"{TXT_DIR}/{selected_file}"
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                st.text_area("data", content, height=300)

            except Exception as e:
                st.error(f"can not read : {e}")
                
def main_layout():
    st.set_page_config(
        page_title="Skeleton AI 1.0.0",
        page_icon="💻",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown("""<h1 style='text-align: center;'>Skeleton AI System</h1>""", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📝 INPUT", "📂 VERIFY"])
    with tab1:
        input_data()
    with tab2:
        verify_data()
    
if __name__ == "__main__":
    dotenv_file = dotenv.find_dotenv()
    r  = redis.Redis(host='redis', port=6379, db=0)
    dotenv.load_dotenv(dotenv_file, override=True)
    main_layout()