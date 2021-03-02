import React, { useState, useContext, useEffect } from "react";
import { Header, Button } from "semantic-ui-react";
import { useLocation } from "react-router-dom";

import EditProfileModal from "./EditProfileModal";
import { Context } from "../../Context";
import "./ProfilePage.scss";

const MyProfileData = (props) => {
  const context = useContext(Context);
  const location = useLocation();
  const [name, updateName] = useState("Loading...");
  const [showEditBtn, updateShowEditBtn] = useState(true);

  useEffect(() => {
    const authorId = window.location.pathname.split("/").pop();
    nameToRender(authorId);
    shouldShowEditBtn(authorId);
  }, [location, props]);

  const shouldShowEditBtn = (authorId) => {
    if (context.user) {
      updateShowEditBtn(authorId === context.user.id);
    }
  };

  const nameToRender = (authorId) => {
    let result = "Loading...";

    if (context.user) {
      if (authorId !== context.user.id) {
        result = props.author.displayName
          ? props.author.displayName
          : props.author.username;
        updateName(result);
        return;
      }
    }

    if (context.user && context.user.displayName) {
      result = context.user.displayName;
    } else if (context.user && context.user.username) {
      result = context.user.username;
    }

    updateName(result);
  };

  return (
    <div>
      <div className="profile-top-section">
        <div className="display-name-heading">
          <Header as="h1" floated="left">
            {name}
          </Header>

          {showEditBtn ? (
            <EditProfileModal />
          ) : (
            <Button>Send Friend Request</Button>
          )}
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
