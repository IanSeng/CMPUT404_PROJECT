import React, { createContext, useState } from "react";

export const Context = createContext();

const ContextProvider = (props) => {
  const [currentUser, updateCurrentUser] = useState(null);

  const context = {
    user: currentUser,
    updateUser: (user) => {
      updateCurrentUser(user);
    },
  };

  return (
    <Context.Provider value={{ ...context }}>{props.children}</Context.Provider>
  );
};

export default ContextProvider;
