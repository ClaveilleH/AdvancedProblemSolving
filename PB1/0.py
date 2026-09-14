import copy
cpt = 0

def compute_cost(cache, endpoints, requests):
    # Placeholder for cost computation logic
    total_cost = 0
    for request in requests:
        video_id, endpoint_id, num_requests = request
        endpoint_latency, linked_caches = endpoints[endpoint_id]

        min_latency = endpoint_latency
        for cache_id, cache_latency in linked_caches:
            if video_id in cache[cache_id]:
                if cache_latency < min_latency:
                    min_latency = cache_latency
                # print(f"Cache {cache_id} with latency {cache_latency}")
        
        total_cost += num_requests * min_latency

    # print(f"Total cost: {total_cost}")
    return total_cost



def greedy_algorithm(N_vid, N_endpoint, N_request, N_cache, caches, caches_sizes, video_sizes, endpoints, requests):
    cost_min = compute_cost(caches, endpoints, requests)
    for video_id in range(N_vid):
        video_size = video_sizes[video_id]
        for cache_id in range(N_cache):
            if video_size <= caches_sizes[cache_id]:
                # Check if the video is already in the cache
                if video_id not in caches[cache_id]:
                    caches[cache_id].append(video_id)
                    if compute_cost(caches, endpoints, requests) < cost_min:
                        cost_min = compute_cost(caches, endpoints, requests)
                        # caches_size -= video_size
                        caches_sizes[cache_id] -= video_size
                    else:
                        caches[cache_id].remove(video_id)  # Remove the video if it doesn't improve the cost    

            
def local_search(N_vid, N_endpoint, N_request, N_cache, caches, caches_sizes, video_sizes, endpoints, requests, interation = 10, prev_mod=None):
    # Placeholder for deep search algorithm
    # This function should implement a more exhaustive search to find a better solution
    """
    On regarde tout les voisins d'une solution, on prend le meilleur voisin et on recommence jusqu'à ce qu'on ne puisse plus améliorer la solution.
    """
    if interation == 0:
        return caches, caches_sizes
    global cpt
    cpt += 1
    base_cost = compute_cost(caches, endpoints, requests)
    voisins = [] # (cost, caches, caches_sizes)
    for video_id in range(N_vid):
        video_size = video_sizes[video_id]
        for cache_id in range(N_cache):
            # Check if the video is already in the cache
            if video_id not in caches[cache_id]:
                if video_size <= caches_sizes[cache_id]:
                    new_caches = copy.deepcopy(caches)
                    new_caches_sizes = copy.deepcopy(caches_sizes)
                    new_caches[cache_id].append(video_id)
                    new_caches_sizes[cache_id] -= video_size
                    new_cost = compute_cost(new_caches, endpoints, requests)
                    voisins.append((new_cost, new_caches, new_caches_sizes))

    best_voisin_cost = base_cost
    best_voisin = (caches, caches_sizes)
    for voisin in voisins:
        if voisin[0] < best_voisin_cost:
            best_voisin_cost = voisin[0]
            best_voisin = (voisin[1], voisin[2])

    if best_voisin_cost < base_cost:
        # print(f"Found a better neighbor with cost {best_voisin_cost}")
        return local_search(N_vid, N_endpoint, N_request, N_cache, best_voisin[0], best_voisin[1], video_sizes, endpoints, requests)
    
    return best_voisin

def read_input_file(input_file):
    try:
        f = open(input_file, 'r')
        # data = f.read().strip().splitlines()
    

        N_vid, N_endpoint, N_request, N_cache, cache_size = map(int, f.readline().split())
        # print(f"Number of videos: {N_vid}, Number of endpoints: {N_endpoint}, Number of requests: {N_request}, Number of caches: {N_cache}, Cache size: {cache_size}")
        video_sizes = list(map(int, f.readline().split()))
        endpoints = []
        for end_id in range(N_endpoint):
            latency, NlinkedCaches = map(int, f.readline().split())
            linked_caches = []
            for cache_id in range(NlinkedCaches):
                cache_info = list(map(int, f.readline().split()))
                linked_caches.append((cache_info[0], cache_info[1]))  # (cache_id, latency)
            endpoints.append((latency, linked_caches))
        # print(f"Endpoints: {endpoints}")

        requests = []
        for req_id in range(N_request):
            video_id, endpoint_id, num_requests = map(int, f.readline().split())
            requests.append((video_id, endpoint_id, num_requests))
    except FileNotFoundError:
            print(f"Error: File '{input_file}' not found.")
            return

    return N_vid, N_endpoint, N_request, N_cache, cache_size, video_sizes, endpoints, requests



def main(args):
    if len(args) != 1:
        print("Usage: python greedy.py <input_file>")
        return

    input_file = args[0]

    N_vid, N_endpoint, N_request, N_cache, cache_size, video_sizes, endpoints, requests = read_input_file(input_file)
    caches = [[] for _ in range(N_cache)]  # la liste des videos stockés dans chaque cache
    caches_sizes = [cache_size] * N_cache  # la taille restante de chaque cache

    base = N_vid, N_endpoint, N_request, N_cache, caches, caches_sizes, video_sizes, endpoints, requests
    # on deepcopy la base pour ne pas modifier les données originales lors de l'algorithme glouton

    base = copy.deepcopy(base)

    # =================================================
    greedy_algorithm(N_vid, N_endpoint, N_request, N_cache, caches, caches_sizes, video_sizes, endpoints, requests)

    print("Caches content:")
    for i, cache in enumerate(caches):
        print(f"Cache {i}: {cache}")

    print("Cost computation:")
    greedyResult = compute_cost(caches, endpoints, requests)
    print(f"Total cost after greedy algorithm: {greedyResult}")

    # =================================================
    N_vid, N_endpoint, N_request, N_cache, caches, caches_sizes, video_sizes, endpoints, requests = base

    caches, caches_sizes = local_search(N_vid, N_endpoint, N_request, N_cache, caches, caches_sizes, video_sizes, endpoints, requests)

    print("Caches content after local search:")
    for i, cache in enumerate(caches):
        print(f"Cache {i}: {cache}")

    deep_search_result = compute_cost(caches, endpoints, requests)
    print(f"Total cost after local search: {deep_search_result}")
    print(f"Number of recursive calls in local search: {cpt}")






        
        


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        main(["instances/test.in"])  # Default input file for testing
    else:
        main(sys.argv[1:])