def has_close_elements(numbers, threshold):
    for i in numbers:
        for j in numbers:
            if abs(i - j) < threshold:
                return True
    return False