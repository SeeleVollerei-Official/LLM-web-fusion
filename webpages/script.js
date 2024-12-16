// 初始化进度条
function initProgressBar() {
    const progress = 50; // 示例进度
    const progressBar = document.getElementById('progressBar');
    progressBar.innerHTML = `
        <div class="progress-container">
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${progress}%"></div>
            </div>
            <div class="progress-text">${progress}%</div>
        </div>
    `;
}

// 初始化饼图
function initPieChart() {
    const chartDom = document.getElementById('pieChart');
    const myChart = echarts.init(chartDom);
    const option = {
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c}元 ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        series: [
            {
                name: '支出分类',
                type: 'pie',
                radius: '70%',
                data: [
                    { value: 1500, name: '食品' },
                    { value: 1200, name: '娱乐' },
                    { value: 800, name: '交通' },
                    { value: 1000, name: '购物' },
                    { value: 500, name: '其他' }
                ],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
    myChart.setOption(option);

    // 响应窗口大小变化
    window.addEventListener('resize', function() {
        myChart.resize();
    });
}

// 页面加载完成后初始化所有组件
document.addEventListener('DOMContentLoaded', function() {
    initProgressBar();
    initPieChart();
}); 