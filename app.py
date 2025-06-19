import streamlit as st
from card_database import CreditCardDatabase
from agent_handler import CreditCardAdvisorAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize session state
def init_session_state():
    if 'conversation_step' not in st.session_state:
        st.session_state.conversation_step = 0
    if 'user_responses' not in st.session_state:
        st.session_state.user_responses = {}
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []

# Initialize database and agent
db = CreditCardDatabase('data/credit_cards.json')
agent = CreditCardAdvisorAgent(api_key=os.getenv("OPENAI_API_KEY"))

# Define conversation flow
QUESTIONS = [
    ("What is your approximate monthly income (in INR)?", "monthly_income"),
    ("What are your main spending categories? (comma separated: fuel, travel, groceries, dining, online_shopping)", "spending_habits"),
    ("What type of benefits do you prefer? (cashback, travel_points, lounge_access)", "preferred_benefit"),
    ("What is your approximate credit score? (or type 'unknown')", "credit_score"),
]

def reset_conversation():
    st.session_state.conversation_step = 0
    st.session_state.user_responses = {}
    st.session_state.recommendations = []

def display_recommendations():
    st.subheader("Here are your personalized credit card recommendations")
    
    if not st.session_state.recommendations:
        st.warning("No recommendations found based on your criteria")
        return
    
    for i, card in enumerate(st.session_state.recommendations, 1):
        with st.expander(f"#{i}: {card.get('name', 'Unknown Card')}"):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(card.get('image_url', 'https://via.placeholder.com/150'), width=150)
            with col2:
                st.write(f"**Issuer:** {card.get('issuer', 'Unknown')}")
                st.write(f"**Annual Fee:** ₹{card.get('annual_fee', 'N/A')}")
                st.write(f"**Joining Fee:** ₹{card.get('joining_fee', 'N/A')}")
                st.write(f"**Reward Type:** {card.get('reward_type', 'N/A').title()}")
                st.write(f"**Reward Rate:** {card.get('reward_rate', 'N/A')}%")
                
                # Eligibility Criteria
                st.write("**Eligibility Criteria:**")
                eligibility = card.get('eligibility', {})
                st.write(f"- Minimum Income: ₹{eligibility.get('min_income', 'N/A')}")
                st.write(f"- Minimum Credit Score: {eligibility.get('credit_score', 'N/A')}")
                
                # Perks
                perks = card.get('perks', [])
                if perks:
                    st.write("**Special Perks:**")
                    for perk in perks:
                        st.write(f"- {perk}")
                
                # Reward Calculation
                if 'monthly_income' in st.session_state.user_responses:
                    try:
                        monthly_spend = float(st.session_state.user_responses['monthly_income']) * 0.3
                        reward_rate = float(card.get('reward_rate', 0))
                        annual_rewards = monthly_spend * (reward_rate/100) * 12
                        st.write(f"**Estimated Annual Rewards:** ₹{annual_rewards:,.2f}")
                    except:
                        st.write("**Reward calculation unavailable**")

def main():
    st.title("Credit Card Advisor")
    st.write("Answer a few questions to get personalized credit card recommendations")
    
    init_session_state()
    
    if st.session_state.conversation_step < len(QUESTIONS):
        question_text, field_name = QUESTIONS[st.session_state.conversation_step]
        if field_name == "spending_habits":
            options = ['Fuel', 'Travel', 'Groceries', 'Dining', 'Online Shopping']
            response = st.multiselect(question_text, options, key=f"q_{st.session_state.conversation_step}")
            response = ", ".join(response)

        elif field_name == "preferred_benefit":
            options = ['Cashback', 'Reward Points', 'Lounge Access']
            response = st.multiselect(question_text, options, key=f"q_{st.session_state.conversation_step}")
            response = ", ".join(response)

        else:
            response = st.text_input(question_text, key=f"q_{st.session_state.conversation_step}")

        if st.button("Submit"):
            if response:
                # Store response in both session state and agent
                st.session_state.user_responses[field_name] = response
                agent.collect_user_data(response, field_name)
                st.session_state.conversation_step += 1
                st.rerun()
            else:
                st.warning("Please provide a response")
    else:
        if not st.session_state.recommendations:
            # Sync stored user responses into agent before recommending
            for field, response in st.session_state.user_responses.items():
                agent.collect_user_data(response, field)
    
            st.session_state.recommendations = agent.recommend_cards(db)
            st.write("Debug - User Data:", st.session_state.user_responses)
            st.write("Debug - Recommendations:", st.session_state.recommendations)
        
        display_recommendations()
        
        if st.button("Start Over"):
            reset_conversation()
            st.rerun()


if __name__ == "__main__":
    main()
