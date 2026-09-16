
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

    # print(f"Total cost: {total_cost}")
    return total_cost




def greedy(N_vid, N_endpoint, N_requests, N_caches, caches_sizes, videoSizes, caches, endpointData, requests):
    """
    
    """
    for request_id in range(N_requests):
        vidId,endpoint_id,numRequests=requests[request_id]
        latency,linkedCaches=endpointData[endpoint_id]
        lowestLatency=latency
        fastestCache=None

        for lc in linkedCaches :
            cacheId,cache_latency=lc
            
            if cache_latency < lowestLatency and caches_sizes[cacheId] >= videoSizes[vidId]:
                lowestLatency=cache_latency
                fastestCache=cacheId

        if fastestCache!=None and vidId not in caches[fastestCache]:
            caches[fastestCache].append(vidId)
            caches_sizes[fastestCache] -= videoSizes[vidId]
    return caches

def local_search(N_vid, N_endpoint, N_requests, N_caches, caches_sizes, videoSizes, caches, endpointData, requests, iteration=10, previous_moves=None, nbCaches=None, nbVideos=None):
    if iteration == 0:
        return caches, caches_sizes
    if nbCaches is None or nbCaches > N_caches:
        nbCaches = N_caches
    if nbVideos is None or nbVideos > N_vid:
        nbVideos = N_vid
    if iteration == 0:
        return caches, caches_sizes
    # print(f"Testing local search iteration {iteration} with {nbCaches}/{N_caches} caches and {nbVideos}/{N_vid} videos")
    # base_cost = compute_cost(caches, endpointData, requests)
    neighbors = []  # (cost, caches, caches_sizes, move)

    # ajouts
    for cache_id in range(nbCaches):
        cache = caches[cache_id]
        for video in range(nbVideos):
            # print(f"Checking video {videoId} for cache {cache_id}")
            if video in cache:
                continue
            if videoSizes[video] <= caches_sizes[caches.index(cache)]:
                caches[cache_id].append(video)
                cost = compute_cost(caches, endpointData, requests)
                caches[cache_id].remove(video)
                move = (1, cache_id, video) # 1 for addition, 0 for removal
                neighbors.append((video, cost, caches, caches_sizes, move))

    # suppression
    if True:  # Disable removal for now
        for cache_id in range(nbCaches):
            cache = caches[cache_id]
            for video in cache[:nbVideos]:  # Only consider the first nbVideos videos in the cache for removal
                caches[cache_id].remove(video)
                cost = compute_cost(caches, endpointData, requests)
                caches[cache_id].append(video)
                move = (0, cache_id, video) # 1 for addition, 0 for removal
                neighbors.append((video, cost, caches, caches_sizes, move))

    neighbors.sort(key=lambda x: x[1])
    if neighbors is None or len(neighbors) == 0:
        print("No neighbors found, returning current state")
        return caches, caches_sizes
    best_neighbor = neighbors[0] if neighbors else (float('inf'), caches, caches_sizes, None)
    # print(f"Best neighbor: {best_neighbor} with cost {best_neighbor[1]}")
    #on applique le mouvement du meilleur voisin
    if best_neighbor[4][0] == 1:
        caches[best_neighbor[4][1]].append(best_neighbor[4][2])
    else:
        print(f"Supression")
        caches[best_neighbor[4][1]].remove(best_neighbor[4][2])
    # caches[best_neighbor[4][1]].append(best_neighbor[4][2])

    caches_sizes[best_neighbor[4][0]] -= videoSizes[best_neighbor[4][1]]
    

    return local_search(N_vid, N_endpoint, N_requests, N_caches, caches_sizes, videoSizes, caches, endpointData, requests, iteration-1, best_neighbor[3], nbCaches, nbVideos)
                

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



def read_input_file(input_file):
    """
    entrée : 
    input_file : str : nom du fichier d'entrée
    ---
    sortie : 
    N_vid : int : nombre de vidéos
    N_endpoint : int : nombre d'endpoints
    N_request : int : nombre de requêtes
    N_cache : int : nombre de caches
    cache_size : int : taille d'un cache
    video_sizes : list[int] : taille de chaque vidéo
    endpoints : list[tuple[int, list[tuple[int, int]]]] : liste des endpoints avec leur latence et les caches liés
    requests : list[tuple[int, int, int]] : liste des requêtes avec l'id de la vidéo, l'id de l'endpoint et le nombre de requêtes
    ---
    """
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
    # print(endpoints)
    # print(requests)
    print(f"{N_vid} videos, {N_endpoint} endpoints, {N_request} requests, {N_cache} caches, cache size {cache_size}")
    return N_vid, N_endpoint, N_request, N_cache, cache_size, video_sizes, endpoints, requests


def main(args):
    import time
    if len(args) != 1:
        print("Usage: python greedy.py <input_file>")
        return

    input_file = args[0]

    N_vid, N_endpoint, N_request, N_cache, cache_size, video_sizes, endpoints, requests = read_input_file(input_file)
    caches = [[] for _ in range(N_cache)]  # la liste des videos stockés dans chaque cache
    caches_sizes = [cache_size] * N_cache  # la taille restante de chaque cache

    greedy(N_vid, N_endpoint, N_request, N_cache, caches_sizes, video_sizes, caches, endpoints, requests)

    if sum([len(cache) for cache in caches]) < 20:
        print("Caches content:")
        for i, cache in enumerate(caches):
            print(f"Cache {i}: {cache}")


    greedyCost= compute_cost(caches, endpoints, requests)
    print(f"Greedy : {greedyCost}")


    current_time = time.time()
    video_sizes_sorted, videos_info = preprocess_data(N_vid, N_endpoint, N_request, N_cache, caches_sizes, video_sizes, caches, endpoints, requests)
    video_sizes = video_sizes_sorted
    print(f"Preprocessing time: {time.time() - current_time:.4f} seconds")
    current_time = time.time()
    local_search(N_vid, N_endpoint, N_request, N_cache, caches_sizes, video_sizes, caches, endpoints, requests, iteration=20, previous_moves=None, nbCaches=50, nbVideos=100)
    print(f"Local search time: {time.time() - current_time:.4f} seconds")

    if sum([len(cache) for cache in caches]) < 20:  
        print("Final caches content:")
        for i, cache in enumerate(caches):
            print(f"Cache {i}: {cache}")

    localSearchCost = compute_cost(caches, endpoints, requests)
    print(f"Local search : {localSearchCost}")

    print(f"Improvement: {greedyCost - localSearchCost} ({(greedyCost - localSearchCost) / greedyCost * 100:.2f}%)")



        
        


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        main(["instances/test.in"])  # Default input file for testing
    else:
        main(sys.argv[1:])