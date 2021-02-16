import React from "react";
import { Link } from "react-router-dom";
import { Message } from "semantic-ui-react";
import "./SignupLoginPage.scss";
import SignupLoginForm from "./SignupLoginForm";
import { ReactComponent as AppName } from "../../assets/AppName.svg";

const LoginPage = (props) => {
  const onSubmit = (username, password) => {
    return (
      <Message
        error
        size="tiny"
        header="Incorrect username or password"
        content="Please enter the correct username or password."
      />
    );
  };

  return (
    <div className="Page">
      <AppName className="AppName" />
      <h2 className="Title">LOGIN</h2>
      <SignupLoginForm onSubmit={onSubmit} buttonText="Login" />
      <div className="LinkContainer">
        <p className="LinkInfo">Don't have an account?</p>
        <Link to="/signup">Sign up</Link>
      </div>
    </div>
  );
};

export default LoginPage;
