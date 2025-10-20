import NavBar from "../components/NavBar";
import TaskList from "../components/TaskList";
import StatusList from "../components/StatusList";

function Dashboard() {
	return (
		<>
			<NavBar />
			<main>
				<TaskList />
        <StatusList />
			</main>
		</>
	)
}

export default Dashboard;