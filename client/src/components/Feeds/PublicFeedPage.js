import React from "react";
import { Card } from "semantic-ui-react";
import PostList from "../Post/PostList";
import { mockedImage } from "../../mocks/mockBase64Image";

const PublicFeedPage = () => {
  // TODO populate card group by mapping GET All posts call to individual post components

  const mockPosts = [
    {
      type: "post",
      title: "Tryna Graduate",
      id: "post1",
      source: "source",
      origin: "origin",
      description: "Some Description",
      contentType: "text/markdown",
      content: "# Testing if markdown works\n * first bullet point",
      author: { username: "testuser", displayName: "Mysterious Ghost" },
      count: 0,
      size: 0,
      published: "2021-02-18T07:21:52.915800Z",
      visibility: "PUBLIC",
      unlisted: false,
    },
    {
      type: "post",
      title: "Tryna Graduate Part 2",
      id: "post2",
      source: "source",
      origin: "origin",
      description: "Some Description",
      contentType: "text/plain",
      content: "# Plain text stuff",
      author: { username: "testuser", displayName: "Mysterious Ghost2" },
      count: 0,
      size: 0,
      published: "2021-02-18T07:21:52.915800Z",
      visibility: "PUBLIC",
      unlisted: false,
    },
    {
      type: "post",
      title: "Tryna Graduate Part 3",
      id: "post3",
      source: "source",
      origin: "origin",
      description: "catcatcatcat",
      contentType: "image/jpeg;base64",
      content: mockedImage,
      author: { username: "testuser", displayName: "Mysterious Ghost2" },
      count: 0,
      size: 0,
      published: "2021-02-18T07:21:52.915800Z",
      visibility: "PUBLIC",
      unlisted: false,
    },
  ];

  return (
    <Card.Group centered itemsPerRow={1}>
      <PostList posts={mockPosts} />
    </Card.Group>
  );
};

export default PublicFeedPage;
