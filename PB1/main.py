from copy import deepcopy
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

    results = {
        "Base": base_cost,
    }

    # ========================== TESTING ==========================
    #! ######## Test greedy algorithm
    from greedy import greedy
    current_time = time.time()
    greedy(N_vid, N_endpoint, N_request, N_cache, caches_sizes, video_sizes, endpoints, requests, caches)
    time_taken = time.time() - current_time
    # print(f"[{time_taken:.4f}s] Greedy algorithm completed")
    results["Greedy"] = compute_cost(caches, endpoints, requests)
    # print(f"Cost after greedy: {results['Greedy']}")
    print(f"[{time_taken:.4f}s] Greedy : {results['Greedy']} ({(base_cost - results['Greedy']) / base_cost * 100:.2f}%)")
    caches_after_greedy = deepcopy(caches)
    caches_sizes_after_greedy = deepcopy(caches_sizes)
    
    #! ######## Test greedy2 
    from greedy2 import greedy2
    caches = [[] for _ in range(N_cache)]  # la liste des videos stockés dans chaque cache
    caches_sizes = [cache_size] * N_cache  # la taille restante de chaque cache
    
    current_time = time.time()
    greedy2(N_vid, N_endpoint, N_request, N_cache, caches_sizes, video_sizes, endpoints, requests, caches)
    time_taken = time.time() - current_time

    results["Greedy2"] = compute_cost(caches, endpoints, requests)
    print(f"[{time_taken:.4f}s] Greedy2 : {results['Greedy2']} ({(base_cost - results['Greedy2']) / base_cost * 100:.2f}%)")

    caches_after_greedy2 = deepcopy(caches)
    caches_sizes_after_greedy2 = deepcopy(caches_sizes)

    #! ######## Test local search algorithm
    from local_search import preprocess_data
    current_time = time.time()
    caches = deepcopy(caches_after_greedy)
    caches_sizes = deepcopy(caches_sizes_after_greedy)
    video_sizes_sorted, videos_info = preprocess_data(N_vid, N_endpoint, N_request, N_cache, caches_sizes, video_sizes, caches, endpoints, requests)
    video_sizes = video_sizes_sorted
    # print(f"Preprocessing: {time.time() - current_time:.4f}s")

    from local_search import local_search
    current_time = time.time()
    local_search(N_vid, N_endpoint, N_request, N_cache, adj_list, video_sizes, caches_sizes, caches, endpoints, requests, iteration=10, previous_moves=None, nbCaches=10, nbVideos=10, supp=True)
    time_taken = time.time() - current_time
    results["LS (greedy)"] = compute_cost(caches, endpoints, requests)
    print(f"[{time_taken:.4f}s] Local Search (Greedy) : {results['LS (greedy)']} ({(base_cost - results['LS (greedy)']) / base_cost * 100:.2f}%)")

    #! ######## Test local search algorithm with greedy2
    current_time = time.time()
    caches = deepcopy(caches_after_greedy2)
    caches_sizes = deepcopy(caches_sizes_after_greedy2)
    # print(f"Preprocessing: {time.time() - current_time:.4f}s")

    local_search(N_vid, N_endpoint, N_request, N_cache, adj_list, video_sizes, caches_sizes, caches, endpoints, requests, iteration=10, previous_moves=None, nbCaches=10, nbVideos=10, supp=True)
    time_taken = time.time() - current_time
    results["LS (Greedy2)"] = compute_cost(caches, endpoints, requests)
    print(f"[{time_taken:.4f}s] Local Search (Greedy2) : {results['LS (Greedy2)']} ({(base_cost - results['LS (Greedy2)']) / base_cost * 100:.2f}%)")

    #! ######## Test tabu search algorithm
    from local_search import random_tabu_search
    iteration=10
    nbCaches=10
    nbVideos=10
    nb_forbiden_moves=0
    caches = [set(cache) for cache in caches_after_greedy]
    caches_sizes = deepcopy(caches_sizes_after_greedy)
    random_tabu_search(nb_forbiden_moves,adj_list,N_vid, N_endpoint, N_request, N_cache, caches_sizes, video_sizes, caches, endpoints, requests, iteration , nbCaches, nbVideos)
    results["TS (Greedy)"] = compute_cost(caches, endpoints, requests)
    print(f"[{time_taken:.4f}s] Tabu Search (Greedy) : {results['TS (Greedy)']} ({(base_cost - results['TS (Greedy)']) / base_cost * 100:.2f}%)")

    #! ######## Test tabu search algorithm with greedy2
 
    caches = [set(cache) for cache in caches_after_greedy2]
    caches_sizes = deepcopy(caches_sizes_after_greedy2)
    random_tabu_search(nb_forbiden_moves,adj_list,N_vid, N_endpoint, N_request, N_cache, caches_sizes, video_sizes, caches, endpoints, requests, iteration , nbCaches, nbVideos)
    results["TS (Greedy2)"] = compute_cost(caches, endpoints, requests)
    print(f"[{time_taken:.4f}s] Tabu Search (Greedy2) : {results['TS (Greedy2)']} ({(base_cost - results['TS (Greedy2)']) / base_cost * 100:.2f}%)")

    from local_search import sorted_tabu_search
    
    caches = [set(cache) for cache in caches_after_greedy]
    caches_sizes = deepcopy(caches_sizes_after_greedy)
    sorted_tabu_search(nb_forbiden_moves,adj_list,N_vid, N_endpoint, N_request, N_cache, caches_sizes, video_sizes, caches, endpoints, requests, iteration , nbCaches, nbVideos)
    results["TS (Greedy)"] = compute_cost(caches, endpoints, requests)
    print(f"[{time_taken:.4f}s] sorted tabu Search (Greedy) : {results['TS (Greedy)']} ({(base_cost - results['TS (Greedy)']) / base_cost * 100:.2f}%)")

    #! ######## Test tabu search algorithm with greedy2
   
    caches = [set(cache) for cache in caches_after_greedy2]
    caches_sizes = deepcopy(caches_sizes_after_greedy2)
    sorted_tabu_search(nb_forbiden_moves,adj_list,N_vid, N_endpoint, N_request, N_cache, caches_sizes, video_sizes, caches, endpoints, requests, iteration , nbCaches, nbVideos)
    results["TS (Greedy2)"] = compute_cost(caches, endpoints, requests)
    print(f"[{time_taken:.4f}s] sorted tabu Search (Greedy2) : {results['TS (Greedy2)']} ({(base_cost - results['TS (Greedy2)']) / base_cost * 100:.2f}%)")


    print_comparison_table(results)
    best_method = min(results, key=results.get)
    print(f"\nBest method: {best_method} with cost {results[best_method]} and improvement of {base_cost - results[best_method]} ({(base_cost - results[best_method]) / base_cost * 100:.2f}%)")
       

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        main(["instances/test.in"])  # Default input file for testing
    else:
        main(sys.argv[1:])