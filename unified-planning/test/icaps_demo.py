# -*- coding: utf-8 -*-
"""ICAPS Demo

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Pf72cAXFgCFAfF6wRfIkFuPQp9HZFueQ

# Welcome!

Welcome to this short demo of the Unified Planning (UP) library. In this interactive demo we will install the library itself, with four planning engines and we will showcase some of the functionalities available in the library. This demo focuses on classical and numeric planning, but the UP library is capable of temporal planning as well and more formalisms will be added soon!

# Let's install the Unified Planning Library and three planners

Let's start by installing the library! The UP library can be installed directly from PIP with a single command.

We install also Pyperplan, Tamer, ENHSP (requires Java 17) and Fast Downward
"""

#!apt-get install openjdk-17-jdk

#!pip install unified-planning[pyperplan,tamer,enhsp,fast-downward]

"""# Creating a simple robot moving problem
Suppose we are given a graph (here generated randomly) of locations each with an associated geometric position...
"""

import matplotlib.pyplot as plt
import networkx as nx

# Use seed when creating the graph for reproducibility
location_map = nx.soft_random_geometric_graph([f'loc_{i}' for i in range(15)], 0.5, seed=2)
# Position is stored as node attribute data for soft_random_geometric_graph
pos = nx.get_node_attributes(location_map, "pos")

# Show the graph
plt.figure(figsize=(8, 8))
nx.draw_networkx_edges(location_map, pos, alpha=0.4)
nx.draw_networkx_nodes(
    location_map,
    pos,
    node_size=1800
)
nx.draw_networkx_labels(location_map, pos)
plt.show()

"""Suppose our robot is initially in location `loc_0` and wants go go in location `loc_10`"""

# Saving initial and goal location names in python variables
INIT = 'loc_0'
DEST = 'loc_10'

"""## Classical planning formulation

We can easily and **programmatically** create a classical planning problem directly from the graph data structure using the UP primitives
"""

from unified_planning.shortcuts import *

# First, we declare a "Location" type 
Location = UserType('Location')

# We create a new problem
problem = Problem('robot')

# Declare the fluents:
# - `robot_at` is a predicate modeling the robot position,
# - `connected` is a static fluent for modeling the graph connectivity relation
robot_at = Fluent('robot_at', BoolType(), position=Location)
connected = Fluent('connected', BoolType(), l_from=Location, l_to=Location)

# Add the fluents to the problem, a Fluent can be resused in many problems
# The default values are optional and can be any value (not forcing closed-world assumption) 
problem.add_fluent(robot_at, default_initial_value=False)
problem.add_fluent(connected, default_initial_value=False)

# Create a simple `move` action  
move = InstantaneousAction('move', l_from=Location, l_to=Location)
l_from = move.parameter('l_from')
l_to = move.parameter('l_to')
move.add_precondition(robot_at(l_from))
move.add_precondition(connected(l_from, l_to))
move.add_effect(robot_at(l_from), False)
move.add_effect(robot_at(l_to), True)
problem.add_action(move)

# Programmatically create a map from location name to a new `Object` of type `Location`
locations = {str(l) : Object(str(l), Location) for l in location_map.nodes}

# Add all the objects to the problem
problem.add_objects(locations.values())

# Setting the initial location
problem.set_initial_value(robot_at(locations[INIT]), True)

# Initializing the connectivity relations by iterating over the graph edges
for (f, t) in location_map.edges:
  problem.set_initial_value(connected(locations[str(f)], locations[str(t)]), True)
  problem.set_initial_value(connected(locations[str(t)], locations[str(f)]), True)

# Setting the goal
problem.add_goal(robot_at(locations[DEST]))

# Printing the problem data structure in human-readable form
# (We can also print in PDDL and ANML)
print(problem)

"""### Solving with classical planners

We can now invoke the classical planners we have installed on our machine in a uniform and convenient way
"""

from unified_planning.engines import PlanGenerationResultStatus

for planner_name in ['pyperplan', 'fast-downward']:
  with OneshotPlanner(name=planner_name) as planner:
    result = planner.solve(problem)
    if result.status == PlanGenerationResultStatus.SOLVED_SATISFICING:
      print(f'{planner_name} found a plan.\nThe plan is: {result.plan}')
    else:
      print("No plan found.")

"""## Extend with numerical fluents

We can easily extend our problem adding numeric fluents
"""

import math
from fractions import Fraction

# A simple function that associates a battery cost to each edge
def battery_consumption(loc_from, loc_to):
  pos = nx.get_node_attributes(location_map, "pos")
  fx, fy = pos[loc_from]
  tx, ty = pos[loc_to]
  distance = math.sqrt((fx - tx)**2 + (fy - ty)**2)
  return int(5 + distance * 30 + 2)

# Adding more fluents:
# - `battery` to model the residual amount of battery
# - `consumption` to model the battery consumption on each edge 
battery = Fluent('battery', RealType(0, 100))
consumption = Fluent('consumption', RealType(), l_from=Location, l_to=Location)

# Adding the fluents to the problem
problem.add_fluent(battery)
problem.add_fluent(consumption, default_initial_value=-1)

# Extend the `move` action
move.add_precondition(GE(consumption(l_from, l_to), 0))
move.add_precondition(GE(battery, consumption(l_from, l_to)))
move.add_effect(battery, Minus(battery, consumption(l_from, l_to)))

# Setting the initial state of the new fluents
problem.set_initial_value(battery, 100)

for (f, t) in location_map.edges:
  problem.set_initial_value(consumption(locations[str(f)], locations[str(t)]), battery_consumption(f, t))
  problem.set_initial_value(consumption(locations[str(t)], locations[str(f)]), battery_consumption(t, f))

print(problem)

"""### Solving the numeric problem

We can use the `problem.kind()` query to obtain a description of the features used in the problem. Using such features the UP library can automatically select a planner capable of solving the problem 
"""

with OneshotPlanner(problem_kind=problem.kind) as planner:
  result = planner.solve(problem)
  if result.status == PlanGenerationResultStatus.SOLVED_SATISFICING:
    print(f'{planner.name} found a plan.\n The plan is: {result.plan}')
  else:
    print("No plan found.")

"""Alternatively, we can specify the planner to run manually"""

with OneshotPlanner(name='tamer') as planner:
  result = planner.solve(problem)
  if result.status == PlanGenerationResultStatus.SOLVED_SATISFICING:
    print(f'{planner.name} found a plan.\n The plan is: {result.plan}')
  else:
    print("No plan found.")

"""It is also possible to execute multiple planners in parallel, also with different parameters"""

with OneshotPlanner(names=['tamer', 'tamer', 'enhsp'],
                    params=[{'heuristic': 'hadd'}, {'heuristic': 'hmax'}, {}]) as planner:
    plan = planner.solve(problem).plan
    print(f'{planner.name} returned: {plan}')

"""## Analyzing the results

The plan objects are fully inspectable programmaticaly, so one can use the results of planning engines in any application setting
"""

import numpy as np
import matplotlib.pyplot as plt

b = [100]
labels = ['<initial value>']
for ai in plan.actions:
  c = problem.initial_value(consumption(*ai.actual_parameters))
  b.append(b[-1] - c.constant_value())
  labels.append(str(ai))

x = list(range(len(plan.actions)+1))
plt.bar(x, b, width=1)

plt.xlabel('Plan')
plt.ylabel('Battery')
plt.xticks(x, labels, rotation='vertical')
plt.title('Battery Consumption')
plt.show()

"""# Beyond plan generation

`OneshotPlanner` is not the only **operation mode** we can invoke from the unified_planning, it is just one way to interact with a planning engine. Another useful functionality is `PlanValidation` that checks if a plan is valid for a problem.
"""

plan = result.plan
with PlanValidator(problem_kind=problem.kind, plan_kind=plan.kind) as validator:
    if validator.validate(problem, plan):
        print('The plan is valid')
    else:
        print('The plan is invalid')

"""It is also possible to use the `Compiler` operation mode to create an equivalent formulation of a problem that does not use parameters for the actions. This operation mode is implemented by an internal python code, but also some engines offer advanced grounding techniques. """

with Compiler(problem_kind=problem.kind, compilation_kind=CompilationKind.GROUNDING) as grounder:
    grounding_result = grounder.compile(problem, CompilationKind.GROUNDING)
    ground_problem, map_back_function = grounding_result.problem, grounding_result.map_back_action_instance

    # The map_back_function can be used to "lift" a ground plan back to the level of the original problem
    with OneshotPlanner(problem_kind=ground_problem.kind) as planner:
        ground_plan = planner.solve(ground_problem).plan
        print('Ground plan: %s' % ground_plan)
        lifted_plan = ground_plan.replace_action_instances(map_back_function)
        print('Lifted plan: %s' % lifted_plan)
        with PlanValidator(problem_kind=problem.kind, plan_kind=ground_plan.kind) as validator:
            assert validator.validate(ground_problem, ground_plan)
            assert validator.validate(problem, lifted_plan)