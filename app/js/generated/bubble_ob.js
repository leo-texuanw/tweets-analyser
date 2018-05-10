var data = [{name: "Residential Apartments",
  text: ["East Melbourne","South Yarra/Melbourne Remainder","Parkville","Port Melbourne","West Melbourne (Residential)","Melbourne (CBD)","Kensington","Southbank","Carlton","Docklands","North Melbourne","West Melbourne (Industrial)"],
  marker: {
    sizemode: "area",
    sizeref: 10,
    size : [9024,11982,10304,14421,3825,50259,14194,29701,13855,21932,8609,0]
  },
  mode: "markers",
  y: [16.2666666667,11.5740740741,18.7037037037,0.666666666667,17.3465346535,63.9181494662,16.8214285714,173.65,19.3526785714,143.055555556,14.5474452555,0.0],
  x: [149,269,80,2,100,280,111,59,223,35,273,0],
}, {name: "House/Townhouse",
  text: ["East Melbourne","South Yarra/Melbourne Remainder","Parkville","Port Melbourne","West Melbourne (Residential)","Melbourne (CBD)","Kensington","Southbank","Carlton","Docklands","North Melbourne","West Melbourne (Industrial)"],
  marker: {
    sizemode: "area",
    sizeref: 10,
    size : [9024,11982,10304,0,3825,50259,14194,29701,13855,21932,8609,0]
  },
  mode: "markers",
  y: [1.10178571429,1.12795275591,1.12443778111,0.0,1.1713747646,1.09756097561,1.13129251701,14.0,1.10960960961,1.19607843137,1.18146067416,0.0],
  x: [559,507,666,0,530,40,2939,1,1331,101,1779,0],
}, {name: "Student Apartments",
  text: ["East Melbourne","South Yarra/Melbourne Remainder","Parkville","Port Melbourne","West Melbourne (Residential)","Melbourne (CBD)","Kensington","Southbank","Carlton","Docklands","North Melbourne","West Melbourne (Industrial)"],
  marker: {
    sizemode: "area",
    sizeref: 10,
    size : [9024,0,10304,0,0,50259,0,0,13855,0,8609,0]
  },
  mode: "markers",
  y: [2.0,0.0,23.25,0.0,0.0,135.0,0.0,0.0,100.885714286,0.0,90.0909090909,0.0],
  x: [1,0,3,0,0,8,0,0,34,0,10,0],
}]

var layout = {
  xaxis: {
    title: 'Number of New Buildings'
  },
  yaxis: {
    title: 'New Dewellings Per Building',
    type: 'log'
  },
  margin: {
    t: 0
  },
  hovermode: 'closest'
};

BUBBLE = document.getElementById('bubble_ob');

Plotly.plot(BUBBLE, data, layout);