from constants import objective_function, summary

def exhaustive_search(min_pt: float, max_pt: float, delta: float = 0.02, is_minimising: bool = False) -> bool:
    x1 = min_pt
    x2 = x1 + delta
    x3 = x2 + delta

    iter_count: int = 0

    while x3 < max_pt:
        f1 = objective_function(x1)
        f2 = objective_function(x2)
        f3 = objective_function(x3)
        
        iter_count += 1
        summary.append([iter_count, x1, x2, x3, f1, f2, f3])


        if is_minimising and (f1 > f2 and f2 < f3):
            print("Found minima")
            return True

        elif not is_minimising and (f1 < f2 and f2 > f3):
            print("Found maxima")
            return True
        
        x1 = x2
        x2 = x1 + delta
        x3 = x2 + delta

    return False