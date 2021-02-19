import React from "react";
import { Card, Icon, Image, Button } from "semantic-ui-react";
import PostComponent from "../Post/PostComponent";

const MyFeedPage = () => {
  return (
    <Card.Group centered>
      <PostComponent />
    </Card.Group>
  );
};

export default MyFeedPage;
