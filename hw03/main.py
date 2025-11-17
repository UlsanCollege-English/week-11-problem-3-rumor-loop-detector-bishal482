"""
HW03 — Rumor Loop Detector (Cycle in Undirected Graph)

Implement:
- has_cycle(graph)
- find_cycle(graph)
"""

def _get_all_nodes(graph):
    """Generates a set of all unique nodes present in the graph (keys and values)."""
    nodes = set(graph.keys())
    for neighbors in graph.values():
        nodes.update(neighbors)
    return nodes

def _dfs_cycle_finder(graph, node, visited, parent_map, cycle_found):
    """Helper function for DFS to detect and find a cycle."""
    
    # Stop search if a cycle was already found and stored
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
            # Cycle detected! Found a back edge to a visited node that is not the parent.
            
            # 1. Handle self-loop case explicitly for clean path reconstruction
            if node == neighbor:
                cycle_path = [node, neighbor]
            else:
                # 2. Reconstruct the cycle by tracing back from the current node
                cycle_end = neighbor
                cycle_path = [cycle_end]
                current = node
                while current != cycle_end:
                    cycle_path.append(current)
                    current = parent_map.get(current)
                
                # 3. Close the cycle and reverse for correct order
                cycle_path.append(cycle_end)
                cycle_path.reverse()
            
            # Store the found cycle (passed by reference)
            cycle_found.extend(cycle_path)
            return True
            
    return False

def has_cycle(graph: dict) -> bool:
    """Return True if the undirected graph has any cycle; else False."""
    visited = set()
    all_nodes = _get_all_nodes(graph) 
    
    for node in all_nodes:
        if node not in visited:
            # Iterative DFS: (current_node, parent_node)
            stack = [(node, None)]
            local_visited = {node}
            
            while stack:
                curr, parent = stack.pop()
                
                for neighbor in graph.get(curr, []):
                    if neighbor not in local_visited:
                        local_visited.add(neighbor)
                        stack.append((neighbor, curr))
                    # Cycle condition: back edge to a visited, non-parent node
                    elif neighbor != parent:
                        return True

            visited.update(local_visited) # Update global visited set

    return False

def find_cycle(graph: dict) -> list or None:
    """Return a list of nodes forming a simple cycle where first == last.
    If no cycle, return None.
    """
    visited = set()
    parent_map = {}
    cycle_found = []
    all_nodes = _get_all_nodes(graph)
    
    for node in all_nodes:
        if node not in visited:
            # Start node of a component has no parent
            parent_map[node] = None 
            
            # Use recursive DFS to find and reconstruct the cycle
            if _dfs_cycle_finder(graph, node, visited, parent_map, cycle_found):
                return cycle_found

    return None