
# Credit Card Advisor System - README

## Overview

This system provides personalized credit card recommendations based on user's financial profile and spending habits. It combines conversational AI with a comprehensive credit card database to offer tailored suggestions.



## Demo

Insert gif or link to demo


## Setup

Prerequisites
Python 3.8+

OpenAI API key

Streamlit

## Installation
## Clone the repository:
``` bash
git clone [repository-url]
cd credit-card-advisor
```
## Create and activate a virtual environment:
``` bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Install dependencies:

```bash
pip install -r requirements.txt
```

Create a .env file in the root directory with your OpenAI API key:

``` text
OPENAI_API_KEY=your-api-key-here
```

## Run the application:

```bash
streamlit run app.py
```

## System Architecture
## Components

* Streamlit Frontend (app.py) - User interface for the application

* Agent Handler (agent_handler.py) - Conversational AI logic

* Card Database (card_database.py) - Credit card data management

* Data File (credit_cards.json) - Credit card information

# Agent Flow Documentation
## Conversation Flow
Initialization:

* System creates a new conversation with the AI agent

* Sets up message history tracking

## Data Collection:

Asks series of questions to gather:

* Monthly income

* Spending categories

* Preferred benefits

* Credit score

## Data Processing:

* Normalizes user responses

* Stores in structured format

* Handles edge cases (unknown credit scores, etc.)

## Recommendation Generation:

* Filters cards based on eligibility

* Ranks cards by reward rate and fees

* Returns top 5 recommendations

## Prompt Design
## The agent uses a structured prompt template with:

* System Message: Defines the agent's role as a credit card advisor

* Message History: Maintains conversation context

* User Input: Current user response

Example prompt structure:

``` text
System: You are a helpful credit card advisor...
[Previous conversation history]
Human: {current user input}
```

## Data Normalization
## The system normalizes user inputs for:

* Spending Categories: Maps various terms to standardized categories

* Preferred Benefits: Standardizes reward types

* Numerical Values: Converts income and credit scores to numbers

## Customization
## To modify the system:

* Add/Remove Questions: Edit the QUESTIONS list in app.py

* Update Card Database: Modify credit_cards.json

* Change Recommendation Logic: Adjust filter_cards and rank_cards in card_database.py

## Troubleshooting
* No Recommendations: Check debug prints in console for filtering issues

* API Errors: Verify OpenAI API key is valid

* Data Issues: Ensure credit_cards.json is properly formatted
