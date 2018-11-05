"""
Edmonds-Karp algorithm
"""

import argparse

def EdmondsKarp(capacities, m):
    """
    Edmonds-Karp algorithm for computing maximum flow in a flow network from source to sink.
    
    args: 
        C : array [m*m], flow capacities between nodes.
        m : int, number of nodes in network. source = 0 and sink = m-1.
        
    returns:
        totalFlow : int, maximum flow thought network.
        steps : int, iterations used.
        cut : array, minimum cut where the capacity over the cut is the same as totalFlow.
        optimalFlow : array, final flow thought network.
    """
    source = 0
    sink = m - 1
    totalFlow = 0
    residual_capacities = [[0 for _ in range(m)] for _ in range(m)] # Residual capacities
    adjacency = [[i for i,e in enumerate(a) if e != 0] for a in capacities] # Adjacency
    steps = 0
    while True:
        steps += 1
        visited = [-1 for _ in range(m)] # visited array
        visited[source] = -2 # to compensate if circular network
        flow = [0 for _ in range(m)]
        flow[source] = float('inf')
        pathFlow, visited = BFS(adjacency, capacities, source, sink, residual_capacities, visited, flow)
        if pathFlow == 0:
            break
        totalFlow += pathFlow
        v = sink
        while v != source:
            u = visited[v]
            residual_capacities[u][v] += pathFlow
            residual_capacities[v][u] -= pathFlow
            v = u
            
    cut = [i for i,e in enumerate(visited) if e >= 0]
    cut.append(source)
    optimalFlow = [[max(a,0) for a in f] for f in residual_capacities]
    return totalFlow, steps, sorted(cut), optimalFlow

class Found(Exception): pass

def BFS(A, C, source, sink, F, V, M):
    """
    Breadth first search for shortest path that has available capacity.
    args:
        A : array, adjacency
        C : array, capacities
        source : int
        sink: int
        F : array, residual capacities
        V : array, visited array
        M : array, cumulative flow
    returns:
        f : int, flow in augmented path. 0 or flow at sink.
        V : array, visited. Can be extrapolated as cut where V >= 0 nodes on source side. V < 0 on sink side.
    """
    queue = [source]
    f = 0
    try:
        while queue:
            u = queue.pop(0) # first in first out
            for v in A[u]:
                available = C[u][v] - F[u][v]
                if available > 0 and V[v] == -1: # If available capacity and v not visited.
                    V[v] = u 
                    M[v] = min(M[u], available) # min(flow from parent, available capacity)
                    if v != sink:
                        queue.append(v)
                    else:
                        f = M[sink]
                        raise Found
    except Found:
        pass
    return f, V

def import_data(filename):
    with open(filename, 'r') as f:
        input_data = []
        for l in f:
            input_data.append([int(a) for a in l.strip().split()])
    m = input_data[0][0]
    capacities = input_data[1:]
    return m, capacities

def export_data(filename, maxFlow, steps, cut, flow):
    with open(filename, 'w') as f:
        f.write('Max Flow: ' + str(maxFlow) + '\n')
        f.write('Cut: ' + ' '.join(str(c) for c in cut) + '\n')
        f.write('Steps: ' + str(steps) + '\n')
        for c in flow:
            f.write(' '.join(str(a) for a in c) + '\n')

def main(input_filename, output_filename):
    m, capacities = import_data(input_filename)
    
    maxFlow, steps, cut, flow = EdmondsKarp(capacities, m)
    
    export_data(output_filename, maxFlow, steps, cut, flow)
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Edmonds-Karp algorithm')
    parser.add_argument('input_filename', metavar='input', type=str, nargs='?',
                    help='input filename')
    parser.add_argument('output_filename', metavar='output', type=str, nargs='?',
                    help='output filename')
    
    args = parser.parse_args()
    main(args.input_filename, args.output_filename)
    

