import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import "semantic-ui-css/semantic.min.css";
import "./index.css";
import App from "./App";
import ContextProvider from "./Context";

ReactDOM.render(
  <React.StrictMode>
    <ContextProvider>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </ContextProvider>
  </React.StrictMode>,
  document.getElementById("root")
);
