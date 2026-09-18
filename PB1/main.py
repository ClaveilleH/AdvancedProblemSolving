from greedy import greedy
from local_search import tabu_search


def compute_cost(cache, endpoints, requests):
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


def make_adj_list(N_vid,N_endpoint,N_requests,N_caches,caches_capa,VideoSizes,EndpointData,Requests):
    """return a list of list where res[i]coresponds to the list of index of the requests that asked for video i """
    res=[[] for _ in range(N_vid)]
    for j in range(N_requests):
        vid_id,_,_=Requests[j]
        res[vid_id].append(j)
    return res



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
    adj_list = make_adj_list(N_vid,N_endpoint,N_request,N_cache,cache_size,video_sizes,endpoints,requests)
    caches_sizes=[cache_size]*N_cache
    print("greedy")
    caches=greedy(caches_sizes,N_vid,N_endpoint,N_request,N_cache,cache_size,video_sizes,endpoints,requests)
  
    
    print("score:")

    cost= compute_cost(caches, endpoints, requests)
    print("local search")
    iteration=1000
    nbCaches=10
    nbVideos=10
    nb_forbiden_moves=10
    forbiden_moves = [None] * nb_forbiden_moves

    caches = tabu_search(nb_forbiden_moves,forbiden_moves,adj_list,N_vid, N_endpoint, N_request, N_cache, caches_sizes, video_sizes, caches, endpoints, requests, iteration , nbCaches, nbVideos)

   
    print("score after local search:")
    cost= compute_cost(caches, endpoints, requests)
        


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        main(["instances/test.in"])  # Default input file for testing
    else:
        main(sys.argv[1:])





        





    
