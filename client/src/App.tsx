import React, { useState } from "react";
import Counter from "./Counter";

const App: React.FC = () => {
  const [count, setCount] = useState(0);

  const handleIncrement = () => {
    setCount(count + 1);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>React TypeScript Counter</h1>
      <Counter count={count} />
      <button
        onClick={handleIncrement}
        style={{ marginTop: "20px", padding: "10px 20px" }}
      >
        Increment
      </button>
    </div>
  );
};

export default App;
