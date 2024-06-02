import streamlit as st 
import requests
from dotenv import load_dotenv
import os

load_dotenv()

llama_key = os.environ.get('LLAMA_API_KEY')



st.title("Your personalized Diabetes checker")
st.write("Please fill in the following details:")
name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:",min_value=0,max_value=100,value=0)
sex = st.number_input("Enter your gender (0 for female and 1 for male)",min_value=0,max_value=1,value=0)
BMI = st.number_input("Enter your BMI",min_value=0,max_value=100,value=0)
BP = st.number_input("Do you have high BP? (0 for No and 1 for Yes)",min_value=0,max_value=1,value=0)
cholestrol = st.number_input("Do you have high cholestrol?(0 for No and 1 for Yes)",min_value=0,max_value=1,value=0)
checked = st.number_input("Have you checked your cholestrol in 5 Years?(0 for No and 1 for Yes)",min_value=0,max_value=1,value=0)
smoke = st.number_input("Do you smoke?(0 for No and 1 for Yes)",min_value=0,max_value=1,value=0)
stroke = st.number_input("Is there any cases of stroke?(0 for No and 1 for Yes)",min_value=0,max_value=1,value=0)
heart_attack = st.number_input("Do you have experienced Heart attack or is there any sign of coronary Heat disease?(0 for No and 1 for Yes)",min_value=0,max_value=1,value=0)
exercise = st.number_input("Do you exercise regularly?(0 for No and 1 for Yes)",min_value=0,max_value=1,value=0)
fruits = st.number_input("Do you eat one or more fruits regularly?(0 for No and 1 for Yes)",min_value=0,max_value=1,value=0)
vegies = st.number_input("Do you eat vegies everyday?(0 for No and 1 for Yes)",min_value=0,max_value=1,value=0)
alcohol = st.number_input("Do you have alcohol drinking habit? (If yes state the maximum number of drinks per week)",min_value=0,max_value=17,value=0)
anyHealthcare = st.number_input("Do you have any healthcare coverage?(0 for No and 1 for Yes)",min_value=0,max_value=1,value=0)
health = st.number_input("Would you say that in general your health is:(1 = excellent 2 = very good 3 = good 4 = fair 5 = poor)",min_value=1,max_value=5,value="min")
mental_health = st.number_input("Number of days your mental health is poor",min_value=0,max_value=30,value=0)
physical_health = st.number_input("physical illness or injury days in past 30 days(0 for No and 1 for Yes)",min_value=0,max_value=1,value=0)
difficulty = st.number_input("Do you have serious difficulty walking or climbing stairs?(0 for No and 1 for Yes)",min_value=0,max_value=1,value=0)
st.write("Thank you for filling in the details. Please click on the button below to check your Diabetes status")

#create a submit button
submit = st.button("Check Diabetes")
if submit:
  st.write("Your Diabetes status is: ")
    #write the code
  import urllib.request
  import json
  import os
  import ssl

  def allowSelfSignedHttps(allowed):
      # bypass the server certificate verification on client side
      if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
          ssl._create_default_https_context = ssl._create_unverified_context

  allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

  # Request data goes here
  # The example below assumes JSON formatting which may be updated
  # depending on the format your endpoint expects.
  # More information can be found here:
  # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
  data =  {
    "input_data": {
      "columns": [
        "Column2",
        "HighBP",
        "HighChol",
        "CholCheck",
        "BMI",
        "Smoker",
        "Stroke",
        "HeartDiseaseorAttack",
        "PhysActivity",
        "Fruits",
        "Veggies",
        "HvyAlcoholConsump",
        "AnyHealthcare",
        "GenHlth",
        "MentHlth",
        "PhysHlth",
        "DiffWalk",
        "Sex",
        "Age"
      ],
      "index": [0],
      "data": [
        [
          "1",
          BP,
          cholestrol,
          checked,
          BMI,
          smoke,
          stroke,
          heart_attack,
          exercise,
          fruits,
          vegies,
          alcohol,
          anyHealthcare,
          health,
          mental_health,
          physical_health,
          difficulty,
          sex,
          age
        ]
      ]
    }
  }

  body = str.encode(json.dumps(data))

  url = 'https://evyd-t2dm-wzflr.eastus2.inference.ml.azure.com/score'
  # Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
  api_key = os.environ.get('AZURE_API_KEY')#'mQ4ZajQ7ztxyE8CcHrA6VVucpbrolYuY'
  if not api_key:
      raise Exception("A key should be provided to invoke the endpoint")

  # The azureml-model-deployment header will force the request to go to a specific deployment.
  # Remove this header to have the request observe the endpoint traffic rules
  headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'diabetes-binary-classificatio-1' }

  req = urllib.request.Request(url, body, headers)

  try:
      response = urllib.request.urlopen(req)

      result = response.read()
      
      if(result.decode("utf-8")[1] == '1'):
        
        
        
        st.write("Demographics")
        if age >=15 and age <= 24:
          age_text = "Young Adult"+"\n"
          st.write(age_text)
          
        elif age >=25 and age <= 64:
          age_text = "Adults"+"\n"
          st.write(age_text)
          
        else:
          age_text = "Seniors"+"\n"
          st.write(age_text)
          
          
        
        st.divider()
        
      
        st.write("Lifestyle attributes")
        if BMI>=12 and BMI<=18 and exercise and fruits and vegies:
          lifestyle = "Maintains a balanced lifestyle,follows a balanced diet"+"\n"
          
        elif BMI>=30 and BMI<=100 or exercise==0 or fruits==0 or vegies==0:
          lifestyle = "Does not maintain a healthy lifestyle, no proper diet is maintained"+"\n"
          
        if smoke and alcohol>=10 and mental_health>=16 and mental_health<=30:
            lifestyle = "Overstressed and shows risk of Depression"+"\n"
            
            
        st.write(lifestyle)
        API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
        headers = {"Authorization": f"Bearer {llama_key}"}
        
        def query(payload):
          response = requests.post(API_URL, headers=headers, json=payload)
          return response.json()

        user_query = "Best practices for a healthy lifestyle are"
        output = query({"inputs": user_query,})
        output = output[0]["generated_text"]
        st.write(output)
        
        st.divider()
        user_query2 = "Driking alcohol causes harmful effects like"
        output = query({"inputs": user_query2,})
        output = output[0]["generated_text"]
        st.write(output)
        
        
        st.divider()
        st.write("Health status")
        if health >=1 and health<=3:
          health_text = "overall health is good"+"\n"
          
        else: 
          health_text = "Needs more improvement in the overall health"+"\n"
          
        st.write(health_text)
        st.divider()
        if mental_health>=16 and mental_health<=30 or stroke or heart_attack:
          mental_health_text = "mental health is poor"+"\n"
          
        else: 
          mental_health_text = "Should maintain the good mental health "+"\n"
          
        
        st.write(mental_health_text)
        API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
        headers = {"Authorization": f"Bearer {llama_key}"}
        user_query = "The best yoga poses for stress relief are"
        def query(payload):
          response = requests.post(API_URL, headers=headers, json=payload)
          return response.json()

        
        output = query({"inputs": user_query,})
        output = output[0]["generated_text"]
        
        st.write(output)
        
        
        
        st.divider()  
        if physical_health>=16 and physical_health<=30 or difficulty or exercise==0:
          physical_health_text = "physical health is poor"+"\n"
          
        else: 
          physical_health_text = "Should incorporate best practices to remain physically fit"+"\n"
        
        st.write(physical_health_text)
        API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
        headers = {"Authorization": f"Bearer {llama_key}"}
        user_query = "Balanced diet for a healthy lifestyle is"
        def query(payload):
          response = requests.post(API_URL, headers=headers, json=payload)
          return response.json()

        
        output = query({"inputs": user_query,})
        output = output[0]["generated_text"]
        
        st.write(output)
        
        
        
      else: 
        st.write("You are not at risk of Diabetes .Keep up the good work!")
       
        API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
        headers = {"Authorization": f"Bearer {llama_key}"}
        user_query = "List Ways To prevent diabetes in 200 words:"
        def query(payload):
          response = requests.post(API_URL, headers=headers, json=payload)
          return response.json()

        
        output = query({"inputs": user_query,})
        output = output[0]["generated_text"]
        output = output[len(user_query):]
        st.write(output)
        
        
  except urllib.error.HTTPError as error:
      print("The request failed with status code: " + str(error.code))

      # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
      print(error.info())
      print(error.read().decode("utf8", 'ignore'))
      
      
st.write("For Organisation ")
orgSubmit = st.button("Check the diabetic population in your area")
st.page_link("pages/test_graph.py", label="See your location", icon="🗺️")
#the graph will be displayed in the next page
