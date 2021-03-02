import React, { useState } from "react";
import { Menu, Segment } from "semantic-ui-react";
import "./ProfilePage.scss";
import ProfileData from "./ProfileData";
import FriendRequestList from "../Friends/FriendRequestList";
import FriendList from "../Friends/FriendList";
import FollowerList from "../Friends/FollowerList";
import FollowingList from "../Friends/FollowingList";

const recentPosts = "Recent Posts";
const friends = "Friends";
const followers = "Followers";
const following = "Following";
const friendRequests = "Friend Requests";

const MyProfilePage = () => {
  const [activeItem, updateActiveItem] = useState(friendRequests);
  const [currentSection, updateSection] = useState(<FriendRequestList />);

  const handleItemClick = (e, { name, section }) => {
    updateActiveItem(name);
    updateSection(section);
  };

  const placeholder = (
    <img
      alt="placeholder "
      src="https://react.semantic-ui.com/images/wireframe/paragraph.png"
    />
  );

  return (
    <div className="profile-page-container">
      <div className="profile-data">
        <ProfileData />
      </div>

      <div className="profile-posts">
        <Menu attached="top" tabular>
          <Menu.Item
            name={recentPosts}
            active={activeItem === recentPosts}
            onClick={handleItemClick}
            section={placeholder}
          />
          <Menu.Item
            name={friends}
            active={activeItem === friends}
            onClick={handleItemClick}
            section={<FriendList />}
          />
          <Menu.Item
            name={followers}
            active={activeItem === followers}
            onClick={handleItemClick}
            section={<FollowerList />}
          />
          <Menu.Item
            name={following}
            active={activeItem === following}
            onClick={handleItemClick}
            section={<FollowingList />}
          />
          <Menu.Item
            name={friendRequests}
            active={activeItem === friendRequests}
            onClick={handleItemClick}
            section={<FriendRequestList />}
          />
        </Menu>

        <Segment attached="bottom">{currentSection}</Segment>
      </div>
    </div>
  );
};

export default MyProfilePage;
