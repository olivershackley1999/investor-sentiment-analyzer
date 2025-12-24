# Earnings Call Sentiment Analyzer

Automated pipeline that analyzes earnings call transcripts to extract sentiment trends, identify key risks, and generate investment insights. 

# Demo

https://github.com/user-attachments/assets/76bcb83e-0ff1-4901-9b3d-5d44f40c26b9

<video src="Azure%20Language%20Project%20copy.mov" controls onloadstart="this.playbackRate = 2.0;"></video>

# What it does

* Processes earnings call transcripts for sentiment trend analysis
* Extracts sentiment scores and key phrases via Azure Language Service
* Generates executive summaries highlighting management tone, forward guidance, and risk factors using Azure AI Foundry (Kimi-K2 Thinking)

# How it works

1. **Input**: Earnings call transcripts (.txt, .pdf, .docx)
2. **Language Service**: Each transcript is processed by Azure Language Servcice
	- Sentiment Analysis
	- Key Phrase Extraction
	- Document Summarization
3. **Data Structuring**: Results are saved as JSON files per document.
4. **AI Synthesis**: Each JSON file is passed to Azure AI Foundry (Kimi-K2 Thinking)
5. **Output**: Markdown report with sentiment trend and investment analysis.

# Tech Stack

* **Azure Language Service** - NLP tasks (sentiment, entities, key phrases, summarization)
* **Azure AI Foundry** - Kimi-K2 Thinking for synthesis, insights, and report generation
* **Python 3.13** - Core pipeline for I/O and endpoint orchestration
* **Streamlit** - Optional for interactive UI

# Installation

**Note**: This project requires two sets of Azure credentials: an Azure Language Service endpoint (and key), and a Foundry endpoint (and key)

1. Clone the repo
   git clone https://github.com/yourusername/earnings-sentiment-analyzer
   cd earnings-sentiment-analyzer

2. Install dependencies
   pip install -r requirements.txt

3. Set up Azure credentials
   - Create Azure Language Service resource
   - Create Azure AI Foundry project
   - Add credentials to `.env`:

     AZURE_LANGUAGE_KEY=your_key
     AZURE_LANGUAGE_ENDPOINT=your_endpoint
     AZURE_FOUNDRY_KEY=your_key
     AZURE_FOUNDRY_ENDPOINT=your_endpoint

4. Run the analysis
   python analyze_transcripts.py

# Sample Output

**Language Service JSON Structure**
<img width="1438" height="898" alt="language-service-output" src="https://github.com/user-attachments/assets/c605f6a3-f80a-4e35-88eb-0551195f9136" />

**Markdown Report**

https://github.com/user-attachments/assets/4aa4b5c5-6a38-466a-bb23-8ce8d0aba198

<video src="Streamlit%20copy.mov" controls></video>

# Project Motivation

Financial analysis goes beyond the numbers and relies heavily on linguistic nuance (tone, emphasis, etc.). I built this explore how NLP could identify
investment signals purely from earnings call language, creating an end-to-end pipeline from transcript to investment recommendation.  

