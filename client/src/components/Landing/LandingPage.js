import React, { useState } from "react";
import NavBar from "./NavBar";
import MyFeedPage from "../Feeds/MyFeedPage";
import PublicFeedPage from "../Feeds/PublicFeedPage";
import CreatePostPage from "../Post/CreatePostForm";
import MyProfilePage from "../MyProfile/MyProfilePage";
import "./LandingPage.scss";

const LandingPage = () => {
  const [page, updatePage] = useState(<MyFeedPage />);

  const renderPage = (page) => {
    if (page === "MyFeed") updatePage(<MyFeedPage />);
    else if (page === "PublicFeed") updatePage(<PublicFeedPage />);
    else if (page === "CreatePost") updatePage(<CreatePostPage />);
    else if (page === "Profile") updatePage(<MyProfilePage />);
    else return updatePage(<MyFeedPage />);
  };

  return (
    <div className="landing-page">
      <NavBar renderPage={renderPage} />
      {page}
    </div>
  );
};

export default LandingPage;
