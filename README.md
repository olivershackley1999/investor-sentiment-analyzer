# Earnings Call Sentiment Analyzer

Automated pipeline for analyzing earnings call transcripts to extract sentiment trends, identify risks, and generate investment insights.

## Demo

- [Terminal Demo](https://olivershackley.com/assets/videos/sentiment-terminal-demo.mov) - Command-line analysis workflow
- [Streamlit Demo](https://olivershackley.com/assets/videos/sentiment-streamlit-demo.mov) - Interactive report visualization

## What it does

- Processes earnings call transcripts for sentiment trend analysis
- Extracts sentiment scores and key phrases via Azure Language Service
- Generates executive summaries highlighting management tone, forward guidance, and risk factors using Azure AI Foundry (Kimi-K2 Thinking)

## How it works

**Five-step pipeline:**

1. **Input**: Accepts earnings call transcripts (.txt, .pdf, .docx)
2. **Language Service**: Azure processes each transcript with sentiment analysis, key phrase extraction, and document summarization
3. **Data Structuring**: Results saved as JSON files per document
4. **AI Synthesis**: JSON files processed by Azure AI Foundry (Kimi-K2 Thinking) for deeper analysis
5. **Output**: Generates Markdown reports with sentiment trends and investment analysis

## Tech Stack

- Azure Language Service (sentiment, entities, key phrases, summarization)
- Azure AI Foundry (Kimi-K2 Thinking for synthesis and insights)
- Python 3.13
- Streamlit (optional interactive UI)

## Installation

**Prerequisites**: Azure Language Service and Azure AI Foundry credentials required.

1. Clone the repository
   ```bash
   git clone https://github.com/olivershackley1999/investor-sentiment-analyzer.git
   cd investor-sentiment-analyzer
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Configure credentials in `.env`
   ```
   AZURE_LANGUAGE_KEY=your_key
   AZURE_LANGUAGE_ENDPOINT=your_endpoint
   AZURE_FOUNDRY_KEY=your_key
   AZURE_FOUNDRY_ENDPOINT=your_endpoint
   ```

4. Run the analysis
   ```bash
   python analyze_transcripts.py
   ```

## Sample Output

```json
{
  "document": "Q3_2025_earnings_call.txt",
  "overall_sentiment": "mixed",
  "confidence": 0.82,
  "key_phrases": ["revenue growth", "margin pressure", "guidance raised"],
  "risk_factors": ["supply chain constraints", "currency headwinds"]
}
```

## Project Motivation

Built to explore whether NLP could identify investment signals purely from earnings call language, creating an end-to-end pipeline from transcript to investment recommendation.
