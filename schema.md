DB Name: `video`

### Users

```
create table Users(id INT NOT NULL AUTO_INCREMENT, username VARCHAR(40), password VARCHAR(40), primary key(id));
```

+ id
+ username
+ password

### Videos

```
create table Videos(user_id INT, video_file VARCHAR(40), summary_file VARCHAR(40), q_file VARCHAR(40), time BIGINT);
```

+ user_id
+ video_file
+ summary_file
+ q_file
+ time