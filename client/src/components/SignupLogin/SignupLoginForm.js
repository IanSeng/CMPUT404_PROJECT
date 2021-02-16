import React, { useState } from "react";
import { Form, Input, Button } from "semantic-ui-react";
import "./SignupLoginForm.scss";

const SignupLoginForm = (props) => {
  const [username, updateUsername] = useState("");
  const [password, updatePassword] = useState("");
  const [error, setError] = useState(false);
  const [message, setMessage] = useState();

  const handleChange = (e, { name, value }) => {
    if (name === "username") {
      updateUsername(value);
    } else if (name === "password") {
      updatePassword(value);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    var message = props.onSubmit(username, password);

    if (message !== null) {
      setError(true);
      setMessage(message);
    }
  };

  return (
    <Form size="big" error={error} onSubmit={handleSubmit}>
      {message ? message : <div />}
      <Form.Field>
        <Input
          fluid
          icon="user"
          iconPosition="left"
          placeholder="username"
          name="username"
          type="text"
          value={username}
          onChange={handleChange}
        />
      </Form.Field>
      <Form.Field>
        <Input
          fluid
          icon="lock"
          iconPosition="left"
          placeholder="password"
          name="password"
          type="password"
          value={password}
          onChange={handleChange}
        />
      </Form.Field>
      <Button fluid type="submit">
        {props.buttonText}
      </Button>
    </Form>
  );
};

export default SignupLoginForm;
