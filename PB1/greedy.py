import random





def greedy(    caches_sizes,N_vid,N_endpoint,N_requests,N_caches,caches_capa,VideoSizes,EndpointData,Requests):
    Sorted_requests=sorted(Requests,key=lambda x: x[2],reverse=True)
    res=[set() for _ in range(N_caches)]
    for request_id in range(N_requests):
        vid_id,endpoint_id,num_requests=Sorted_requests[request_id]
        latency,linked_caches=EndpointData[endpoint_id]
        fastest_latency=latency
        fastest_cache=None
        for lc in linked_caches :
            cacheid,cache_latency=lc

            if cache_latency<fastest_latency and caches_sizes[cacheid]>=VideoSizes[vid_id]:
                fastest_latency=cache_latency
                fastest_cache=cacheid
        if fastest_cache!=None and vid_id not in res[fastest_cache]:
            res[fastest_cache].add(vid_id)
            caches_sizes[fastest_cache]-=VideoSizes[vid_id]
    return res
