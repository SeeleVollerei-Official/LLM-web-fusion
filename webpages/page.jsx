import React, { useEffect, useState } from 'react';

const HomePage = () => {
  const [userInfo, setUserInfo] = useState([]);
  const [monthlyStats, setMonthlyStats] = useState([]);

  // 获取用户信息
  useEffect(() => {
    const fetchUserInfo = async () => {
      try {
        const response = await fetch('/api/user/info');
        const data = await response.json();
        setUserInfo(data);
        
        // 同时获取月度统计
        const statsResponse = await fetch('/api/user/monthly-stats');
        const statsData = await statsResponse.json();
        setMonthlyStats(statsData);
      } catch (error) {
        console.error('获取用户信息失败:', error);
        // 这里可以添加错误提示
      }
    };
    
    fetchUserInfo();
  }, []);

  return (
    <div className="home-container">
      {/* 渲染用户信息和统计数据 */}
    </div>
  );
};

export default HomePage; 