$(function () {
    $('#sub').highcharts({
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 45,
                beta: 0
            }
        },
        title: {
            text: 'Proportion of New Buildings by Suburb (2002 - 2015)'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.y:.0f}</b> ({point.percentage:.1f}%)'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                depth: 35,
                dataLabels: {
                    enabled: true,
                    format: '{point.name}'
                }
            }
        },
        series: [{
            type: 'pie',
            name: 'New Buildings',
            data: [
				['East Melbourne', 4749],
				['South Yarra/Melbourne Remainder', 5397],
				['Carlton', 10870],
				['North Melbourne', 12946],
				['Kensington', 17386],
				['West Melbourne (Industrial)', 2],
				['Port Melbourne', 5],
				['Docklands', 325],
				['Southbank', 334],
				{
                    name: 'Melbourne (CBD)',
                    y: 2086,
                    sliced: true
                },
				['West Melbourne (Residential)', 4152],
				['Parkville', 4594]
            ]
        }]
    });
});