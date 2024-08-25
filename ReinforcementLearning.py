class RLAgent:
    def __init__(self, state_size, action_size, k_paths, path_count, modulation_count, slot_count, max_required_slots, rl_params):
        """
        Initialize the RL Agent with given parameters.
        
        :param state_size: Dimension of the state space
        :param action_size: Dimension of the action space
        :param k_paths: Dictionary of k shortest paths for each source-destination pair
        :param path_count: Number of paths to consider for each source-destination pair
        :param modulation_count: Number of available modulation formats
        :param slot_count: Total number of frequency slots
        :param max_required_slots: Maximum number of slots that can be required for a request
        :param rl_params: Dictionary containing RL hyperparameters
        """
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = rl_params['learning_rate']
        self.discount_factor = rl_params['discount_factor']
        self.epsilon = rl_params['epsilon']  # Exploration rate
        self.epsilon_decay = rl_params['epsilon_decay']
        self.epsilon_min = rl_params['epsilon_min']
        self.q_table = {}  # Q-table to store state-action values
        self.k_paths = k_paths
        self.path_count = path_count
        self.modulation_count = modulation_count
        self.slot_count = slot_count
        self.max_required_slots = max_required_slots
        self.modulations_gsnr_thresholds = None  # Will be set later
        self.src = None  # Current source node
        self.dst = None  # Current destination node

    def get_state_key(self, state):
        """
        Convert the state array to a tuple for use as a dictionary key.
        Round the state values to reduce the state space.
        
        :param state: numpy array representing the current state
        :return: tuple representation of the state
        """
        return tuple(state.round(2))

    def act(self, state, available_resources):
        """
        Choose an action using epsilon-greedy policy.
        
        :param state: Current state of the environment
        :param available_resources: List of available actions
        :return: Chosen action
        """
        state_key = self.get_state_key(state)
        
        # Explore: choose a random action
        if np.random.rand() <= self.epsilon:
            return random.choice(available_resources)
        
        # If state is not in Q-table, choose a random action
        if state_key not in self.q_table:
            return random.choice(available_resources)
        
        # Exploit: choose the best action based on Q-values
        q_values = self.q_table[state_key]
        available_q_values = [(i, q) for i, q in enumerate(q_values) if self.decode_action(i) in available_resources]
        
        # If no available actions have Q-values, choose a random action
        if not available_q_values:
            return random.choice(available_resources)
        
        # Choose the action with the highest Q-value
        best_action_index = max(available_q_values, key=lambda x: x[1])[0]
        return self.decode_action(best_action_index)

    def learn(self, state, action, reward, next_state):
        """
        Update Q-values based on the observed transition.
        
        :param state: Current state
        :param action: Chosen action
        :param reward: Received reward
        :param next_state: Next state after taking the action
        """
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)
        
        # Initialize Q-values for new states
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)
        
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(self.action_size)
        
        # Encode the action and get current Q-value
        action_index = self.encode_action(*action)
        current_q = self.q_table[state_key][action_index]
        
        # Compute the new Q-value
        next_max_q = np.max(self.q_table[next_state_key])
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        
        # Update Q-table
        self.q_table[state_key][action_index] = new_q
        
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def encode_action(self, path, modulation_format, start_slot, required_slot):
        """
        Encode an action (path, modulation, start slot, required slots) into a single integer.
        
        :param path: Chosen path
        :param modulation_format: Chosen modulation format
        :param start_slot: Starting slot for spectrum allocation
        :param required_slot: Number of required slots
        :return: Encoded action as an integer
        """
        path_index = self.k_paths[(self.src, self.dst)].index(path)
        modulation_index = list(self.modulations_gsnr_thresholds.keys()).index(modulation_format)
        return (path_index * self.modulation_count * self.slot_count * self.max_required_slots +
                modulation_index * self.slot_count * self.max_required_slots +
                start_slot * self.max_required_slots +
                required_slot - 1)

    def decode_action(self, action_index):
        """
        Decode an integer action into (path, modulation, start slot, required slots).
        
        :param action_index: Encoded action as an integer
        :return: Tuple of (path, modulation_format, start_slot, required_slot)
        """
        path_index = action_index // (self.modulation_count * self.slot_count * self.max_required_slots)
        remainder = action_index % (self.modulation_count * self.slot_count * self.max_required_slots)
        modulation_index = remainder // (self.slot_count * self.max_required_slots)
        remainder %= (self.slot_count * self.max_required_slots)
        start_slot = remainder // self.max_required_slots
        required_slot = (remainder % self.max_required_slots) + 1
        path = self.k_paths[(self.src, self.dst)][path_index]
        modulation_format = list(self.modulations_gsnr_thresholds.keys())[modulation_index]
        return path, modulation_format, start_slot, required_slot