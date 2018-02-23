from sklearn import cluster
from sklearn.cluster import AffinityPropagation

import numpy as np
import json
import sys

def affPropClusters():

  lines = sys.stdin.readlines()
  everything = json.loads(lines[0])
  datastore = everything['data']
  axis = everything['plotLayout']

  X = []
  Z = []
  xVal = datastore['x']
  yVal = datastore['y']
  zVal = datastore['z']

  for index, item in enumerate(xVal):
    X.append([xVal[index], yVal[index], zVal[index]])

  X = np.asarray(X)

  # use affine propagation to determine number of clusters to use
  af = AffinityPropagation().fit(X)
  cluster_centers_indices = af.cluster_centers_indices_

  return len(cluster_centers_indices)


def main():
  cluster_num = affPropClusters()
  print(cluster_num)


if __name__ == '__main__':
  main()
