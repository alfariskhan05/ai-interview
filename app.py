# app.py
import streamlit as st
import requests
import random

def get_job_opportunities(course_name, location, age):
    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id=YOUR_APP_ID&app_key=YOUR_APP_KEY&what={course_name}&where={location}"
    response = requests.get(url)

    if response.status_code == 200:
        jobs = response.json().get("results", [])[:5]  # Get top 5 job listings
        return [f"{job['title']} - {job['redirect_url']}" for job in jobs] if jobs else ["No jobs found. Try modifying your search."]
    else:
        return ["Error fetching jobs. Try again later."]

def virtual_interview(course_name):
    question_bank = {
        "Python": ["What are Python's key features?", "Explain list vs tuple."],
        "Data Analysis": ["How do you handle missing data?", "Explain data normalization."],
        "Marketing": ["How do you conduct market research?", "Explain digital marketing trends."],
    }

    job_category = "General"
    for key in question_bank:
        if key.lower() in course_name.lower():
            job_category = key
            break

    questions = question_bank.get(job_category, ["Describe yourself.", "Why should we hire you?"])
    random.shuffle(questions)

    return questions

def main():
    st.title("Job Finder & Virtual Interview Assistant")

    course_name = st.text_input("Enter Course/Training Completed")
    location = st.text_input("Enter Your Location")
    age = st.number_input("Enter Your Age", min_value=0, max_value=100, step=1)

    if course_name and location and age:
        st.subheader("Job Opportunities")
        jobs = get_job_opportunities(course_name, location, age)
        for job in jobs:
            st.write("-", job)

        st.subheader("Virtual Interview")
        questions = virtual_interview(course_name)
        answers = []
        scores = []

        for q in questions:
            st.markdown(f"**Q: {q}**")
            a = st.text_area(f"Your Answer to: {q}", key=q)
            if a:
                answers.append(a)
                score = random.randint(5, 10)
                scores.append(score)
                st.markdown(f"Score: {score}/10")

        if scores:
            final_score = sum(scores) / len(scores)
            st.success(f"Final Interview Score: {final_score}/10")

if __name__ == "__main__":
    main()
