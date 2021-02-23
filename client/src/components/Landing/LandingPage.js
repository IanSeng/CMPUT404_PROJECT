import React, { useState, useContext } from "react";
import { useHistory } from "react-router-dom";
import { Context } from "../../Context";
import NavBar from "./NavBar";
import MyFeedPage from "../Feeds/MyFeedPage";
import PublicFeedPage from "../Feeds/PublicFeedPage";
import CreatePostPage from "../Post/CreatePostPage";
import ProfilePage from "../Profile/ProfilePage";
import {
  ROUTE_MY_FEED,
  ROUTE_PUBLIC_FEED,
  PAGE_MY_FEED,
  PAGE_PUBLIC_FEED,
  PAGE_PROFILE,
  PAGE_CREATE_POST,
} from "../../Constants";
import "./LandingPage.scss";

const LandingPage = ({ subComponent, activeMenuItem }) => {
  const context = useContext(Context);
  let history = useHistory();

  const [page, updatePage] = useState(subComponent);

  const renderPage = (page) => {
    if (page === PAGE_MY_FEED) {
      updatePage(<MyFeedPage />);
      history.push(ROUTE_MY_FEED);
    } else if (page === PAGE_PUBLIC_FEED) {
      updatePage(<PublicFeedPage />);
      history.push(ROUTE_PUBLIC_FEED);
    } else if (page === PAGE_CREATE_POST) {
      updatePage(<CreatePostPage />);
      history.push(`/author/createpost`);
    } else if (page === PAGE_PROFILE) {
      updatePage(<ProfilePage />);
      history.push(`/author/${context.user.id}`);
    } else {
      updatePage(<MyFeedPage />);
      history.push(ROUTE_MY_FEED);
    }
  };

  return (
    <div className="landing-page">
      <NavBar renderPage={renderPage} activeMenuItem={activeMenuItem} />
      {page}
    </div>
  );
};

export default LandingPage;
