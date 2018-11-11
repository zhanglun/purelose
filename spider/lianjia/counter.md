table chenjiao

~alter table chengjiao change sign_method sign_method varchar(10) DEFAULT NULL COMMENT '签约方式';~
~alter table chengjiao change total_price total_price varchar(10) DEFAULT NULL COMMENT '总价(单位：万元)';~
~alter table chengjiao change unit_price unit_price varchar(10) DEFAULT NULL COMMENT '单价(单位：元)';~
~alter table chengjiao change building_structure building_structure varchar(16) DEFAULT NULL COMMENT '结构';~
~alter table chengjiao change building_floor building_floor varchar(10) DEFAULT NULL COMMENT '楼层';~
alter table chengjiao change building_size building_size varchar(10) DEFAULT NULL COMMENT '建筑面积';
alter table chengjiao change building_meta building_meta varchar(120) DEFAULT NULL COMMENT '房屋其他信息';
alter table chengjiao change building_style building_style varchar(10) DEFAULT NULL COMMENT '建筑形态';
alter table chengjiao change building_towards building_towards varchar(10) DEFAULT NULL COMMENT '朝向';
alter table chengjiao change building_year building_year varchar(10) DEFAULT NULL COMMENT '建造年份';
alter table chengjiao change city city varchar(10) DEFAULT NULL COMMENT '所在城市';
alter table chengjiao change city_area city_area varchar(16) DEFAULT NULL COMMENT '所在城区';
alter table chengjiao change area_name area_name varchar(16) DEFAULT NULL COMMENT '所在地区';
alter table chengjiao change community_name community_name varchar(30) DEFAULT NULL COMMENT '所在小区';
