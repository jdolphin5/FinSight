import React, { useState } from "react";

const App: React.FC = () => {
  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <div>
        <h1>React App</h1>
      </div>
      <div>
        <iframe src="http://localhost:8050" width="900" height="800" />
      </div>
    </div>
  );
};

export default App;
