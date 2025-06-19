from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Dict, Any, List

class CreditCardAdvisorAgent:
    def __init__(self, api_key: str):
        # Set up the chat model
        self.llm = ChatOpenAI(
            api_key=api_key,
            temperature=0.7,
            model="gpt-3.5-turbo"
        )
        
        # Set up the conversation chain
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful credit card advisor. Ask relevant questions to recommend the best credit cards."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ])
        
        self.chain = self.prompt | self.llm
        self.message_history = ChatMessageHistory()
        self.conversation = RunnableWithMessageHistory(
            self.chain,
            lambda session_id: self.message_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        
        self.user_data: Dict[str, Any] = {}
    
    def ask_question(self, question: str) -> str:
        response = self.conversation.invoke(
            {"input": question},
            config={"configurable": {"session_id": "user123"}},
        )
        return response.content
    
    def collect_user_data(self, response: str, field: str) -> None:
        """Store user responses in the agent's memory"""
        self.user_data[field] = response.strip()

        if field == 'spending_habits':
            alias_map = {
                'online shopping': 'online_spends',
                'groceries': 'grocery',
                'grocery': 'grocery',
                'fuel': 'fuel',
                'travel': 'travel',
                'dining': 'dining',
                'upi': 'upi',
                'digital payments': 'digital_payments',
                'food delivery': 'food_delivery',
                'entertainment': 'entertainment',
                'supermarkets': 'supermarkets'
            }

            categories = [cat.strip().lower() for cat in response.split(',')]
            normalized = list(set(alias_map.get(cat, cat) for cat in categories))
            self.user_data[field] = normalized

        elif field == 'preferred_benefit':
            # Normalize benefit input
            alias_map = {
                'cashback': 'cashback',
                'reward points': 'reward points',
                'lounge access': 'lounge_access'
            }

            selected = [b.strip().lower() for b in response.split(',')]
            normalized = [alias_map.get(b, b) for b in selected]
            # Use only the first valid one for filtering
            self.user_data[field] = normalized[0] if normalized else ''

        elif field in ['monthly_income', 'credit_score']:
            try:
                self.user_data[field] = float(response) if '.' in response else int(response)
            except ValueError:
                self.user_data[field] = 0
    
    def get_user_data(self) -> Dict[str, Any]:
        return self.user_data
    
    def recommend_cards(self, db_handler) -> List[Dict[str, Any]]:
        try:
            print("\nDEBUG - User Data:", self.user_data)  # Debug print
            
            filters = {
                'min_income': self.user_data.get('monthly_income', 0) * 12,
                'credit_score': self.user_data.get('credit_score', 0),
                'reward_type': self.user_data.get('preferred_benefit', '').lower(),
                'spending_categories': self.user_data.get('spending_habits', [])
            }
            
            print("DEBUG - Filters:", filters)  # Debug print
            
            filtered = db_handler.filter_cards(filters)
            print("DEBUG - Filtered cards count:", len(filtered))  # Debug print
            
            ranked = db_handler.rank_cards(filtered, self.user_data)
            print("DEBUG - Final recommendations:", ranked)  # Debug print
            
            return ranked
        except Exception as e:
            print(f"ERROR in recommend_cards: {str(e)}")
            return []