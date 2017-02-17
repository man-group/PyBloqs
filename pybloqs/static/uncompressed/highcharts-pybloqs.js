Highcharts.theme = {
    exporting: {
        buttons: {
            contextButton: {
                menuItems: [{
                    text: 'Download CSV',
                    onclick: function() {
                        var blob = new Blob([this.getCSV()], {type: "application/octet-stream"});
                        window.open(window.URL.createObjectURL(blob), "_self");
                    }
                }]
            }
        }
    },
    chart: {
        animation: false
    },
    title: {
        text: null
    },
    colors: [
        "#017AC3", // Blue
        "#F88200", // Orange
        "#828282", // Grey
        "#80C19A", // LightGreen
        "#F7E300", // Yellow
        "#7FACDC", // LightBlue
        "#008233", // Green
        "#B01C8C", // Pink
        "#590984", // Purple
        "#007F94", // Turquoise
        "#982D3A", // BrickRed
        "#80D4E1"  // Cyan
    ],
    credits: {
        enabled: false
    },
    plotOptions: {
        area: {lineWidth: 1},
        arearange: {lineWidth: 1},
        areaspline: {lineWidth: 1},
        areasplinerange: {lineWidth: 1},
        line: {lineWidth: 1},
        spline: {lineWidth: 1},
        series: {
            dataGrouping: {
                enabled: false
            },
            animation: false
        }
    },
    xAxis: {
        gridLineDashStyle: "dash",
        gridLineColor: "#C0C0C0"
    },
    yAxis: {
        gridLineDashStyle: "dash",
        gridLineColor: "#C0C0C0",
        tickWidth: 1
    },
    legend: {
        align: "right",
        verticalAlign: "middle",
        layout: "vertical"
    }
};

var highchartsDefaultOptions = Highcharts.setOptions(Highcharts.theme);
