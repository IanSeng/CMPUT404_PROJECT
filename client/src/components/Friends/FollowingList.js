import React, { useEffect, useState } from "react";
import FriendFollowerComponent from "./FriendFollowerComponent";

const FollowerList = () => {
  const [following, updateFollowing] = useState([{ username: "bui1" }]);

  useEffect(() => {
    // call get all following list
  }, []);

  return (
    <div>
      {following.map((author) => (
        <FriendFollowerComponent username={author.username} />
      ))}
    </div>
  );
};

export default FollowerList;
