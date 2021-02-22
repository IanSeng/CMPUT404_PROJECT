import React, { useState, useContext } from "react";
import { Header, Button } from "semantic-ui-react";
import EditProfileModal from "./EditProfileModal";
import { Context } from "../../Context";
import "./ProfilePage.scss";

const MyProfileData = () => {
  const context = useContext(Context);

  let nameToRender = "Loading...";

  if (context.user && context.user.displayName) {
    nameToRender = context.user.displayName;
  } else if (context.user && context.user.username) {
    nameToRender = context.user.username;
  }

  return (
    <div>
      <div className="profile-top-section">
        <div className="display-name-heading">
          <Header as="h1" floated="left">
            {nameToRender}
          </Header>
          <EditProfileModal />
        </div>

        <div className="display-name-heading">
          <Header as="h4" floated="left">
            GitHub:
          </Header>
          <span>
            {context.user && context.user.github ? context.user.github : "N/A"}
          </span>
        </div>
      </div>

      <div className="profile-stats-table">
        <div className="display-name-heading">
          <Header as="h4" floated="left">
            Posts:
          </Header>
          <span>4</span>
        </div>
        <div className="display-name-heading">
          <Header as="h4" floated="left">
            Friends:
          </Header>
          <span>2</span>
        </div>
        <div className="display-name-heading">
          <Header as="h4" floated="left">
            Followers:
          </Header>
          <span>5</span>
        </div>
        <div className="display-name-heading">
          <Header as="h4" floated="left">
            Following:
          </Header>
          <span>5</span>
        </div>
      </div>
    </div>
  );
};

export default MyProfileData;
