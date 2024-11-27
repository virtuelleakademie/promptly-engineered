import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import csv

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def read_markdown_file(file_path):
    """Read content from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generate_qa_pairs(text):
    """Generate Q&A pairs using OpenAI API."""
    system_prompt = """
    You are a helpful assistant that creates flashcard content about classical music.
    Generate question-answer pairs from the provided text.
    Format your response as a list of JSON objects with 'question' and 'answer' fields.
    Keep questions clear and concise.
    Keep answers comprehensive but not too long.
    """
    
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        response_format={ "type": "json" },
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Create flashcard Q&A pairs from this text:\n\n{text}"}
        ]
    )
    
    return response.choices[0].message.content

def save_to_csv(qa_pairs, output_file):
    """Save Q&A pairs to CSV file in Anki format."""
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Question', 'Answer'])  # Header
        for pair in qa_pairs:
            writer.writerow([pair['question'], pair['answer']])

def main():
    # Example usage with a markdown file
    input_file = Path('input/baroque_era.md')  # You'll need to create this
    output_file = Path('output/baroque_flashcards.csv')
    
    # Create output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Read content
    content = read_markdown_file(input_file)
    
    # Generate Q&A pairs
    qa_pairs = generate_qa_pairs(content)
    
    # Save to CSV
    save_to_csv(qa_pairs, output_file)
    
    print(f"Flashcards generated and saved to {output_file}")

if __name__ == "__main__":
    main() 