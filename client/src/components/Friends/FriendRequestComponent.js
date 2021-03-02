import React from "react";
import { Header, Button } from "semantic-ui-react";
import "./FriendFollower.scss";

const FriendRequestComponent = (props) => {
  const handleAccept = () => {
    // call props onHandleAccept
    // delete entry from friend request list
    // make post request to update friends list
  };

  const handleDecline = () => {};

  return (
    <div className="friendrequest-container">
      <Header as="a" size="large" href="#" className="userlink">
        {props.username}
      </Header>

      <div className="test">
        <Button onClick={handleDecline}>Decline</Button>
        <Button className="accept-request-btn" onClick={handleAccept}>
          Accept
        </Button>
      </div>
    </div>
  );
};

export default FriendRequestComponent;
