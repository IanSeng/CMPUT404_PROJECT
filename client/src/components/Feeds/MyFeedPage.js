import React from "react";
import { Card } from "semantic-ui-react";
import PostComponent from "../Post/PostComponent";
import moment from "moment";

const MyFeedPage = () => {
  return (
    <Card.Group centered itemsPerRow={1}>
      <PostComponent
        title="Tryna Graduate"
        description="Some Description"
        content="# Testing if markdown works\n * first bullet point"
        contentType="text/markdown"
        author={{ displayName: "Mysterious Ghost" }}
        published={moment("2021-02-18T07:21:52.915800Z").format(
          "MMMM Do YYYY, h:mm:ss a"
        )}
        visibility="PUBLIC"
        imageUrl="https://cw-gbl-gws-prod.azureedge.net/-/media/cw/americas/canada/office-pages/edmonton-mobile.jpg?rev=6ec6a6b628cd46fda0f0312309408a67"
      />
      <PostComponent
        title="Tryna Graduate Part 2"
        description="Some Description"
        content="# Plain text stuff"
        contentType="text/plain"
        author={{ displayName: "Mysterious Ghost2" }}
        published={moment("2021-02-18T07:21:52.915800Z").format(
          "MMMM Do YYYY, h:mm:ss a"
        )}
        visibility="PUBLIC"
      />
    </Card.Group>
  );
};

export default MyFeedPage;
