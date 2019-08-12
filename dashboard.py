import json

import pgraph

results = pgraph.query(nth=100)

vulnerable_nodes = [
    node
    for node in results.organization.repositories.nodes
    if node.vulnerabilityAlerts.edges
]

print(json.dumps(vulnerable_nodes, indent=2))
