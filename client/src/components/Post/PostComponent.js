import React from "react";
import { Card, Icon, Image, Button, Label } from "semantic-ui-react";
import ReactMarkdown from "react-markdown";
import gfm from "remark-gfm";
import "./PostComponent.scss";

const markdownType = "text/markdown";
const plainTextType = "text/plain";

const defaultProps = {
  title: "Test Title",
  description: "Some Description",
  content: "Some Content",
  contentType: "text/plain",
  author: { displayName: "John Appleseed" },
  published: "2021-02-18T07:21:52.915800Z",
  visibility: "PUBLIC",
};

const PostComponent = (props) => {
  const passedValues = { ...defaultProps, ...props };
  const {
    title,
    description,
    content,
    contentType,
    author,
    published,
    visibility,
  } = passedValues;

  const markdown = `# Hello World \n**This markdown thing is really cool**`;

  const renderContent = () => {
    if (contentType.includes("image")) {
      return <Image src={content} size="medium" />;
    } else if (contentType === markdownType) {
      return <ReactMarkdown plugins={[gfm]} children={markdown} />;
    } else if (contentType === plainTextType) {
      return <p>{content}</p>;
    }
  };

  return (
    <div className="custom-card">
      <Card fluid raised centered>
        <Card.Content>
          <Button basic color="black" floated="right" icon="share alternate" />
          <Button basic color="black" floated="right" icon="trash alternate" />
          <Button basic color="black" floated="right" icon="pencil" />
          <Card.Header>{title}</Card.Header>
          <Card.Meta>
            <div>
              <Icon name="eye" />
              <span>
                {visibility.charAt(0) + visibility.substring(1).toLowerCase()}
              </span>
            </div>
            <div>
              <span className="date">
                Posted by <a href="/home">{author.displayName}</a> on{" "}
                {published}
              </span>
            </div>
          </Card.Meta>
          <Card.Description>{description}</Card.Description>
        </Card.Content>
        <Card.Content>
          <Card.Description>{renderContent()}</Card.Description>
        </Card.Content>
        <Card.Content extra>
          <Button as="div" labelPosition="right">
            <Button color="red">
              <Icon name="heart" />
              Like
            </Button>
            <Label as="a" basic color="red" pointing="left">
              2,048
            </Label>
          </Button>
          <Button as="div" labelPosition="left">
            <Button color="blue" floated="right">
              <Icon name="comments" />
              Comment
            </Button>
            <Label as="a" basic color="blue" pointing="left">
              2,048
            </Label>
          </Button>
        </Card.Content>
      </Card>
    </div>
  );
};

export default PostComponent;
