import React, { useState } from "react";
import { Menu, Segment } from "semantic-ui-react";
import "./MyProfilePage.scss";

const recentPosts = "Recent Posts";
const friends = "Friends";
const followers = "Followers";
const following = "Following";
const friendRequests = "Friend Requests";

const MyProfilePage = () => {
  const [activeItem, updateActiveItem] = useState(recentPosts);

  const handleItemClick = (e, { name }) => {
    updateActiveItem(name);
  };

  // TODO depending on the active menu item, display the right profile component using segment
  return (
    <div className="profile-page-container">
      <div className="profile-data">
        <Segment>
          <img
            alt="placeholder "
            src="https://react.semantic-ui.com/images/wireframe/paragraph.png"
          />
        </Segment>
      </div>

      <div className="profile-posts">
        <Menu attached="top" tabular>
          <Menu.Item
            name={recentPosts}
            active={activeItem === recentPosts}
            onClick={handleItemClick}
          />
          <Menu.Item
            name={friends}
            active={activeItem === friends}
            onClick={handleItemClick}
          />
          <Menu.Item
            name={followers}
            active={activeItem === followers}
            onClick={handleItemClick}
          />
          <Menu.Item
            name={following}
            active={activeItem === following}
            onClick={handleItemClick}
          />
          <Menu.Item
            name={friendRequests}
            active={activeItem === friendRequests}
            onClick={handleItemClick}
          />
        </Menu>

        <Segment attached="bottom">
          <img
            alt="placeholder "
            src="https://react.semantic-ui.com/images/wireframe/paragraph.png"
          />
        </Segment>
      </div>
    </div>
  );
};

export default MyProfilePage;
