#!/usr/bin/env python

import itertools
import math
import re

_NAME = 'name'
_NEIGHBORS = 'neighbors'
_FOUND = 'found'
_CENTRALITY = 'centrality'
_ALPHA = 0.5

def _or_sets(sets):
  acc = set()
  for subset in sets:
    acc |= subset
  return acc

def all_pair_shortest_path(graph):
  count = len(graph)
  for key, node in graph.iteritems():
    node[_FOUND] = set([key]) | node[_NEIGHBORS][0]
  for i in itertools.count(1):
    found_new = False
    for node in graph.itervalues():
      if len(node[_NEIGHBORS]) < i:
        continue
      fringe = _or_sets([graph[x][_NEIGHBORS][0] for x in node[_NEIGHBORS][i-1]])
      fringe -= node[_FOUND]
      if len(fringe):
        found_new = True
        node[_FOUND] |= fringe
        node[_NEIGHBORS].append(fringe)
    if not found_new:
      break
  for node in graph.itervalues():
    del node[_FOUND]

def katz_centrality(node):
  centrality = 0
  for i in xrange(len(node[_NEIGHBORS])):
    centrality += math.pow(_ALPHA, i) * len(node[_NEIGHBORS][i])
  return centrality

def centrality_ordered_names(graph):
  all_pair_shortest_path(graph)
  for node in graph.itervalues():
    node[_CENTRALITY] = katz_centrality(node)
  return [x[_NAME] for x in sorted(graph.values(), key=lambda node: -node[_CENTRALITY])]

def parse_dotfile():
  fptr = open('dotfile', 'r')
  newLabel = re.compile(r'(\d+)\s\[label="([^"]+)"\]')
  newEdge = re.compile(r'(\d+)\s--\s(\d+)')

  graph = {}

  for line in fptr:
    label = newLabel.search(line)
    edge = newEdge.search(line)
    if label:
      #neighbors is 1 set for each level, neighbors[0] are direct neighbors
      #neighbors[1] are second degree
      graph[label.groups()[0]] = {_NAME: label.groups()[1], _NEIGHBORS: [set()]}
    elif edge:
      if not(edge.groups()[0] in graph or edge.groups()[1] in graph):
        raise Exception("Edge inclides non-nodes: %s or %s" % (edge.groups()[0], edge.groups()[1]))
      graph[edge.groups()[0]][_NEIGHBORS][0].add(edge.groups()[1])
      graph[edge.groups()[1]][_NEIGHBORS][0].add(edge.groups()[0])
  return graph

if __name__ == '__main__':
  print "\n".join(centrality_ordered_names(parse_dotfile()))
