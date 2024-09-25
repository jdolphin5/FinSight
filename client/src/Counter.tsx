import React from "react";

interface CounterProps {
  count: number;
}

const Counter: React.FC<CounterProps> = ({ count }) => {
  return (
    <div>
      <h2>Current Count: {count}</h2>
    </div>
  );
};

export default Counter;
