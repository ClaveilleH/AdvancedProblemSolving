import random


def Sort_vid(N_vid,Requests):
    N_request_per_video=[0]*N_vid
    for request in Requests:
        vid_id,endpoint_id,num_requests=request
        N_request_per_video[vid_id]+=num_requests
    return sorted(range(N_vid), key=lambda x: N_request_per_video[x], reverse=True)
    

def greedy(N_vid,N_endpoint,N_requests,N_caches,caches_capa,VideoSizes,EndpointData,Requests):
    Sorted_requests=sorted(Requests,key=lambda x: x[2],reverse=True)
    res=[[] for _ in range(N_caches)]
    cap_per_cache=[caches_capa]*N_caches
    for request_id in range(N_requests):
        vid_id,endpoint_id,num_requests=Sorted_requests[request_id]
        latency,linked_caches=EndpointData[endpoint_id]
        fastest_latency=latency
        fastest_cache=None
        for lc in linked_caches :
            cacheid,cache_latency=lc

            if cache_latency<fastest_latency and cap_per_cache[cacheid]>=VideoSizes[vid_id]:
                fastest_latency=cache_latency
                fastest_cache=cacheid
        if fastest_cache!=None and vid_id not in res[fastest_cache]:
            res[fastest_cache].append(vid_id)
            cap_per_cache[fastest_cache]-=VideoSizes[vid_id]
    return res

def get_neighbors(N,M,caches, N_vid, N_caches,Requests):
    neighbors=[]
    Bigger_vid=Sort_vid(N_vid,Requests)
    Bigger_vid=Bigger_vid[:N]
    for vid_id in Bigger_vid:
        for cache_id in random.sample(range(N_caches), M):
            new_caches= caches.copy()
            if vid_id not in caches[cache_id]  :
              new_caches[cache_id].append(vid_id) #add a video to a cache
              neighbors.append(new_caches)
            else:
              new_caches[cache_id].remove(vid_id) #remove a video from a cache
              neighbors.append(new_caches)
    
    return neighbors

def tabu_search(N_iter,N_forbid_step,N,M,N_vid,N_endpoint,N_requests,N_caches,caches_capa,VideoSizes,EndpointData,Requests):
    res=greedy(N_vid,N_endpoint,N_requests,N_caches,caches_capa,VideoSizes,EndpointData,Requests)
    forbiden_moves=[None]*N_forbid_step
    for i in range  (N_iter):
        print(f"Iteration {i+1}/{N_iter}")
        neighbors= get_neighbors(N,M,res,N_vid,N_caches,Requests)
        print(f"Number of neighbors: {len(neighbors)}")

        best_neighbor=None
        best_cost=float('inf')
        for neighbor in neighbors:
            cost=compute_cost(neighbor,EndpointData,Requests)
            if cost<best_cost and neighbor not in forbiden_moves:
                best_cost=cost
                best_neighbor=neighbor
        if best_neighbor!=None:
            res=best_neighbor
            forbiden_moves[i%N_forbid_step]=best_neighbor
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

    caches=tabu_search(1, 7, 2,3, N_vid, N_endpoint, N_request, N_cache, cache_size, video_sizes, endpoints, requests)

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





        





    
