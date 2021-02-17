import React, { useState, useEffect } from "react";
import { Button, Input, Message, Header, Modal, Form } from "semantic-ui-react";

const EditProfileModal = () => {
  const [open, setOpen] = useState(false);
  const [displayName, updateDisplayName] = useState("");
  const [githubUsername, updateGithubUsername] = useState("");
  const [error, setError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleChange = (e, { name, value }) => {
    if (name === "displayName") {
      updateDisplayName(value);
    } else if (name === "githubUsername") {
      updateGithubUsername(value);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // TODO validate user input
    // Check if display name is valid
    // Check if GitHub username exists

    // Validate if django backend saved user profile correctly
    // If so close modal, and display toast message saying success
    // Otherwise, show error message in modal
    // setOpen(false);
  };

  return (
    <Modal
      onClose={() => setOpen(false)}
      onOpen={() => setOpen(true)}
      closeIcon
      open={open}
      size="tiny"
      trigger={<Button>Edit</Button>}
    >
      {error && <Message error header="Error" content={errorMessage} />}
      <Modal.Content className="modal-content-wrapper">
        <Form size="large" error={error} className="edit-profile-form">
          <Header as="h3">Display Name</Header>
          <Form.Field>
            <Input
              fluid
              placeholder="Display Name"
              name="displayName"
              type="text"
              value={displayName}
              onChange={handleChange}
            />
          </Form.Field>
          <Header as="h3">GitHub Username</Header>
          <Form.Field>
            <Input
              fluid
              placeholder="Github Username"
              name="githubUsername"
              type="text"
              value={githubUsername}
              onChange={handleChange}
            />
          </Form.Field>
          <Button
            fluid
            type="submit"
            onClick={handleSubmit}
            className="edit-profile-save-btn"
          >
            Save
          </Button>
        </Form>
      </Modal.Content>
    </Modal>
  );
};

export default EditProfileModal;
