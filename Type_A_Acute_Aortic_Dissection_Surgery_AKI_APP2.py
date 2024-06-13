import streamlit as st
import lightgbm as lgb
import numpy as np

# Load the AKI model
aki_model = lgb.Booster(model_file='Type_A_Acute_Aortic_Dissection_Surgery_AKI_model.txt')

# Define mapping dictionaries

hydragogue_mapping = {"without": 0, "20mg": 1, "＞200mg": 2}
ebrantil_mapping = { "without": 0, "with": 1}
natriuretic_peptide_mapping = { "without": 0, "with": 1}

def predict_aki_probability(features):
    aki_prob = aki_model.predict(features)
    return aki_prob[0]

def main():
    st.title('Morbidity Prediction in Acute Kidney lnjury after Type A Acute Aortic Dissection Surgery')

# User selects which content to display
    selected_content = st.radio("", ("Model Introduction", "AKI Prediction"))

    if selected_content == "Model Introduction":
        st.subheader("Model Introduction")
        st.write("This online platform provides prediction for the probability of acute kidney injury after type a acute aortic dissection surgery using a LightGBMmodel.")
        # Disclaimer
        st.subheader("Disclaimer")
        st.write("The predictions generated by this model are based on historical data and statistical patterns, and they may not be entirely accurate or applicable to every individual.")
        st.write("**For Patients:**")
        st.write("- The predictions presented by this platform are intended for informational purposes only and should not be regarded as a substitute for professional medical advice, diagnosis, or treatment.")
        st.write("- Consult with your healthcare provider for personalized medical guidance and decisions concerning your health.")
        st.write("**For Healthcare Professionals:**")
        st.write("- This platform should be considered as a supplementary tool to aid clinical decision-making and should not be the sole determinant of patient care.")
        st.write("- Clinical judgment and expertise should always take precedence in medical practice.")
        st.write("**For Researchers:**")
        st.write("- While this platform can serve as a valuable resource for research purposes, it is crucial to validate its predictions within your specific clinical context and patient population.")
        st.write("- Ensure that your research adheres to all ethical and regulatory standards.")
        st.write("The creators of this online platform and model disclaim any responsibility for decisions or actions taken based on the predictions provided herein. Please use this tool responsibly and always consider individual patient characteristics and clinical context when making medical decisions.")
        st.write("By utilizing this online platform, you agree to the terms and conditions outlined in this disclaimer.")

    elif selected_content == "AKI Prediction":
        st.subheader("AKI Prediction in Patients Following Type A Acute Aortic Dissection Surgery.")

    # Feature input
    features = []

    st.subheader("AKI Features")

    ventilation_time = st.number_input("Ventilation time (h)", value=0.0, format="%.2f")
    MIN_urine = st.number_input("Urine output_min (ml)", value=0.0, format="%.2f")
    hydragogue = st.selectbox("Diuretics", ["without", "20mg", "＞200mg"])
    SCR = st.number_input("Scr (μmol/L)", value=0.0, format="%.2f")
    HR = st.number_input("Heart rate (bpm/min)", value=0, format="%d")
    UREA = st.number_input("Urea (mmol/L)", value=0.0, format="%.2f")
    natriuretic_peptide = st.selectbox("Natriuretic_peptide", ["without", "with"])
    ebrantil = st.selectbox("ebrantil", ["without", "with"])
    GLU =  st.number_input("Blood Glucose (mmol/L)", value=0.0, format="%.2f")
    MCHC =  st.number_input("MCHC (g/L)", value=0.0, format="%.2f")
   
    # 根据用户选择从映射字典中获取相应的数字值
    hydragogue_value = hydragogue_mapping[hydragogue]
    ebrantil_value = ebrantil_mapping[ebrantil]
    natriuretic_peptide_value = natriuretic_peptide_mapping[natriuretic_peptide]
    
    # 将特征添加到列表中
    features.extend([ventilation_time, hydragogue_value, SCR, MIN_urine, HR, natriuretic_peptide_value, ebrantil_value, UREA, GLU, MCHC])
  
    # Create a button to make predictions
    if st.button('Predict AKI Probability'):
        features_array = np.array(features).reshape(1, -1)
        aki_probability = predict_aki_probability(features_array)
        st.write(f'AKI Probability: {aki_probability:.2f}')

if __name__ == '__main__':
    main()


#===================================
#-------------------------------------------转TXT文本--------------------------------------
import pandas as pd
from prefunc import *
from funs import *
plt.rcParams['font.family'] = 'Times New Roman'
from sklearn.utils import resample
from scipy.stats import norm
import statsmodels.api as sm

#----------------------------------------------------------------------ALL-调参-----------
# 将CSV文件读取到DataFrame中
df = pd.read_csv('C:/Users/75454\Desktop/毕业课题/机器学习风险预测/数据/Python代码等/ATAAD-AKI代码/anzhen_P1_imputed.csv', encoding="utf_8_sig") 
#------------------------------------------------------------------------TOP10AUROC------------
features = ['ventilation_time', 'hydragogue', 'SCR', 'MIN_urine', 'HR', 'natriuretic_peptide', 'ebrantil', 'UREA', 'GLU', 'MCHC']
X = df[features]
y = df['AKI'].astype(int)

params = {
    'max_depth' : 9,
    'num_leaves' : 3,
    'learning_rate' : 0.1,
    'n_estimators' : 288,
    'verbose' : -1,
    'force_col_wise' : True
}
model = lgb.LGBMRegressor(**params)
model.fit(X, y)

booster = model.booster_
booster.save_model('Type_A_Acute_Aortic_Dissection_Surgery_AKI_model.txt')