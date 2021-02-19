import React, { createContext, useState, useEffect } from "react";
import * as Cookies from "js-cookie";
import { getCurrentUserObject } from "./ApiUtils";

export const Context = createContext();

export const setSessionCookie = (token) => {
  Cookies.remove("session");
  Cookies.set("session", token, { expires: 1 });
};

export const getSessionCookie = () => {
  const sessionCookie = Cookies.get("session");

  if (sessionCookie === undefined) {
    return null;
  } else {
    return sessionCookie;
  }
};

export const removeSessionCookie = () => {
  Cookies.remove("session");
};

const ContextProvider = (props) => {
  const [currentUser, updateCurrentUser] = useState(null);
  const [cookie, updateCurrentCookie] = useState(getSessionCookie());

  const context = {
    user: currentUser,
    updateUser: (user) => {
      updateCurrentUser(user);
    },
    cookie,
    updateCookie: (token) => {
      setSessionCookie(token);
      updateCurrentCookie(getSessionCookie());
    },
    deleteCookie: () => {
      removeSessionCookie();
      updateCurrentCookie(null);
    },
  };

  return (
    <Context.Provider value={{ ...context }}>{props.children}</Context.Provider>
  );
};

export default ContextProvider;
