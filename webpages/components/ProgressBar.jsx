const ProgressBar = ({ percent, goal }) => {
  return (
    <div className="progress-container">
      <div className="progress-bar">
        <div 
          className="progress-fill"
          style={{ width: `${percent}%` }}
        />
      </div>
      <div className="progress-text">
        <span>目标: ¥{goal}</span>
        <span>{percent}%</span>
      </div>
    </div>
  );
};

export default ProgressBar; 