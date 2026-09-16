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



def local_search(adj_list,N_vid, N_endpoint, N_requests, N_caches, caches_sizes, videoSizes, caches, endpointData, requests, iteration=10, nbCaches=None, nbVideos=None):
    if iteration == 0:
        return caches, caches_sizes
    if nbCaches is None or nbCaches > N_caches:
        nbCaches = N_caches
    if nbVideos is None or nbVideos > N_vid:
        nbVideos = N_vid
    
   # print(f"Testing local search iteration {iteration} with {nbCaches}/{N_caches} caches and {nbVideos}/{N_vid} videos")
    # base_cost = compute_cost(caches, endpointData, requests)
    best_delta=float('inf')
    best_move=[0,0]
    # ajouts
    for cache_id in random.sample(range(N_caches), nbCaches):
        cache = caches[cache_id]
        for videoId in random.sample(range(N_vid), nbVideos):
           # print(f"Checking video {videoId} for cache {cache_id}")
            if videoId in cache:
                continue
            if videoSizes[videoId] <= caches_sizes[cache_id]:
                current_video_cost = calculate_video_latency(adj_list, caches, videoId, N_vid, N_endpoint, N_requests, N_caches, caches_sizes, videoSizes, endpointData, requests)
                caches[cache_id].add(videoId)
                new_video_cost = calculate_video_latency(adj_list, caches, videoId, N_vid, N_endpoint, N_requests, N_caches, caches_sizes, videoSizes, endpointData, requests)
                delta = new_video_cost - current_video_cost
                caches[cache_id].remove(videoId)
                if delta < best_delta:
                    best_delta = delta
                    best_move = (cache_id, videoId)
    caches[best_move[0]].add(best_move[1])
    caches_sizes[best_move[0]] -= videoSizes[best_move[1]]

    
    return local_search(adj_list,N_vid, N_endpoint, N_requests, N_caches, caches_sizes, videoSizes, caches, endpointData, requests, iteration-1, nbCaches, nbVideos)
                
