import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import pickle
import datetime
from deta import Deta



DETA_KEY = 'd0g6tcjzwmg_Vx5vesEaXcFYgRDYe6FyfmvEQuy6GKi3'
deta = Deta(DETA_KEY)
user_db = deta.Base('database')

def insert_user(username, email, password):
   
    date_joined = str(datetime.datetime.now())
    user_data = {'key': email, 'username': username, 'password': password, 'date_joined': date_joined}

    try:
        user_db.put(user_data)
        return user_data
    except Exception as e:
        st.error(f"Error inserting user data: {str(e)}")

insert_user('testing@gmail.com', 'test', '123456')


def homepage():
    st.title("Heart Disease Prediction App")
    st.image("https://d14b9ctw0m6fid.cloudfront.net/ugblog/wp-content/uploads/2021/03/1986.png", width=800)
    st.write("This web application allows you to predict the likelihood of heart disease based on various health parameters.")
    st.subheader("Get Started:")
    my_paragraph = "A Heart Disease Prediction App is a user-friendly and convenient tool that allows individuals to assess their risk of heart disease from the comfort of their homes. By inputting personal health data, users can receive a risk assessment, empowering them with valuable insights into their heart health. These apps often provide educational content, raising awareness about heart disease risk factors and promoting a heart-healthy lifestyle. Healthcare professionals can also use the data to identify high-risk individuals and provide timely interventions. Moreover, these apps can contribute to research by providing aggregated data, improving our understanding of heart disease trends. In summary, Heart Disease Prediction Apps offer accessible risk assessment, education, and research opportunities, benefitting individuals and healthcare providers."
    st.write(my_paragraph)
    st.write()
    st.video("https://youtu.be/bx99qQoHk5I?si=rDU1Bza3evlbQ1n9")
    

    
# Sign-up
def signup():
    st.title("Sign Up")
    username = st.text_input("Username")
    email=st.text_input("Email")
    password = st.text_input("Password", type="password")
    save_button = st.button("Sign Up")
    
    
    if save_button:
        if username and email and password:
            insert_user(email, username, password)
            st.success("Account created successfully.")
            st.session_state.is_authenticated = True
        else:
            st.error("Please fill in all fields.")

def logout():
    st.session_state.is_authenticated = False
    #st.experimental_rerun() #hide


# Login
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Log In"):
        if username:  # Check if username is not empty
            user_data = user_db.get(username)
            
            if user_data:
                if user_data['password'] == password:
                    st.success("Login successful!")
                    st.session_state.is_authenticated = True
                else:
                    st.error("Login failed. Incorrect password.")
            else:
                st.error("User not found. Please register.")
        else:
            st.error("Please enter your username.")

            

 
model = pickle.load(open("C:/Users/Edwin Loys/Desktop/Final model/Heart Disease.pkl", "rb"))

def prediction_page(predict):
    st.title('Heart Disease Prediction')
    age = st.slider('Age', 18)
    sex_options = ['Male', 'Female']
    sex = st.selectbox('Sex', sex_options)
    sex_num = 1 if sex == 'Male' else 0 
    cp_options = ['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymptomatic']
    cp = st.selectbox('Chest Pain Type', cp_options)
    cp_num = cp_options.index(cp)
    trestbps = st.slider('Resting Blood Pressure')
    chol = st.slider('Cholesterol')
    fbs_options = ['False', 'True']
    fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl', fbs_options)
    fbs_num = fbs_options.index(fbs)
    restecg_options = ['Normal', 'ST-T Abnormality', 'Left Ventricular Hypertrophy']
    restecg = st.selectbox('Resting Electrocardiographic Results', restecg_options)
    restecg_num = restecg_options.index(restecg)
    thalach = st.slider('Maximum Heart Rate Achieved')
    exang_options = ['No', 'Yes']
    exang = st.selectbox('Exercise Induced Angina', exang_options)
    exang_num = exang_options.index(exang)
    oldpeak = st.slider('ST Depression Induced by Exercise Relative to Rest', 0.0, 6.2, 1.0)
    slope_options = ['Upsloping', 'Flat', 'Downsloping']
    slope = st.selectbox('Slope of the Peak Exercise ST Segment', slope_options)
    slope_num = slope_options.index(slope)
    ca = st.slider('Number of Major Vessels Colored by Fluoroscopy', 0, 4, 1)
    thal_options = ['Normal', 'Fixed Defect', 'Reversible Defect']
    thal = st.selectbox('Thalassemia', thal_options)
    thal_num = thal_options.index(thal)



    if st.button('Predict'):
        user_input = pd.DataFrame(data={
            'age': [age],
            'sex': [sex_num],  
            'cp': [cp_num],
            'trestbps': [trestbps],
            'chol': [chol],
            'fbs': [fbs_num],
            'restecg': [restecg_num],
            'thalach': [thalach],
            'exang': [exang_num],
            'oldpeak': [oldpeak],
            'slope': [slope_num],
            'ca': [ca],
            'thal': [thal_num]
        })
        prediction = model.predict(user_input)
        prediction_proba = model.predict_proba(user_input)

        if prediction[0] == 1:
            bg_color = 'red'
            prediction_result = 'Positive'
        else:
            bg_color = 'green'
            prediction_result = 'Negative'
        
        confidence = prediction_proba[0][1] if prediction[0] == 1 else prediction_proba[0][0]

        st.markdown(f"<p style='background-color:{bg_color}; color:white; padding:10px;'>Prediction: {prediction_result}<br>Confidence: {((confidence*10000)//1)/100}%</p>", unsafe_allow_html=True)

def main(page, model):
    st.sidebar.title('WEB APP')
    page = st.sidebar.selectbox("Select Your Page", ["Home", "Sign Up", "Log In", "Prediction"])

    def initialize_session_state():
        return {'is_authenticated': False}


    session_state = st.session_state
    if not hasattr(session_state, 'is_authenticated'):
        session_state.is_authenticated = False

    if session_state.is_authenticated: #hide
        if page == "Home":
            homepage()
        elif page == "Prediction":
            prediction_page(model)
        if st.sidebar.button("Log Out", on_click=logout):
            pass
    else:
        if page == "Home":
            homepage()
        elif page == "Sign Up":
            signup()
        elif page == "Log In":
            login()
        elif page == "Prediction":
            st.title("Please register or log in first to access the prediction page.")
            st.image("https://media.tenor.com/oQImZjcKwBIAAAAi/backhand-index-pointing-up-joypixels.gif", width=200)
            


if __name__ == "__main__":
    st.set_page_config(page_title="Heart Disease Tester", page_icon='heart')
    model = pickle.load(open("C:/Users/Edwin Loys/Desktop/Final model/Heart Disease.pkl", "rb"))
    page = "Log In"
    main(model,page)

   

