import React, { useEffect, useState, useContext } from "react";
import { Card, Message, Dimmer, Loader } from "semantic-ui-react";
import axios from "axios";
import PostList from "../Post/PostList";
import { SERVER_HOST } from "../../Constants";
import { Context } from "../../Context";

const MyFeedPage = () => {
  const context = useContext(Context);

  const [posts, updatePosts] = useState([]);
  const [error, updateError] = useState(false);
  const [loading, updateLoading] = useState(true);

  const getAllMyPosts = async () => {
    try {
      const response = await axios.get(
        `${SERVER_HOST}/service/author/${context.user.id}/posts/`,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${context.cookie}`,
          },
        }
      );

      updatePosts(response.data);
    } catch (error) {
      updateError(true);
    }
    updateLoading(false);
  };

  const getAllInboxItems = () => {};

  useEffect(() => {
    if (context.user) {
      getAllMyPosts();
      getAllInboxItems();
    }
  }, []);

  return (
    <div>
      {loading && (
        <Dimmer inverted active>
          <Loader size="medium">Loading Posts...</Loader>
        </Dimmer>
      )}
      {error && (
        <Message
          error
          size="large"
          header="Error"
          content="Something happened on our end. Please try again later."
        />
      )}
      <Card.Group centered itemsPerRow={1}>
        <PostList posts={posts} />
      </Card.Group>
    </div>
  );
};

export default MyFeedPage;
