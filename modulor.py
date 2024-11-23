# Importing necessary libraries
import streamlit as st
import pandas as pd
import pickle

# Modelni yuklash
model_path = "or1.pkl"  # Yuklangan fayl bilan bir xil joyda saqlang
try:
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error(f"Model fayli topilmadi: {model_path}. Iltimos, faylni to'g'ri joylashtiring.")
    st.stop()
except Exception as e:
    st.error(f"Modelni yuklashda xato: {str(e)}")
    st.stop()

# Streamlit UI sozlamalari
st.set_page_config(page_title="Predictive Maintenance", page_icon="🔧", layout="centered")
st.title("Mashinani Bashoratli Texnik Xizmat Ko'rsatishni Bashorat Qilish")

# Foydalanuvchi kiritmalari
st.sidebar.header("Kiritmalar")
air_temp = st.sidebar.number_input("Havo Harorati (K)", min_value=0.0, max_value=500.0, value=298.2)
process_temp = st.sidebar.number_input("Jarayon Harorati (K)", min_value=0.0, max_value=500.0, value=308.7)
rotational_speed = st.sidebar.number_input("Aylanish tezligi (rpm)", min_value=0.0, max_value=3000.0, value=1408.0)
torque = st.sidebar.number_input("Moment (Nm)", min_value=0.0, max_value=1000.0, value=46.3)
tool_wear = st.sidebar.number_input("Asbob kiyish (min)", min_value=0.0, max_value=500.0, value=3.0)
failure_type = st.sidebar.selectbox("Muvaffaqiyatsizlik Turi", ["L", "H"])

# Bashorat qilish tugmasi
if st.sidebar.button("Bashorat qilish"):
    try:
        # Foydalanuvchi kiritgan ma'lumotlarni tayyorlash
        input_data = pd.DataFrame([[air_temp, process_temp, rotational_speed, torque, tool_wear]],
                                  columns=["Air temperature [K]", "Process temperature [K]",
                                           "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]"])
        
        # Model orqali prediksiya qilish
        prediction = model.predict(input_data)

        # Natijani chiqarish
        st.success(f"Bashorat: {'Muvaffaqiyatsizlik kutilmoqda' if prediction[0] == 1 else 'Muvaffaqiyatsizlik kutilmaydi'}")
    except Exception as e:
        st.error(f"Prediksiya jarayonida xato: {str(e)}")
