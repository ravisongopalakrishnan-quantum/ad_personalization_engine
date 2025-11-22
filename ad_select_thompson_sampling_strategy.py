import numpy as np

class AdThompsonSamplingStrategy:
    """
    Thompson Sampling strategy for advertisement selection using Beta-Bernoulli bandits.
    
    This implementation uses Bayesian inference to balance exploration and exploitation
    when selecting advertisements for different user personas. Each ad's performance is
    modeled using a Beta distribution with parameters updated based on success/failure
    feedback from user interactions.
    
    Attributes:
        persona_ad_dict: Mapping of persona IDs to their associated advertisement IDs
        reward_dict: Tracking success and failure counts for each advertisement
    """

    def __init__(self):
        """Initialize the Thompson Sampling strategy with empty tracking dictionaries."""
        self.persona_ad_dict = {}
        self.reward_dict = {}

    def register_persona_ads(self, persona_id, ad_ids):
        """
        Register the set of advertisements available for a specific persona.
        
        Initializes reward tracking for any new advertisements that haven't been
        seen before, ensuring all ads start with zero success and failure counts.
        
        Args:
            persona_id: Unique identifier for the user persona
            ad_ids: List of advertisement IDs to associate with this persona
        """
        self.persona_ad_dict[persona_id] = ad_ids

        for ad in ad_ids:
            if ad not in self.reward_dict:
                self.reward_dict[ad] = {"success": 0, "failure": 0}

    def update(self, ad_id, reward):
        """
        Update the reward statistics for an advertisement based on user interaction feedback.
        
        This method implements the learning component of Thompson Sampling by updating
        the Beta distribution parameters (alpha, beta) based on observed outcomes.
        
        Args:
            ad_id: Unique identifier for the advertisement
            reward: Dictionary containing 'success' and 'failure' counts to add
                   (e.g., {"success": 1, "failure": 0} for a click)
        """
        if ad_id not in self.reward_dict:
            self.reward_dict[ad_id] = {"success": 0, "failure": 0}

        self.reward_dict[ad_id]["success"] += reward["success"]
        self.reward_dict[ad_id]["failure"] += reward["failure"]

    def select_ad(self, persona_id):
        """
        Select the optimal advertisement for a persona using Thompson Sampling.
        
        For each candidate ad, samples from its Beta distribution (parameterized by
        success and failure counts) and selects the ad with the highest sampled value.
        This probabilistic approach naturally balances exploration of uncertain ads
        with exploitation of known high-performers.
        
        Args:
            persona_id: Unique identifier for the user persona
            
        Returns:
            The advertisement ID with the highest sampled probability, or None if
            the persona has no registered advertisements
        """
        if persona_id not in self.persona_ad_dict:
            return None

        ad_ids = self.persona_ad_dict[persona_id]
        theta_samples = []

        for ad_id in ad_ids:
            stats = self.reward_dict.get(ad_id, {"success": 0, "failure": 0})
            alpha = stats["success"] + 1  # Beta prior: alpha = successes + 1
            beta = stats["failure"] + 1   # Beta prior: beta = failures + 1

            theta = np.random.beta(alpha, beta)
            theta_samples.append(theta)

        best_index = np.argmax(theta_samples)
        return ad_ids[best_index]
