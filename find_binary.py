import node

def find_binary(id, node_lst):
    '''
    Uses binary search to look for a Node object with given integer id 
    in the given list of Node objects.
    Returns a Node object, or None if not found.
    Preconditions: id is an integer; node_lst is a list of Node objects that are 
    sorted by id in an increasing order. node_lst can be empty.
    '''
    if len(node_lst) == 0:
        return None

    i = len(node_lst) // 2
    curr_node = node_lst[i]

    if curr_node.id < id:
        return find_binary(id, node_lst[i+1:])
    elif curr_node.id > id:
        return find_binary(id, node_lst[:i])
    return curr_node