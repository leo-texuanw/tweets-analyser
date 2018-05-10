var data = [{name: "C#",
  text: ["Adelaide","Brisbane","Canberra","Gold Coast","Logan City","Melbourne","Newcastle","Perth","Sydney","Wollongong"],
  marker: {
    sizemode: "area",
    sizeref: 10,
    size : [518]
  },
  mode: "markers",
  y: [637],
  x: [0.9858712715855573],
}, {name: "C++",
  text: ["Adelaide","Brisbane","Canberra","Gold Coast","Logan City","Melbourne","Newcastle","Perth","Sydney","Wollongong"],
  marker: {
    sizemode: "area",
    sizeref: 10,
    size : [518]
  },
  mode: "markers",
  y: [637],
  x: [0.9858712715855573],
}, {name: "Haskell",
  text: ["Adelaide","Brisbane","Canberra","Gold Coast","Logan City","Melbourne","Newcastle","Perth","Sydney","Wollongong"],
  marker: {
    sizemode: "area",
    sizeref: 10,
    size : [518]
  },
  mode: "markers",
  y: [637],
  x: [0.9858712715855573],
}, {name: "Java",
  text: ["Adelaide","Brisbane","Canberra","Gold Coast","Logan City","Melbourne","Newcastle","Perth","Sydney","Wollongong"],
  marker: {
    sizemode: "area",
    sizeref: 10,
    size : [518]
  },
  mode: "markers",
  y: [637],
  x: [0.9858712715855573],
}, {name: "JavaScript",
  text: ["Adelaide","Brisbane","Canberra","Gold Coast","Logan City","Melbourne","Newcastle","Perth","Sydney","Wollongong"],
  marker: {
    sizemode: "area",
    sizeref: 10,
    size : [518]
  },
  mode: "markers",
  y: [637],
  x: [0.9858712715855573],
}, {name: "MATLAB",
  text: ["Adelaide","Brisbane","Canberra","Gold Coast","Logan City","Melbourne","Newcastle","Perth","Sydney","Wollongong"],
  marker: {
    sizemode: "area",
    sizeref: 10,
    size : [518]
  },
  mode: "markers",
  y: [637],
  x: [0.9858712715855573],
}, {name: "PHP",
  text: ["Adelaide","Brisbane","Canberra","Gold Coast","Logan City","Melbourne","Newcastle","Perth","Sydney","Wollongong"],
  marker: {
    sizemode: "area",
    sizeref: 10,
    size : [518]
  },
  mode: "markers",
  y: [637],
  x: [0.9858712715855573],
}, {name: "Prolog",
  text: ["Adelaide","Brisbane","Canberra","Gold Coast","Logan City","Melbourne","Newcastle","Perth","Sydney","Wollongong"],
  marker: {
    sizemode: "area",
    sizeref: 10,
    size : [518]
  },
  mode: "markers",
  y: [637],
  x: [0.9858712715855573],
}, {name: "Python",
  text: ["Adelaide","Brisbane","Canberra","Gold Coast","Logan City","Melbourne","Newcastle","Perth","Sydney","Wollongong"],
  marker: {
    sizemode: "area",
    sizeref: 10,
    size : [518]
  },
  mode: "markers",
  y: [637],
  x: [0.9858712715855573],
}, {name: "SQL",
  text: ["Adelaide","Brisbane","Canberra","Gold Coast","Logan City","Melbourne","Newcastle","Perth","Sydney","Wollongong"],
  marker: {
    sizemode: "area",
    sizeref: 10,
    size : [518]
  },
  mode: "markers",
  y: [637],
  x: [0.9858712715855573],
}]

var layout = {
  xaxis: {
    title: 'Non-negative Rate'
  },
  yaxis: {
    title: 'Number of Tweets',
    type: 'log'
  },
  margin: {
    t: 20
  },
  hovermode: 'closest'
};

BUBBLE = document.getElementById('bubble');

Plotly.plot(BUBBLE, data, layout);