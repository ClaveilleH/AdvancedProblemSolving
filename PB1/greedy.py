import random





def greedy(caches_sizes, N_vid, N_endpoint, N_requests, N_caches, caches_capa, videoSizes, endpointData, requests):
    # tri des requêtes par nombre de requêtes décroissant
    sorted_requests = sorted(requests,key=lambda x: x[2],reverse=True)
    res=[set() for _ in range(N_caches)]

    for request_id in range(N_requests):
        vid_id, endpoint_id, num_requests = sorted_requests[request_id]
        latency, linked_caches = endpointData[endpoint_id]
        fastest_latency = latency
        fastest_cache = None

        for lc in linked_caches :
            cacheid, cache_latency = lc

            if cache_latency < fastest_latency and caches_sizes[cacheid] >= videoSizes[vid_id]:
                fastest_latency = cache_latency
                fastest_cache = cacheid

        if fastest_cache != None and vid_id not in res[fastest_cache]:
            res[fastest_cache].add(vid_id)
            caches_sizes[fastest_cache] -= videoSizes[vid_id]
            
    return res
