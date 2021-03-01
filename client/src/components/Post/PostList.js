import React from "react";
import moment from "moment";
import PostComponent from "./PostComponent";

const PostList = (props) => {
  const posts = props.posts.map(
    ({
      title,
      description,
      content,
      contentType,
      author,
      published,
      visibility,
    }) => {
      return (
        <PostComponent
          title={title}
          description={description}
          content={content}
          contentType={contentType}
          author={author}
          published={moment(published).format("MMMM Do YYYY, h:mm:ss a")}
          visibility={visibility}
        />
      );
    }
  );

  return <div>{posts}</div>;
};

export default PostList;
