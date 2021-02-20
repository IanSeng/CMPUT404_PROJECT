import React, { useState } from "react";
import { Header, Icon } from "semantic-ui-react";
import CreatePostForm from "./CreatePostForm";
import "./CreatePostPage.scss";

const CreatePostPage = (props) => {
  return (
    <div className="create-post">
      <Header as="h2">
        <Icon name="edit" />
        <Header.Content>Create Post</Header.Content>
      </Header>
      <CreatePostForm />
    </div>
  );
};

export default CreatePostPage;
