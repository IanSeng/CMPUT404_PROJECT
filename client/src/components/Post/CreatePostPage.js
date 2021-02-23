import React, { useContext } from "react";
import axios from "axios";
import { Header, Icon } from "semantic-ui-react";
import CreatePostForm from "./CreatePostForm";
import { Context } from "../../Context";
import { SERVER_HOST } from "../../Constants";
import "./CreatePostPage.scss";

const CreatePostPage = (props) => {
  const context = useContext(Context);

  const onSubmit = async (body) => {
    try {
      const response = await axios.post(
        `${SERVER_HOST}/service/author/${context.user.id}/posts/`,
        body,
        {
          headers: {
            Authorization: `Token ${context.cookie}`,
            "Content-Type": "application/json",
          },
        }
      );

      console.log(response);
    } catch (error) {
      console.log(error.response);
    }
  };

  return (
    <div className="create-post-page">
      <Header as="h2">
        <Icon name="edit" />
        <Header.Content>Create Post</Header.Content>
      </Header>
      <CreatePostForm submit={onSubmit} />
    </div>
  );
};

export default CreatePostPage;
