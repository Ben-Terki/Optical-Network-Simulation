def first_fit(self, path, required_slots, modulation_threshold, path_all_gsnr):
    """
    Implements the First-Fit spectrum assignment algorithm with wavelength continuity constraint.

    :param path: List of nodes representing the path
    :param required_slots: Number of frequency slots required for the request
    :param modulation_threshold: GSNR threshold for the chosen modulation format
    :param path_all_gsnr: GSNR values for all slots along the path
    :return: Starting index of the assigned spectrum block, or -1 if no suitable block is found
    """
    # If wavelength continuity is not required, use the flexible version
    if not self.wavelength_continuity:
        return self.first_fit_flexible(path, required_slots, modulation_threshold, path_all_gsnr)
    
    # Compute the overall spectrum usage along the entire path
    path_spectrum = np.logical_or.reduce([self.spectrum[self._get_edge_key((path[j], path[j+1]))] for j in range(len(path) - 1)])
    
    # Search for the first block of contiguous slots that satisfies both spectrum availability and GSNR requirements
    for i in range(self.num_channels - required_slots + 1):
        if not np.any(path_spectrum[i:i+required_slots]) and all(x >= modulation_threshold for x in path_all_gsnr[i:i+required_slots]):
            return i
    
    # Return -1 if no suitable spectrum block is found
    return -1

def first_fit_flexible(self, path, required_slots, modulation_threshold, path_all_gsnr):
    """
    Implements the First-Fit spectrum assignment algorithm without wavelength continuity constraint.

    :param path: List of nodes representing the path
    :param required_slots: Number of frequency slots required for the request
    :param modulation_threshold: GSNR threshold for the chosen modulation format
    :param path_all_gsnr: GSNR values for all slots along the path
    :return: Starting index of the assigned spectrum block, or -1 if no suitable block is found
    """
    # Compute the overall spectrum usage along the entire path
    path_spectrum = np.logical_or.reduce([self.spectrum[self._get_edge_key((path[j], path[j+1]))] for j in range(len(path) - 1)])
    
    # Search for the first block of contiguous slots that satisfies both spectrum availability and GSNR requirements
    # Note: This implementation is currently identical to first_fit, but can be modified for truly flexible assignment
    for i in range(self.num_channels - required_slots + 1):
        if not np.any(path_spectrum[i:i+required_slots]) and all(x >= modulation_threshold for x in path_all_gsnr[i:i+required_slots]):
            return i
    
    # Return -1 if no suitable spectrum block is found
    return -1
