import React, { useState } from "react";
import { Header, Segment, Button } from "semantic-ui-react";
import "./MyProfilePage.scss";

const MyProfileData = () => {
  return (
    <div>
      <div className="profile-top-section">
        <div className="display-name-heading">
          <Header as="h1" floated="left">
            Test User
          </Header>
          <Button>Edit</Button>
        </div>

        <div className="display-name-heading">
          <Header as="h4" floated="left">
            GitHub:
          </Header>
          <span>bui1</span>
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
