import random

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



def calculate_video_latency(adj_list, caches, vid_id, requests, endpoint_data):
    """Total latency cost of all requests that target a given video."""
    total_cost = 0
    for i in adj_list[vid_id]:
        video_id, endpoint_id, num_requests = requests[i]
        endpoint_latency, linked_caches = endpoint_data[endpoint_id]
        min_latency = endpoint_latency
        for cache_id, cache_latency in linked_caches:
            if video_id in caches[cache_id] and cache_latency < min_latency:
                min_latency = cache_latency
        total_cost += num_requests * min_latency
    return total_cost


def compute_cost(caches, endpoints, requests):
    total_cost = 0
    for video_id, endpoint_id, num_requests in requests:
        endpoint_latency, linked_caches = endpoints[endpoint_id]
        min_latency = endpoint_latency
        for cache_id, cache_latency in linked_caches:
            if video_id in caches[cache_id] and cache_latency < min_latency:
                min_latency = cache_latency
        total_cost += num_requests * min_latency
    return total_cost


def tabu_search(nb_forbidden_moves, adj_list, N_vid, N_endpoint,
                 N_requests, N_caches, caches_sizes, video_sizes, caches,
                 endpoint_data, requests, iteration=10, nb_caches=None, nb_videos=None):
    if nb_caches is None or nb_caches > N_caches:
        nb_caches = N_caches
    if nb_videos is None or nb_videos > N_vid:
        nb_videos = N_vid
    forbidden_moves = [None] * nb_forbidden_moves
    best_caches = [c.copy() for c in caches]
    current_total_delta = 0
    best_total_delta = 0

    for iter_step in range(iteration):
        best_delta = float('inf')
        best_move = None  # (cache_id, video_id, action) — action: 0 = remove, 1 = add

        for cache_id in random.sample(range(N_caches), nb_caches):
            cache = caches[cache_id]
            for video_id in random.sample(range(N_vid), nb_videos):
                current_vid_latency = calculate_video_latency(
                    adj_list, caches, video_id, requests, endpoint_data
                )

                if video_id in cache and (cache_id, video_id, 1) not in forbidden_moves:
                    # Try removing it
                    cache.remove(video_id)
                    new_video_latency = calculate_video_latency(
                        adj_list, caches, video_id, requests, endpoint_data
                    )
                    current_delta = new_video_latency - current_vid_latency
                    move = (cache_id, video_id, 0)
                    cache.add(video_id)  # undo, we're just evaluating

                elif (video_id not in cache
                      and caches_sizes[cache_id] >= video_sizes[video_id]
                      and (cache_id, video_id, 0) not in forbidden_moves):
                    # Try adding it (only if it actually fits)
                    cache.add(video_id)
                    new_video_latency = calculate_video_latency(
                        adj_list, caches, video_id, requests, endpoint_data
                    )
                    current_delta = new_video_latency - current_vid_latency
                    move = (cache_id, video_id, 1)
                    cache.remove(video_id)  # undo, we're just evaluating

                else:
                    continue

                if current_delta < best_delta:
                    best_delta = current_delta
                    best_move = move

        if best_move is None:
            break

        move_cache_id, move_video_id, action = best_move
        if action == 0:
            # Actually remove it, and reclaim the space
            caches[move_cache_id].remove(move_video_id)
            caches_sizes[move_cache_id] += video_sizes[move_video_id]
        else:
            # Actually add it, and spend the space
            caches[move_cache_id].add(move_video_id)
            caches_sizes[move_cache_id] -= video_sizes[move_video_id]

        # Ban the reverse of the move we just made
        forbidden_moves[iter_step % nb_forbidden_moves] = (
            move_cache_id, move_video_id, (action + 1) % 2
        )
        current_total_delta += best_delta

        if current_total_delta < best_total_delta:
            best_total_delta = current_total_delta
            best_caches = [c.copy() for c in caches]

    return best_caches