import React from "react";
import { useHistory } from "react-router-dom";
import { Button, Icon } from "semantic-ui-react";
import { PAGE_CREATE_POST } from "../../Constants";
import "./CreatePostPage.scss";

const PostSuccess = () => {
  let history = useHistory();
  const handleCreateClick = () => {
    history.push(PAGE_CREATE_POST);
  };
  return (
    <div className="post-success">
      <Icon name="check circle outline" className="check-icon" size="huge" />
      <div className="success-content">
        <h1>Post created successfully!</h1>
        <Button className="success-view-post">View Post</Button>
        <Button className="success-createpost" onClick={handleCreateClick}>
          Create Another Post
        </Button>
      </div>
    </div>
  );
};

export default PostSuccess;
