import * as echarts from 'echarts';
import { useEffect, useRef } from 'react';

const PieChart = ({ data }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    const chart = echarts.init(chartRef.current);
    
    const option = {
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c} ({d}%)'
      },
      series: [{
        type: 'pie',
        radius: '70%',
        data: data.map(item => ({
          name: item.category,
          value: item.amount
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }]
    };
    
    chart.setOption(option);
    
    return () => chart.dispose();
  }, [data]);

  return <div ref={chartRef} style={{ width: '100%', height: '300px' }} />;
};

export default PieChart; 