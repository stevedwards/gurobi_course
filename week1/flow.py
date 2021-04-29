#!/usr/bin/env python3.7

# Copyright 2021, Gurobi Optimization, LLC
# Solve a maximum flow problem. 


import gurobipy as gp
from gurobipy import GRB


def max_flow(nodes, arcs, capacity):

    # Create optimization model
    m = gp.Model('flow')

    # Create variables
    flow = m.addVars(arcs, obj=1, name="flow")

    # Objective
    m.setObjective(gp.quicksum(var for (i, j), var in flow.items() if i == "s"), sense=-1)

    # Arc-capacity constraints
    m.addConstrs(
        (flow.sum(i, j) <= capacity[i, j] for i, j in arcs), "cap")

    # Flow-conservation constraints
    m.addConstrs(
        (flow.sum(j, '*') == flow.sum('*', j)
            for j in nodes if j not in ('s', 't')), "node")

    # Compute optimal solution
    m.optimize()

    # Print solution
    if m.status == GRB.OPTIMAL:
        solution = m.getAttr('x', flow)
        print('\nOptimal flows')
        for i, j in arcs:
            if solution[i, j] > 0:
                print('%s -> %s: %g' % (i, j, solution[i, j]))


def min_cut(nodes, arcs, capacity):

    # TODO

    return None


if __name__ == "__main__":

    # Base data
    nodes = ['s', 'A', 'B', 'C', 'D', 't']

    arcs, capacity = gp.multidict({
        ('s', 'A'):   100,
        ('s', 'B'):  150,
        ('A', 'B'):  120,
        ('A',  'C'):   90,
        ('B',  'D'): 110,
        ('C',  'D'):  120,
        ('C', 't'): 140,
        ('D', 't'): 90,
        }
    )

    max_flow(nodes, arcs, capacity)
    min_cut(nodes, arcs, capacity)