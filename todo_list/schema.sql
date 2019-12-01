DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks(
    task text not null,
    status text not null,
    primary key(task)
);
