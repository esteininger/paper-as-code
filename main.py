import os
from tika import parser
import requests
import json
import PyPDF2


url = "https://api.openai.com/v1/chat/completions"

def chatgpt(msg):
    payload = json.dumps({
      "model": "gpt-3.5-turbo",
      "messages": [
        {
          "role": "user",
          "content": msg
        }
      ]
    })
    headers = {
      'Authorization': 'Bearer API_KEY',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)  


def split_pdf(input_pdf_path, output_dir):
    # Open the input PDF
    input_pdf = open(input_pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(input_pdf)

    # Get the total number of pages in the PDF
    num_pages = len(pdf_reader.pages)

    # Split the PDF into 1-page chunks
    for i in range(0, num_pages, 1):
        # Create a new PDF writer
        pdf_writer = PyPDF2.PdfWriter()

        # Add 1 pages to the new PDF
        for j in range(i, min(i+1, num_pages)):
            pdf_writer.add_page(pdf_reader.pages[j])

        # Save the new PDF to a file
        output_path = os.path.join(output_dir, f'{i+1}-{i+1}.pdf')
        with open(output_path, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

    # Close the input PDF
    input_pdf.close()



def main():
  chatgpt("you are a machine learning engineer in academia, you will be accepting the following pages of research and build a class with methods that implements said research, understood?")

  # Iterate through every file in the folder
  for filename in os.listdir("pages"):
      file_path = os.path.join("pages", filename)
      parsed_pdf = parser.from_file(file_path)['content']
      if isinstance(parsed_pdf, str):
          chatgpt(parsed_pdf)
      
      
  chatgpt("now write me a class with various methods that implements this research paper")


if __name__ == '__main__':
    main()
