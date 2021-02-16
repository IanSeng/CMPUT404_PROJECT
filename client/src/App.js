import React, { useState, useContext } from "react";
import { Route, withRouter, Switch, Redirect } from "react-router-dom";
import LoginPage from "./components/SignupLogin/LoginPage";
import SignupPage from "./components/SignupLogin/SignupPage";
import MyFeedPage from "./components/MyFeed/MyFeedPage";
import MyProfilePage from "./components/MyProfile/MyProfilePage";
import { Context } from "./Context";
import "./App.scss";

const App = (props) => {
  const context = useContext(Context);

  return (
    <div className="App">
      <Route exact path="/">
        {context.user ? <Redirect to="/myfeed" /> : <Redirect to="/login" />}
      </Route>
      <Switch key={props.location.key}>
        <Route path="/login" component={LoginPage} />
        <Route path="/signup" component={SignupPage} />
        <Route path="/myfeed" component={MyFeedPage} />
        <Route path="/profile" component={MyProfilePage} />
      </Switch>
    </div>
  );
};

export default withRouter(App);
