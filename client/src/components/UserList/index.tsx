import "./style.css"

const UserList = ({ users }: { users: string[] | null }) => {
	return (
		<div className="userlist">
			<strong>Users Playing:</strong>
			<ul>{users?.map((user, i) => <li key={i}>{user}</li>)}</ul>
		</div>
	)
}

export default UserList
