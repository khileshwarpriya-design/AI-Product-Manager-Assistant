# AI Product Manager Assistant

An AI-powered assistant designed to explore how Generative AI and agentic workflows can support everyday Product Management activities.

Built as a hands-on learning project, this application combines product thinking with practical implementation using Python, LangGraph, Groq, and Streamlit.

## 🎯 Problem Statement

Product Managers regularly work on PRDs, user stories, feature prioritization, and product success metrics. This project explores how an AI assistant can help structure and accelerate these workflows through conversational interaction and tool-enabled reasoning.

## ✨ Key Features

- **PRD Generation:** Help draft structured Product Requirement Documents.
- **User Story Creation:** Turn product requirements into user stories.
- **Feature Prioritization:** Explore prioritization approaches such as RICE.
- **Product Metrics:** Identify relevant KPIs and success measures.
- **Tool Calling:** Invoke tools for calculations and text analysis.
- **Conversational Memory:** Preserve conversation context using SQLite-backed LangGraph checkpointing.
- **Interactive UI:** Use a Streamlit interface with product-management quick actions.
- **Tool Visibility:** Inspect tool calls and their input arguments.

## 🛠️ Technology Stack

- Python
- LangGraph
- LangChain
- Groq LLM
- Streamlit
- SQLite
- Git and GitHub

## 🏗️ How It Works

1. A user submits a product-management question through the Streamlit interface.
2. The application passes the request to the LangGraph agent.
3. The language model determines whether a tool is needed.
4. The agent invokes the relevant tool when appropriate and processes the result.
5. The assistant returns a response in the interface.
6. SQLite-backed checkpointing supports conversational continuity.

## 🚀 Getting Started

### Prerequisites

- Python installed
- A Groq API key
- Git

### 1. Clone the repository

```bash
git clone https://github.com/khileshwarpriya-design/AI-Product-Manager-Assistant.git
cd AI-Product-Manager-Assistant
```

### 2. Create and activate a virtual environment

On macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

A `requirements.txt` file will be added in a future step to make installation reproducible.

### 4. Configure the API key

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own key. Never commit `.env` or publish API keys.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal.

## 🗺️ Roadmap

- [ ] Add a reproducible dependency file
- [ ] Add application screenshots and a demo
- [ ] Evaluate response quality across representative PM tasks
- [ ] Add structured output validation and error handling
- [ ] Improve tool safety and reliability
- [ ] Add user feedback and quality metrics
- [ ] Explore product analytics and evaluation dashboards

## 💡 Product Management Perspective

This project explores the intersection of AI product design and engineering: identifying useful workflows, designing interactions, orchestrating tools, managing conversational context, and defining ways to evaluate the resulting experience.

## ⚠️ Project Status

This is an evolving learning prototype, not a production-ready product. Outputs may require human review. Response quality, reliability, security, and business impact have not yet been formally validated.

## 👤 Author

**Khileshwar Priya**

Product Management | Technical Product Management | AI Product Development

[View GitHub Repository](https://github.com/khileshwarpriya-design/AI-Product-Manager-Assistant)