import React, { useState } from "react";
import Counter from "./Counter";

const App: React.FC = () => {
  const [count, setCount] = useState(0);

  const handleIncrement = () => {
    setCount(count + 1);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <div>
        <h1>React TypeScript Counter</h1>
        <Counter count={count} />
        <button
          onClick={handleIncrement}
          style={{ marginTop: "20px", padding: "10px 20px" }}
        >
          Increment
        </button>
      </div>
      <div>
        <iframe src="http://localhost:8050" width="700" height="600" />
      </div>
    </div>
  );
};

export default App;
