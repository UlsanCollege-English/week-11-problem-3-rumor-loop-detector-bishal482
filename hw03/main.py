def _get_all_nodes(graph):
    """Generates a set of all unique nodes present in the graph (keys and values)."""
    nodes = set(graph.keys())
    for neighbors in graph.values():
        nodes.update(neighbors)
    return nodes

def _dfs_cycle_finder(graph, node, visited, parent_map, cycle_found):
    # (The body of this function remains the same)
    if cycle_found:
        return True

    visited.add(node)
    
    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            parent_map[neighbor] = node
            if _dfs_cycle_finder(graph, neighbor, visited, parent_map, cycle_found):
                return True
        elif neighbor != parent_map.get(node):
            # Cycle detected and path reconstruction logic (unchanged)
            cycle_end = neighbor
            cycle_path = [cycle_end]
            current = node
            while current != cycle_end:
                cycle_path.append(current)
                current = parent_map.get(current)
            
            cycle_path.append(cycle_end)
            cycle_path.reverse()
            
            cycle_found.extend(cycle_path)
            return True
            
    return False

def has_cycle(graph: dict) -> bool:
    """
    Checks if an undirected graph contains any cycles.
    """
    visited = set()
    all_nodes = _get_all_nodes(graph) # Use all unique nodes
    
    # Iterate over all nodes to handle disconnected components
    for node in all_nodes:
        if node not in visited:
            # Iterative DFS for cycle detection
            stack = [(node, None)]  # (current_node, parent_node)
            local_visited = {node}
            
            while stack:
                curr, parent = stack.pop()
                
                # Use .get() defensively against missing keys
                for neighbor in graph.get(curr, []): 
                    if neighbor not in local_visited:
                        local_visited.add(neighbor)
                        stack.append((neighbor, curr))
                    elif neighbor != parent:
                        # Back edge to a visited but non-parent node found
                        return True

            # Merge results for all components
            visited.update(local_visited)

    return False

def find_cycle(graph: dict) -> list or None:
    """
    Finds one cycle in an undirected graph and returns it as a list, 
    where the first and last elements are the same node.
    """
    visited = set()
    parent_map = {}
    cycle_found = []
    all_nodes = _get_all_nodes(graph) # Use all unique nodes
    
    # Iterate over all nodes to ensure we check disconnected components
    for node in all_nodes:
        if node not in visited:
            # Set the parent for the start node of the component
            parent_map[node] = None 
            
            # Recursive DFS for cycle finding
            if _dfs_cycle_finder(graph, node, visited, parent_map, cycle_found):
                return cycle_found

    return None