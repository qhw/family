CREATE TABLE  `Family_Tree`.`Relationship` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fatherid` int(11) NOT NULL DEFAULT '0',
  `motherid` int(11) NOT NULL DEFAULT '0',
  `childid` int(11) NOT NULL DEFAULT '0',
  `gender` int(11) NOT NULL DEFAULT '0',
  `photo_path` char(80) CHARACTER SET ucs2 NOT NULL,
  `description` char(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1
