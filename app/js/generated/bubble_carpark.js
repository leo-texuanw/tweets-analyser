var data = [{name: "Residential Apartments",
  text: ["East Melbourne","South Yarra/Melbourne Remainder","Parkville","Port Melbourne","West Melbourne (Residential)","Melbourne (CBD)","Kensington","Southbank","Carlton","Docklands","North Melbourne","West Melbourne (Industrial)"],
  marker: {
    sizemode: "area",
    sizeref:0.3,
    size : [60.16,44.3777777778,127.209876543,4807.0,37.8712871287,178.857651246,126.732142857,495.016666667,61.8526785714,609.222222222,31.4197080292,0.0]
  },
  mode: "markers",
  y: [16.2666666667,11.5740740741,18.7037037037,0.666666666667,17.3465346535,63.9181494662,16.8214285714,173.65,19.3526785714,143.055555556,14.5474452555,0.0],
  x: [9024,11982,10304,14421,3825,50259,14194,29701,13855,21932,8609,0],
}, {name: "House/Townhouse",
  text: ["East Melbourne","South Yarra/Melbourne Remainder","Parkville","Port Melbourne","West Melbourne (Residential)","Melbourne (CBD)","Kensington","Southbank","Carlton","Docklands","North Melbourne","West Melbourne (Industrial)"],
  marker: {
    sizemode: "area",
    sizeref:8,
    size : [16.1142857143,23.5866141732,15.4482758621,0.0,7.20338983051,1225.82926829,4.82789115646,14850.5,10.4016516517,215.019607843,4.83651685393,0.0]
  },
  mode: "markers",
  y: [1.10178571429,1.12795275591,1.12443778111,0.0,1.1713747646,1.09756097561,1.13129251701,14.0,1.10960960961,1.19607843137,1.18146067416,0.0],
  x: [9024,11982,10304,0,3825,50259,14194,29701,13855,21932,8609,0],
}, {name: "Student Apartments",
  text: ["East Melbourne","South Yarra/Melbourne Remainder","Parkville","Port Melbourne","West Melbourne (Residential)","Melbourne (CBD)","Kensington","Southbank","Carlton","Docklands","North Melbourne","West Melbourne (Industrial)"],
  marker: {
    sizemode: "area",
    sizeref:0.8,
    size : [4512.0,0.0,2576.0,0.0,0.0,5584.33333333,0.0,0.0,395.857142857,0.0,782.636363636,0.0]
  },
  mode: "markers",
  y: [2.0,0.0,23.25,0.0,0.0,135.0,0.0,0.0,100.885714286,0.0,90.0909090909,0.0],
  x: [9024,0,10304,0,0,50259,0,0,13855,0,8609,0],
}]

var layout = {
  xaxis: {
    title: 'Number of New Carparks'
  },
  yaxis: {
    title: 'New Dewellings Per Building',
    type: 'log'
  },
  margin: {
    t: 20
  },
  hovermode: 'closest'
};

BUBBLE = document.getElementById('bubble_carpark');

Plotly.plot(BUBBLE, data, layout);