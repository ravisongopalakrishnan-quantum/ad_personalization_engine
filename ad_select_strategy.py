from abc import ABC, abstractmethod


class AdStrategy(ABC):
    """
    Abstract base class for implementing bandit-based ML inference strategies
    for advertisement prompt selection.
    
    This strategy pattern enables different multi-armed bandit algorithms to be
    used interchangeably for optimizing the selection of advertisement prompts
    based on user personas. The bandit approach allows the system to balance
    exploration (trying different prompts) and exploitation (using known
    high-performing prompts) to maximize advertisement effectiveness.
    
    Concrete implementations should define specific bandit algorithms such as:
    - Epsilon-greedy
    - Thompson Sampling
    - Upper Confidence Bound (UCB)
    - Contextual bandits
    
    Each strategy learns from user interactions to improve prompt selection over time.
    """

    @abstractmethod
    def select_persona(self, persona_id, ad_ids):
        """
        Select the optimal persona-prompt combination for a given set of advertisements.
        
        Uses bandit-based inference to determine which persona and prompt combination
        is most likely to perform well for the provided advertisement IDs.
        
        Args:
            persona_id: Identifier for the target user persona
            ad_ids: List of advertisement IDs to consider for prompt selection
            
        Returns:
            Selected persona-prompt configuration optimized for the given ads
        """
        pass

    @abstractmethod
    def update(self, persona_id, ad_id, reward):
        """
        Update the bandit model with the outcome of a given persona-ad interaction.
        
        Args:
            persona_id: Identifier for the target user persona
            ad_id: Identifier for the advertisement that was shown to the persona
            reward: Reward value indicating the success of the advertisement for the persona
        """
        pass 
       
    @abstractmethod
    def select_ad(self, persona_id):
        """
        Select the optimal advertisement for a given persona using bandit inference.
        
        Leverages the bandit algorithm to choose which advertisement (and associated
        prompt) is most likely to engage the specified persona, balancing exploration
        of new options with exploitation of known successful combinations.
        
        Args:
            persona_id: Identifier for the target user persona
            
        Returns:
            Selected advertisement ID optimized for the given persona
        """
        pass



    
    