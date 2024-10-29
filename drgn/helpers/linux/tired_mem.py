from drgn import Object, Program
from drgn.helpers.common.prog import takes_program_or_default

__all__ = (
    "is_top_tier",
    "get_node",
    "print_numa_balancing_info",
    "print_thrashing_table",
    "test_page_in_thrashing_table",
)


@takes_program_or_default
def is_top_tier(prog: Program, node_id: int) -> bool:
    """
    Return whether a NUMA node id is a top-tier node in tiering
    memory-tiers.c `node_is_toptier`
    """
    # toptier = False
    node = get_node(node_id)
    if not node:
        return False
    memtier = node.memtier
    if not memtier:
        return True
    top_tier_adistance = prog["top_tier_adistance"]
    if memtier.adistance_start <= top_tier_adistance:
        return True
    else:
        return False


@takes_program_or_default
def get_node(prog: Program, node_id: int) -> Object:
    """
    Return a NUMA node struct by its id
    """
    try:
        return prog["node_data"][node_id]
    except KeyError:
        return None


@takes_program_or_default
def print_numa_balancing_info(prog: Program, node_id: int) -> None:
    """
    Print all promotion related variables in pg_data_t of the node.
    """
    node = get_node(node_id)
    if not node:
        print(f"Node {node_id} doesn't exist!")
        return
    print(f"===numa balancing info for node {node_id}===")
    print(f"nbp_rl_start: {node.nbp_rl_start}")
    print(f"nbp_rl_nr_cand: {node.nbp_rl_nr_cand}")
    print(f"nbp_threshold: {node.nbp_threshold}")
    print(f"nbp_th_start: {node.nbp_th_start}")
    print(f"nbp_th_nr_cand: {node.nbp_th_nr_cand}")


@takes_program_or_default
def print_thrashing_table(prog: Program) -> None:
    try:
        thrashing_table = prog["promote_demote_table"]
        print(f"capacity is {thrashing_table.capacity}")
        arr = thrashing_table.arr
        for it in arr:
            print(f"key: {it.key}, val: {it.val}")
    except KeyError:
        return


@takes_program_or_default
def test_page_in_thrashing_table(prog: Program, page: int) -> bool:
    try:
        thrashing_table = prog["promote_demote_table"]
        arr = thrashing_table.arr
        for it in arr:
            if page == it.key:
                return True
        return False
    except KeyError:
        return False
