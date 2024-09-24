import pdfplumber
import pandas as pd
import re

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to parse bank statement text into structured data
def parse_bank_statement(text):
    # Regular expression to match transactions (date, description, and amount)
    # Customize the pattern based on your bank statement format
    transaction_pattern = re.compile(r"(\d{2}/\d{2}/\d{4})\s+([A-Za-z0-9 ]+)\s+(-?\d+\.\d{2})")
    
    transactions = []
    
    # Find all transactions using regex
    for match in re.findall(transaction_pattern, text):
        date, description, amount = match
        transactions.append({
            "Date": date,
            "Description": description.strip(),
            "Amount": float(amount)
        })
    
    return transactions

# Function to save transactions to CSV
def save_to_csv(transactions, csv_path):
    df = pd.DataFrame(transactions)
    df.to_csv(csv_path, index=False)
    print(f"Bank statement saved to {csv_path}")

# Example usage
pdf_path = "path_to_your_bank_statement.pdf"  # Replace with your PDF file path
csv_output_path = "output_bank_statement.csv"  # Replace with desired output path

# Extract text from PDF
pdf_text = extract_text_from_pdf(pdf_path)

# Parse the bank statement text
transactions = parse_bank_statement(pdf_text)

# Save the transactions to CSV
save_to_csv(transactions, csv_output_path)
