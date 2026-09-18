from utils import compute_cost, make_adj_list, read_input_file, print_comparison_table


def main(args):
    import time
    if len(args) != 1:
        print("Usage: python greedy.py <input_file>")
        return

    # ========================== INIT ==========================

    
    input_file = args[0]
    N_vid, N_endpoint, N_request, N_cache, cache_size, video_sizes, endpoints, requests = read_input_file(input_file)
    caches = [[] for _ in range(N_cache)]  # la liste des videos stockés dans chaque cache
    caches_sizes = [cache_size] * N_cache  # la taille restante de chaque cache

    current_time = time.time()
    base_cost = compute_cost(caches, endpoints, requests)
    print(f"[{time.time() - current_time:.4f}s] Base cost (no videos in caches): {base_cost}")

    current_time = time.time()
    global adj_list
    adj_list = make_adj_list(N_vid, N_request, requests)
    print(f"[{time.time() - current_time:.4f}s] Adjacency list created")

    # ========================== TESTING ==========================
    #! Test greedy algorithm
    

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        main(["instances/test.in"])  # Default input file for testing
    else:
        main(sys.argv[1:])