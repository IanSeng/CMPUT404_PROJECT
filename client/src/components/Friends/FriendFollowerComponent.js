import React from "react";
import { Header, Button } from "semantic-ui-react";
import "./FriendFollower.scss";

const FriendFollowerComponent = (props) => {
  const handleDelete = () => {
    // call props function depending if parent is FriendList, FollowerList, FollowingList
  };

  return (
    <div className="friendfollower-container">
      <Header as="a" size="large" href="#" className="userlink">
        {props.username}
      </Header>

      <Button onClick={handleDelete}>Remove</Button>
    </div>
  );
};

export default FriendFollowerComponent;
