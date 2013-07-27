/**
 * Created with IntelliJ IDEA.
 * User: lancejenkin
 * Date: 26/07/13
 * Time: 9:58 PM
 * To change this template use File | Settings | File Templates.
 */

(function($){

    var seriesOptions = [],
        yAxisOptions = [],
        seriesCounter = 0,
        names = ['phase 1', 'phase 2', 'phase 3'],
        colors = Highcharts.getOptions().colors;

    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });

    $.each(names, function(i, name) {

        $.getJSON('http://localhost:5000/usage?phase='+ name.toLowerCase() ,	function(data) {

            seriesOptions[i] = {
                name: name,
                data: data
            };

            // As we're loading the data asynchronously, we don't know what order it will arrive. So
            // we keep a counter and create the chart when all the data is loaded.
            seriesCounter++;

            if (seriesCounter == names.length) {
                createChart();
            }
        });
    });



    // create the chart when all data is loaded
    function createChart() {

        $('#usageGraph').highcharts('StockChart', {
            chart: {
                events:{
                    load : function() {

                        // set up the updating of the chart each second
                        var series = this.series;
                        var chart = this;
                        setInterval(function() {
                            $.each(names, function(i, name) {

                                if(series[i].data.length > 0){
                                    var last_epoch = series[i].data[series[i].data.length - 1].x;
                                    $.getJSON('http://localhost:5000/usage?phase='+ name.toLowerCase()  + '&start=' +
                                        last_epoch,	function(data) {
                                        if(data.length > 0){
                                            for(var data_index =0; data_index < data.length; data_index++){
                                                series[i].addPoint(data[data_index], false, true);
                                            }

                                            chart.redraw();
                                        }

                                    });
                                }
                            });


                        }, 5000);
                    }
                }
            },

            rangeSelector: {
                selected: 4
            },

            yAxis: {
                plotLines: [{
                    value: 0,
                    width: 2,
                    color: 'silver'
                }],
                min: 0,
                title: {
                    text: "Usage (Watts)"
                }
            },
            xAxis: {
                type: 'datetime'
            },


            rangeSelector: {
                buttons: [{
                    count: 5,
                    type: 'minute',
                    text: '5M'
                },{
                    count: 1,
                    type: 'hour',
                    text: '1H'
                }, {
                    count: 10,
                    type: 'hour',
                    text: '10H'
                }, {
                    count: 1,
                    type: 'day',
                    text: '1D'
                }, {
                    type: 'all',
                    text: 'All'
                }],
                inputEnabled: false,
                selected: 0
            },

            tooltip: {
                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
                valueDecimals: 2
            },
            title:{
                text: "Current Energy Usage"
            },
            series: seriesOptions
        });
    }



})(jQuery);