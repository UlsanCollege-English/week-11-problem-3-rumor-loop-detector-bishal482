from collections import deque

def _dfs_cycle_finder(graph, node, visited, parent_map, cycle_found):
    """
    Helper function for Depth-First Search to detect and find a cycle.
    
    :param graph: The adjacency list dictionary.
    :param node: The current node being visited.
    :param visited: Set of nodes already visited.
    :param parent_map: Dictionary to store the parent of each node: {child: parent}.
    :param cycle_found: List to store the cycle when found (passed by reference).
    :return: True if a cycle is detected and stored, False otherwise.
    """
    
    # Check if a cycle was already found by a previous recursive call
    if cycle_found:
        return True

    visited.add(node)
    
    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            # Explore unvisited neighbor
            parent_map[neighbor] = node
            if _dfs_cycle_finder(graph, neighbor, visited, parent_map, cycle_found):
                return True
        elif neighbor != parent_map.get(node):
            # Cycle detected! Found a back edge to an already visited node 
            # that is not the direct parent.
            
            # 1. Identify the cycle start/end point (the neighbor)
            cycle_end = neighbor
            cycle_path = [cycle_end]
            
            # 2. Trace back from the current node (the one that found the back edge)
            current = node
            while current != cycle_end:
                cycle_path.append(current)
                current = parent_map.get(current)
            
            # 3. Add the starting node again to close the cycle
            cycle_path.append(cycle_end)
            
            # 4. Reverse the path to get the cycle in the correct traversal order
            cycle_path.reverse()
            
            # Store the found cycle
            cycle_found.extend(cycle_path)
            return True
            
    return False

def has_cycle(graph: dict) -> bool:
    """
    Checks if an undirected graph contains any cycles.
    """
    visited = set()
    
    # Iterate over all nodes to handle disconnected components
    for node in graph:
        if node not in visited:
            # We use a simplified DFS check here, as we only need True/False
            stack = [(node, None)]  # (current_node, parent_node)
            local_visited = {node}
            
            while stack:
                curr, parent = stack.pop()
                
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
    
    # Iterate over all nodes to ensure we check disconnected components
    for node in graph:
        if node not in visited:
            # For the first node of a component, it has no parent
            parent_map[node] = None 
            
            # If the cycle finder finds a cycle in this component, return it
            if _dfs_cycle_finder(graph, node, visited, parent_map, cycle_found):
                return cycle_found

    return None