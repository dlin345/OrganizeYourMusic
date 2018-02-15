from sklearn import datasets
from sklearn import cluster
from sklearn.cluster import AffinityPropagation

import plotly
import plotly.graph_objs as go

import numpy as np
import pandas as pd
import json
import sys

def runKMeans():

  lines = sys.stdin.readlines()
  everything = json.loads(lines[0])
  datastore = everything['data']
  axis = everything['plotLayout']

  X = []
  Z = []
  xVal = datastore['x']
  yVal = datastore['y']
  zVal = datastore['z']
  track = datastore['text']

  for index, item in enumerate(xVal):
    X.append([xVal[index], yVal[index], zVal[index]])
    Z.append(track[index])

  X = np.asarray(X)
  Z = np.asarray(Z)

  # use affine propagation to determine number of clusters to use
  n_clusters = getClusterNum(datastore)

  kmeans = cluster.KMeans(n_clusters=n_clusters).fit(pd.DataFrame({
    'x': datastore['x'], 
    'y': datastore['y'], 
    'z': datastore['z']
    }))

  labels = kmeans.labels_
  colors = kmeans.labels_
  data = []
  count = 0
  for k, col, in zip(range(n_clusters), colors):
    name = 'trace ' + str(count)
    count = count + 1
    class_members = labels == k
    trace = go.Scatter3d( x=X[class_members, 0],
                          y=X[class_members, 1],
                          z=X[class_members, 2],
                          text=Z[class_members],
                          legendgroup=name,
                          name=name,
                          showlegend=True,
                          mode='markers', marker=dict(color=col,
                                                      size=3))
    data.append(trace)

  camera = dict(up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=0.1, y=1.8, z=0.1)
  )

  myChart = plotly.offline.plot({
      'data': data,
      'layout': go.Layout(scene = dict( xaxis = dict(title = axis['xaxis']['title']),
                                        yaxis = dict(title = axis['yaxis']['title']),
                                        zaxis = dict(title = axis['zaxis']['title']),
                                        camera = camera,
                                      ),
                          showlegend = True,
                          autosize = True,
                          width = 1000, # fix me: fixed window size
                          height = 400, # fix me: fixed window size
                          hovermode = 'closest',
                        )},
      include_plotlyjs = False,
      output_type = 'div',
  )

  # fix me: hard code zero margin
  divOutput = myChart.replace("\"showlegend\": true", 
    "\"showlegend\": true, \"margin\": {\"l\":0, \"r\":0, \"t\":0, \"b\":0,}")
  
  return divOutput


def getClusterNum(datastore):
  X = []
  Z = []
  xVal = datastore['x']
  yVal = datastore['y']
  zVal = datastore['z']
  track = datastore['text']

  for index, item in enumerate(xVal):
    X.append([xVal[index],yVal[index],zVal[index]])
    Z.append(track[index])

  X = np.asarray(X)
  Z = np.asarray(Z)

  af = AffinityPropagation().fit(X)
  cluster_centers_indices = af.cluster_centers_indices_
  labels = af.labels_

  n_clusters_ = len(cluster_centers_indices)

  return n_clusters_


def main():
  div = runKMeans()
  print(div)


if __name__ == '__main__':
  main()
