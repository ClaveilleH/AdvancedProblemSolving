from greedy import greedy, compute_cost, read_input_file, tabu_search
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

    print(f"Total cost: {total_cost}")
    return total_cost


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

        last_line_index = 2 + N_endpoint * (1 + N_cache)

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
    caches = [[] for _ in range(N_cache)]  # la liste des videos stockÃ©s dans chaque cache

    caches=greedy( N_vid, N_endpoint, N_request, N_cache, cache_size, video_sizes, endpoints, requests)

    print("Caches content:")
    for i, cache in enumerate(caches):
        print(f"Cache {i}: {cache}")
    print("score:")

    cost= compute_cost(caches, endpoints, requests)


        
        


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        main(["instances/kittens.in"])  # Default input file for testing
    else:
        main(sys.argv[1:])





        





    
