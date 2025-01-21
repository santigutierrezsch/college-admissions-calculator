import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

import os

def clrhome():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def get_admissions_chance(user_info, college_name):
    prompt = f"""
    Based on the following student profile, calculate the percentage chance of getting into {college_name} and provide actionable advice to improve their chances:
    
    Student Profile:
    - GPA: {user_info['GPA']}
    - SAT Score: {user_info['SAT']}
    - ACT Score: {user_info['ACT']}
    - Extracurriculars: {user_info['Extracurriculars']}
    - Intended Major: {user_info['Major']}
    - State of Residence: {user_info['State']}
    - Additional Info: {user_info['AdditionalInfo']}
    
    Provide a JSON response with these keys:
    - "chance" (admission percentage)
    - "tips" (advice to improve chances)
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are a college admissions advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        
        result = response['choices'][0]['message']['content']
        
        print("Raw API Response:", result)
        
        result = result.strip("```json").strip("```")
        
        parsed_result = json.loads(result)
        return parsed_result
    
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return None
    except Exception as e:
        print(f"Error with ChatGPT API: {e}")
        return None

def gather_user_info():
    print("\n--- Enter Your Information ---")
    user_info = {
        "GPA": float(input("Enter your GPA (e.g., 3.8): ")),
        "SAT": int(input("Enter your SAT score (e.g., 1350): ")),
        "ACT": int(input("Enter your ACT score (if applicable, else enter 0): ")),
        "Extracurriculars": input("Describe your extracurricular activities (e.g., sports, clubs, volunteering): "),
        "Major": input("What is your intended major?: "),
        "State": input("What state do you live in?: "),
        "AdditionalInfo": input("Anything else you'd like to share (e.g., honors, unique skills)?: ")
    }
    return user_info

def main():
    clrhome()
    print("🎓 Welcome to the College Admissions Predictor! 🎓")
    user_info = gather_user_info()

    while True:
        college_name = input("\nEnter the name of the college you want to check: ")

        print("\n🔍 Calculating your chances of admission...")
        result = get_admissions_chance(user_info, college_name)
        
        if result:
            print("\n--- Estimation Results ---")
            try:
                print(f"🎯 Chance of Admission: {result['chance']}%")
                print("💡 Tips for Improvement:")
                for tip in result["tips"]:
                    print(f" - {tip}")
            except Exception as e:
                print(f"Error processing the response: {e}")
                print("Here's the raw output:")
                print(result)
        else:
            print("Failed to calculate admission chances. Please try again.")
        
        choice = input("\nWould you like to check another college? (yes/no): ").lower()
        if choice == "no":
            print("Goodbye! Best of luck with your college applications. 🎓")
            break

if __name__ == "__main__":
    main()