create table system_user
(
    id            int auto_increment
        primary key,
    name          varchar(50)                         not null,
    pwd_hash      varchar(255)                        not null,
    role          varchar(32)                         not null comment '用户角色',
    status        tinyint(1)                          not null comment '状态：启用 = 1，禁用 = 0',
    created_at    timestamp default CURRENT_TIMESTAMP not null,
    updated_at    timestamp default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP,
    constraint name
        unique (name)
);
