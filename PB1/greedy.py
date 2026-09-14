def greedy(N_vid,N_endpoint,N_requests,N_caches,caches_capa,VideoSizes,EndpointData,Requests):
    res=[[] for _ in range(N_caches)]
    cap_per_cache=[caches_capa]*N_caches
    for request_id in range(N_requests):
        vid_id,endpoint_id,num_requests=Requests[request_id]
        latency,linked_caches=EndpointData[endpoint_id]
        fastest_latency=latency
        fastest_cache=None
        for lc in linked_caches :
            cacheid,cache_latency=lc

            if cache_latency<fastest_latency and cap_per_cache[cacheid]>=VideoSizes[vid_id]:
                fastest_latency=cache_latency
                fastest_cache=cacheid
        if fastest_cache!=None:
            res[fastest_cache].append(vid_id)
            cap_per_cache[fastest_cache]-=VideoSizes[vid_id]
    return res

def local_search(N_vid,N_endpoint,N_requests,N_caches,caches_capa,VideoSizes,EndpointData,Requests):
    res=greedy(N_vid,N_endpoint,N_requests,N_caches,caches_capa,VideoSizes,EndpointData,Requests)
    




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

def main(args):
    if len(args) != 1:
        print("Usage: python greedy.py <input_file>")
        return

    input_file = args[0]

    N_vid, N_endpoint, N_request, N_cache, cache_size, video_sizes, endpoints, requests = read_input_file(input_file)
    caches = [[] for _ in range(N_cache)]  # la liste des videos stockÃ©s dans chaque cache

    caches=greedy(N_vid, N_endpoint, N_request, N_cache, cache_size, video_sizes, endpoints, requests)

    print("Caches content:")
    for i, cache in enumerate(caches):
        print(f"Cache {i}: {cache}")
    print("score:")

    cost= compute_cost(caches, endpoints, requests)


        
        


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        main(["instances/test.in"])  # Default input file for testing
    else:
        main(sys.argv[1:])