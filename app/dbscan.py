import plotly
import plotly.graph_objs as go
import matplotlib.pyplot as plt

import numpy as np
import json
import sys

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler

def runDbscan():

  lines = sys.stdin.readlines()
  everything = json.loads(lines[0])
  datastore = everything['data']
  axis = everything['plotLayout']

  if (everything['epsilon'] < 1):
    epsilon = 10.0 # default value
  else:
    epsilon = everything['epsilon']

  if (everything['minPts'] < 1):
    min_samples = 5 # default value
  else:
    min_samples = everything['minPts']

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

  # #############################################################################
  # Compute DBSCAN
  db = DBSCAN(eps=epsilon, min_samples=min_samples).fit(X)
  core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
  core_samples_mask[db.core_sample_indices_] = True
  labels = db.labels_

  # Number of clusters in labels, ignoring noise if present.
  n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

  # #############################################################################
  # Plot result
  unique_labels = set(labels)

  colors = matplotlib_to_plotly(plt.cm.Spectral, len(unique_labels))
  data = []

  for k, col in zip(unique_labels, colors):
    if k == -1:
      # Black used for noise.
      col = 'black'
    else:
      col = col[1]
    
    class_member_mask = (labels == k)
   
    xy = X[class_member_mask & core_samples_mask]
    z = Z[class_member_mask & core_samples_mask]

    trace1 = go.Scatter3d(x=xy[:, 0], y=xy[:, 1], z=xy[:, 2], mode='markers', 
                          marker=dict(color=col, size=3,
                                      line=dict(color='black', width=1)),
                          text=z)

    xy = X[class_member_mask & ~core_samples_mask]
    z = Z[class_member_mask & ~core_samples_mask]
    trace2 = go.Scatter3d(x=xy[:, 0], y=xy[:, 1], z=xy[:, 2], mode='markers', 
                          marker=dict(color=col, size=3,
                                      line=dict(color='black', width=1)),
                          text=z)
    # one of these is noise?
    data.append(trace1)
    data.append(trace2)

  camera = dict(
    up=dict(x=0, y=0, z=1),
    center=dict(x=0, y=0, z=0),
    eye=dict(x=0.1, y=2.1, z=0.1)
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

  # fix me: hard code zero margin
  divOutput = myChart.replace("\"showlegend\": true", 
    "\"showlegend\": true, \"margin\": {\"l\":0, \"r\":0, \"t\":0, \"b\":0,}")
  
  return divOutput


def matplotlib_to_plotly(cmap, pl_entries):
  h = 1.0/(pl_entries-1)
  pl_colorscale = []
  
  for k in range(pl_entries):
      C = map(np.uint8, np.array(cmap(k*h)[:3])*255)
      pl_colorscale.append([k*h, 'rgb'+str((C[0], C[1], C[2]))])
      
  return pl_colorscale


def main():
  div = runDbscan()
  print(div)


if __name__ == '__main__':
  main()
