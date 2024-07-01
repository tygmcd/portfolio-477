CREATE TABLE IF NOT EXISTS `feedback` (
`comment_id`        int(11)        NOT NULL AUTO_INCREMENT COMMENT 'The unique comment id',
`name`              varchar(100)   NOT NULL                COMMENT 'Name of commenter' ,
`email`             varchar(100)   NOT NULL                COMMENT 'Email of commenter',
`comment`           varchar(500)   NOT NULL                COMMENT 'Comment itself',
PRIMARY KEY (`comment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Content from feedback form";