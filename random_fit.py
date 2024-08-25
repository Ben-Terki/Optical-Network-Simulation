
def random_fit(self, path, required_slots, modulation_threshold, path_all_gsnr):
    """
    Implements the Random-Fit spectrum assignment algorithm with wavelength continuity constraint.

    :param path: List of nodes representing the path
    :param required_slots: Number of frequency slots required for the request
    :param modulation_threshold: GSNR threshold for the chosen modulation format
    :param path_all_gsnr: GSNR values for all slots along the path
    :return: Randomly chosen starting index of the assigned spectrum block, or -1 if no suitable block is found
    """
    # If wavelength continuity is not required, use the flexible version
    if not self.wavelength_continuity:
        return self.random_fit_flexible(path, required_slots, modulation_threshold, path_all_gsnr)
    
    # Compute the overall spectrum usage along the entire path
    path_spectrum = np.logical_or.reduce([self.spectrum[self._get_edge_key((path[j], path[j+1]))] for j in range(len(path) - 1)])
    
    # Find all suitable starting slots that satisfy both spectrum availability and GSNR requirements
    available_slots = []
    for i in range(self.num_channels - required_slots + 1):
        if not np.any(path_spectrum[i:i+required_slots]) and all(x >= modulation_threshold for x in path_all_gsnr[i:i+required_slots]):
            available_slots.append(i)
    
    # Randomly choose one of the available starting slots, or return -1 if none are found
    return self.rng.choice(available_slots) if available_slots else -1

def random_fit_flexible(self, path, required_slots, modulation_threshold, path_all_gsnr):
    """
    Implements the Random-Fit spectrum assignment algorithm without wavelength continuity constraint.

    :param path: List of nodes representing the path
    :param required_slots: Number of frequency slots required for the request
    :param modulation_threshold: GSNR threshold for the chosen modulation format
    :param path_all_gsnr: GSNR values for all slots along the path
    :return: Randomly chosen starting index of the assigned spectrum block, or -1 if no suitable block is found
    """
    # Find all suitable starting slots that satisfy both spectrum availability and GSNR requirements
    # This version checks each link individually for spectrum availability
    available_slots = []
    for i in range(self.num_channels - required_slots + 1):
        if all(not np.any(self.spectrum[self._get_edge_key((path[j], path[j+1]))][i:i+required_slots]) for j in range(len(path) - 1)) and \
           all(x >= modulation_threshold for x in path_all_gsnr[i:i+required_slots]):
            available_slots.append(i)
    
    # Randomly choose one of the available starting slots, or return -1 if none are found
    return self.rng.choice(available_slots) if available_slots else -1