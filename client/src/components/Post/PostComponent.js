import React, { useState, useContext } from "react";
import {
  Card,
  Icon,
  Image,
  Button,
  Label,
  CardContent,
} from "semantic-ui-react";
import axios from "axios";
import { SERVER_HOST } from "../../Constants";
import { Context } from "../../Context";
import { getUserObject } from "../../ApiUtils";
import "./PostComponent.scss";

const PostComponent = (
  {
    title = "Test Title",
    description = "Some Description",
    content = "Some Content",
    contentType = "text/plain",
    author = { displayName: "John Appleseed" },
    published = "2021-02-18T07:21:52.915800Z",
    visibility = "PUBLIC",
  },
  ...props
) => {
  const context = useContext(Context);

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
                Posted by {author.displayName} on {published}
              </span>
            </div>
          </Card.Meta>
          <Card.Description>{description}</Card.Description>
        </Card.Content>
        <Image
          src="https://cw-gbl-gws-prod.azureedge.net/-/media/cw/americas/canada/office-pages/edmonton-mobile.jpg?rev=6ec6a6b628cd46fda0f0312309408a67"
          wrapped
          ui={false}
        />
        <Card.Content>
          <Card.Description>{content}</Card.Description>
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
            <Button basic color="blue" floated="right">
              <Icon name="comments" />
              Comment
            </Button>
            <Label as="a" basic color="blue" pointing="left">
              2,048
            </Label>
          </Button>
        </Card.Content>
      </Card>

      <Card fluid raised centered>
        <Card.Content>
          <Button basic color="black" floated="right" icon="share alternate" />
          <Button basic color="black" floated="right" icon="trash alternate" />
          <Button basic color="black" floated="right" icon="pencil" />
          <Card.Header>Test Post Title</Card.Header>
          <Card.Meta>
            <div>
              <Icon name="eye" />
              <span>Public Post</span>
            </div>
            <div>
              <span className="date">
                Posted by User on Dec 15 2020 at X:XX PM
              </span>
            </div>
          </Card.Meta>
          <Card.Description>
            "Sed ut perspiciatis unde omnis iste natus error sit voluptatem
            accusantium doloremque laudantium, totam rem aperiam, eaque ipsa
            quae ab illo inventore veritatis et quasi architecto beatae vitae
            dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
            pariatur?"
          </Card.Description>
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
            <Button basic color="blue" floated="right">
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
