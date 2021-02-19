import React, { useEffect, useContext } from "react";
import { Route, withRouter, Switch, Redirect } from "react-router-dom";
import LoginPage from "./components/SignupLogin/LoginPage";
import SignupPage from "./components/SignupLogin/SignupPage";
import LandingPage from "./components/Landing/LandingPage";
import MyProfilePage from "./components/MyProfile/MyProfilePage";
import { Context } from "./Context";
import { getCurrentUserObject } from "./ApiUtils";
import "./App.scss";

const App = (props) => {
  const context = useContext(Context);

  // Protected React Routes
  // From StackOverflow https://stackoverflow.com/a/43171515
  // From Tyler McGinnis https://stackoverflow.com/users/1867084/tyler-mcginnis
  const PrivateRoute = ({ component: Component, isAuthorized, ...rest }) => {
    return (
      <Route
        {...rest}
        render={(props) =>
          isAuthorized ? (
            <Component {...props} />
          ) : (
            <Redirect
              to={{ pathname: "/login", state: { from: props.location } }}
            />
          )
        }
      />
    );
  };

  const updateUserObject = async () => {
    const response = await getCurrentUserObject(context.cookie);

    if (response.data && response.data.username) {
      context.updateUser(response.data);
    }
  };

  useEffect(() => {
    updateUserObject();
  }, []);

  return (
    <div className="app">
      <Route exact path="/">
        {context.cookie ? <Redirect to="/home" /> : <Redirect to="/login" />}
      </Route>

      <Switch key={props.location.key}>
        <Route path="/login" component={LoginPage} />
        <Route path="/signup" component={SignupPage} />
        <PrivateRoute
          isAuthorized={context.cookie}
          path="/home"
          component={LandingPage}
        />
        <PrivateRoute
          isAuthorized={context.cookie}
          path="/profile"
          component={MyProfilePage}
        />
      </Switch>
    </div>
  );
};

export default withRouter(App);
