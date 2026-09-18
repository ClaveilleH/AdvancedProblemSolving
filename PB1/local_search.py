import random

def calculate_video_latency(adj_list,caches,vid_id,N__vid,N_endpoint,N_requests,N_caches,caches_capa,VideoSizes,EndpointData,Requests):
    total_cost=0
    for i in adj_list[vid_id]:
        video_id, endpoint_id, num_requests = Requests[i]
        endpoint_latency, linked_caches = EndpointData[endpoint_id]
        min_latency = endpoint_latency
        for cache_id, cache_latency in linked_caches:
            if video_id in caches[cache_id] and cache_latency < min_latency:
                    min_latency = cache_latency
        total_cost += num_requests * min_latency
        
    return total_cost



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

def tabu_search(nb_forbiden_moves,forbiden_moves,adj_list,N_vid, N_endpoint, N_requests, N_caches, caches_sizes, videoSizes, caches, endpointData, requests, iteration=10, nbCaches=None, nbVideos=None):
    
    if nbCaches is None or nbCaches > N_caches:
        nbCaches = N_caches
    if nbVideos is None or nbVideos > N_vid:
        nbVideos = N_vid
    best_caches = [c.copy() for c in caches]
    current_total_delta = 0
    best_total_delta=0

    for iter_step in range(iteration):
        best_delta = float('inf')
        best_move = None

        for cache_id in random.sample(range(N_caches), nbCaches):
            cache = caches[cache_id]
            for videoId in random.sample(range(N_vid), nbVideos):
                ...  # unchanged evaluation

        if best_move is None:
            break

        if best_move[2] == 0:
            caches[best_move[0]].remove(best_move[1])
            caches_sizes[best_move[0]] += videoSizes[best_move[1]]
            forbiden_moves[iter_step % nb_forbiden_moves] = (best_move[0], best_move[1], 1)
        else:
            caches[best_move[0]].add(best_move[1])
            caches_sizes[best_move[0]] -= videoSizes[best_move[1]]
            forbiden_moves[iter_step % nb_forbiden_moves] = (best_move[0], best_move[1], 0)


        current_total_delta += best_delta
        if current_total_delta < best_total_delta:
            best_total_delta = current_total_delta
            best_caches = [c.copy() for c in caches]
            best_sizes = list(caches_sizes)

    return best_caches