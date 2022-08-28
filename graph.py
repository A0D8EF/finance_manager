# function draw_bar_graph() のdataの後に追加（今書いてるものと置き換える）
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                tooltip: {
                    enabled: false
                },
                datalabels: {
                    // font: {
                    //     size: 14
                    // },
                    formatter: function( value, context ) {
                        return "\xA5" + value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
                    },
                    color: "#000"
                },
                legend: {
                    display: false,
                }
            }
        },
        plugins: [
            ChartDataLabels,
        ],

# myChartのdataの後に追加
,
        options: {
            plugins: {
                tooltip: {
                    enabled: false
                },
                datalabels: {
                    font: {
                        size: 14
                    },
                    // formatter: function( value, context ) {
                    //     return value.toString() + '円';
                    // },
                    color: "#ffffff"
                },
                legend: {
                        display: false,
                },
                pieceLabel: {
                    render: 'label',
                    position: 'outside'
                }
            }
        },
        plugins: [
            ChartDataLabels,
        ],