import random
from utils import calculate_video_latency, compute_cost
#! ATTENTION : supprimer l'utilisation de compute_cost dans local_search

def tabu_search(iter_step,nb_forbiden_moves,forbiden_moves,adj_list,N_vid, N_endpoint, N_requests, N_caches, caches_sizes, videoSizes, caches, endpointData, requests, iteration=10, nbCaches=None, nbVideos=None):
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
            if videoId in cache or (cache_id, videoId) in forbiden_moves:
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
    forbiden_moves[iter_step % nb_forbiden_moves] = best_move

    
    return tabu_search(iter_step + 1, nb_forbiden_moves, forbiden_moves, adj_list,N_vid, N_endpoint, N_requests, N_caches, caches_sizes, videoSizes, caches, endpointData, requests, iteration-1, nbCaches, nbVideos)
                

def local_search(N_vid, N_endpoint, N_requests, N_caches, adj_list, videoSizes, caches_sizes, caches, endpointData, requests, iteration=10, previous_moves=None, nbCaches=None, nbVideos=None, supp = False):
    if iteration == 0:
        return caches, caches_sizes
    if nbCaches is None or nbCaches > N_caches:
        nbCaches = N_caches
    if nbVideos is None or nbVideos > N_vid:
        nbVideos = N_vid
    if iteration == 0:
        return caches, caches_sizes

    # print(f"previous_moves={previous_moves}")

    # print(f"Testing local search iteration {iteration} with {nbCaches}/{N_caches} caches and {nbVideos}/{N_vid} videos")
    # base_cost = compute_cost(caches, endpointData, requests)
    neighbors = []  # (cost, caches, caches_sizes, move)
    cost = compute_cost(caches, endpointData, requests)
    # ajouts
    for cache_id in range(nbCaches):
        cache = caches[cache_id]
        for video in range(nbVideos):
            # print(f"Checking video {videoId} for cache {cache_id}")
            if video in cache:
                continue
            if videoSizes[video] <= caches_sizes[caches.index(cache)]:
                previous_cost = calculate_video_latency(adj_list, caches, video, N_vid, N_endpoint, N_requests, N_caches, caches_sizes, videoSizes, endpointData, requests)
                caches[cache_id].append(video)
                new_cost = calculate_video_latency(adj_list, caches, video, N_vid, N_endpoint, N_requests, N_caches, caches_sizes, videoSizes, endpointData, requests)
                delta = new_cost - previous_cost

                caches[cache_id].remove(video)
                move = (1, cache_id, video) # 1 for addition, 0 for removal
                neighbors.append((video, cost + delta, caches, caches_sizes, move))

    # suppression
    if supp:
        for cache_id in range(nbCaches):
            cache = caches[cache_id]
            for video in cache[:nbVideos]:  # Only consider the first nbVideos videos in the cache for removal
                previous_cost = calculate_video_latency(adj_list, caches, video, N_vid, N_endpoint, N_requests, N_caches, caches_sizes, videoSizes, endpointData, requests)
                caches[cache_id].remove(video)
                new_cost = calculate_video_latency(adj_list, caches, video, N_vid, N_endpoint, N_requests, N_caches, caches_sizes, videoSizes, endpointData, requests)
                delta = new_cost - previous_cost
                # cost = compute_cost(caches, endpointData, requests)
                caches[cache_id].append(video)
                move = (0, cache_id, video) # 1 for addition, 0 for removal
                neighbors.append((video, cost + delta, caches, caches_sizes, move))

    neighbors.sort(key=lambda x: x[1])
    if neighbors is None or len(neighbors) == 0:
        print(f"No neighbors found at iteration {iteration}, current state: previous_moves={previous_moves}, nVideos={nbVideos}, nCaches={nbCaches}, supp={supp}")
        return caches, caches_sizes
    best_neighbor = neighbors[0] if neighbors else (float('inf'), caches, caches_sizes, None)
    # print(f"Best neighbor: {best_neighbor} with cost {best_neighbor[1]}")
    #on applique le mouvement du meilleur voisin
    if best_neighbor[4][0] == 1:
        caches[best_neighbor[4][1]].append(best_neighbor[4][2])
    else:
        # print(f"Supression")
        caches[best_neighbor[4][1]].remove(best_neighbor[4][2])
    # caches[best_neighbor[4][1]].append(best_neighbor[4][2])

    caches_sizes[best_neighbor[4][0]] -= videoSizes[best_neighbor[4][1]]
    
#          local_search(N_vid, N_endpoint, N_request, N_cache, adj_list, video_sizes, caches_sizes, caches, endpoints, requests, iteration=10, previous_moves=None, nbCaches=50, nbVideos=100, supp=True)
    return local_search(N_vid, N_endpoint, N_requests, N_caches, adj_list, videoSizes, caches_sizes, caches, endpointData, requests, iteration-1, best_neighbor[4], nbCaches, nbVideos, supp)
                

    # for videos 
                
def preprocess_data(N_vid, N_endpoint, N_requests, N_caches, caches_sizes, videoSizes, caches, endpointData, requests):
    """
    Preprocess the data to sort the videos by size and number of requests.
    """
    video_request_count = [0] * N_vid
    video_endpoint_data = [0] * N_vid  # To store the endpoint data for each video
    for video_id, endpoint_id, num_requests in requests:
        video_request_count[video_id] += num_requests


    # Create a list of videos with their sizes and request counts
    videos_info = [(video_id, videoSizes[video_id], video_request_count[video_id], ) for video_id in range(N_vid)]
    

    # Sort videos by request count (descending) and then by size (ascending)
    videos_info.sort(key=lambda x: (-x[2], x[1]))

    video_sizes_sorted = [video[1] for video in videos_info]
    return video_sizes_sorted, videos_info

