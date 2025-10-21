//Replace when authentication implemented
const TEAM_ID = 1;
const USER_ID = 1;
const API_URL = "http://localhost:5555";

export const fetchUserTasks = async () => {
  try {
    const response = await fetch(`${API_URL}/teams/${TEAM_ID}/users/${USER_ID}/tasks`);
    if (!response.ok) {
      throw new Error(`Could not fetch tasks for user ${USER_ID}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching users:", error);
    throw error; // Re-throw to allow component-level error handling
  }
};
