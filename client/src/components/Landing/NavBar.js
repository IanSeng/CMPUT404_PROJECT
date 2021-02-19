import React, { useState, useContext } from "react";
import { useHistory } from "react-router-dom";
import { Menu, Dropdown, Icon } from "semantic-ui-react";
import { Context } from "../../Context";
import { ReactComponent as AppLogo } from "../../assets/AppLogo.svg";
import "./NavBar.scss";

const NavBar = (props) => {
  const context = useContext(Context);
  let history = useHistory();

  const [active, updateActive] = useState("MyFeed");

  const handleClick = (e, { name }) => {
    updateActive(name);
    props.renderPage(name);
  };

  const handleLogout = () => {
    context.updateUser(null);
    context.deleteCookie();
    history.push("/login");
  };

  return (
    <div className="nav-bar">
      <Menu className="nav-bar-content" size="large" icon="labeled">
        <Menu.Item className="app-logo">
          <AppLogo />
        </Menu.Item>
        <Menu.Item
          className="menu-item"
          name="MyFeed"
          active={active === "MyFeed"}
          onClick={handleClick}
        >
          <Icon inverted name="newspaper outline" />
          My Feed
        </Menu.Item>
        <Menu.Item
          className="menu-item"
          name="PublicFeed"
          active={active === "PublicFeed"}
          onClick={handleClick}
        >
          <Icon inverted name="bullhorn" />
          Public Feed
        </Menu.Item>
        <Menu.Menu position="right">
          <Menu.Item
            className="menu-item"
            name="CreatePost"
            active={active === "CreatePost"}
            onClick={handleClick}
          >
            <Icon inverted name="edit outline" />
            Create Post
          </Menu.Item>
          <Dropdown
            className="menu-item"
            as="a"
            item
            icon={null}
            trigger={
              <>
                <Icon inverted name="user" />
                {context.user ? context.user.username : "loading"}
              </>
            }
          >
            <Dropdown.Menu>
              <Dropdown.Item
                text="Profile"
                name="Profile"
                onClick={handleClick}
              />
              <Dropdown.Item
                text="Friend Requests"
                name="Friend Requests"
                onClick={handleClick}
              />
              <Dropdown.Item
                icon="sign-out"
                text="Logout"
                onClick={handleLogout}
              />
            </Dropdown.Menu>
          </Dropdown>
        </Menu.Menu>
      </Menu>
    </div>
  );
};

export default NavBar;
