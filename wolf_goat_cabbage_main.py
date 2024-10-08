from wolf_goat_cabbage.environment import State, Entity, Coast

from solvers import bfs, dfs, dfs_with_cmp, ucs, bnb

state = State(
    left=Entity.WOLF | Entity.GOAT | Entity.CABBAGE,
    right=Entity(0),
    boat=Entity(0),
    coast=Coast.LEFT,
)

solvers = {"bfs": bfs, "dfs": dfs, "dfs_with_cmp": dfs_with_cmp, "ucs": ucs, "bnb": bnb}

solver = input("Enter solver (bfs, dfs, dfs_with_cmp, ucs, bnb): ")

if solver not in solvers:
    print("Invalid solver. Exiting...")
    exit()

actions = solvers[solver](state)

if actions is None:
    print("No solution found. Exiting...")
    exit()

for action in actions:
    state = state.make_move(action)
    state.draw()

input()
