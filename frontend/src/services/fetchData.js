//Replace when authentication implemented
const TEAM_ID = 1;
const USER_ID = 1;
const API_URL = "http://localhost:5555";

export const fetchTeamUsers = async () => {
  try {
    const response = await fetch(`${API_URL}/teams/${TEAM_ID}/users`);
    if (!response.ok) {
      throw new Error(`Could not fetch users for team ${TEAM_ID}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching users:", error);
    throw error;
  }
}

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
    throw error;
  }
};

export const createTimeEntry = async (task_id) => {
  const start_time = new Date().getTime();
  try {
    const response = await fetch(`${API_URL}/teams/${TEAM_ID}/users/${USER_ID}/time_entries`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        task_id: task_id,
        start_time: start_time
      }),
    });
    if (!response.ok) {
      throw new Error(`Could not create time entry`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
};

export const endTimeEntry = async (entry_id) => {
  const end_time = new Date().getTime();
  try {
    const response = await fetch(`${API_URL}/teams/${TEAM_ID}/users/${USER_ID}/time_entries/${entry_id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        end_time: end_time
      }),
    });
    if (!response.ok) {
      throw new Error(`Could not edit time entry`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
};

export const patchTask = async(client_id, project_id, task_id, body) => {
  try {
    const response = await fetch(`${API_URL}/clients/${client_id}/projects/${project_id}/tasks/${task_id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: body,
    });
    if (!response.ok) {
      throw new Error(`Could not edit task`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}