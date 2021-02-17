import * as Cookies from "js-cookie";

export const setSessionCookie = (session) => {
  Cookies.remove("session");
  Cookies.set("session", session, { expires: 1 });
};

export const getSessionCookie = () => {
  const sessionCookie = Cookies.get("session");

  if (sessionCookie === undefined) {
    return {};
  } else {
    return JSON.parse(sessionCookie);
  }
};

export const removeSessionCookie = () => {
  Cookies.remove("session");
};
