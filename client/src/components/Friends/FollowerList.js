import React, { useEffect, useState } from "react";
import FriendFollowerComponent from "./FriendFollowerComponent";

const FollowerList = () => {
  const [followers, updateFollowers] = useState([{ username: "bui1" }]);

  useEffect(() => {
    // call get all followers list
  }, []);

  return (
    <div>
      {followers.map((author) => (
        <FriendFollowerComponent username={author.username} />
      ))}
    </div>
  );
};

export default FollowerList;
