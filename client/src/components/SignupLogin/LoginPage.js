import React, { useState, useContext } from "react";
import { Link, Redirect } from "react-router-dom";
import { Message, Dimmer, Loader } from "semantic-ui-react";
import axios from "axios";
import "./SignupLoginPage.scss";
import SignupLoginForm from "./SignupLoginForm";
import { ReactComponent as AppName } from "../../assets/AppName.svg";
import { SERVER_HOST } from "../../Constants";
import { Context } from "../../Context";
import { getUserObject } from "../../ApiUtils";

const LoginPage = (props) => {
  const [loading, updateLoading] = useState(false);
  const context = useContext(Context);

  const onSubmit = async (username, password) => {
    username = username.trim();

    if (!validate(username, password)) {
      return (
        <Message
          error
          size="tiny"
          header="Insufficient username or password length"
          list={[
            "Usernames must be 3 characters or more",
            "Passwords must be 5 characters or more",
          ]}
        />
      );
    }

    updateLoading(true);

    const response = await signinRequest(username, password);
    const { status } = response;
    const { token, id } = response.data;

    if (status !== 200) {
      updateLoading(false);
    }

    if (status === 401) {
      return (
        <Message
          error
          size="tiny"
          header="Account Not Approved"
          content="Please wait for admin approval to login."
        />
      );
    } else if (status === 400) {
      return (
        <Message
          error
          size="tiny"
          header="Invalid Username or Password"
          content="Please check if your username or password is correct."
        />
      );
    } else if (status === 200) {
      // save cookie and redirect user to the myfeed page
      const getAuthorResponse = await getUserObject(token, id);

      updateLoading(false);
      const getAuthorStatus = getAuthorResponse.status;
      const userData = getAuthorResponse.data;

      if (getAuthorStatus !== 200) {
        return (
          <Message
            error
            size="tiny"
            header="Error"
            content="Please try again."
          />
        );
      }

      context.updateUser(userData);
      return <Redirect to="/myfeed" token={token} />;
    } else {
      return (
        <Message error size="tiny" header="Error" content="Please try again." />
      );
    }
  };

  const validate = (username, password) => {
    if (username.length >= 3 && password.length >= 5) {
      return true;
    }

    return false;
  };

  const signinRequest = async (username, password) => {
    const request = {
      username,
      password,
    };

    try {
      const response = await axios.post(
        `${SERVER_HOST}/service/author/auth/`,
        request
      );
      return response;
    } catch (error) {
      return error.response;
    }
  };

  return (
    <div className="Page">
      {loading && (
        <Dimmer active>
          <Loader size="medium">Logging In...</Loader>
        </Dimmer>
      )}
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
