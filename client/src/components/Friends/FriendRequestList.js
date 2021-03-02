import React, { useEffect, useState } from "react";
import FriendRequestComponent from "./FriendRequestComponent";

const FriendRequestList = () => {
  const [friendRequests, updateFriendRequests] = useState([
    { username: "bui1" },
  ]);

  useEffect(() => {
    // call get all followers list
  }, []);

  return (
    <div>
      {friendRequests.map((author) => (
        <FriendRequestComponent username={author.username} />
      ))}
    </div>
  );
};

export default FriendRequestList;
