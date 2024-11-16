import React from "react";
import logo from "./logo.svg";
import "./App.css";
import Test  from "./components/Test.js";


function App() {
  const [data, setData] = React.useState(null);
  const [input, setInput] = React.useState("None");

  const onInputChange = (e) => {
    setInput(e.target.value);
  }

  React.useEffect(() => {
    fetch("/api")
      .then(res => res.json())
      .then(data => setData(data.message))
      .catch(err => {
        setData("Error"); 
      });
  }, []);
  
  return (
    <div>
      <Test />
      <p>{!data ? "Loading.." : data}</p>
      <input type="text" onChange={onInputChange} />
      <p>Input: {input}</p>
    </div>
    
  );
}

export default App;