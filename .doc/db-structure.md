# DB-Structure

##Theme
```
{
	alias: "php",
	name: "PHP",
	discussions: [
		...
	]
}
```

##Discussion
```
{
	alias: "php",
	truncated: false,
	title: "PHP",
	articles: [
		...
	]
}
```

##Article
```
{
	alias: "php",
	truncated: false,
	title: "PHP",
	content: "PHP ist voll toll! :)",
	owner: "luk",
	timestamp: 123456789
}
```

##User
```
{
	alias: "luk",
	truncated: false,
	name: "Lukas",
	password: "012345",
	role: "ADMIN"
}
```
Valid user-roles are `ADMIN`, `USER`, `USER_READONLY` or `GUEST`.