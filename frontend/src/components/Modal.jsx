import { useState } from "react";

function Modal({ setIsEditMode, task, teammates, onSubmit }) {
  const [taskName, setTaskName] = useState(task ? task.name : '');
  const [priority, setPriority] = useState(task ? task.priority : 'Low');
  const [assignee, setAssignee] = useState(task ? task.assignee.id : null);

  const handleClose = () => {
    setIsEditMode(false);
  }

  const handleNameChange = (event) => {
    setTaskName(event.target.value);
  }

  const handlePriorityChange = (event) => {
    setPriority(event.target.value);
  }

  const handleAssigneeChange = (event) => {
    setAssignee(event.target.value);
  }

  const handleFormSubmit = (event) => {
    event.preventDefault();
    const data = JSON.stringify({
      "name": taskName,
      "priority": priority,
      "assignee_id": assignee
    })
    onSubmit(task, data);
    handleClose();
  }

	return (
		<div className="modal-container">
      <div className="modal">
        
        <form onSubmit={handleFormSubmit}>
          <div className="form-group">
            <button className="close" onClick={handleClose}>X</button>
            <label htmlFor="taskName">Task Name:</label>
            <input type="text" id="taskName" value={taskName} onChange={handleNameChange} />
          </div>
          <div className="form-group">
            <label htmlFor="priority">Priority:</label>
            <select id="priority" value={priority} onChange={handlePriorityChange}>
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="assignee">Assignee:</label>
            <select id="assignee" value={assignee} onChange={handleAssigneeChange}>
              {teammates.map(person => (
                <option key={person.id} value={person.id}>{person.name}</option>
              ))}
            </select>
          </div>
          <input type="submit" value="Submit" />
        </form>
      </div>
		</div>
	)
}

export default Modal;