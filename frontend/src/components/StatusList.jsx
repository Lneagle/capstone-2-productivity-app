function StatusList({ teammates, setTeammates }) {
  const priorityMapping = {
    'High': '🔴',
    'Medium': '🟡',
    'Low': '🟢'
  };

  const statuses = teammates.map(person => {
    const statusObj = {};
    statusObj.name = person.name;
    statusObj.task = "free";
    statusObj.priority = 'Low';
    person.time_entries.forEach(entry => {
      if (entry.end_time == null) {
        statusObj.task = entry.task.name;
        statusObj.priority = entry.task.priority;
      }
    })
    return statusObj;
  });

  const teamList = statuses.map(person => 
    <li>
      <h4>{person.name}</h4>
      <span>{priorityMapping[person.priority]}</span> {person.task}
    </li>
  );

	return (
		<ul>
      {teamList}
		</ul>
	)
}

export default StatusList;