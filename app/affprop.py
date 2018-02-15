from sklearn.cluster import AffinityPropagation
from sklearn import metrics

import plotly
import plotly.graph_objs as go
import matplotlib.pyplot as plt

import numpy as np
import json
import sys

def runAffProp():

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
    X.append([xVal[index],yVal[index],zVal[index]])
    Z.append(track[index])

  X = np.asarray(X)
  Z = np.asarray(Z)

  af = AffinityPropagation().fit(X)
  cluster_centers_indices = af.cluster_centers_indices_
  labels = af.labels_

  n_clusters_ = len(cluster_centers_indices)

  colors = ['blue','green','red','cyan','magenta']
  data = []
  count = 0;
  for k, col, in zip(range(n_clusters_), colors):
    name = 'trace ' + str(count);
    count = count + 1;
    class_members = labels == k
    cluster_center = X[cluster_centers_indices[k]]
    trace1 = go.Scatter3d(x=X[class_members, 0], 
                        y=X[class_members, 1],
                        z=X[class_members, 2],
                        text=Z[class_members],
                        legendgroup = name,
                        name = name,
                        showlegend = True,
                        mode='markers', marker=dict(color=col, size=3))
    
    trace2 = go.Scatter3d(x=[cluster_center[0]], 
                        y=[cluster_center[1]],
                        z=[cluster_center[2]], 
                        text=Z[class_members],
                        legendgroup = name,
                        name = name,
                        showlegend=False,
                        mode='markers', marker=dict(color=col, size=3))
    data.append(trace1)
    data.append(trace2)
    for x in X[class_members]:
      trace3 = go.Scatter3d(x = [cluster_center[0], x[0]], 
                          y=[cluster_center[1], x[1]],
                          z=[cluster_center[2], x[2]],
                          legendgroup = name,
                          name = name,
                          showlegend=False,
                          mode='lines', line=dict(color=col, width=2))
      data.append(trace3)

  camera = dict(
    up=dict(x=0, y=0, z=1),
    center=dict(x=0, y=0, z=0),
    eye=dict(x=0.1, y=1.8, z=0.1)
  )

  layout = go.Layout( scene = dict(xaxis = dict(title = axis['xaxis']['title']),
                                  yaxis = dict(title = axis['yaxis']['title']),
                                  zaxis = dict(title = axis['zaxis']['title']),
                                  camera = camera,
                              ),
                      showlegend = True,
                      autosize = True,
                      width = 1000, # fix me: fixed window size
                      height = 400, # fix me: fixed window size
                      hovermode = 'closest',
                    )

  myChart = plotly.offline.plot({
      'data': data,
      'layout': layout,
    },
    include_plotlyjs = False,
    output_type = 'div',
  )

  divOutput = myChart.replace("\"showlegend\": true", 
    "\"showlegend\": true, \"margin\": {\"l\":0, \"r\":0, \"t\":0, \"b\":0,}")

  return divOutput


def main():
  div = runAffProp()
  print(div)


if __name__ == '__main__':
  main()
