import os
import re
import requests
import json
from pypdf import PdfReader
from dotenv import load_dotenv
from azure.ai.textanalytics import (
    TextAnalyticsClient,
    AbstractiveSummaryAction
)
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI

# Load environment variables
load_dotenv()

FILES_TO_PROCESS = [
    "Archer-Daniels-Midland-Company-Q1-2024-Earnings-Call-Apr-30-2024-Final.pdf",
    "2024-Jul-30-ADM-N-Transcript.pdf",
    "ADM-_-USQ_Transcript_2024-12-03.pdf",
    "ADM_N-Transcript-2025-02-04T15_00.pdf"
]

def clean_text(text):
    """
    Cleans raw text by removing headers, footers, and excessive whitespace.
    """
    text = re.sub(r'Copyright © \d{4} S&P Global Market Intelligence.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'spglobal\.com/marketintelligence.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_pdf(pdf_path):
    """
    Parses the entire PDF into one string.
    """
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    return clean_text(full_text)

def analyze_document(text):
    """
    Calls Azure Language Service for Sentiment, Key Phrases, and Summary.
    """
    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
    key = os.getenv("AZURE_LANGUAGE_KEY")
    
    if not endpoint or not key:
        print("Error: Azure credentials not found in .env")
        return None

    client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    print("Analyzing...")
    
    # Azure limits: Take first 5000 chars for sentiment and phrases
    short_text = text[:5000]
    
    # 1. Sentiment Analysis
    sentiment_result = client.analyze_sentiment(documents=[short_text])[0]
    
    # 2. Key Phrase Extraction
    key_phrases_result = client.extract_key_phrases(documents=[short_text])[0]
    key_phrases = key_phrases_result.key_phrases
    
    # 3. Abstractive Summarization
    poller = client.begin_analyze_actions(
        documents=[text],
        actions=[
            AbstractiveSummaryAction(sentence_count=5)
        ]
    )
    actions_result = poller.result()
    
    summary_text = "Summary not available."
    for result in actions_result:
        for doc_result in result:
            if not doc_result.is_error:
                summary_text = " ".join([s.text for s in doc_result.summaries])

    return {
        "sentiment": sentiment_result.sentiment,
        "confidence_scores": {
            "positive": sentiment_result.confidence_scores.positive,
            "neutral": sentiment_result.confidence_scores.neutral,
            "negative": sentiment_result.confidence_scores.negative
        },
        "key_phrases": key_phrases,
        "summary": summary_text
    }

def call_foundry_ai(aggregated_data, return_report=False):
    """
    Calls Azure AI Foundry to generate an executive summary.
    If return_report is True, returns the report content as a string.
    Otherwise, writes it to 'earnings_analysis.md'.
    """
    foundry_key = os.getenv("FOUNDRY_API_KEY")
    endpoint = "https://oliver-shackley-7725-resource.openai.azure.com/openai/v1/"
    deployment_name = "Kimi-K2-Thinking"
    
    if not foundry_key:
        print("Error: Foundry API key not found in .env")
        return None

    if not return_report:
        print("\nCalling Azure AI Foundry...")
    
    client = OpenAI(base_url=endpoint, api_key=foundry_key)

    input_content = "Last 4 quarters of earnings calls data:\n\n"
    for i, data in enumerate(aggregated_data):
        res = data['results']
        input_content += f"--- QUARTER {i+1} ---\n"
        input_content += f"Summary: {res.get('summary')}\n"
        input_content += f"Sentiment: {res.get('sentiment')} (Scores: {res.get('confidence_scores')})\n"
        input_content += f"Key Phrases: {res.get('key_phrases')[:10]}\n\n"

    system_prompt = (
        "You are an AI Assistant that performs scrupulous analysis of earnings call transcripts to "
        "determine investor sentiment and investment risks in the target company. "
        "Focus analysis on Risk Factors, Management Tone, and Forward Guidance. "
        "Generate a Markdown report with a sentiment trend chart (formatted as a standard Markdown Table, NOT ASCII art), "
        "sentiment scores (0-100), key themes across quarters, investment recommendation, "
        "and a final sentiment over time visualization (also as a Markdown Table). "
        "Ensure no lines of text or charts are excessively long to prevent layout overflow. "
        "Use clear, concise language (2000 most common English words)."
    )
    
    try:
        completion = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_content}
            ],
            temperature=0.7,
        )
        
        report_content = completion.choices[0].message.content
        
        if return_report:
            return report_content
        else:
            with open("earnings_analysis.md", "w") as f:
                f.write(report_content)
            print("Report generated and saved at earnings_analysis.md")
            
    except Exception as e:
        print(f"Failed to call Foundry API: {e}")
        return None

def main():
    aggregated_results = []

    for i, pdf_file in enumerate(FILES_TO_PROCESS):
        if not os.path.exists(pdf_file):
            print(f"File not found: {pdf_file}")
            continue

        print(f"Processing {pdf_file}...")
        text = parse_pdf(pdf_file)
        results = analyze_document(text)
        
        if results:
            scores = results['confidence_scores']
            print(f"Sentiment: {results['sentiment']} (Positive: {scores['positive']:.2f}, Neutral: {scores['neutral']:.2f}, Negative: {scores['negative']:.2f})")
            
            file_data = {"filename": pdf_file, "results": results}
            aggregated_results.append(file_data)
            
            with open(f"transcript_{i+1}.json", 'w') as f:
                json.dump(file_data, f, indent=4)
    
    if aggregated_results:
        call_foundry_ai(aggregated_results)

if __name__ == "__main__":
    main()
