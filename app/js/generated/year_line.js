$(function () {
    $('#year_line').highcharts({
        chart: {
            type: 'line'
        },
        title: {
            text: 'New Dewellings vs Year'
        },
        subtitle: {
            text: 'From 2002 to 2015'
        },
        xAxis: {
            categories: [2002,2004,2006,2008,2011,2013,2015]
        },
        yAxis: {
            title: {
                text: 'New Dewellings'
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: false
            }
        },
        series: [{
            name: 'New Dewellings',
            data: [30461, 34996, 42033, 48392, 53340, 58711, 68067]
        }]
    });
});