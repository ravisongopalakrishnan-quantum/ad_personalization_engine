from ad_select_thompson_sampling_strategy import AdThompsonSamplingStrategy


class AdSelectFactory:
    """
    Factory for creating and managing multi-armed bandit advertisement selection strategies.
    
    This factory implements the Strategy pattern, allowing different bandit algorithms
    (Thompson Sampling, Epsilon-Greedy, UCB, etc.) to be used interchangeably for
    advertisement selection and optimization. The factory handles strategy instantiation
    and provides a unified interface for all bandit operations.
    
    Usage:
        >>> factory = AdSelectFactory(strategy_type="thompson_sampling")
        >>> factory.register_persona_ads("persona_123", ["ad_1", "ad_2", "ad_3"])
        >>> selected_ad = factory.select_ad("persona_123")
        >>> factory.update(selected_ad, {"success": 1, "failure": 0})
    
    Attributes:
        STRATEGIES: Class-level registry mapping strategy names to implementation classes
        strategy_type: The type of bandit strategy currently in use
        strategy: The instantiated strategy object handling ad selection logic
    """
    
    STRATEGIES = {
        "thompson_sampling": AdThompsonSamplingStrategy,
        # Future strategies can be registered here:
        # "epsilon_greedy": AdEpsilonGreedyStrategy,
        # "ucb": AdUCBStrategy,
        # "contextual_bandit": AdContextualBanditStrategy,
    }
    
    def __init__(self, strategy_type="thompson_sampling"):
        """
        Initialize the factory with a specific bandit strategy.
        
        Args:
            strategy_type: Name of the bandit algorithm to use. Must be a key in
                          the STRATEGIES registry. Defaults to "thompson_sampling".
        
        Raises:
            ValueError: If the specified strategy_type is not registered in STRATEGIES.
        """
        if strategy_type not in self.STRATEGIES:
            raise ValueError(
                f"Unknown strategy: {strategy_type}. "
                f"Available: {list(self.STRATEGIES.keys())}"
            )
        
        self.strategy_type = strategy_type
        self.strategy = self.STRATEGIES[strategy_type]()
    
    def register_persona_ads(self, persona_id, ad_ids):
        """
        Register the set of advertisements available for a specific user persona.
        
        This method delegates to the underlying strategy to initialize tracking
        for the persona-ad associations.
        
        Args:
            persona_id: Unique identifier for the user persona
            ad_ids: List of advertisement IDs to associate with this persona
        
        Returns:
            Result from the strategy's register_persona_ads method (typically None)
        """
        return self.strategy.register_persona_ads(persona_id, ad_ids)
    
    def update(self, ad_id, reward):
        """
        Update the bandit model with feedback from a user interaction.
        
        This method is called after an advertisement is shown to update the
        strategy's internal state based on whether the interaction was successful.
        
        Args:
            ad_id: Unique identifier for the advertisement that was shown
            reward: Dictionary containing success/failure feedback, typically
                   {"success": 1, "failure": 0} for a click or conversion,
                   {"success": 0, "failure": 1} for an impression without engagement
        
        Returns:
            Result from the strategy's update method (typically None)
        """
        return self.strategy.update(ad_id, reward)
    
    def select_ad(self, persona_id):
        """
        Select the optimal advertisement for a given persona using the bandit algorithm.
        
        The selection balances exploration (trying different ads to learn their
        performance) with exploitation (showing ads known to perform well).
        
        Args:
            persona_id: Unique identifier for the user persona
        
        Returns:
            The advertisement ID selected by the bandit algorithm, or None if
            the persona has no registered advertisements
        """
        return self.strategy.select_ad(persona_id)