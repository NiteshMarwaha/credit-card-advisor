import json
from typing import List, Dict, Any

class CreditCardDatabase:
    def __init__(self, file_path: str):
        with open(file_path, 'r') as f:
            self.cards = json.load(f)
    
    def get_all_cards(self) -> List[Dict[str, Any]]:
        return self.cards
    
    def filter_cards(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        filtered = []
        for card in self.cards:
            matches = True
            
            # Income filter (user must meet card's minimum)
            if 'min_income' in filters:
                card_min_income = card.get('eligibility', {}).get('min_income', 0)
                if filters['min_income'] < card_min_income:
                    matches = False
            
            # Credit score filter (if provided)
            if matches and 'credit_score' in filters and filters['credit_score'] > 0:
                card_min_score = card.get('eligibility', {}).get('credit_score', 0)
                if filters['credit_score'] < card_min_score:
                    matches = False
            
            # Reward type filter (if specified)
            if matches and 'reward_type' in filters and filters['reward_type']:
                if card.get('reward_type', '').lower() != filters['reward_type']:
                    matches = False
            
            # Spending categories (at least one match)
            if matches and 'spending_categories' in filters and filters['spending_categories']:
                card_categories = [c.lower() for c in card.get('reward_categories', [])]
                user_categories = filters['spending_categories']
                if not any(cat in card_categories for cat in user_categories):
                    matches = False
            
            if matches:
                filtered.append(card)
        
        return filtered
    
    def rank_cards(self, cards: List[Dict[str, Any]], user_prefs: Dict[str, Any]) -> List[Dict[str, Any]]:
        return sorted(
            cards,
            key=lambda x: (
                -x.get('reward_rate', 0),  # Higher reward rate first
                x.get('annual_fee', 0)     # Lower fees first
            )
        )[:5]  # Return top 5