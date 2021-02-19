import React, { Component } from "react";
import NavBar from "./NavBar";
import MyFeedPage from "../Feeds/MyFeedPage";
import PublicFeedPage from "../Feeds/PublicFeedPage";
import MyProfilePage from "../MyProfile/MyProfilePage";
import { getCurrentUserObject } from "../../ApiUtils";
import { Context } from "../../Context";
import "./LandingPage.scss";

class LandingPage extends Component {
  constructor(props) {
    super(props);

    this.state = { page: <MyFeedPage />, name: "" };
  }

  renderPage = (page) => {
    if (page === "MyFeed") this.setState({ page: <MyFeedPage /> });
    else if (page === "PublicFeed") this.setState({ page: <PublicFeedPage /> });
    else if (page === "Profile") this.setState({ page: <MyProfilePage /> });
    else return this.setState({ page: <MyFeedPage /> });
  };

  render() {
    return (
      <div className="landing-page">
        <NavBar renderPage={this.renderPage} />
        {this.state.page}
      </div>
    );
  }
}

LandingPage.contextType = Context;

export default LandingPage;
