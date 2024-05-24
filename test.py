import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import openai

# Set your OpenAI API key
openai.api_key = 'your_openai_api_key'

def fetch_google_form(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to fetch the form")

def parse_form(html):
    soup = BeautifulSoup(html, 'html.parser')
    questions = []
    for div in soup.find_all('div', class_='freebirdFormviewerComponentsQuestionBaseRoot'):
        question_text = div.find('div', class_='freebirdFormviewerComponentsQuestionBaseTitle').get_text()
        options = [option.get_text() for option in div.find_all('div', class_='docssharedWizToggleLabeledContent')]
        questions.append({
            'question': question_text,
            'options': options
        })
    return questions

def get_correct_answers(questions):
    correct_answers = []
    for q in questions:
        question_text = q['question']
        options = q['options']
        prompt = f"Question: {question_text}\nOptions:\n" + "\n".join(options) + "\nWhich option is correct?"
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0
        )
        
        correct_answer = response.choices[0].text.strip()
        correct_answers.append(correct_answer)
    return correct_answers

def create_pdf(questions, answers, filename='output.pdf'):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    
    y_position = height - 40
    for idx, q in enumerate(questions):
        question_text = f"Q{idx+1}: {q['question']}"
        c.drawString(40, y_position, question_text)
        y_position -= 20
        
        for option in q['options']:
            c.drawString(60, y_position, f"- {option}")
            y_position -= 20

        correct_answer_text = f"Correct Answer: {answers[idx]}"
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y_position, correct_answer_text)
        c.setFont("Helvetica", 12)
        y_position -= 40
        
        if y_position < 40:
            c.showPage()
            y_position = height - 40

    c.save()

if __name__ == "__main__":
    google_form_url = input("Enter the Google Form URL: ")
    html_content = fetch_google_form(google_form_url)
    questions = parse_form(html_content)
    
    correct_answers = get_correct_answers(questions)

    create_pdf(questions, correct_answers)
    print("PDF created successfully!")
