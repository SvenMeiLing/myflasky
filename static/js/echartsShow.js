/* 
    *global console
    *FileName:echartsShow.js
    *PATH:static/js
    *Time: 2023/6/13 17:05
    *Author: zzy
*/


function showEcharts(data) {
    // 展示玫瑰图
    let myChart = echarts.init(document.getElementById("echarts"), "auto");
    let option = {
        title: {
            text: "chart1",
            textStyle: {
                fontSize: 24
            }
        },
        tooltip: {},
        series: [
            {
                type: 'pie',
                data,
                yAxis: {},
                roseType: 'area'
            }
        ]
    };
    myChart.setOption(option)
    return myChart;
}

function showEcharts2(line1, line2, line3, line4) {
    let myChart = echarts.init(document.getElementById("echarts2"));
    let option = {
        color: ['#80FFA5', '#00DDFF', '#37A2FF', '#FF0087'],
        title: {
            text: "chart2",
            textStyle: {
                fontSize: 17,
                color: "#c05166"
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#6a7985'
                }
            },
            triggerOn: 'mousemove'
        },
        legend: {
            data: ['其他', '番茄叶斑病', '苹果黑星病', '葡萄黑腐病']
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            }
        ],
        yAxis: [
            {
                type: 'value',
            }
        ],
        series: [
            {
                name: '其他',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                    width: 0
                },
                showSymbol: false,
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgb(128, 255, 165)'
                        },
                        {
                            offset: 1,
                            color: 'rgb(1, 191, 236)'
                        }
                    ])
                },
                emphasis: {
                    focus: 'series'
                },
                data: line1
            },
            {
                name: '番茄叶斑病',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                    width: 0
                },
                showSymbol: false,
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgb(0, 221, 255)'
                        },
                        {
                            offset: 1,
                            color: 'rgb(77, 119, 255)'
                        }
                    ])
                },
                emphasis: {
                    focus: 'series'
                },
                data: line2
            },
            {
                name: '苹果黑星病',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                    width: 0
                },
                showSymbol: false,
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgb(55, 162, 255)'
                        },
                        {
                            offset: 1,
                            color: 'rgb(116, 21, 219)'
                        }
                    ])
                },
                emphasis: {
                    focus: 'series'
                },
                data: line3
            },
            {
                name: '葡萄黑腐病',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                    width: 0
                },
                showSymbol: false,
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgb(255, 0, 135)'
                        },
                        {
                            offset: 1,
                            color: 'rgb(135, 0, 157)'
                        }
                    ])
                },
                emphasis: {
                    focus: 'series'
                },
                data: line4
            }
        ]
    };
    myChart.setOption(option)
    return myChart
}


async function collectReqData() {
    // 收集所需数据, 来源于接口中用户提供的
    let req;
    let chartsObj;
    await axios.put(
        "/data/data_analysis"
    ).then((response) => {
        let data = response.data
        chartsObj = showEcharts(data)
        req = data
        return true
    }).catch((error) => {
        alert("网络有问题")
        console.log(error)
        return false
    })
    return [req, chartsObj]
}

async function collectReqData2() {
    // 收集图表2的请求数据
    let line = []
    let chartObj;
    let result = await axios.get(
        "/plant_details",
    )
    for (let obj of result.data['data']) {
        for (let li of obj) {
            let res = li.map(innerArr => innerArr[1])
            line.push(res)
        }
    }
    chartObj = showEcharts2(line[0], line[1], line[2], line[3])
    return chartObj
}








