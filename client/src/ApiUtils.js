import axios from "axios";
import { SERVER_HOST } from "./Constants";

export const getUserObject = async (token, id) => {
  try {
    const response = await axios.get(`${SERVER_HOST}/service/author/${id}/`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
    });

    return response;
  } catch (error) {
    return error.response;
  }
};
