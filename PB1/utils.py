
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

    # print(f"Total cost: {total_cost}")
    return total_cost


def make_adj_list(N_vid, N_requests, requests):
    """
    return a list of list where res[i] coresponds to the list of index of 
    the requests that asked for video i 
    """
    res = [[] for _ in range(N_vid)]

    for j in range(N_requests):
        vid_id, _, _ = requests[j]
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


def print_comparison_table(results):
    """
    Fonction générée par claude
    results : dict {nom_méthode: cout}
    Affiche un tableau ASCII où la case [i][j] = amélioration (%) 
    de la méthode j par rapport à la méthode i.
    amélioration > 0 => j est meilleur (coût plus bas) que i
    """
    names = list(results.keys())
    n = len(names)

    # largeur de colonne = max entre nom le plus long et 8 (pour "+123.45%")
    col_width = max(max(len(n_) for n_ in names), 9) + 2

    def cell(i, j):
        if i == j:
            return "-"
        ci, cj = results[names[i]], results[names[j]]
        if ci == 0:
            return "n/a"
        improvement = (ci - cj) / ci * 100
        return f"{improvement:+.2f}%"

    # ligne d'en-tête
    header = " " * col_width + "|" + "|".join(f"{n_:^{col_width}}" for n_ in names)
    sep = "-" * len(header)

    print(sep)
    print(header)
    print(sep)
    for i, name_i in enumerate(names):
        row = f"{name_i:<{col_width}}|" + "|".join(f"{cell(i, j):^{col_width}}" for j in range(n))
        print(row)
    print(sep)


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