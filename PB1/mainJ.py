from greedy import greedy
from local_search import tabu_search

from utils import compute_cost, make_adj_list, read_input_file



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





        





    
